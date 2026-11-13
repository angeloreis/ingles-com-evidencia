"""Validação dos CSVs de baralho do kit (kit/dados/*.csv)."""
from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field
from pathlib import Path

OBRIGATORIAS = ("id", "en", "pt", "fonte", "licenca")
GRUPO = ("situacao", "faixa")
OPCIONAIS = ("silaba", "autor")
CONHECIDAS = OBRIGATORIAS + GRUPO + OPCIONAIS

LICENCAS = ("CC BY-SA 4.0", "CC BY 2.0 FR", "CC0")
LICENCAS_POR_FONTE = {
    "ngsl": ("CC BY-SA 4.0",),
    "projeto": ("CC BY-SA 4.0",),
    "tatoeba": ("CC BY 2.0 FR", "CC0"),
}
LICENCAS_COM_AUTOR = ("CC BY 2.0 FR",)

RE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
RE_FONTE = re.compile(r"ngsl|projeto|tatoeba:\d+")
RE_NUMERO = re.compile(r"\d+")


@dataclass(frozen=True)
class Erro:
    arquivo: str
    linha: int  # 0 = o arquivo inteiro, 1 = o cabeçalho
    mensagem: str

    def __str__(self) -> str:
        return f"{self.arquivo}:{self.linha}: {self.mensagem}"


@dataclass
class Relatorio:
    arquivos: int = 0
    linhas: int = 0
    erros: list[Erro] = field(default_factory=list)


def validar_pasta(pasta: Path) -> Relatorio:
    """Valida os *.csv da pasta (sem subpastas), com ids únicos entre todos."""
    arquivos = sorted(p for p in Path(pasta).glob("*.csv") if p.is_file())
    if not arquivos:
        return Relatorio(erros=[Erro(str(pasta), 0, "nenhum CSV encontrado na pasta")])
    total = Relatorio()
    ids_vistos: dict[str, tuple[str, int]] = {}
    for caminho in arquivos:
        r = validar_arquivo(caminho, ids_vistos)
        total.arquivos += r.arquivos
        total.linhas += r.linhas
        total.erros.extend(r.erros)
    return total


def validar_arquivo(caminho: Path, ids_vistos: dict[str, tuple[str, int]]) -> Relatorio:
    """Valida um CSV e registra em ids_vistos cada id novo com (arquivo, linha)."""
    nome = str(caminho)
    relatorio = Relatorio(arquivos=1)
    try:
        texto = Path(caminho).read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError:
        relatorio.erros.append(Erro(nome, 0, "o arquivo não está em UTF-8: exporte de novo pelo Google "
                                              "Planilhas ou pelo LibreOffice Calc, que já salvam em UTF-8"))
        return relatorio

    leitor = csv.DictReader(io.StringIO(texto, newline=""))
    if not leitor.fieldnames:
        relatorio.erros.append(Erro(nome, 0, "arquivo vazio: falta o cabeçalho com os nomes das colunas"))
        return relatorio
    cabecalho = [c.strip() for c in leitor.fieldnames]
    leitor.fieldnames = cabecalho

    erros_cabecalho = _conferir_cabecalho(cabecalho)
    if erros_cabecalho:
        relatorio.erros.extend(Erro(nome, 1, m) for m in erros_cabecalho)
        return relatorio

    grupo = "situacao" if "situacao" in cabecalho else "faixa"
    registros = iter(leitor)
    while True:
        inicio = leitor.line_num + 1  # linha em que o próximo registro começa
        try:
            campos = next(registros)
        except StopIteration:
            break
        except csv.Error:
            # aspa aberta num arquivo grande: o campo engole o resto e estoura o limite
            relatorio.erros.append(Erro(nome, inicio, MENSAGEM_ASPA))
            break
        if _em_branco(campos):
            continue
        relatorio.linhas += 1
        if any("\n" in v or "\r" in v for v in _valores(campos)):
            relatorio.erros.append(Erro(nome, inicio, MENSAGEM_ASPA))
            continue
        problema = _conferir_linha(campos, grupo, ids_vistos, nome, leitor.line_num)
        if problema:
            relatorio.erros.append(Erro(nome, leitor.line_num, problema))
    return relatorio


MENSAGEM_ASPA = ('aspa sem fechar a partir desta linha: o campo engoliu as linhas seguintes. '
                 'Confira as aspas da frase, como em "Hi, how are you?"')


