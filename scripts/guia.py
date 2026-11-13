"""Conferência dos capítulos do guia (desenho 5.1) e do registro de leitura (docs/pesquisa/referencias.md).

Capítulo de técnica: Faixa, título e Carimbo; as seções "O que os cursos dizem", "O que a pesquisa
diz" e "Como praticar", nessa ordem; "## Armadilhas"; e "## Referências" por último.
Toda citação no texto tem referência, toda referência é citada, tem link https e tem uma entrada
no registro de leitura com o resumo escrito com palavras próprias.
"""
from __future__ import annotations

import re
from pathlib import Path

from scripts.validar import Erro

# Capítulos publicados: slug → número (desenho 5.1). Cada capítulo novo entra aqui.
CAPITULOS: dict[str, int] = {
    "como-usar": 1,
    "frases-chave": 6,
    "shadowing": 8,
    "fluencia": 9,
    "medo-de-falar": 10,
    "ia-modo-de-voz": 11,
}

# Capítulos sem técnica: dispensados de carimbo e das três seções.
SEM_CARIMBO = {"como-usar"}

SECOES = ("O que os cursos dizem", "O que a pesquisa diz", "Como praticar")
CAMPOS_DO_REGISTRO = ("Link", "Lido em", "O que o resumo diz", "Usado em")

# "Hamada (2016)", "Foote e McDonough (2017)", "Boers et al. (2006)", "De Jong e Perfetti (2011)".
_SOBRENOME = r"(?:(?:De|Van|Von|Da|Di|Du|Del|Der|Le|La) )?[A-ZÀ-Ý][A-Za-zÀ-ÿ'’-]+"
RE_CITACAO = re.compile(rf"(?<![\w-])({_SOBRENOME})(?: e {_SOBRENOME}| et al\.)? \(([0-9]{{4}})\)")
# Formas fora das três permitidas, que a conferência não ligaria a uma referência:
# "(Hamada, 2016)", "(Teimouri et al., 2019; Botes et al., 2020)" e o ano com letra, "Hamada (2016a)".
RE_FORMA_PROIBIDA = re.compile(
    r"\([^()]*[A-ZÀ-Ý][\w'’-]*(?: et al\.)?, ?[0-9]{4}[a-z]?[^()]*\)|[A-ZÀ-Ý][\w'’-]* \([0-9]{4}[a-z]\)")
RE_ROTULO = re.compile(r'pp-secao__rotulo">([^<]*)<')
RE_CARIMBO = re.compile(r'class="pp-carimbo[^"]*"[^>]*data-nivel="[0-3]"')
RE_TITULO = re.compile(r"^## +(.+?) *$", re.M)
RE_ENTRADA = re.compile(r"^- ([^:]+): *(.*)$")


def chave(texto: str) -> tuple[str, str] | None:
    """Chave de uma citação ("Boers et al. (2006)") ou de um título do registro: (sobrenome, ano)."""
    m = RE_CITACAO.fullmatch(texto.strip())
    return (m.group(1), m.group(2)) if m else None


def _rotulo(k: tuple[str, str]) -> str:
    return f"{k[0]} ({k[1]})"


def ler_registro(caminho: Path) -> dict[tuple[str, str], dict[str, str]]:
    """Entradas do registro de leitura, pela chave (primeiro sobrenome, ano). Arquivo ausente: vazio."""
    caminho = Path(caminho)
    if not caminho.exists():
        return {}
    registro: dict[tuple[str, str], dict[str, str]] = {}
    atual: dict[str, str] | None = None
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            k = chave(linha[3:])
            atual = registro.setdefault(k, {}) if k else None
        elif atual is not None:
            m = RE_ENTRADA.match(linha)
            if m:
                atual[m.group(1).strip()] = m.group(2).strip()
    return registro


def _referencias(texto: str) -> list[tuple[str, str | None]]:
    """Linhas da lista de "## Referências": (linha, ano) — a chave é o texto antes da 1ª vírgula + ano."""
    return [(l, (re.search(r"\(([0-9]{4})[a-z]?\)", l) or [None, None])[1])
            for l in texto.splitlines() if l.startswith("- ")]


