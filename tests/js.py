"""Roda o JavaScript do site no pytest, com o V8 do mini-racer (sem Node)."""
from __future__ import annotations

import json

from py_mini_racer import MiniRacer

from scripts import RAIZ


def contexto(*arquivos: str) -> MiniRacer:
    """Avalia conteudo/js/<arquivo> em ordem, num contexto novo."""
    ctx = MiniRacer()
    for arquivo in arquivos:
        ctx.eval((RAIZ / "conteudo" / "js" / arquivo).read_text(encoding="utf-8"))
    return ctx


def chamar(ctx: MiniRacer, funcao: str, *args):
    """Chama `funcao` com argumentos em JSON e devolve o resultado convertido de JSON."""
    argumentos = ", ".join(json.dumps(a, ensure_ascii=False) for a in args)
    return json.loads(ctx.eval(f"JSON.stringify({funcao}({argumentos}))"))


def avaliar(ctx: MiniRacer, expressao: str):
    return json.loads(ctx.eval(f"JSON.stringify({expressao})"))
