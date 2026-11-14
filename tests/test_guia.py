"""Conferência dos capítulos do guia (Fase 1B, Tarefa 6): estrutura, citações e registro de leitura."""
import re

import pytest

from scripts import RAIZ
from scripts import guia
from scripts.construir import main
from scripts.guia import conferir_capitulo, conferir_guia, ler_registro

CARIMBO = ('<span class="pp-carimbo" data-nivel="2"><span class="pp-carimbo__barras" aria-hidden="true">'
           '<i></i><i></i><i></i></span>Evidência moderada</span>')


def secao(rotulo, texto):
    return f'<section class="pp-secao" markdown>\n<span class="pp-secao__rotulo">{rotulo}</span>\n\n{texto}\n\n</section>\n'


CURSOS = secao("O que os cursos dizem", "Repetir junto com o áudio destrava a fala.")
PESQUISA = secao("O que a pesquisa diz", "Hamada (2016) e Foote e McDonough (2017) acharam ganhos.")
PRATICAR = secao("Como praticar", "Cinco minutos por dia.")
REF_HAMADA = "- Hamada, Y. (2016). Shadowing: Who benefits and how? *Language Teaching Research*, 20(1), 35–52. <https://doi.org/10.1177/1362168815597504>"
REF_FOOTE = "- Foote, J. A., & McDonough, K. (2017). Using shadowing with mobile technology. *Journal of Second Language Pronunciation*, 3(1), 34–56. <https://doi.org/10.1075/jslp.3.1.02foo>"


def capitulo(carimbo=CARIMBO, secoes=(CURSOS, PESQUISA, PRATICAR), armadilhas=True,
             referencias=(REF_HAMADA, REF_FOOTE)):
    partes = ['<div class="pp-faixa"><span>Guia</span><span>Capítulo 8</span></div>\n', "# Shadowing\n", carimbo, "\n"]
    partes += list(secoes)
    if armadilhas:
        partes.append("## Armadilhas\n\n- Só repetir sem entender.\n")
    if referencias is not None:
        partes.append("## Referências\n\n" + "\n".join(referencias) + "\n")
    return "\n".join(partes)


def entrada(cabecalho, resumo="O estudo comparou grupos e achou ganho na compreensão."):
    linhas = [f"## {cabecalho}", "", "- Link: https://doi.org/10.1/x", "- Lido em: 2026-11-14"]
    if resumo is not None:
        linhas.append(f"- O que o resumo diz: {resumo}")
    linhas.append('- Usado em: capítulo 8, "O que a pesquisa diz"')
    return "\n".join(linhas) + "\n"


REGISTRO = "# Registro de leitura\n\n" + entrada("Hamada (2016)") + "\n" + entrada("Foote e McDonough (2017)")


@pytest.fixture
def pasta(tmp_path, monkeypatch):
    monkeypatch.setattr(guia, "CAPITULOS", {"shadowing": 8})
    (tmp_path / "guia").mkdir()
    (tmp_path / "referencias.md").write_text(REGISTRO, encoding="utf-8")
    return tmp_path


def conferir(pasta, texto, slug="shadowing", registro=None):
    caminho = pasta / "guia" / f"{slug}.md"
    caminho.write_text(texto, encoding="utf-8")
    if registro is not None:
        (pasta / "referencias.md").write_text(registro, encoding="utf-8")
    return conferir_capitulo(caminho, ler_registro(pasta / "referencias.md"))


def mensagens(erros):
    return " | ".join(e.mensagem for e in erros)


def test_ler_registro_usa_primeiro_sobrenome_e_ano(pasta):
    registro = ler_registro(pasta / "referencias.md")
    assert set(registro) == {("Hamada", "2016"), ("Foote", "2017")}
    assert registro[("Hamada", "2016")]["O que o resumo diz"].startswith("O estudo comparou")


def test_capitulo_completo_sem_erros(pasta):
    assert conferir(pasta, capitulo()) == []


def test_falta_secao(pasta):
    erros = conferir(pasta, capitulo(secoes=(CURSOS, PESQUISA)))
    assert erros and "Como praticar" in mensagens(erros)


def test_secoes_fora_de_ordem(pasta):
    erros = conferir(pasta, capitulo(secoes=(PESQUISA, CURSOS, PRATICAR)))
    assert erros and "ordem" in mensagens(erros)


