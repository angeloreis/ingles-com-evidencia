"""Baralhos do Anki (.apkg) da trilha Destravar a fala: cartas de "produzir".

Português na frente; a pessoa fala em inglês, em voz alta, e confere no verso com o áudio.
O guid de cada nota vem do id da linha, então corrigir uma tradução atualiza a carta de quem
já importou o baralho, em vez de duplicar.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

import genanki

from scripts.paginas import nome_audio, silaba_html
from scripts.situacoes import SITUACOES

# Gerados uma vez com random.randrange(1 << 30, 1 << 31). Nunca mudar: o Anki usa para reconhecer
# o modelo e os baralhos já importados.
MODELO_ID = 1791116790
BARALHO_BASE_ID = 1726547164

CSS = """
.card { font-family: Figtree, system-ui, sans-serif; font-size: 22px; line-height: 1.5;
        color: #0f231e; background: #f1f5f3; text-align: center; padding: 16px; }
.pt { font-weight: 700; }
.dica { color: #4f655d; font-size: 16px; }
.en { font-weight: 700; color: #0e5a49; }
.silaba { color: #4f655d; font-size: 16px; }
.credito { color: #4f655d; font-size: 12px; margin-top: 24px; }
.nightMode .card, .night_mode .card { color: #e2ece8; background: #0c1613; }
.nightMode .en, .night_mode .en { color: #5cc6a7; }
.nightMode .dica, .nightMode .silaba, .nightMode .credito,
.night_mode .dica, .night_mode .silaba, .night_mode .credito { color: #93a89f; }
"""

MODELO = genanki.Model(
    MODELO_ID,
    "Inglês com Evidência — Produzir",
    fields=[{"name": "Id"}, {"name": "Portugues"}, {"name": "Ingles"}, {"name": "Silaba"},
            {"name": "Audio"}, {"name": "Credito"}],
    templates=[{
        "name": "Produzir",
        "qfmt": '<div class="pt">{{Portugues}}</div><p class="dica">Fale em inglês, em voz alta.</p>',
        "afmt": ('{{FrontSide}}<hr id=answer><div class="en" lang="en">{{Ingles}}</div>'
                 '{{#Silaba}}<div class="silaba">Sílaba forte: {{Silaba}}</div>{{/Silaba}}'
                 '{{Audio}}<div class="credito">{{Credito}}</div>'),
    }],
    css=CSS,
)


class Nota(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def _credito(linha: dict) -> str:
    partes = [linha["fonte"], linha["licenca"]]
    if linha.get("autor"):
        partes.append(linha["autor"])
    return escape(" · ".join(partes))


def gerar_baralho(situacao: int, linhas: list[dict], pasta_audio: Path, destino: Path) -> Path:
    slug, titulo = SITUACOES[situacao]
    nome = f"Inglês com Evidência::Destravar a fala::{situacao:02d} {titulo}"
    baralho = genanki.Deck(BARALHO_BASE_ID + situacao, nome)
    midias = []
    for linha in linhas:
        audio = Path(pasta_audio) / nome_audio(linha["id"])
        if not audio.exists():
            raise RuntimeError(f"sem áudio: {linha['id']} (rode python -m scripts.construir --audio)")
        midias.append(str(audio))
        baralho.add_note(Nota(model=MODELO, fields=[
            escape(linha["id"]), escape(linha["pt"]), escape(linha["en"]),
            silaba_html(linha["silaba"]) if linha.get("silaba") else "",
            f"[sound:{nome_audio(linha['id'])}]", _credito(linha),
        ]))
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    caminho = destino / f"ice-destravar-situacao-{situacao:02d}.apkg"
    pacote = genanki.Package(baralho)
    pacote.media_files = midias
    pacote.write_to_file(str(caminho))
    return caminho
