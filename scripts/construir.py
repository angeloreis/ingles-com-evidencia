"""Roda as etapas do kit. Na Fase 0, só a validação dos CSVs.

Uso: python -m scripts.construir [--dados PASTA]
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from scripts import RAIZ
from scripts.validar import validar_pasta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida os CSVs dos baralhos do kit.")
    parser.add_argument("--dados", type=Path, default=RAIZ / "kit" / "dados",
                        help="pasta com os CSVs (padrão: kit/dados)")
    args = parser.parse_args(argv)

    relatorio = validar_pasta(args.dados)
    if relatorio.erros:
        for erro in relatorio.erros:
            print(f"{os.path.relpath(erro.arquivo)}:{erro.linha}: {erro.mensagem}", file=sys.stderr)
        print(f"{len(relatorio.erros)} problema(s) encontrado(s).", file=sys.stderr)
        return 1
    print(f"Tudo certo: {relatorio.arquivos} arquivo(s), {relatorio.linhas} linha(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