def test_sem_carimbo(pasta):
    erros = conferir(pasta, capitulo(carimbo=""))
    assert erros and "carimbo" in mensagens(erros)


def test_carimbo_depois_da_primeira_secao_nao_vale(pasta):
    texto = capitulo(carimbo="").replace(PESQUISA, PESQUISA + CARIMBO + "\n")
    assert "carimbo" in mensagens(conferir(pasta, texto))


def test_como_usar_sem_carimbo_pode(pasta, monkeypatch):
    monkeypatch.setattr(guia, "CAPITULOS", {"como-usar": 1})
    texto = "# Como usar este guia\n\nCada capítulo traz um selo.\n"
    assert conferir(pasta, texto, slug="como-usar") == []


def test_sem_armadilhas(pasta):
    assert "Armadilhas" in mensagens(conferir(pasta, capitulo(armadilhas=False)))


def test_referencias_tem_de_ser_a_ultima_secao(pasta):
    texto = capitulo() + "\n## Para saber mais\n\nNada.\n"
    assert "Referências" in mensagens(conferir(pasta, texto))


def test_capitulo_de_tecnica_sem_referencias(pasta):
    texto = capitulo(referencias=None).replace("Hamada (2016) e Foote e McDonough (2017) acharam ganhos.", "Sem citação.")
    assert "Referências" in mensagens(conferir(pasta, texto))


def test_citacao_sem_referencia(pasta):
    erros = conferir(pasta, capitulo(referencias=(REF_FOOTE,)))
    assert erros and "Hamada (2016)" in mensagens(erros)


@pytest.mark.parametrize("citacao, ref", [
    ("Boers et al. (2006)", "- Boers, F., Eyckmans, J., & Stengers, H. (2006). T. *R*, 10(3), 245–261. <https://doi.org/10.1/b>"),
    ("De Jong e Perfetti (2011)", "- De Jong, N., & Perfetti, C. A. (2011). T. *R*, 61(2), 533–568. <https://doi.org/10.1/d>"),
])
def test_formas_de_citacao(pasta, citacao, ref):
    sobrenome = citacao.split(" e ")[0].split(" et al.")[0].split(" (")[0]
    registro = REGISTRO + "\n" + entrada(citacao)
    texto = capitulo(referencias=(REF_HAMADA, REF_FOOTE, ref)).replace("acharam ganhos.", f"acharam ganhos, como {citacao}.")
    assert conferir(pasta, texto, registro=registro) == [], sobrenome


def test_referencia_sem_citacao(pasta):
    texto = capitulo().replace("Hamada (2016) e ", "")
    erros = conferir(pasta, texto)
    assert erros and "Hamada (2016)" in mensagens(erros) and "não é citada" in mensagens(erros)


def test_referencia_sem_link_https(pasta):
    ref = REF_HAMADA.replace(" <https://doi.org/10.1177/1362168815597504>", "")
    erros = conferir(pasta, capitulo(referencias=(ref, REF_FOOTE)))
    assert erros and "https" in mensagens(erros)


def test_referencia_fora_do_registro(pasta):
    erros = conferir(pasta, capitulo(), registro="# Registro de leitura\n\n" + entrada("Hamada (2016)"))
    assert erros and "registro de leitura" in mensagens(erros) and "Foote (2017)" in mensagens(erros)


def test_registro_sem_resumo(pasta):
    registro = "# Registro de leitura\n\n" + entrada("Hamada (2016)", resumo=None) + "\n" + entrada("Foote e McDonough (2017)")
    erros = conferir(pasta, capitulo(), registro=registro)
    assert erros and "O que o resumo diz" in mensagens(erros)


def test_slug_desconhecido(pasta):
    (pasta / "guia" / "pular-o-basico.md").write_text(capitulo(), encoding="utf-8")
    (pasta / "guia" / "shadowing.md").write_text(capitulo(), encoding="utf-8")
    erros = conferir_guia(pasta / "guia", pasta / "referencias.md")
    assert len(erros) == 1 and "CAPITULOS" in erros[0].mensagem and "pular-o-basico" in erros[0].arquivo


def test_capitulo_listado_sem_arquivo(pasta):
    erros = conferir_guia(pasta / "guia", pasta / "referencias.md")
    assert len(erros) == 1 and "shadowing" in str(erros[0]) and "sem arquivo" in erros[0].mensagem


