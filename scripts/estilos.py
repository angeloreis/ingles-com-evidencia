"""Gera conteudo/estilos/tokens.css a partir de design/passaporte/tokens.json.

Uso: python -m scripts.estilos
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from scripts import RAIZ

TOKENS_JSON = RAIZ / "design/passaporte/tokens.json"
TOKENS_CSS = RAIZ / "conteudo/estilos/tokens.css"

CABECALHO = "/* Gerado por scripts/estilos.py a partir de design/passaporte/tokens.json. Não edite à mão. */"
SELETOR_CLARO = ':root, [data-md-color-scheme="default"]'
SELETOR_ESCURO = '[data-md-color-scheme="slate"]'
TEMAS = {"light": SELETOR_CLARO, "dark": SELETOR_ESCURO}

RE_APELIDO = re.compile(r"\{([a-z0-9-]+)\}")


def carregar_tokens(caminho: Path = TOKENS_JSON) -> dict:
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def resolver_cores(tokens: dict) -> dict[str, dict[str, str]]:
    """{"light": {nome: "#hex"}, "dark": {...}}, com os apelidos "{outro}" resolvidos."""
    brutos = {t["name"]: t["value"] for t in tokens["color"]["tokens"]}

    def resolver(nome: str, tema: str) -> str:
        valor = brutos[nome]
        apelido = RE_APELIDO.fullmatch(valor) if isinstance(valor, str) else None
        return resolver(apelido.group(1), tema) if apelido else valor[tema]

    return {tema: {nome: resolver(nome, tema) for nome in brutos} for tema in TEMAS}


def gerar_tokens_css(tokens: dict) -> str:
    blocos = [CABECALHO]
    for tema, seletor in TEMAS.items():
        linhas = []
        for t in tokens["color"]["tokens"]:
            valor = t["value"]
            apelido = RE_APELIDO.fullmatch(valor) if isinstance(valor, str) else None
            linhas.append((t["name"], f"var(--{apelido.group(1)})" if apelido else valor[tema]))
        blocos.append(_bloco(seletor, linhas))

    gerais = [(f"font-{nome}", valor) for nome, valor in tokens["type"]["families"].items()]
    for grupo in tokens["type"]["groups"]:
        for estilo in grupo["styles"]:
            nome = estilo["name"]
            gerais += [(f"{nome}-tamanho", estilo["fontSize"]),
                       (f"{nome}-altura", estilo["lineHeight"]),
                       (f"{nome}-peso", estilo["fontWeight"])]
            if "letterSpacing" in estilo:
                gerais.append((f"{nome}-espacamento", estilo["letterSpacing"]))
    for familia in ("spacing", "radius", "medida"):
        gerais += [(t["name"], t["value"]) for t in tokens[familia]["tokens"]]
    blocos.append(_bloco(":root", gerais))
    return "\n\n".join(blocos) + "\n"


def _bloco(seletor: str, linhas: list[tuple[str, object]]) -> str:
    corpo = "\n".join(f"  --{nome}: {valor};" for nome, valor in linhas)
    return f"{seletor} {{\n{corpo}\n}}"


def contraste(cor_a: str, cor_b: str) -> float:
    """Razão de contraste WCAG 2.x entre duas cores #rrggbb (a ordem não importa)."""
    claro, escuro = sorted((_luminancia(cor_a), _luminancia(cor_b)), reverse=True)
    return (claro + 0.05) / (escuro + 0.05)


def _luminancia(cor: str) -> float:
    h = cor.lstrip("#")
    canais = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def main() -> int:
    TOKENS_CSS.write_text(gerar_tokens_css(carregar_tokens()), encoding="utf-8")
    print(f"Gerado: {TOKENS_CSS.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
