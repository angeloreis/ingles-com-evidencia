"""Roda as etapas do kit: valida os CSVs, os planos e o guia; gera páginas, áudio e baralhos.

Uso: python -m scripts.construir [--dados PASTA] [--dialogos PASTA] [--planos PASTA] [--conteudo PASTA] [--audio] [--baralhos]
"""
from __future__ import annotations

import argparse
import csv
import io
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


def situacoes_com_cartas(dados: Path) -> set[int]:
    """Os números da coluna situacao dos CSVs de baralho (os que não são número ficam para a validação)."""
    arquivos = [dados] if dados.is_file() else sorted(dados.glob("*.csv"))
    situacoes: set[int] = set()
    for arquivo in arquivos:
        for campos in csv.DictReader(io.StringIO(arquivo.read_bytes().decode("utf-8-sig", "replace"), newline="")):
            valor = (campos.get("situacao") or "").strip()
            if valor.isdigit():
                situacoes.add(int(valor))
    return situacoes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida os CSVs do kit.")
    parser.add_argument("--dados", type=Path,
                        help="pasta (ou arquivo) com os CSVs dos baralhos (padrão: kit/dados); "
                             "de fora do projeto, só confere e não gera nada")
    parser.add_argument("--dialogos", type=Path,
                        help="pasta com os CSVs dos diálogos (padrão: kit/dialogos); de fora, só confere")
    parser.add_argument("--planos", type=Path,
                        help="pasta com os planos das trilhas (padrão: kit/planos); de fora, só confere")
    parser.add_argument("--conteudo", type=Path, default=RAIZ / "conteudo",
                        help="pasta do site, onde os links são conferidos e os dados gravados")
    parser.add_argument("--audio", action="store_true",
                        help="gera os áudios com a voz Kokoro (baixa o modelo na primeira vez)")
    parser.add_argument("--baralhos", action="store_true",
                        help="gera os baralhos do Anki em dist/baralhos (exige --audio)")
    args = parser.parse_args(argv)
    if args.baralhos and not args.audio:
        parser.error("--baralhos precisa de --audio junto, porque cada carta leva o áudio da frase")
    # A raiz do projeto é a pasta acima de conteudo/. Dados de fora de <raiz>/kit só são conferidos:
    # as páginas, os créditos e o áudio sempre leem <raiz>/kit (M2 da 1A).
    raiz = args.conteudo.parent
    proprias = {nome: raiz / "kit" / nome for nome in ("dados", "dialogos", "planos")}
    de_fora = False
    for nome, propria in proprias.items():
        dado = getattr(args, nome)
        if dado is None:
            setattr(args, nome, propria)
        elif dado.resolve() != propria.resolve():
            de_fora = True
    if de_fora and (args.audio or args.baralhos):
        parser.error("--audio e --baralhos geram arquivos e precisam dos dados do próprio projeto, "
                     "sem --dados, --dialogos ou --planos de fora")

    relatorio = validar_kit(args.dados, args.dialogos)
    # Só com as cartas do próprio projeto: dados de fora não dizem que situações o plano do projeto pode pedir.
    situacoes = situacoes_com_cartas(args.dados) if args.dados.resolve() == proprias["dados"].resolve() else None
    planos = {t: args.planos / f"{t}.csv" for t in TRILHAS if (args.planos / f"{t}.csv").exists()}
    for trilha, csv_plano in planos.items():
        relatorio.erros.extend(validar_plano(csv_plano, trilha, args.conteudo, situacoes))
    relatorio.erros.extend(conferir_guia(args.conteudo / "guia",
                                         args.conteudo.parent / "docs" / "pesquisa" / "referencias.md"))
    if relatorio.erros:
        for erro in relatorio.erros:
            print(f"{os.path.relpath(erro.arquivo)}:{erro.linha}: {erro.mensagem}", file=sys.stderr)
        print(f"{len(relatorio.erros)} problema(s) encontrado(s).", file=sys.stderr)
        return 1
    if de_fora:
        print(f"Só conferência: os dados vêm de fora de {os.path.relpath(raiz / 'kit')}, então nada foi gerado.")
        print(f"Tudo certo: {relatorio.arquivos} arquivo(s), {relatorio.linhas} linha(s).")
        return 0
    for trilha, csv_plano in planos.items():
        gravar_dados(csv_plano, trilha, args.conteudo / "dados" / f"{trilha}.json")
    gerar_tudo(raiz)
    from scripts.creditos import gerar_creditos

    (raiz / "CREDITOS.md").write_text(gerar_creditos(raiz), encoding="utf-8")
    if args.audio:
        from scripts.audio import baixar_modelos, gerar_audios, itens_de_audio, pasta_modelos, sintetizador_kokoro

        modelo, vozes = baixar_modelos(pasta_modelos())
        manifesto = gerar_audios(itens_de_audio(raiz), args.conteudo / "audio",
                                 sintetizador_kokoro(modelo, vozes))
        print(f"Áudio: {len(manifesto)} arquivo(s) em {os.path.relpath(args.conteudo / 'audio')}.")
    if args.baralhos:
        from scripts.baralhos import gerar_baralho
        from scripts.paginas import _ler_csvs

        linhas = [l for l in _ler_csvs(args.dados if args.dados.is_dir() else args.dados.parent) if l.get("situacao")]
        for situacao in sorted({int(l["situacao"]) for l in linhas}):
            caminho = gerar_baralho(situacao, [l for l in linhas if int(l["situacao"]) == situacao],
                                    args.conteudo / "audio", raiz / "dist" / "baralhos")
            print(f"Baralho: {os.path.relpath(caminho)}")
    print(f"Tudo certo: {relatorio.arquivos} arquivo(s), {relatorio.linhas} linha(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