def _conferir_cabecalho(cabecalho: list[str]) -> list[str]:
    if len(cabecalho) == 1 and ";" in cabecalho[0]:
        return ['o separador deve ser vírgula, não ponto e vírgula. O Excel em português grava ";" '
                "mesmo no formato CSV: exporte pelo Google Planilhas (Arquivo → Fazer download → "
                "Valores separados por vírgula) ou pelo LibreOffice Calc (Salvar como → CSV, com a "
                "vírgula como delimitador de campo)"]
    problemas = []
    for coluna in cabecalho:
        if coluna not in CONHECIDAS:
            problemas.append(f"coluna desconhecida: {coluna} (as colunas aceitas são {', '.join(CONHECIDAS)})")
    for coluna in OBRIGATORIAS:
        if coluna not in cabecalho:
            problemas.append(f"falta a coluna obrigatória {coluna}")
    if sum(c in cabecalho for c in GRUPO) != 1:
        problemas.append("o arquivo precisa de uma coluna situacao ou faixa, e só de uma das duas")
    return problemas


def _valores(campos: dict) -> list[str]:
    """Todos os valores da linha, inclusive os que passaram do cabeçalho."""
    return [v for k, v in campos.items() if k is not None and v is not None] + list(campos.get(None) or [])


def _em_branco(campos: dict) -> bool:
    return all(not v.strip() for v in _valores(campos))


def _conferir_linha(campos: dict, grupo: str, ids_vistos: dict[str, tuple[str, int]],
                    nome: str, linha: int) -> str | None:
    """Devolve a mensagem do primeiro problema da linha, ou None."""
    if None in campos:
        if all(not x.strip() for x in campos[None]):
            return "vírgula sobrando no fim da linha: apague a última vírgula"
        return 'a linha tem mais colunas que o cabeçalho: frases com vírgula precisam ficar entre aspas, como "Hi, how are you?"'
    if any(v is None for v in campos.values()):
        return ("a linha tem menos colunas que o cabeçalho: lembre que campo vazio também leva vírgula "
                "(a linha termina em vírgula quando o autor fica vazio)")

    v = {c: (campos.get(c) or "").strip() for c in CONHECIDAS}
    licenca_fora = [c for c in campos if c != "licenca" and (campos[c] or "").strip() in LICENCAS]
    if v["licenca"] not in LICENCAS and licenca_fora:
        return (f"as colunas parecem deslocadas: a licença caiu na coluna {licenca_fora[0]}. "
                "Confira se uma frase com vírgula ficou sem aspas ou se falta a vírgula de um campo vazio")
    for coluna in OBRIGATORIAS + (grupo,):
        if not v[coluna]:
            return f"o campo {coluna} está vazio"

    if not RE_ID.fullmatch(v["id"]):
        return f"id inválido: {v['id']} (use letras minúsculas sem acento, números e hífen, como reuniao-01)"
    if v["id"] in ids_vistos:
        arquivo, linha_anterior = ids_vistos[v["id"]]
        return f"id repetido: {v['id']} (já usado em {arquivo}:{linha_anterior})"
    ids_vistos[v["id"]] = (nome, linha)

    numero = v[grupo]
    if grupo == "situacao" and not (RE_NUMERO.fullmatch(numero) and 1 <= int(numero) <= 8):
        return f"situacao precisa ser um número de 1 a 8, não {numero}"
    if grupo == "faixa" and not (RE_NUMERO.fullmatch(numero) and int(numero) >= 1):
        return f"faixa precisa ser um número a partir de 1, não {numero}"

    if not RE_FONTE.fullmatch(v["fonte"]):
        return f"fonte inválida: {v['fonte']} (use ngsl, tatoeba:<número da frase> ou projeto)"
    if v["licenca"] not in LICENCAS:
        return f"licença não permitida: {v['licenca']} (use {', '.join(LICENCAS)})"
    tipo = v["fonte"].split(":")[0]
    if v["licenca"] not in LICENCAS_POR_FONTE[tipo]:
        aceitas = " ou ".join(LICENCAS_POR_FONTE[tipo])
        return f"a fonte {tipo} só aceita a licença {aceitas}, não {v['licenca']}"
    if v["licenca"] in LICENCAS_COM_AUTOR and not v["autor"]:
        return f"a licença {v['licenca']} exige o nome do autor na coluna autor"

    silaba = v["silaba"]
    if silaba:
        if "·" not in silaba:
            return f"silaba precisa separar as sílabas com ·, como va·CA·tion (veio {silaba})"
        palavra = re.escape(silaba.replace("·", "").lower())
        if not re.search(rf"(?<!\w){palavra}(?!\w)", v["en"].lower()):
            return f"silaba {silaba} não bate com nenhuma palavra da frase em inglês"
    return None
