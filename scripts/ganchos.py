"""Ganchos (hooks) do Claude Code para este projeto.

A configuração fica em `.claude/settings.json`, fora do git; a lógica fica aqui, com testes:

- `python -m scripts.ganchos guarda` (antes de Edit e Write): barra a edição à mão de um arquivo gerado
  e o texto com dado pessoal (os mesmos termos que `test_repositorio_sem_dados_pessoais` procura).
- `python -m scripts.ganchos construir` (depois de Edit e Write em `kit/`, `scripts/` ou `conteudo/`):
  roda `python -m scripts.construir` e, se ele falhar, devolve a saída ao Claude.

O evento chega em JSON na entrada padrão. Código 2 bloqueia (antes) ou avisa o Claude (depois).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Callable

from scripts import RAIZ

# Gerados não se editam à mão (CLAUDE.md): saem do `construir`.
GERADOS = ("kit/gerado/", "conteudo/dados/", "CREDITOS.md", "conteudo/estilos/tokens.css")
# Montados por partes para este arquivo não acusar a si mesmo no teste do repositório.
PESSOAIS = ["ingles-" + "pessoal", "/ho" + "me/", "/tm" + "p/", "espo" + "sa", "Ang" + "elo"]
# O `construir` confere dados, planos e guia: vale rodar depois de mexer nestas pastas.
CONFERIDOS = ("kit/", "scripts/", "conteudo/")


def _relativo(evento: dict, raiz: Path) -> str | None:
    caminho = (evento.get("tool_input") or {}).get("file_path")
    if not caminho:
        return None
    try:
        return Path(caminho).resolve().relative_to(Path(raiz).resolve()).as_posix()
    except ValueError:
        return None


def _texto_novo(evento: dict) -> str:
    entrada = evento.get("tool_input") or {}
    partes = [entrada.get("content") or "", entrada.get("new_string") or ""]
    partes += [e.get("new_string") or "" for e in entrada.get("edits") or []]
    return "\n".join(partes)


def guarda(evento: dict, raiz: Path = RAIZ) -> str | None:
    """O motivo para barrar a edição, ou None se ela pode seguir. Só olha arquivos do projeto."""
    relativo = _relativo(evento, raiz)
    if relativo is None:
        return None
    if any(relativo == g or (g.endswith("/") and relativo.startswith(g)) for g in GERADOS):
        return (f"{relativo} é gerado e não se edita à mão: mude o CSV ou o script de origem e rode "
                ".venv/bin/python -m scripts.construir.")
    achados = [t for t in PESSOAIS if t in _texto_novo(evento)]
    if achados:
        return (f"o texto novo de {relativo} tem dado pessoal ou caminho da máquina ({', '.join(achados)}), "
                "que não pode entrar no repositório (test_repositorio_sem_dados_pessoais).")
    return None


def _executar_construir(raiz: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "-m", "scripts.construir"], cwd=raiz, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def construir_depois(evento: dict, raiz: Path = RAIZ,
                     executar: Callable[[Path], tuple[int, str]] = _executar_construir) -> str | None:
    """A saída do `construir` quando ele falha depois da edição; None quando passa ou não se aplica."""
    relativo = _relativo(evento, raiz)
    if relativo is None or not relativo.startswith(CONFERIDOS):
        return None
    codigo, saida = executar(raiz)
    if codigo == 0:
        return None
    return f"Depois de editar {relativo}, o construir acusou:\n{saida}"


def main(argv: list[str]) -> int:
    evento = json.loads(sys.stdin.read() or "{}")
    if argv[:1] == ["guarda"]:
        motivo = guarda(evento)
    elif argv[:1] == ["construir"]:
        motivo = construir_depois(evento)
    else:
        print("uso: python -m scripts.ganchos guarda|construir", file=sys.stderr)
        return 1
    if motivo:
        print(motivo, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
