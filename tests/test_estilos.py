import re

import pytest

from scripts import RAIZ
from scripts.estilos import carregar_tokens, contraste, gerar_tokens_css, resolver_cores

TOKENS = carregar_tokens()
CORES = resolver_cores(TOKENS)
CSS = gerar_tokens_css(TOKENS)


def bloco(seletor):
    return CSS.split(seletor + " {", 1)[1].split("}", 1)[0]


def test_apelidos_resolvidos():
    assert CORES["light"]["foco"] == "#0e5a49"
    assert CORES["dark"]["evidencia-nenhuma"] == "#93a89f"


def test_temas_seguem_o_atributo_do_zensical():
    claro = bloco(':root, [data-md-color-scheme="default"]')
    escuro = bloco('[data-md-color-scheme="slate"]')
    assert "--fundo: #f1f5f3;" in claro and "--fundo: #0c1613;" in escuro
    assert "--foco: var(--passaporte);" in escuro
    assert "prefers-color-scheme" not in CSS


def test_familias_tipos_e_medidas():
    for trecho in ['--font-texto: "Figtree", system-ui', "--corpo-tamanho: 17px;",
                   "--titulo-1-peso: 800;", "--etiqueta-espacamento: 0.08em;",
                   "--espaco-4: 16px;", "--raio-painel: 12px;", "--alvo-toque: 48px;",
                   "--largura-texto: 68ch;"]:
        assert trecho in CSS


def test_tokens_css_do_repositorio_em_dia():
    assert (RAIZ / "conteudo/estilos/tokens.css").read_text(encoding="utf-8") == CSS


def test_bundle_so_usa_variaveis_definidas():
    bundle = (RAIZ / "conteudo/estilos/bundle.css").read_text(encoding="utf-8")
    assert set(re.findall(r"var\(--([a-z0-9-]+)", bundle)) <= set(re.findall(r"--([a-z0-9-]+):", CSS))


def test_contraste_valores_conhecidos():
    assert contraste("#000000", "#ffffff") == pytest.approx(21.0)
    assert contraste("#ffffff", "#777777") == pytest.approx(4.48, abs=0.01)


PARES = [("tinta", "fundo"), ("tinta", "superficie"), ("tinta-suave", "fundo"),
         ("tinta-suave", "superficie"), ("passaporte", "fundo"), ("passaporte", "superficie"),
         ("sobre-passaporte", "passaporte"), ("evidencia-forte", "fundo"),
         ("evidencia-forte", "superficie"), ("evidencia-moderada", "fundo"),
         ("evidencia-moderada", "superficie"), ("evidencia-fraca", "fundo"),
         ("evidencia-fraca", "superficie"), ("evidencia-nenhuma", "superficie")]


@pytest.mark.parametrize("tema", ["light", "dark"])
@pytest.mark.parametrize("texto, fundo", PARES)
def test_contraste_aa(tema, texto, fundo):
    assert contraste(CORES[tema][texto], CORES[tema][fundo]) >= 4.5
