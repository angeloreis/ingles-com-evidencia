import pytest

from js import avaliar, chamar, contexto


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


# Fase 1B, Tarefa 3 (M11): estado salvo com campo null abre como primeira visita.
def test_ler_plano_com_campo_nulo(ctx):
    assert chamar(ctx, "ICE.plano.ler", '{"versao": 1, "inicio": null, "feitos": null}') == \
        {"versao": 1, "inicio": None, "feitos": {}}


def test_ler_ficha_com_campo_nulo(ctx):
    assert chamar(ctx, "ICE.ficha.ler", '{"versao": 1, "semanas": null}') == {"versao": 1, "semanas": {}}


# Fase 1B, Tarefa 5 (M9): depois da última semana publicada, "Hoje" sugere o que fazer.
def test_ultima_semana(ctx):
    assert chamar(ctx, "ICE.plano.ultimaSemana", PLANO) == 1
    passo = {"passo": "A", "minutos": 5, "link": "", "dia": 1, "ordem": 1}
    plano = {"trilha": "destravar", "semanas": 12,
             "passos": [{**passo, "semana": 1}, {**passo, "semana": 3}]}
    assert chamar(ctx, "ICE.plano.ultimaSemana", plano) == 3
    assert chamar(ctx, "ICE.plano.ultimaSemana", {"passos": []}) == 0


# Revisão final da 1B: semana depois da última publicada, também quando passou das 12 semanas.
def test_depois_do_publicado(ctx):
    passo = {"passo": "A", "minutos": 20, "link": "", "dia": 1, "ordem": 1}
    seis = {"trilha": "destravar", "semanas": 12, "passos": [{**passo, "semana": s} for s in range(1, 7)]}
    doze = {"trilha": "destravar", "semanas": 12, "passos": [{**passo, "semana": s} for s in range(1, 13)]}
    assert chamar(ctx, "ICE.plano.depoisDoPublicado", seis, 6) is False
    assert chamar(ctx, "ICE.plano.depoisDoPublicado", seis, 8) is True
    assert chamar(ctx, "ICE.plano.depoisDoPublicado", seis, 13) is True
    assert chamar(ctx, "ICE.plano.depoisDoPublicado", doze, 13) is False
    assert chamar(ctx, "ICE.plano.depoisDoPublicado", {"semanas": 12, "passos": []}, 13) is False


VAZIO = {"versao": 1, "inicio": None, "feitos": {}}


@pytest.mark.parametrize("inicio", ['"13/11/2026"', '"2026-02-30"', "20261113"])
def test_ler_plano_com_inicio_invalido(ctx, inicio):
    texto = '{"versao": 1, "inicio": ' + inicio + ', "feitos": {}}'
    assert chamar(ctx, "ICE.plano.ler", texto) == VAZIO


def test_ler_plano_com_inicio_valido(ctx):
    texto = '{"versao": 1, "inicio": "2026-11-13", "feitos": {"s1d1": [1]}}'
    assert chamar(ctx, "ICE.plano.ler", texto) == {"versao": 1, "inicio": "2026-11-13", "feitos": {"s1d1": [1]}}


PASSOS = [{"ordem": 1}, {"ordem": 2}, {"ordem": 3}]


@pytest.mark.parametrize("feitos, esperado", [([], 1), ([1], 2), ([2], 1), ([1, 2, 3], None)])
def test_proximo_aberto(ctx, feitos, esperado):
    assert chamar(ctx, "ICE.plano.proximoAberto", PASSOS, feitos) == esperado


@pytest.mark.parametrize("feitos, esperado", [
    ([], "0 de 3 passos feitos."),
    ([1, 3], "2 de 3 passos feitos."),
    ([1, 2, 3], "Dia concluído: todos os passos de hoje estão feitos."),
])
def test_resumo_do_dia(ctx, feitos, esperado):
    assert chamar(ctx, "ICE.plano.resumoDoDia", PASSOS, feitos) == esperado


def test_mensagem_de_falha(ctx):
    # o chamar passa os argumentos por JSON, que não leva um Error
    assert avaliar(ctx, 'ICE.plano.mensagemDeFalha(new Error("HTTP 404"))') == \
        "O plano desta trilha ainda não foi publicado."
    assert avaliar(ctx, 'ICE.plano.mensagemDeFalha(new TypeError("Failed to fetch"))') == \
        "Não foi possível carregar o plano. Confira a conexão e recarregue a página."


def test_depois_do_publicado_com_o_plano_completo(ctx):
    completo = {"semanas": 12, "passos": [{"semana": 1, "dia": 1, "ordem": 1}, {"semana": 12, "dia": 1, "ordem": 1}]}
    assert chamar(ctx, "ICE.plano.depoisDoPublicado", completo, 13) is False
