"""Validação dos CSVs do kit: baralhos (kit/dados) e diálogos (kit/dialogos)."""
from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Esquema:
    nome: str
    obrigatorias: tuple[str, ...]
    grupo: tuple[str, ...]  # exatamente uma destas colunas (vazio = sem grupo)
    opcionais: tuple[str, ...]

    @property
    def conhecidas(self) -> tuple[str, ...]:
        return self.obrigatorias + self.grupo + self.opcionais


BARALHO = Esquema("baralho", ("id", "en", "pt", "fonte", "licenca"), ("situacao", "faixa"), ("silaba", "autor"))
DIALOGO = Esquema("diálogo", ("id", "situacao", "ordem", "falante", "en", "pt", "fonte", "licenca"), (),
                  ("autor",))

# Mantidos para quem já importava os nomes da Fase 0.
OBRIGATORIAS = BARALHO.obrigatorias
GRUPO = BARALHO.grupo
OPCIONAIS = BARALHO.opcionais
CONHECIDAS = BARALHO.conhecidas

LICENCAS = ("CC BY-SA 4.0", "CC BY 2.0 FR", "CC0")
LICENCAS_POR_FONTE = {
    "ngsl": ("CC BY-SA 4.0",),
    "projeto": ("CC BY-SA 4.0",),
    "tatoeba": ("CC BY 2.0 FR", "CC0"),
}
LICENCAS_COM_AUTOR = ("CC BY 2.0 FR",)
FALANTES = ("A", "B")

RE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
RE_FONTE = re.compile(r"ngsl|projeto|tatoeba:[0-9]+")
RE_NUMERO = re.compile(r"[0-9]+")


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


def validar_pasta(pasta: Path, esquema: Esquema = BARALHO,
                  ids_vistos: dict[str, tuple[str, int]] | None = None) -> Relatorio:
    """Valida os *.csv da pasta (sem subpastas), ou o próprio arquivo se `pasta` for um CSV.

    Os ids são únicos entre todos os arquivos que compartilham o mesmo `ids_vistos`.
    """
    pasta = Path(pasta)
    if pasta.is_file():
        arquivos = [pasta]
    else:
        arquivos = sorted(p for p in pasta.glob("*.csv") if p.is_file())
    if not arquivos:
        return Relatorio(erros=[Erro(str(pasta), 0, "nenhum CSV encontrado na pasta")])
    ids = {} if ids_vistos is None else ids_vistos
    total = Relatorio()
    for caminho in arquivos:
        r = validar_arquivo(caminho, ids, esquema)
        total.arquivos += r.arquivos
        total.linhas += r.linhas
        total.erros.extend(r.erros)
    return total


def validar_arquivo(caminho: Path, ids_vistos: dict[str, tuple[str, int]],
                    esquema: Esquema = BARALHO) -> Relatorio:
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

    erros_cabecalho = _conferir_cabecalho(cabecalho, esquema)
    if erros_cabecalho:
        relatorio.erros.extend(Erro(nome, 1, m) for m in erros_cabecalho)
        return relatorio

    numericas = [c for c in ("situacao", "faixa") if c in cabecalho]
    ordens_vistas: set[tuple[str, str]] = set()
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
        problema = _conferir_linha(campos, esquema, numericas, ids_vistos, ordens_vistas, nome, leitor.line_num)
        if problema:
            relatorio.erros.append(Erro(nome, leitor.line_num, problema))
    return relatorio


MENSAGEM_ASPA = ('aspa sem fechar a partir desta linha: o campo engoliu as linhas seguintes. '
                 'Confira as aspas da frase, como em "Hi, how are you?"')


def _conferir_cabecalho(cabecalho: list[str], esquema: Esquema) -> list[str]:
    if len(cabecalho) == 1 and ";" in cabecalho[0]:
        return ['o separador deve ser vírgula, não ponto e vírgula. O Excel em português grava ";" '
                "mesmo no formato CSV: exporte pelo Google Planilhas (Arquivo → Fazer download → "
                "Valores separados por vírgula) ou pelo LibreOffice Calc (Salvar como → CSV, com a "
                "vírgula como delimitador de campo)"]
    problemas = []
    vistas: set[str] = set()
    for coluna in cabecalho:
        if not coluna:
            problemas.append("coluna sem nome (vírgula sobrando no cabeçalho?)")
        elif coluna in vistas:
            problemas.append(f"coluna repetida: {coluna}")
        elif coluna not in esquema.conhecidas:
            problemas.append(f"coluna desconhecida: {coluna} "
                             f"(as colunas aceitas são {', '.join(esquema.conhecidas)})")
        vistas.add(coluna)
    for coluna in esquema.obrigatorias:
        if coluna not in cabecalho:
            problemas.append(f"falta a coluna obrigatória {coluna}")
    if esquema.grupo and sum(c in cabecalho for c in esquema.grupo) != 1:
        problemas.append(f"o arquivo precisa de uma coluna {' ou '.join(esquema.grupo)}, e só de uma delas")
    return problemas


