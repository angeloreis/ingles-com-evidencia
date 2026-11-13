"""Trechos gerados para as páginas (frases, diálogo, semanas) e os dados das cartas.

Os trechos ficam em kit/gerado/ e entram nas páginas escritas à mão pelo pymdownx.snippets.
"""
from __future__ import annotations

import csv
import io
import json
import re
from html import escape
from pathlib import Path

from scripts.planos import RE_LINK, TRILHAS, dados_do_plano


def nome_audio(id_: str) -> str:
    return f"ice-{id_}.mp3"


def _e(texto: str) -> str:
    return escape(texto, quote=True)


# Os caracteres que o Python-Markdown aceita escapar com barra (o > some no escape de HTML).
_ESPECIAIS_MD = re.compile(r"([\\`*_{}\[\]()#+\-.!])")


def _texto_md(texto: str) -> str:
    """Texto puro dentro de Markdown: sem HTML e sem formatação."""
    return _ESPECIAIS_MD.sub(r"\\\1", escape(texto, quote=False))


def silaba_html(silaba: str) -> str:
    """'va·CA·tion' → 'va·<b>CA</b>·tion': a parte em maiúsculas é a sílaba forte."""
    partes = []
    for parte in silaba.split("·"):
        partes.append(f"<b>{_e(parte)}</b>" if parte.isupper() else _e(parte))
    return "·".join(partes)


def _frase_li(linha: dict, falante: str | None = None) -> str:
    partes = ['<li class="pp-frase">']
    if falante:
        partes.append(f'<span class="pp-frase__falante">Pessoa {_e(falante)}</span>')
    partes.append(f'<p class="pp-frase__en" lang="en">{_e(linha["en"])}</p>')
    partes.append(f'<p class="pp-frase__pt">{_e(linha["pt"])}</p>')
    if linha.get("silaba"):
        partes.append(f'<p class="pp-frase__silaba">Sílaba forte: {silaba_html(linha["silaba"])}</p>')
    partes.append(f'<button type="button" class="pp-botao" data-audio="{nome_audio(linha["id"])}">Ouvir</button>')
    partes.append("</li>")
    return "\n".join(partes)


def trecho_frases(linhas: list[dict]) -> str:
    return "\n".join(['<ul class="pp-frases">', *(_frase_li(l) for l in linhas), "</ul>"]) + "\n"


def trecho_dialogo(linhas: list[dict]) -> str:
    ordenadas = sorted(linhas, key=lambda l: int(l["ordem"]))
    sequencia = " ".join(nome_audio(l["id"]) for l in ordenadas)
    return "\n".join([
        '<ul class="pp-frases">',
        *(_frase_li(l, l["falante"]) for l in ordenadas),
        "</ul>",
        f'<button type="button" class="pp-botao pp-botao--largo" data-audio-sequencia="{sequencia}">'
        "Ouvir o diálogo inteiro</button>",
    ]) + "\n"


def trecho_semanas(dados: dict) -> str:
    """Lista das semanas para a página da trilha (incluída em trilhas/<trilha>/index.md)."""
    blocos: list[str] = []
    semanas = sorted({p["semana"] for p in dados["passos"]})
    for semana in semanas:
        blocos.append(f"### Semana {semana}\n")
        dias = sorted({p["dia"] for p in dados["passos"] if p["semana"] == semana})
        for dia in dias:
            passos = [p for p in dados["passos"] if p["semana"] == semana and p["dia"] == dia]
            total = sum(p["minutos"] for p in passos)
            itens = []
            for p in passos:
                if p["link"] and not RE_LINK.fullmatch(p["link"]):
                    raise ValueError(f"link fora do formato no plano: {p['link']!r}")
                texto = _texto_md(p["passo"])
                if p["link"]:
                    texto = f"[{texto}](../../{p['link']})"
                itens.append(f"- {texto} — {p['minutos']} min")
            blocos.append(f"**Dia {dia} — {total} min**\n\n" + "\n".join(itens) + "\n")
    ultima = max(semanas) if semanas else 0
    if ultima < dados["semanas"]:
        blocos.append(f"*As semanas {ultima + 1} a {dados['semanas']} ainda não foram publicadas.*\n")
    return "\n".join(blocos)


def cartas(linhas_baralho: list[dict]) -> list[dict]:
    return [{"id": l["id"], "en": l["en"], "pt": l["pt"], "silaba": l.get("silaba", ""),
             "situacao": int(l["situacao"]), "audio": nome_audio(l["id"])}
            for l in linhas_baralho if l.get("situacao")]


def _ler_csvs(pasta: Path) -> list[dict]:
    linhas: list[dict] = []
    if not pasta.is_dir():
        return linhas
    for caminho in sorted(pasta.glob("*.csv")):
        texto = caminho.read_bytes().decode("utf-8-sig")
        for campos in csv.DictReader(io.StringIO(texto, newline="")):
            valores = {(k or "").strip(): (v or "").strip() for k, v in campos.items() if k is not None}
            if any(valores.values()):
                linhas.append(valores)
    return linhas


def _gravar(caminho: Path, texto: str, gravados: list[Path]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8")
    gravados.append(caminho)


def gerar_tudo(raiz: Path) -> list[Path]:
    """Gera os trechos e os dados a partir de raiz/kit; apaga trechos que deixaram de existir."""
    raiz = Path(raiz)
    gravados: list[Path] = []
    gerado = raiz / "kit" / "gerado"
    baralho = _ler_csvs(raiz / "kit" / "dados")
    dialogos = _ler_csvs(raiz / "kit" / "dialogos")

    for situacao in sorted({int(l["situacao"]) for l in baralho if l.get("situacao")}):
        linhas = [l for l in baralho if l.get("situacao") and int(l["situacao"]) == situacao]
        _gravar(gerado / f"frases-{situacao:02d}.md", trecho_frases(linhas), gravados)
    for situacao in sorted({int(l["situacao"]) for l in dialogos}):
        linhas = [l for l in dialogos if int(l["situacao"]) == situacao]
        _gravar(gerado / f"dialogo-{situacao:02d}.md", trecho_dialogo(linhas), gravados)
    for trilha in TRILHAS:
        csv_plano = raiz / "kit" / "planos" / f"{trilha}.csv"
        if csv_plano.exists():
            texto = trecho_semanas(dados_do_plano(csv_plano, trilha))
        else:
            texto = "*O plano desta trilha ainda não foi publicado.*\n"
        _gravar(gerado / f"semanas-{trilha}.md", texto, gravados)

    if gerado.is_dir():
        for antigo in gerado.glob("*.md"):
            if antigo not in gravados:
                antigo.unlink()
    _gravar(raiz / "conteudo" / "dados" / "cartas.json",
            json.dumps(cartas(baralho), ensure_ascii=False, indent=2) + "\n", gravados)
    return gravados
