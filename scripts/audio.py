"""Áudio das frases e dos diálogos com a voz sintética Kokoro (kokoro-onnx).

Os arquivos vão para conteudo/audio/ (fora do git), com um manifesto.json que o site lê
para saber quais botões "Ouvir" têm áudio. Só o que mudou é gerado de novo.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from scripts.paginas import _ler_csvs, nome_audio

VOZ_PRINCIPAL = "af_heart"   # frases e pessoa A do diálogo
VOZ_PARCEIRA = "am_michael"  # pessoa B do diálogo
VELOCIDADE = 0.9

_RELEASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1"
MODELO = {"arquivo": "kokoro-v1.0.onnx", "url": f"{_RELEASE}/kokoro-v1.0.onnx",
          "sha256": "beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a"}
VOZES = {"arquivo": "voices-v1.0.bin", "url": f"{_RELEASE}/voices-v1.0.bin",
         "sha256": "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d"}


@dataclass(frozen=True)
class ItemAudio:
    id: str
    texto: str
    voz: str


def pasta_modelos() -> Path:
    return Path(os.environ.get("ICE_MODELOS") or Path.home() / ".cache" / "ingles-com-evidencia" / "kokoro")


def _sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def baixar_modelos(pasta: Path, arquivos: tuple[dict, ...] = (MODELO, VOZES)) -> tuple[Path, ...]:
    """Baixa só o que falta e confere o sha256; arquivo que não confere é apagado."""
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    caminhos = []
    for a in arquivos:
        destino = pasta / a["arquivo"]
        if destino.exists() and (a["sha256"] is None or _sha256(destino) == a["sha256"]):
            caminhos.append(destino)
            continue
        parcial = destino.with_name(destino.name + ".parcial")
        try:
            with urllib.request.urlopen(a["url"]) as resposta, open(parcial, "wb") as saida:
                for bloco in iter(lambda: resposta.read(1 << 20), b""):
                    saida.write(bloco)
            obtido = _sha256(parcial)
            if a["sha256"] is None:
                print(f"aviso: sha256 de {a['arquivo']} ainda não registrado em scripts/audio.py: {obtido}",
                      file=sys.stderr)
            elif obtido != a["sha256"]:
                raise RuntimeError(f"o sha256 de {a['arquivo']} não confere: esperado {a['sha256']}, veio {obtido}. "
                                   "O arquivo foi apagado; confira a URL e tente de novo.")
            parcial.replace(destino)
        finally:
            if parcial.exists():
                parcial.unlink()
        caminhos.append(destino)
    return tuple(caminhos)


def itens_de_audio(raiz: Path) -> list[ItemAudio]:
    raiz = Path(raiz)
    itens = [ItemAudio(l["id"], l["en"], VOZ_PRINCIPAL) for l in _ler_csvs(raiz / "kit" / "dados")]
    for l in _ler_csvs(raiz / "kit" / "dialogos"):
        itens.append(ItemAudio(l["id"], l["en"], VOZ_PARCEIRA if l["falante"] == "B" else VOZ_PRINCIPAL))
    return itens


def _assinatura(item: ItemAudio, modelo: str) -> str:
    return hashlib.sha256(f"{item.texto}|{item.voz}|{VELOCIDADE}|{modelo}".encode("utf-8")).hexdigest()


def gerar_audios(itens: list[ItemAudio], destino: Path,
                 sintetizar: Callable[[str, str], tuple], modelo: str = MODELO["arquivo"]) -> dict:
    """Gera ice-<id>.mp3 para cada item, pula o que não mudou e apaga os órfãos."""
    import soundfile as sf

    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    caminho_manifesto = destino / "manifesto.json"
    try:
        antigo = json.loads(caminho_manifesto.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        antigo = {}

    manifesto: dict[str, str] = {}
    for item in itens:
        arquivo = nome_audio(item.id)
        assinatura = _assinatura(item, modelo)
        if antigo.get(arquivo) == assinatura and (destino / arquivo).exists():
            manifesto[arquivo] = assinatura
            continue
        amostras, taxa = sintetizar(item.texto, item.voz)
        sf.write(str(destino / arquivo), amostras, taxa, format="MP3")
        manifesto[arquivo] = assinatura

    for orfao in destino.glob("ice-*.mp3"):
        if orfao.name not in manifesto:
            orfao.unlink()
    manifesto = dict(sorted(manifesto.items()))
    caminho_manifesto.write_text(json.dumps(manifesto, indent=2) + "\n", encoding="utf-8")
    return manifesto


def sintetizador_kokoro(modelo: Path, vozes: Path) -> Callable[[str, str], tuple]:
    from kokoro_onnx import Kokoro

    kokoro = Kokoro(str(modelo), str(vozes))

    def sintetizar(texto: str, voz: str) -> tuple:
        return kokoro.create(texto, voice=voz, speed=VELOCIDADE, lang="en-us")

    return sintetizar
