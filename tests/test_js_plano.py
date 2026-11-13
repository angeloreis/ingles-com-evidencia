import pytest

from js import chamar, contexto


@pytest.fixture
def ctx():
    return contexto("logica/datas.js", "logica/plano.js", "logica/ficha.js")


@pytest.mark.parametrize("inicio, hoje, esperado", [
    ("2026-11-01", "2026-11-01", {"semana": 1, "dia": 1, "terminou": False}),
    ("2026-11-01", "2026-11-15", {"semana": 3, "dia": 1, "terminou": False}),
    ("2026-11-01", "2027-01-24", {"semana": 13, "dia": 1, "terminou": True}),
    ("2026-11-20", "2026-11-13", {"semana": 1, "dia": 1, "terminou": False}),  # relógio voltou
])
def test_posicao(ctx, inicio, hoje, esperado):
    assert chamar(ctx, "ICE.plano.posicao", inicio, hoje, 12) == esperado


def test_inicio_para_semana(ctx):
    assert chamar(ctx, "ICE.plano.inicioParaSemana", "2026-11-13", 3) == "2026-10-30"


PLANO = {"trilha": "destravar", "semanas": 12, "passos": [
    {"semana": 1, "dia": 2, "ordem": 3, "passo": "C", "minutos": 5, "link": ""},
    {"semana": 1, "dia": 2, "ordem": 1, "passo": "A", "minutos": 10, "link": ""},
    {"semana": 1, "dia": 2, "ordem": 2, "passo": "B", "minutos": 10, "link": ""},
    {"semana": 1, "dia": 1, "ordem": 1, "passo": "X", "minutos": 20, "link": ""},
]}


def test_passos_do_dia_e_semana_vazia(ctx):
    assert [p["passo"] for p in chamar(ctx, "ICE.plano.passosDoDia", PLANO, 1, 2)] == ["A", "B", "C"]
    assert chamar(ctx, "ICE.plano.passosDoDia", PLANO, 7, 1) == []


def test_dias_concluidos(ctx):
    assert chamar(ctx, "ICE.plano.diasConcluidos", PLANO, {"s1d1": [1], "s1d2": [1, 3]}) == 1
    assert chamar(ctx, "ICE.plano.diasConcluidos", PLANO, {"s1d1": [1], "s1d2": [3, 2, 1]}) == 2


def test_ler_plano_tolerante(ctx):
    vazio = {"versao": 1, "inicio": None, "feitos": {}}
    for texto in ["{quebrado", None, '{"versao": 2}']:
        assert chamar(ctx, "ICE.plano.ler", texto) == vazio


def test_ficha_registrar(ctx):
    estado = chamar(ctx, "ICE.ficha.ler", None)
    campos = {"gravacao": "2026-11-13", "tempo4": 220, "tempo3": "3:40", "tempo2": 120,
              "conversa": True, "confianca": "7"}
    novo = chamar(ctx, "ICE.ficha.registrar", estado, 2, campos)
    assert novo["semanas"]["2"] == {"gravacao": "2026-11-13", "tempo4": 220, "tempo3": None, "tempo2": 120,
                                    "conversa": True, "confianca": None}
    assert chamar(ctx, "ICE.ficha.registrar", estado, 1, {**campos, "gravacao": "13/11", "confianca": "4"})[
        "semanas"]["1"]["confianca"] == 4


# O tempo entra em dois campos (minutos e segundos), porque o teclado numérico
# do iPhone e do Gboard não tem ":" (achado C1 da revisão final).
@pytest.mark.parametrize("minutos, segs, esperado", [
    ("3", "40", 220), ("4", "", 240), ("", "40", 40), (" 3 ", "05", 185), ("0", "0", 0), ("", "", None),
])
def test_ficha_tempo_em_dois_campos(ctx, minutos, segs, esperado):
    assert chamar(ctx, "ICE.ficha.tempo", minutos, segs) == {"segundos": esperado, "erro": None}


@pytest.mark.parametrize("minutos, segs", [
    ("3", "75"), ("3.5", ""), ("3:40", ""), ("abc", ""), ("", "-5"), ("123", "0"),
])
def test_ficha_tempo_invalido_avisa_em_vez_de_sumir(ctx, minutos, segs):
    resultado = chamar(ctx, "ICE.ficha.tempo", minutos, segs)
    assert resultado["segundos"] is None
    assert resultado["erro"]