def _valores(campos: dict) -> list[str]:
    """Todos os valores da linha, inclusive os que passaram do cabeçalho."""
    return [v for k, v in campos.items() if k is not None and v is not None] + list(campos.get(None) or [])


def _em_branco(campos: dict) -> bool:
    return all(not v.strip() for v in _valores(campos))


def _conferir_linha(campos: dict, esquema: Esquema, numericas: list[str],
                    ids_vistos: dict[str, tuple[str, int]], ordens_vistas: set[tuple[str, str]],
                    nome: str, linha: int) -> str | None:
    """Devolve a mensagem do primeiro problema da linha, ou None."""
    if None in campos:
        if all(not x.strip() for x in campos[None]):
            return "vírgula sobrando no fim da linha: apague a última vírgula"
        return 'a linha tem mais colunas que o cabeçalho: frases com vírgula precisam ficar entre aspas, como "Hi, how are you?"'
    if any(v is None for v in campos.values()):
        return ("a linha tem menos colunas que o cabeçalho: lembre que campo vazio também leva vírgula "
                "(a linha termina em vírgula quando o autor fica vazio)")

    v = {c: (campos.get(c) or "").strip() for c in esquema.conhecidas}
    licenca_fora = [c for c in campos if c != "licenca" and (campos[c] or "").strip() in LICENCAS]
    if v["licenca"] not in LICENCAS and licenca_fora:
        return (f"as colunas parecem deslocadas: a licença caiu na coluna {licenca_fora[0]}. "
                "Confira se uma frase com vírgula ficou sem aspas ou se falta a vírgula de um campo vazio")
    for coluna in esquema.obrigatorias + tuple(c for c in esquema.grupo if c in numericas):
        if not v[coluna]:
            return f"o campo {coluna} está vazio"

    if not RE_ID.fullmatch(v["id"]):
        return f"id inválido: {v['id']} (use letras minúsculas sem acento, números e hífen, como reuniao-01)"
    if v["id"] in ids_vistos:
        arquivo, linha_anterior = ids_vistos[v["id"]]
        return f"id repetido: {v['id']} (já usado em {arquivo}:{linha_anterior})"
    ids_vistos[v["id"]] = (nome, linha)

    if "situacao" in numericas and not (RE_NUMERO.fullmatch(v["situacao"]) and 1 <= int(v["situacao"]) <= 8):
        return f"situacao precisa ser um número de 1 a 8, não {v['situacao']}"
    if "faixa" in numericas and not (RE_NUMERO.fullmatch(v["faixa"]) and int(v["faixa"]) >= 1):
        return f"faixa precisa ser um número a partir de 1, não {v['faixa']}"

    if "ordem" in esquema.obrigatorias:
        if not (RE_NUMERO.fullmatch(v["ordem"]) and int(v["ordem"]) >= 1):
            return f"ordem precisa ser um número a partir de 1, não {v['ordem']}"
        chave = (v["situacao"], str(int(v["ordem"])))
        if chave in ordens_vistas:
            return f"ordem repetida: a fala {v['ordem']} já existe na situação {v['situacao']}"
        ordens_vistas.add(chave)
    if "falante" in esquema.obrigatorias and v["falante"] not in FALANTES:
        return f"falante precisa ser A ou B, não {v['falante']}"

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

    silaba = v.get("silaba", "")
    if silaba:
        if "·" not in silaba:
            return f"silaba precisa separar as sílabas com ·, como va·CA·tion (veio {silaba})"
        palavra = re.escape(silaba.replace("·", "").lower())
        if not re.search(rf"(?<!\w){palavra}(?!\w)", v["en"].lower()):
            return f"silaba {silaba} não bate com nenhuma palavra da frase em inglês"
    return None
