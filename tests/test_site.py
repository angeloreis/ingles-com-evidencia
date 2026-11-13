import re
import subprocess
import sys

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
