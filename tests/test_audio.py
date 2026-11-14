import hashlib
import http.server
import json
import threading
from functools import partial

import numpy as np
import pytest
import soundfile as sf

from scripts.audio import ItemAudio, baixar_modelos, gerar_audios, itens_de_audio


class SintetizadorFalso:
    def __init__(self):
        self.chamadas = []

    def __call__(self, texto, voz):
        self.chamadas.append((texto, voz))
        t = np.linspace(0, 0.2, 4800, dtype=np.float32)
        return (0.2 * np.sin(2 * np.pi * 440 * t)).astype(np.float32), 24000


ITENS = [ItemAudio("a-01", "Can we talk?", "af_heart"), ItemAudio("a-02", "Sure.", "am_michael")]


def test_gera_mp3_e_manifesto(tmp_path):
    falso = SintetizadorFalso()
    manifesto = gerar_audios(ITENS, tmp_path, falso)
    assert sorted(manifesto) == ["ice-a-01.mp3", "ice-a-02.mp3"]
    assert sf.info(str(tmp_path / "ice-a-01.mp3")).format == "MP3"
    assert json.loads((tmp_path / "manifesto.json").read_text(encoding="utf-8")) == manifesto


def test_nao_regera_o_que_nao_mudou(tmp_path):
    gerar_audios(ITENS, tmp_path, SintetizadorFalso())
    falso = SintetizadorFalso()
    gerar_audios(ITENS, tmp_path, falso)
    assert falso.chamadas == []


def test_regera_quando_o_texto_muda(tmp_path):
    gerar_audios(ITENS, tmp_path, SintetizadorFalso())
    falso = SintetizadorFalso()
    gerar_audios([ITENS[0], ItemAudio("a-02", "Sure thing.", "am_michael")], tmp_path, falso)
    assert falso.chamadas == [("Sure thing.", "am_michael")]


def test_apaga_orfaos(tmp_path):
    gerar_audios(ITENS, tmp_path, SintetizadorFalso())
    manifesto = gerar_audios(ITENS[:1], tmp_path, SintetizadorFalso())
    assert not (tmp_path / "ice-a-02.mp3").exists() and "ice-a-02.mp3" not in manifesto


def test_vozes_do_dialogo(tmp_path):
    (tmp_path / "kit" / "dados").mkdir(parents=True)
    (tmp_path / "kit" / "dialogos").mkdir()
    (tmp_path / "kit" / "dados" / "s.csv").write_text(
        "id,en,pt,situacao,fonte,licenca\nf-01,Hello,Olá,6,projeto,CC BY-SA 4.0\n", encoding="utf-8")
    (tmp_path / "kit" / "dialogos" / "d.csv").write_text(
        "id,situacao,ordem,falante,en,pt,fonte,licenca\n"
        "d-01,6,1,A,Hi,Oi,projeto,CC BY-SA 4.0\nd-02,6,2,B,Hey,Ei,projeto,CC BY-SA 4.0\n", encoding="utf-8")
    vozes = {i.id: i.voz for i in itens_de_audio(tmp_path)}
    assert vozes == {"f-01": "af_heart", "d-01": "af_heart", "d-02": "am_michael"}


@pytest.fixture
def servidor(tmp_path):
    pasta = tmp_path / "servidor"
    pasta.mkdir()
    (pasta / "modelo.bin").write_bytes(b"conteudo do modelo")
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
                                            partial(http.server.SimpleHTTPRequestHandler, directory=str(pasta)))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def test_sha256_errado_apaga_e_avisa(tmp_path, servidor):
    destino = tmp_path / "modelos"
    arquivo = {"arquivo": "modelo.bin", "url": f"{servidor}/modelo.bin", "sha256": "0" * 64}
    with pytest.raises(RuntimeError, match="sha256"):
        baixar_modelos(destino, (arquivo,))
    assert not any(destino.iterdir())


def test_sha256_certo_baixa(tmp_path, servidor):
    certo = hashlib.sha256(b"conteudo do modelo").hexdigest()
    arquivo = {"arquivo": "modelo.bin", "url": f"{servidor}/modelo.bin", "sha256": certo}
    (caminho,) = baixar_modelos(tmp_path / "modelos", (arquivo,))
    assert caminho.read_bytes() == b"conteudo do modelo"


def test_itens_de_audio_usam_a_leitura(tmp_path):
    (tmp_path / "kit" / "dados").mkdir(parents=True)
    (tmp_path / "kit" / "dialogos").mkdir()
    (tmp_path / "kit" / "dados" / "s.csv").write_text(
        "id,en,pt,situacao,fonte,licenca,leitura\n"
        "t-01,We moved to PostgreSQL.,Mudamos para o PostgreSQL.,7,projeto,CC BY-SA 4.0,We moved to post gres Q L.\n"
        "t-02,Hello,Olá,7,projeto,CC BY-SA 4.0,\n", encoding="utf-8")
    (tmp_path / "kit" / "dialogos" / "d.csv").write_text(
        "id,situacao,ordem,falante,en,pt,fonte,licenca,leitura\n"
        "t-d01,7,1,A,Hi.,Oi.,projeto,CC BY-SA 4.0,\n"
        "t-d02,7,2,B,I use regex.,Eu uso regex.,projeto,CC BY-SA 4.0,I use rej ex.\n", encoding="utf-8")
    assert itens_de_audio(tmp_path) == [
        ItemAudio("t-01", "We moved to post gres Q L.", "af_heart"),
        ItemAudio("t-02", "Hello", "af_heart"),
        ItemAudio("t-d01", "Hi.", "af_heart"),
        ItemAudio("t-d02", "I use rej ex.", "am_michael"),
    ]


# --- Revisão final da Fase 1B: leituras conferidas com o Oxford (IPA americano) ---------------
import csv as _csv

from scripts import RAIZ as _RAIZ


def _linha(arquivo, ident):
    with open(_RAIZ / "kit" / arquivo, encoding="utf-8", newline="") as f:
        return next(l for l in _csv.DictReader(f) if l["id"] == ident)


@pytest.mark.parametrize("arquivo, ident, trecho", [
    ("dados/situacao-08.csv", "entrevista-06", "A-synchronously"),  # /eɪˈsɪŋkrənəs/, não "uh-sink"
    ("dados/situacao-07.csv", "tecnologia-09", "algorhythm"),       # /ˈælɡərɪðəm/, com ð e não θ
    ("dados/situacao-07.csv", "tecnologia-04", "queery"),           # /ˈkwɪri/, e não "kway-ree"
])
def test_leitura_segue_o_dicionario(arquivo, ident, trecho):
    assert trecho in _linha(arquivo, ident)["leitura"]


def test_dialogo_da_situacao_7_concorda_o_pronome():
    fala = _linha("dialogos/situacao-07.csv", "tecnologia-d05")
    assert fala["en"] == "The AI wrote the first drafts, and I fixed two of them."
    assert fala["pt"] == "A IA escreveu as primeiras versões, e eu corrigi duas delas."


def test_baixar_usa_tempo_limite(tmp_path, monkeypatch):
    # M12 da 1A: sem tempo limite, uma conexão parada travava o build para sempre
    import io
    import urllib.request

    pedidos = []

    def abrir(url, timeout=None):
        pedidos.append(timeout)
        return io.BytesIO(b"x")

    monkeypatch.setattr(urllib.request, "urlopen", abrir)
    baixar_modelos(tmp_path, ({"arquivo": "m", "url": "https://exemplo", "sha256": hashlib.sha256(b"x").hexdigest()},))
    assert pedidos == [60]