def conferir_capitulo(caminho: Path, registro: dict) -> list[Erro]:
    caminho = Path(caminho)
    nome = str(caminho)
    texto = caminho.read_text(encoding="utf-8")
    erros: list[Erro] = []

    def erro(mensagem: str) -> None:
        erros.append(Erro(nome, 0, mensagem))

    titulos = [(m.group(1), m.start()) for m in RE_TITULO.finditer(texto)]
    nomes = [t for t, _ in titulos]
    pos_refs = next((p for t, p in titulos if t == "Referências"), None)
    corpo = texto if pos_refs is None else texto[:pos_refs]
    lista_refs = "" if pos_refs is None else texto[pos_refs:].split("\n", 1)[-1]

    if caminho.stem not in SEM_CARIMBO:
        rotulos = [m.group(1).strip() for m in RE_ROTULO.finditer(texto)]
        primeira_secao = texto.find('class="pp-secao"')
        antes = texto if primeira_secao < 0 else texto[:primeira_secao]
        if not RE_CARIMBO.search(antes):
            erro('falta o carimbo (pp-carimbo com data-nivel de 0 a 3) entre o título e a primeira seção')
        for s in SECOES:
            if s not in rotulos:
                erro(f'falta a seção "{s}"')
        presentes = [r for r in rotulos if r in SECOES]
        if presentes != [s for s in SECOES if s in presentes]:
            erro('as seções estão fora de ordem: "' + '", "'.join(SECOES) + '"')
        if "Armadilhas" not in nomes:
            erro('falta a seção "## Armadilhas"')
        if pos_refs is None:
            erro('falta a seção "## Referências"')
    if pos_refs is not None and nomes[-1] != "Referências":
        erro('"## Referências" tem de ser a última seção do capítulo')

    for m in RE_FORMA_PROIBIDA.finditer(corpo):
        erro(f'forma de citação não permitida: "{m.group(0)}"; use "Sobrenome (AAAA)", '
             '"Sobrenome e Sobrenome (AAAA)" ou "Sobrenome et al. (AAAA)"')
    citadas = {(m.group(1), m.group(2)) for m in RE_CITACAO.finditer(corpo)}
    referidas: set[tuple[str, str]] = set()
    for linha, ano in _referencias(lista_refs):
        sobrenome = linha[2:].split(",", 1)[0].strip()
        if not ano:
            erro(f"referência sem ano entre parênteses: {linha[2:60]}")
            continue
        k = (sobrenome, ano)
        referidas.add(k)
        if not re.search(r"<https://[^>\s]+>", linha):
            erro(f"a referência {_rotulo(k)} não tem link https entre < e >")
        entrada = registro.get(k)
        if entrada is None:
            erro(f"a referência {_rotulo(k)} não está no registro de leitura (docs/pesquisa/referencias.md)")
            continue
        for campo in CAMPOS_DO_REGISTRO:
            if not entrada.get(campo):
                erro(f'a entrada {_rotulo(k)} do registro de leitura não tem "{campo}"')
        if entrada.get("Link") and not entrada["Link"].startswith("https://"):
            erro(f"o link da entrada {_rotulo(k)} do registro de leitura não começa com https://")
    for k in sorted(citadas - referidas):
        erro(f"a citação {_rotulo(k)} não tem referência em \"## Referências\"")
    for k in sorted(referidas - citadas):
        erro(f"a referência {_rotulo(k)} não é citada no texto")
    return erros


def conferir_guia(pasta: Path, caminho_registro: Path) -> list[Erro]:
    """Confere todo capítulo de `pasta` (menos index.md). Pasta ausente: nada a conferir."""
    pasta = Path(pasta)
    if not pasta.is_dir():
        return []
    registro = ler_registro(caminho_registro)
    erros: list[Erro] = []
    arquivos = {p.stem: p for p in sorted(pasta.glob("*.md")) if p.name != "index.md"}
    for slug, caminho in arquivos.items():
        if slug not in CAPITULOS:
            erros.append(Erro(str(caminho), 0, "capítulo fora da lista CAPITULOS de scripts/guia.py"))
            continue
        erros.extend(conferir_capitulo(caminho, registro))
    for slug in CAPITULOS:
        if slug not in arquivos:
            erros.append(Erro(str(pasta / f"{slug}.md"), 0, "capítulo listado em CAPITULOS, mas sem arquivo"))
    return erros
