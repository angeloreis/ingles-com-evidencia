"""Roda as etapas do kit: valida os CSVs, os planos e o guia; gera páginas, áudio e baralhos.

Uso: python -m scripts.construir [--dados PASTA] [--dialogos PASTA] [--planos PASTA] [--conteudo PASTA] [--audio] [--baralhos]
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from scripts import RAIZ
from scripts.guia import conferir_guia
from scripts.paginas import gerar_tudo
from scripts.planos import TRILHAS, gravar_dados, validar_plano
from scripts.validar import BARALHO, DIALOGO, Relatorio, validar_pasta


def validar_kit(dados: Path, dialogos: Path) -> Relatorio:
    """Baralhos (obrigatórios) e diálogos (opcionais), com ids únicos entre os dois."""
    ids: dict[str, tuple[str, int]] = {}
    total = validar_pasta(dados, BARALHO, ids)
    if dialogos.is_file() or any(dialogos.glob("*.csv")):
        r = validar_pasta(dialogos, DIALOGO, ids)
        total.arquivos += r.arquivos
        total.linhas += r.linhas
        total.erros.extend(r.erros)
    return total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida os CSVs do kit.")
    parser.add_argument("--dados", type=Path, default=RAIZ / "kit" / "dados",
                        help="pasta (ou arquivo) com os CSVs dos baralhos (padrão: kit/dados)")
    parser.add_argument("--dialogos", type=Path, default=RAIZ / "kit" / "dialogos",
                        help="pasta com os CSVs dos diálogos (padrão: kit/dialogos)")
    parser.add_argument("--planos", type=Path, default=RAIZ / "kit" / "planos",
                        help="pasta com os planos das trilhas (padrão: kit/planos)")
    parser.add_argument("--conteudo", type=Path, default=RAIZ / "conteudo",
                        help="pasta do site, onde os links são conferidos e os dados gravados")
    parser.add_argument("--audio", action="store_true",
                        help="gera os áudios com a voz Kokoro (baixa o modelo na primeira vez)")
    parser.add_argument("--baralhos", action="store_true",
                        help="gera os baralhos do Anki em dist/baralhos (exige --audio)")
    args = parser.parse_args(argv)
    if args.baralhos and not args.audio:
        parser.error("--baralhos precisa de --audio junto, porque cada carta leva o áudio da frase")

    relatorio = validar_kit(args.dados, args.dialogos)
    planos = {t: args.planos / f"{t}.csv" for t in TRILHAS if (args.planos / f"{t}.csv").exists()}
    for trilha, csv_plano in planos.items():
        relatorio.erros.extend(validar_plano(csv_plano, trilha, args.conteudo))
    relatorio.erros.extend(conferir_guia(args.conteudo / "guia",
                                         args.conteudo.parent / "docs" / "pesquisa" / "referencias.md"))
    if relatorio.erros:
        for erro in relatorio.erros:
            print(f"{os.path.relpath(erro.arquivo)}:{erro.linha}: {erro.mensagem}", file=sys.stderr)
        print(f"{len(relatorio.erros)} problema(s) encontrado(s).", file=sys.stderr)
        return 1
    for trilha, csv_plano in planos.items():
        gravar_dados(csv_plano, trilha, args.conteudo / "dados" / f"{trilha}.json")
    gerar_tudo(args.conteudo.parent)
    from scripts.creditos import gerar_creditos

    (args.conteudo.parent / "CREDITOS.md").write_text(gerar_creditos(args.conteudo.parent), encoding="utf-8")
    if args.audio:
        from scripts.audio import baixar_modelos, gerar_audios, itens_de_audio, pasta_modelos, sintetizador_kokoro

        modelo, vozes = baixar_modelos(pasta_modelos())
        manifesto = gerar_audios(itens_de_audio(args.conteudo.parent), args.conteudo / "audio",
                                 sintetizador_kokoro(modelo, vozes))
        print(f"Áudio: {len(manifesto)} arquivo(s) em {os.path.relpath(args.conteudo / 'audio')}.")
    if args.baralhos:
        from scripts.baralhos import gerar_baralho
        from scripts.paginas import _ler_csvs

        linhas = [l for l in _ler_csvs(args.dados if args.dados.is_dir() else args.dados.parent) if l.get("situacao")]
        for situacao in sorted({int(l["situacao"]) for l in linhas}):
            caminho = gerar_baralho(situacao, [l for l in linhas if int(l["situacao"]) == situacao],
                                    args.conteudo / "audio", RAIZ / "dist" / "baralhos")
            print(f"Baralho: {os.path.relpath(caminho)}")
    print(f"Tudo certo: {relatorio.arquivos} arquivo(s), {relatorio.linhas} linha(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
