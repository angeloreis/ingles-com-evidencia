import re
import subprocess
import sys
from html.parser import HTMLParser

import pytest

from scripts import RAIZ


@pytest.fixture(scope="session")
def site():
    subprocess.run([sys.executable, "-m", "zensical", "build", "--clean", "--strict"], cwd=RAIZ, check=True)
    return RAIZ / "site"


def paginas(site):
    return {p: p.read_text(encoding="utf-8") for p in site.rglob("*.html")}


def test_pagina_inicial_em_portugues(site):
    html = (site / "index.html").read_text(encoding="utf-8")
    assert '<html lang="pt"' in html and "Pular para conteúdo" in html
    assert (site / "sobre/index.html").is_file() and "Sobre e créditos" in html


def test_docs_do_projeto_fora_do_site(site):
    assert not (site / "superpowers").exists()
    assert "desenho do projeto" not in (site / "search.json").read_text(encoding="utf-8")


def test_estilos_na_ordem_e_relativos(site):
    html = (site / "index.html").read_text(encoding="utf-8")
    posicoes = [html.index(f'href="./estilos/{n}.css"') for n in ["fontes", "tokens", "bundle", "ponte"]]
    assert posicoes == sorted(posicoes)


def test_nada_de_terceiros_nem_caminho_absoluto(site):
    for caminho, html in paginas(site).items():
        for proibido in ["fonts.googleapis.com", "fonts.gstatic.com", "api.github.com"]:
            assert proibido not in html, caminho
        assert not re.findall(r'<script[^>]+src="(?:https?:)?//', html), caminho
        assert not re.findall(r'<link rel="(?:stylesheet|preload|modulepreload|icon)"[^>]+href="(?:https?:)?//', html), caminho
        assert not re.findall(r'(?:href|src)="/(?!/|ingles-com-evidencia/)', html), caminho


def test_dois_temas_com_botao(site):
    html = (site / "index.html").read_text(encoding="utf-8")
    for trecho in ['data-md-color-scheme="slate"', 'data-md-color-media="(prefers-color-scheme: dark)"',
                   'aria-label="Mudar para o tema escuro"', 'aria-label="Mudar para o tema claro"']:
        assert trecho in html


def test_tema_comeca_seguindo_o_aparelho(site):
    # Sem a opção automática como primeira, o tema grava o esquema do primeiro
    # acesso e deixa de acompanhar o aparelho de quem nunca tocou no botão.
    html = (site / "index.html").read_text(encoding="utf-8")
    opcoes = re.findall(r'<input class="md-option"[^>]*>', html)
    assert 'data-md-color-media="(prefers-color-scheme)"' in opcoes[0]
    assert 'aria-label="Seguir o tema do aparelho"' in html


def test_fontes_publicadas(site):
    assert (site / "estilos/fontes/figtree-latin-wght-normal.woff2").is_file()


def test_ponte_liga_o_passaporte():
    ponte = (RAIZ / "conteudo/estilos/ponte.css").read_text(encoding="utf-8")
    tokens = (RAIZ / "conteudo/estilos/tokens.css").read_text(encoding="utf-8")
    assert "--md-default-bg-color: var(--fundo);" in ponte and "--md-typeset-a-color: var(--passaporte);" in ponte
    usadas = {v for v in re.findall(r"var\(--([a-z0-9-]+)", ponte) if not v.startswith("md-")}
    assert usadas <= set(re.findall(r"--([a-z0-9-]+):", tokens))


def test_botoes_do_cabecalho_com_area_de_toque():
    # menu, tema, busca e o botão flutuante do índice saem com 36-38 px no tema
    ponte = (RAIZ / "conteudo/estilos/ponte.css").read_text(encoding="utf-8")
    regra = re.search(r"\.md-header__button,\s*\.md-sidebar-button\s*\{([^}]*)\}", ponte)
    assert regra
    assert "min-width: var(--alvo-toque);" in regra.group(1)
    assert "min-height: var(--alvo-toque);" in regra.group(1)


