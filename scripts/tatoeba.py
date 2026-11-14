"""Confere as frases do Tatoeba do kit com a API pública, frase a frase (sem baixar o export).

Uso: python -m scripts.tatoeba. Roda à mão, ao acrescentar ou revisar frases; não entra no
construir nem na Action, para o build não depender da rede do Tatoeba.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from typing import Callable

from scripts import RAIZ
from scripts.paginas import _ler_csvs

API = "https://api.tatoeba.org/unstable/sentences/"
TEMPO_LIMITE = 20
# Licença como a API devolve → como fica na coluna licenca do CSV.
LICENCAS = {"CC BY 2.0 FR": "CC BY 2.0 FR", "CC0 1.0": "CC0"}


def buscar_frase(numero: int) -> dict | None:
    pedido = urllib.request.Request(API + str(numero),
                                    headers={"User-Agent": "ingles-com-evidencia (conferencia de frases)"})
    try:
        with urllib.request.urlopen(pedido, timeout=TEMPO_LIMITE) as resposta:
            return json.load(resposta)["data"]
    except urllib.error.HTTPError as erro:
        if erro.code == 404:
            return None
        raise


def conferir_linhas(linhas: list[dict], buscar: Callable[[int], dict | None]) -> list[str]:
    problemas: list[str] = []
    for linha in linhas:
        if not linha.get("fonte", "").startswith("tatoeba:"):
            continue
        ident = linha["id"]
        frase = buscar(int(linha["fonte"].split(":", 1)[1]))
        if frase is None:
            problemas.append(f"{ident}: não existe mais no Tatoeba")
            continue
        if frase.get("text") != linha["en"]:
            problemas.append(f'{ident}: texto diferente do Tatoeba ("{linha["en"]}" × "{frase.get("text")}")')
        licenca = LICENCAS.get(frase.get("license"), frase.get("license"))
        if licenca != linha["licenca"]:
            problemas.append(f"{ident}: licença diferente (CSV {linha['licenca']}, Tatoeba {licenca})")
        dono = frase.get("owner")
        if not dono:
            problemas.append(f"{ident}: frase sem dono no Tatoeba")
        elif dono != linha.get("autor"):
            problemas.append(f"{ident}: autor diferente (CSV {linha.get('autor')}, Tatoeba {dono})")
        if frase.get("is_unapproved"):
            problemas.append(f"{ident}: frase ainda não aprovada no Tatoeba")
    return problemas


def main(argv: list[str] | None = None) -> int:
    linhas = _ler_csvs(RAIZ / "kit" / "dados") + _ler_csvs(RAIZ / "kit" / "dialogos")
    problemas = conferir_linhas(linhas, buscar_frase)
    if problemas:
        for p in problemas:
            print(p)
        return 1
    total = sum(1 for l in linhas if l.get("fonte", "").startswith("tatoeba:"))
    print(f"Frases do Tatoeba conferidas: {total}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