def test_index_do_guia_nao_e_conferido(pasta):
    (pasta / "guia" / "index.md").write_text("# Guia\n", encoding="utf-8")
    (pasta / "guia" / "shadowing.md").write_text(capitulo(), encoding="utf-8")
    assert conferir_guia(pasta / "guia", pasta / "referencias.md") == []


def test_pasta_do_guia_ausente_sem_erros(tmp_path):
    assert conferir_guia(tmp_path / "nao-existe", tmp_path / "referencias.md") == []


def test_construir_acusa_capitulo_com_problema(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(guia, "CAPITULOS", {"shadowing": 8})
    conteudo = tmp_path / "conteudo"
    (conteudo / "guia").mkdir(parents=True)
    (conteudo / "guia" / "shadowing.md").write_text(capitulo(carimbo=""), encoding="utf-8")
    (tmp_path / "docs" / "pesquisa").mkdir(parents=True)
    (tmp_path / "docs" / "pesquisa" / "referencias.md").write_text(REGISTRO, encoding="utf-8")
    planos = tmp_path / "planos"
    planos.mkdir()
    codigo = main(["--planos", str(planos), "--conteudo", str(conteudo)])
    assert codigo == 1
    assert "carimbo" in capsys.readouterr().err


def test_guia_do_repositorio_sem_problemas():
    assert conferir_guia(RAIZ / "conteudo" / "guia", RAIZ / "docs" / "pesquisa" / "referencias.md") == []


def test_indice_do_guia_liga_os_capitulos_publicados():
    indice = (RAIZ / "conteudo" / "guia" / "index.md").read_text(encoding="utf-8")
    for slug in guia.CAPITULOS:
        assert f"]({slug}.md)" in indice, slug


# Ligação obrigatória de cada capítulo de técnica com o kit (plano da 1B, Tarefas 8 a 12).
LIGACOES = {
    "frases-chave": ("../situacoes/telefonar.md", "../situacoes/tecnologia.md", "../situacoes/entrevista.md"),
    "shadowing": ("../situacoes/telefonar.md#dialogo", "../situacoes/tecnologia.md#dialogo",
                  "../situacoes/entrevista.md#dialogo"),
    "fluencia": ("../trilhas/destravar/ficha.md", "../treinar.md"),
    "medo-de-falar": ("../trilhas/destravar/index.md", "../trilhas/destravar/ficha.md"),
    "ia-modo-de-voz": tuple(f"../situacoes/{s}.md#treinar-com-ia-no-modo-de-voz"
                            for s in ("telefonar", "tecnologia", "entrevista")),
}


@pytest.mark.parametrize("slug", sorted(LIGACOES))
def test_capitulo_liga_o_kit(slug):
    assert slug in guia.CAPITULOS, slug
    texto = (RAIZ / "conteudo" / "guia" / f"{slug}.md").read_text(encoding="utf-8")
    for destino in LIGACOES[slug]:
        assert f"]({destino}" in texto, destino


# Risco da seção 7 do desenho: a voz do kit é sintética; o capítulo 8 diz isso e indica fala real.
def test_shadowing_avisa_voz_sintetica_e_indica_fala_real():
    texto = (RAIZ / "conteudo" / "guia" / "shadowing.md").read_text(encoding="utf-8")
    corpo = texto.split("## Referências")[0]
    assert "sintética" in corpo
    externos = {l for l in re.findall(r"\]\((https://[^)]+)\)", corpo) if "doi.org" not in l}
    assert len(externos) >= 2, externos


# Capítulo com mais de uma técnica: um carimbo reto por técnica logo abaixo do título (plano da 1B).
def test_fluencia_um_carimbo_por_tecnica():
    texto = (RAIZ / "conteudo" / "guia" / "fluencia.md").read_text(encoding="utf-8")
    antes = texto.split('class="pp-secao"')[0]
    assert len(re.findall(r'class="pp-carimbo pp-carimbo--reto"[^>]*data-nivel="[0-3]"', antes)) == 3


# Restrição geral da 1B: nenhum nome de produto de IA, e aviso para não colar dados pessoais.
def test_ia_sem_nome_de_produto_e_com_aviso_de_dados():
    texto = (RAIZ / "conteudo" / "guia" / "ia-modo-de-voz.md").read_text(encoding="utf-8")
    corpo = texto.split("## Referências")[0]
    assert "dados pessoais" in corpo
    for produto in ("ChatGPT", "GPT", "Gemini", "Claude", "Copilot", "Alexa", "Siri", "Duolingo", "Llama"):
        assert not re.search(rf"\b{produto}\b", texto), produto


# --- Revisão final da Fase 1B -------------------------------------------------

@pytest.mark.parametrize("citacao", [
    "(Hamada, 2016)",
    "(Teimouri et al., 2019; Botes et al., 2020)",
    "Hamada (2016a)",
])
def test_citacao_fora_das_formas_permitidas_e_acusada(pasta, citacao):
    texto = capitulo().replace("acharam ganhos.", f"acharam ganhos {citacao}.")
    erros = conferir(pasta, texto)
    assert "forma de citação não permitida" in mensagens(erros), mensagens(erros)


def test_parenteses_com_ano_sem_citacao_passam(pasta):
    texto = capitulo().replace("acharam ganhos.", "acharam ganhos (em estudos de 2007 a 2020).")
    assert conferir(pasta, texto) == []


def test_fluencia_selo_de_cada_tecnica():
    texto = (RAIZ / "conteudo" / "guia" / "fluencia.md").read_text(encoding="utf-8")
    antes = texto.split('class="pp-secao"')[0]
    # 4/3/2 moderada; gravar a voz fraca; cartas ao contrário fraca (poucos experimentos, com palavras soltas).
    assert re.findall(r'pp-carimbo--reto" data-nivel="([0-3])"', antes) == ["2", "1", "1"]


def test_como_usar_explica_o_selo_pela_pratica_proposta():
    texto = (RAIZ / "conteudo" / "guia" / "como-usar.md").read_text(encoding="utf-8")
    assert "como o guia propõe praticá-la" in texto


@pytest.mark.parametrize("slug, trecho", [
    ("shadowing", "no celular"),                       # o resumo de Foote e McDonough (2017) diz iPods
    ("shadowing", "entre professores"),                # Hamada (2016) fala de ideias vindas de estudos
    ("shadowing", "Sotaque não impede"),               # afirmação sem estudo
    ("fluencia", "o ajuste dá correção"),              # Thai e Boers (2016): só pequenos ganhos
    ("fluencia", "O selo é moderado: poucos experimentos"),
    ("ia-modo-de-voz", "invente"),                     # a situação 8 pede a experiência real
    ("fluencia", "estudos controlados"),               # revisão da 1B: são estudos comparativos
    ("ia-modo-de-voz", "Uma IA que conversa por voz dá muitas"),  # agora marcada como conclusão do guia
])
def test_trecho_corrigido_na_revisao_final(slug, trecho):
    texto = (RAIZ / "conteudo" / "guia" / f"{slug}.md").read_text(encoding="utf-8")
    assert trecho not in texto


# --- Fase 2A, ajustes de texto da revisão da 1B ----------------------------------------------
def _secao_do_capitulo(texto, rotulo):
    depois = texto.split(f'pp-secao__rotulo">{rotulo}</span>', 1)
    return depois[1].split("</section>", 1)[0] if len(depois) == 2 else None


def _capitulos_publicados():
    for slug in guia.CAPITULOS:
        caminho = RAIZ / "conteudo" / "guia" / f"{slug}.md"
        if caminho.exists():
            yield slug, caminho.read_text(encoding="utf-8")


def test_inferencia_do_guia_marcada():
    texto = (RAIZ / "conteudo" / "guia" / "ia-modo-de-voz.md").read_text(encoding="utf-8")
    assert "conclusão própria, que os estudos não testaram" in _secao_do_capitulo(texto, "O que a pesquisa diz")


def test_passos_de_como_praticar_com_tempo():
    vistos = 0
    for slug, texto in _capitulos_publicados():
        praticar = _secao_do_capitulo(texto, "Como praticar")
        if praticar is None:
            continue
        for negrito in re.findall(r"^[0-9]+\. \*\*(.+?)\*\*", praticar, re.M):
            vistos += 1
            assert re.search(r"\([0-9]+ minutos?", negrito), (slug, negrito)
    assert vistos >= 20


def test_cursos_dizem_sem_aspas():
    vistos = 0
    for slug, texto in _capitulos_publicados():
        cursos = _secao_do_capitulo(texto, "O que os cursos dizem")
        if cursos is None:
            continue
        vistos += 1
        sem_tags = re.sub(r"<[^>]+>", "", cursos)
        for aspa in ('"', "“", "”"):
            assert aspa not in sem_tags, (slug, aspa)
    assert vistos == 5