def test_botao_primario_vence_a_cor_de_link_do_tema():
    # .md-typeset a pinta links com a cor da marca; sem esta regra o texto do
    # botão primário (um link) some sobre o próprio fundo, inclusive no hover.
    ponte = (RAIZ / "conteudo/estilos/ponte.css").read_text(encoding="utf-8")
    regra = ponte.split(".md-typeset a.pp-botao--primario:hover", 1)[1].split("}", 1)[0]
    assert "color: var(--sobre-passaporte);" in regra


def test_scripts_relativos_na_ordem(site):
    html = (site / "index.html").read_text(encoding="utf-8")
    nucleo = html.index('src="./js/nucleo.js"')
    audio = html.index('src="./js/paginas/audio.js"')
    assert nucleo < audio


def test_situacao_6_publicada(site):
    html = (site / "situacoes/telefonar/index.html").read_text(encoding="utf-8")
    assert html.count('class="pp-frase"') >= 10
    assert 'lang="en"' in html and "data-audio-sequencia" in html and "pp-roteiro" in html


def test_paginas_da_trilha(site):
    for pagina in ["trilhas/destravar/hoje", "trilhas/destravar/ficha", "trilhas/destravar", "treinar"]:
        assert (site / pagina / "index.html").is_file(), pagina


def test_sem_textos_do_tema_em_ingles(site):
    for caminho, html in paginas(site).items():
        assert "Made with" not in html, caminho
        assert 'title="Permanent link"' not in html, caminho


def test_links_internos_apontam_para_paginas_que_existem(site):
    # O Zensical reescreve href relativo do HTML cru como se fosse relativo ao .md de origem;
    # um link escrito relativo à URL da página sai com um nível a mais e quebra.
    from urllib.parse import urljoin, urlsplit

    base = "https://exemplo.test/ingles-com-evidencia/"
    quebrados = []
    for caminho, html in paginas(site).items():
        url_pagina = urljoin(base, caminho.relative_to(site).as_posix().removesuffix("index.html"))
        for href in re.findall(r'<a [^>]*href="([^"#][^"]*)"', html):
            if href.startswith(("http:", "https:", "mailto:", "//")):
                continue
            alvo = urlsplit(urljoin(url_pagina, href)).path
            if not alvo.startswith("/ingles-com-evidencia/"):
                quebrados.append(f"{caminho.relative_to(site)}: {href} (sai do site)")
                continue
            relativo = alvo.removeprefix("/ingles-com-evidencia/")
            arquivo = site / relativo
            if relativo.endswith("/") or relativo == "":
                arquivo = arquivo / "index.html"
            if not arquivo.exists():
                quebrados.append(f"{caminho.relative_to(site)}: {href}")
    assert quebrados == []


class _TextoForaDoIngles(HTMLParser):
    """Junta o texto da página que não está dentro de um elemento com lang="en"."""
    VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.pilha = [("", False)]
        self.partes = []

    def handle_starttag(self, tag, attrs):
        if tag in self.VAZIOS:
            return
        lang = dict(attrs).get("lang")
        ingles = lang.startswith("en") if lang else self.pilha[-1][1]
        self.pilha.append((tag, ingles or tag in ("script", "style")))

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, 0, -1):
            if self.pilha[i][0] == tag:
                del self.pilha[i:]
                break

    def handle_data(self, data):
        if not self.pilha[-1][1]:
            self.partes.append(data)


INGLES = re.compile(r"\b(you|your|the|could|can|does|how's|what|sorry|again|week|time|p\.m|a\.m)\b", re.I)


def _fora_do_ingles(html):
    leitor = _TextoForaDoIngles()
    leitor.feed(html)
    return "".join(leitor.partes)


# Toda frase em inglês leva lang="en" (leitor de tela) e vem com tradução (achado I3 da revisão final).
def test_ingles_entre_aspas_marcado_com_lang_en(site):
    achados = []
    for caminho, html in paginas(site).items():
        # aspas em volta de um trecho todo marcado com lang="en" ficam vazias; sem tirá-las, a aspa
        # de fechamento casa com a próxima citação e o "time" (equipe) do meio parece inglês
        for trecho in re.findall(r'"([^"]{1,200})"', _fora_do_ingles(html).replace('""', "")):
            if INGLES.search(trecho):
                achados.append(f"{caminho}: {trecho}")
    assert achados == []


