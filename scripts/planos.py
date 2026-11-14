"""Planos das trilhas (kit/planos/<trilha>.csv): validação e dados para a página "Hoje"."""
from __future__ import annotations

import csv
import io
import json
import re
import unicodedata
from pathlib import Path

from scripts.validar import RE_NUMERO, Erro

TRILHAS = {
    "destravar": {"titulo": "Destravar a fala", "semanas": 12, "minutos": (20, 30)},
}
COLUNAS = ("semana", "dia", "ordem", "passo", "minutos", "link")
# Caminho do site, com ?consulta e #trecho opcionais, como treinar/?situacao=6. Sem espaço, aspas,
# parênteses ou <: o link vai para dentro do Markdown da página de semanas.
RE_LINK = re.compile(r"[a-z0-9/-]*(?:\?[A-Za-z0-9=&_-]*)?(?:#[A-Za-z0-9_-]*)?")


def _ler(caminho: Path) -> tuple[list[str], list[tuple[int, dict]]]:
    texto = Path(caminho).read_bytes().decode("utf-8-sig")
    leitor = csv.DictReader(io.StringIO(texto, newline=""))
    cabecalho = [c.strip() for c in (leitor.fieldnames or [])]
    leitor.fieldnames = cabecalho
    linhas = []
    for campos in leitor:
        if all(not (v or "").strip() for k, v in campos.items() if k is not None):
            continue
        linhas.append((leitor.line_num, {k: (v or "").strip() for k, v in campos.items() if k is not None}))
    return cabecalho, linhas


def _inteiro(texto: str, minimo: int, maximo: int) -> int | None:
    if RE_NUMERO.fullmatch(texto) and minimo <= int(texto) <= maximo:
        return int(texto)
    return None


def _pagina_do_link(link: str, raiz_conteudo: Path) -> Path | None:
    """A página .md que o link abre (<caminho>.md ou <caminho>/index.md), ou None."""
    caminho = link.split("#", 1)[0].split("?", 1)[0].strip("/")
    candidatas = [raiz_conteudo / "index.md"] if not caminho else [
        raiz_conteudo / f"{caminho}.md", raiz_conteudo / caminho / "index.md"]
    return next((c for c in candidatas if c.exists()), None)


def _slug(titulo: str) -> str:
    """O id que o Python-Markdown dá a um título (a extensão toc, com o slugify padrão)."""
    texto = re.sub(r"<[^>]+>", "", titulo).replace("*", "").replace("`", "")
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^\w\s-]", "", texto).strip().lower()
    return re.sub(r"[-\s]+", "-", texto)


def ancoras(pagina: Path) -> set[str]:
    """As âncoras dos títulos (# a ######) de uma página .md."""
    return {_slug(m.group(1)) for m in re.finditer(r"^#{1,6} +(.+?) *#*$",
                                                    Path(pagina).read_text(encoding="utf-8"), re.M)}


def validar_plano(caminho: Path, trilha: str, raiz_conteudo: Path,
                  situacoes: set[int] | None = None) -> list[Erro]:
    """situacoes: as situações com cartas; um link ?situacao=N fora delas é erro (None: não confere)."""
    nome = str(caminho)
    config = TRILHAS[trilha]
    try:
        cabecalho, linhas = _ler(caminho)
    except UnicodeDecodeError:
        return [Erro(nome, 0, "o arquivo não está em UTF-8")]
    faltando = [c for c in COLUNAS if c not in cabecalho]
    if faltando:
        return [Erro(nome, 1, f"falta a coluna obrigatória {c}") for c in faltando]

    erros: list[Erro] = []
    dias: dict[tuple[int, int], dict] = {}
    for numero, v in linhas:
        semana = _inteiro(v["semana"], 1, config["semanas"])
        dia = _inteiro(v["dia"], 1, 7)
        ordem = _inteiro(v["ordem"], 1, 99)
        minutos = _inteiro(v["minutos"], 1, 30)
        if semana is None:
            erros.append(Erro(nome, numero, f"semana precisa ser um número de 1 a {config['semanas']}, não {v['semana']}"))
            continue
        if dia is None:
            erros.append(Erro(nome, numero, f"dia precisa ser um número de 1 a 7, não {v['dia']}"))
            continue
        if ordem is None:
            erros.append(Erro(nome, numero, f"ordem precisa ser um número a partir de 1, não {v['ordem']}"))
            continue
        if not v["passo"]:
            erros.append(Erro(nome, numero, "o campo passo está vazio"))
            continue
        if minutos is None:
            erros.append(Erro(nome, numero, f"minutos precisa ser um número de 1 a 30, não {v['minutos']}"))
            continue
        link = v["link"]
        if link and (link.startswith("/") or "://" in link or link.startswith("http")):
            erros.append(Erro(nome, numero, f"link precisa ser um caminho do site sem / no início, "
                                             f"como situacoes/telefonar/ (veio {link})"))
            continue
        if link and not RE_LINK.fullmatch(link):
            erros.append(Erro(nome, numero, "o link só pode ter letras minúsculas sem acento, números e os sinais "
                                             f"/ - ? # = & _, como treinar/?situacao=6 (veio {link})"))
            continue
        pagina = _pagina_do_link(link, raiz_conteudo) if link else None
        if link and pagina is None:
            erros.append(Erro(nome, numero, f"o link {link} não existe em conteudo/"))
            continue
        # Os dois erros abaixo não tiram os minutos do passo da soma do dia, para não somar um erro falso.
        pedida = re.search(r"[?&]situacao=([0-9]+)", link)
        if pedida and situacoes is not None and int(pedida.group(1)) not in situacoes:
            erros.append(Erro(nome, numero, f"o link pede a situação {int(pedida.group(1))}, que não tem cartas"))
        trecho = link.split("#", 1)[1] if "#" in link else ""
        if trecho and trecho not in ancoras(pagina):
            destino = pagina.relative_to(raiz_conteudo).as_posix()
            erros.append(Erro(nome, numero, f"a página {destino} não tem o trecho #{trecho}"))
        registro = dias.setdefault((semana, dia), {"linha": numero, "minutos": 0, "ordens": set()})
        if ordem in registro["ordens"]:
            erros.append(Erro(nome, numero, f"ordem repetida: o passo {ordem} já existe no dia {dia} da semana {semana}"))
            continue
        registro["ordens"].add(ordem)
        registro["minutos"] += minutos

    minimo, maximo = config["minutos"]
    for (semana, dia), registro in sorted(dias.items()):
        if not minimo <= registro["minutos"] <= maximo:
            erros.append(Erro(nome, registro["linha"],
                              f"o dia {dia} da semana {semana} soma {registro['minutos']} minutos; "
                              f"a trilha pede de {minimo} a {maximo} minutos por dia"))
    return erros


def dados_do_plano(caminho: Path, trilha: str) -> dict:
    """Dados do plano para o site (supõe um plano já validado)."""
    config = TRILHAS[trilha]
    _, linhas = _ler(caminho)
    passos = [{"semana": int(v["semana"]), "dia": int(v["dia"]), "ordem": int(v["ordem"]),
               "passo": v["passo"], "minutos": int(v["minutos"]), "link": v["link"]} for _, v in linhas]
    passos.sort(key=lambda p: (p["semana"], p["dia"], p["ordem"]))
    return {"trilha": trilha, "titulo": config["titulo"], "semanas": config["semanas"], "passos": passos}


def gravar_dados(caminho_csv: Path, trilha: str, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(dados_do_plano(caminho_csv, trilha), ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
    return destino
