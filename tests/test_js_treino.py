import pytest

from js import avaliar, chamar, contexto


@pytest.fixture
def ctx():
    return contexto("logica/datas.js", "logica/treino.js")


def test_acertar_carta_nova(ctx):
    assert chamar(ctx, "ICE.treino.responder", None, True, "2026-11-13") == {"caixa": 1, "proxima": "2026-11-14"}


def test_caixa_maxima(ctx):
    assert chamar(ctx, "ICE.treino.responder", {"caixa": 4, "proxima": "2026-11-13"}, True, "2026-11-13") == \
        {"caixa": 5, "proxima": "2026-12-13"}
    assert chamar(ctx, "ICE.treino.responder", {"caixa": 5, "proxima": "2026-11-13"}, True, "2026-11-13") == \
        {"caixa": 5, "proxima": "2026-12-13"}


def test_errar_volta_para_hoje(ctx):
    assert chamar(ctx, "ICE.treino.responder", {"caixa": 3, "proxima": "2026-11-01"}, False, "2026-11-13") == \
        {"caixa": 0, "proxima": "2026-11-13"}


# A carta errada volta no mesmo treino; acertar na repetição não pode render
# intervalo maior que acertar de primeira (achado I1 da revisão final).
@pytest.mark.parametrize("antes", [None, {"caixa": 5, "proxima": "2026-11-13"}])
def test_errar_e_acertar_no_mesmo_dia_volta_amanha(ctx, antes):
    errada = chamar(ctx, "ICE.treino.responder", antes, False, "2026-11-13")
    assert chamar(ctx, "ICE.treino.responder", errada, True, "2026-11-13") == {"caixa": 1, "proxima": "2026-11-14"}


def test_carta_errada_entra_na_fila_do_dia_e_nao_conta_como_nova(ctx):
    cartas = {"a": {"caixa": 0, "proxima": "2026-11-13"}}
    assert chamar(ctx, "ICE.treino.fila", ["a", "b"], cartas, "2026-11-13", 10, 1) == ["a"]


def test_fila_vencidas_antes_das_novas_com_limite(ctx):
    cartas = {"b": {"caixa": 1, "proxima": "2026-11-12"},
              "e": {"caixa": 2, "proxima": "2026-11-10"},
              "c": {"caixa": 3, "proxima": "2026-11-20"}}
    assert chamar(ctx, "ICE.treino.fila", ["a", "b", "c", "d", "e"], cartas, "2026-11-13", 9, 10) == ["e", "b", "a"]


def test_fila_usa_o_limite_padrao(ctx):
    ids = [f"n{i}" for i in range(15)]
    assert len(chamar(ctx, "ICE.treino.fila", ids, {}, "2026-11-13", 0)) == 10


def test_ler_tolerante(ctx):
    vazio = avaliar(ctx, "ICE.treino.estadoVazio()")
    assert vazio == {"versao": 1, "cartas": {}, "novas": {"dia": None, "quantidade": 0}}
    for texto in ["{quebrado", None, '{"versao": 99}']:
        assert chamar(ctx, "ICE.treino.ler", texto) == vazio