def test_notas_da_situacao_6_em_ingles_marcado_e_traduzido(site):
    html = (site / "situacoes/telefonar/index.html").read_text(encoding="utf-8")
    fora = _fora_do_ingles(html)
    for termo in ["calendar invite", "shadowing", "Eastern Time", "Pacific"]:
        assert termo in html and termo not in fora, termo
    assert "como está indo a sua semana" in fora


# --- Fase 1B ---------------------------------------------------------------

def secoes_do_menu(html):
    return re.findall(r'id="__nav_\d+_label"[^>]*>\s*<span class="md-ellipsis">\s*([^<]+?)\s*</span>', html)


def test_guia_no_menu(site):
    assert (site / "guia/index.html").is_file() and (site / "guia/como-usar/index.html").is_file()
    secoes = secoes_do_menu((site / "index.html").read_text(encoding="utf-8"))
    assert "Guia" in secoes and secoes.index("Guia") < secoes.index("Situações"), secoes


def test_tabelas_com_o_tamanho_do_texto():
    # o tema põe as tabelas em 0.64rem (12,8 px); o projeto pede 17 px ou mais (tabela dos selos, pronúncia)
    ponte = (RAIZ / "conteudo/estilos/ponte.css").read_text(encoding="utf-8")
    regra = re.search(r"\[data-md-color-scheme\] \.md-typeset table:not\(\[class\]\)\s*\{([^}]*)\}", ponte)
    assert regra and "font-size: var(--corpo-tamanho);" in regra.group(1)


def test_avisos_com_o_tamanho_do_texto():
    # os avisos (!!! note, !!! info) também saem com 12,8 px no tema
    ponte = (RAIZ / "conteudo/estilos/ponte.css").read_text(encoding="utf-8")
    regra = re.search(r"\[data-md-color-scheme\] \.md-typeset \.admonition\s*\{([^}]*)\}", ponte)
    assert regra and "font-size: var(--corpo-tamanho);" in regra.group(1)


def test_situacao_7_publicada(site):
    html = (site / "situacoes/tecnologia/index.html").read_text(encoding="utf-8")
    assert html.count('class="pp-frase"') >= 20
    assert "data-audio-sequencia" in html and "pp-roteiro" in html
    tabela = html.split('id="pronuncia-dos-termos"', 1)[1].split("</table>", 1)[0]
    linhas = re.findall(r"<tr>(.*?)</tr>", tabela, re.S)[1:]
    assert len(linhas) >= 10
    for linha in linhas:
        assert 'href="https://' in linha and 'lang="en"' in linha, linha


def test_situacao_8_publicada(site):
    html = (site / "situacoes/entrevista/index.html").read_text(encoding="utf-8")
    assert html.count('class="pp-frase"') >= 18
    assert "data-audio-sequencia" in html and "pp-roteiro" in html


def _artigo(html):
    """Só o conteúdo da página, sem o menu (que liga todas as páginas)."""
    return re.search(r"<article.*?</article>", html, re.S).group(0)


def test_entrada_cita_o_que_esta_no_ar(site):
    inicio = _artigo((site / "index.html").read_text(encoding="utf-8"))
    assert 'href="guia/"' in inicio
    assert "a primeira semana já está no ar" not in inicio
    situacoes = _artigo((site / "situacoes/index.html").read_text(encoding="utf-8"))
    for slug in ("telefonar", "tecnologia", "entrevista"):
        assert f'href="{slug}/"' in situacoes, slug
    sobre = _artigo((site / "sobre/index.html").read_text(encoding="utf-8"))
    assert 'href="../guia/shadowing/"' in sobre  # M15: o capítulo 8 indica a fala real


def test_filtro_do_treino_cabe_na_tela():
    # com os títulos das situações (Tarefa 2), a opção mais longa deixava o seletor com 498 px a 320 px
    ponte = (RAIZ / "conteudo/estilos/ponte.css").read_text(encoding="utf-8")
    regra = re.search(r"\.ice-treino__filtro select\s*\{([^}]*)\}", ponte)
    assert regra and "max-width: 100%;" in regra.group(1)
