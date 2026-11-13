import pytest

from js import avaliar, chamar, contexto


@pytest.fixture
def ctx():
    return contexto("logica/datas.js", "logica/audio.js")


def test_iso_usa_data_local(ctx):
    # 23h30 no horário local ainda é dia 13, mesmo que em UTC já seja dia 14
    assert avaliar(ctx, "ICE.datas.iso(new Date(2026, 10, 13, 23, 30))") == "2026-11-13"


@pytest.mark.parametrize("iso, n, esperado", [
    ("2026-10-31", 1, "2026-11-01"),
    ("2026-12-31", 1, "2027-01-01"),
    ("2026-11-13", -7, "2026-11-06"),
])
def test_somar_dias(ctx, iso, n, esperado):
    assert chamar(ctx, "ICE.datas.somarDias", iso, n) == esperado


def test_dias_entre(ctx):
    assert chamar(ctx, "ICE.datas.diasEntre", "2026-11-13", "2026-11-20") == 7
    assert chamar(ctx, "ICE.datas.diasEntre", "2026-11-20", "2026-11-13") == -7


def test_botao_de_audio(ctx):
    manifesto = {"ice-a.mp3": "hash"}
    assert chamar(ctx, "ICE.audio.estadoDoBotao", manifesto, "ice-a.mp3") == {"habilitado": True, "rotulo": "Ouvir"}
    assert chamar(ctx, "ICE.audio.estadoDoBotao", manifesto, "ice-b.mp3") == {"habilitado": False,
                                                                              "rotulo": "Sem áudio aqui"}
    assert chamar(ctx, "ICE.audio.estadoDoBotao", None, "ice-a.mp3")["habilitado"] is False


def test_todos_os_scripts_do_site_tem_sintaxe_valida():
    # Os scripts de página tocam no DOM e não rodam aqui; ao menos a sintaxe é conferida.
    import json as _json

    from py_mini_racer import MiniRacer

    from scripts import RAIZ

    ctx = MiniRacer()
    arquivos = sorted((RAIZ / "conteudo" / "js").rglob("*.js"))
    assert arquivos
    for arquivo in arquivos:
        fonte = arquivo.read_text(encoding="utf-8")
        assert ctx.eval(f"(function () {{ new Function({_json.dumps(fonte)}); return true; }})()"), arquivo
