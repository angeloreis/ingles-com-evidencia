# Fase 0 (esqueleto): plano de implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: use superpowers:subagent-driven-development (recomendada) ou superpowers:executing-plans para executar este plano tarefa por tarefa. Os passos usam caixas (`- [ ]`) para acompanhamento.

**Objetivo:** pôr no ar o esqueleto do Inglês com Evidência: repositório com licenças, validador dos CSVs, site Zensical com o design system Passaporte e fontes próprias, publicado no GitHub Pages por uma Action.

**Arquitetura:** os dados ficam em CSV (`kit/dados/`) e são conferidos por `scripts/validar.py`, chamado por `scripts/construir.py`. O Passaporte entra como fonte (`design/passaporte/tokens.json`), e `scripts/estilos.py` gera dele o `conteudo/estilos/tokens.css`. Um `ponte.css` liga os tokens às variáveis do tema do Zensical, que publica só a pasta `conteudo/`.

**Tecnologias:** Python 3.12, Zensical 0.1.1, pytest 9.2.0, GitHub Actions (configure-pages@v6, checkout@v7, setup-python@v6, upload-pages-artifact@v5, deploy-pages@v5). Fontes Fontsource 5.3.0 (Archivo e Figtree variáveis, IBM Plex Mono 500 e 600).

**Desenho:** `docs/superpowers/specs/2026-11-12-ingles-com-evidencia-design.md` (leia junto com este plano).

## Restrições gerais

- Python 3.12; Zensical instalado via pip (`zensical==0.1.1`); **sem Node** no repositório.
- Conteúdo **CC BY-SA 4.0**; scripts **MIT**; nada com licença "não comercial" (NC).
- Licenças aceitas nos dados: `CC BY-SA 4.0`, `CC BY 2.0 FR`, `CC0`. Fontes aceitas: `ngsl`, `tatoeba:<id da frase>`, `projeto`.
- Celular primeiro: texto com 17 px ou mais, áreas de toque com 48 px ou mais, uma coluna até 768 px, tabelas que viram cartões, tema escuro automático, **nenhuma rolagem para os lados**.
- Tudo em português do Brasil; toda frase em inglês vem com tradução.
- O site não usa rastreadores e não carrega nada de servidores de terceiros (fontes incluídas).
- Contraste WCAG AA nos dois temas, foco visível, nenhuma informação só por cor.
- Nenhum texto promete prazo ou resultado.
- Nenhum dado pessoal dos mantenedores no repositório.
- **Git é do mantenedor:** ele faz commit, push e deploy. Cada tarefa termina sugerindo **um commit por bloco**, sem linha `Co-Authored-By`. Quem executa não roda git e não espera os commits: segue para a próxima tarefa e entrega a lista de commits no fim.
- **Downloads só com o OK do mantenedor**, pedido uma vez antes da Tarefa 4, com a lista da seção "Downloads da fase".

## Pontos de atenção na revisão

1. **Vírgula sem aspas numa frase em inglês** ("Hi, how are you?" num CSV editado à mão): o validador aponta a linha e diz para pôr a frase entre aspas, em vez de acusar campos trocados. *Teste na Tarefa 1.*
2. **CSV salvo por planilha** (BOM, fim de linha do Windows, separador `;`, codificação Latin-1): BOM e CRLF passam; `;` e Latin-1 geram um erro claro em português, sem rastro de exceção. *Testes na Tarefa 1.*
3. **Celular estreito (320 px) com palavra longa ou link**: nada faz a página rolar para o lado. *Regra `overflow-wrap` na Tarefa 5 e medição a 320 px na Tarefa 7.*
4. **Tema trocado à mão contra a preferência do sistema** (aparelho escuro, pessoa escolhe claro): as cores do Passaporte seguem o botão, não o sistema. *Teste na Tarefa 3 e conferência no navegador na Tarefa 7.*
5. **Site publicado em subpasta** (`angeloreis.github.io/ingles-com-evidencia/`): CSS, fontes e links continuam funcionando, porque nenhum caminho começa com `/`. *Testes nas Tarefas 4 e 5 e conferência no endereço publicado na Tarefa 7.*

## Downloads da fase

Pedir o OK do mantenedor uma vez, antes da Tarefa 4, para estes arquivos:

| Arquivo | Origem | Tamanho |
|---|---|---|
| `archivo-latin-wght-normal.woff2` e `LICENSE` | `https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo@5.3.0/` (`files/…` e `LICENSE`) | 35 KB |
| `figtree-latin-wght-normal.woff2` e `LICENSE` | `https://cdn.jsdelivr.net/npm/@fontsource-variable/figtree@5.3.0/` | 20 KB |
| `ibm-plex-mono-latin-500-normal.woff2`, `ibm-plex-mono-latin-600-normal.woff2` e `LICENSE` | `https://cdn.jsdelivr.net/npm/@fontsource/ibm-plex-mono@5.3.0/` | 31 KB |
| `legalcode.txt` (vira `LICENSE`) | `https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt` | cerca de 20 KB |

O subconjunto `latin` cobre todos os acentos do português, o `·` da sílaba forte e o travessão.

## Mapa dos arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `pyproject.toml` | Só a configuração do pytest | 1 |
| `requirements-site.txt` e `requirements-dev.txt` | Dependências fixas do site e dos testes | 1 |
| `.gitignore` | `site/`, `.cache/`, `.venv/`, `__pycache__/`, `.pytest_cache/`, `*.apkg`, `.claude/` | 1 |
| `scripts/__init__.py` | `RAIZ` (pasta do repositório) | 1 |
| `scripts/validar.py` | Regras dos CSVs de baralho | 1 |
| `scripts/construir.py` | Linha de comando que roda tudo (na Fase 0, só a validação) | 2 |
| `kit/dados/exemplo.csv` | CSV de exemplo (sai na Fase 1) | 2 |
| `design/passaporte/` | Fonte do design system: `tokens.json`, `README.md`, `components/<Comp>/README.md`, `fontes.md` | 3 e 4 |
| `scripts/estilos.py` | Gera o `tokens.css` e calcula contraste | 3 |
| `conteudo/estilos/tokens.css` | Gerado, versionado | 3 |
| `conteudo/estilos/bundle.css` | Cópia fiel do `components/bundle.css` do Passaporte | 3 |
| `conteudo/estilos/fontes.css` e `conteudo/estilos/fontes/` | `@font-face`, arquivos `.woff2` e licenças OFL | 4 |
| `conteudo/estilos/ponte.css` | Liga o Passaporte às variáveis do tema do Zensical | 5 |
| `zensical.toml`, `conteudo/index.md`, `conteudo/sobre.md` | Site | 5 |
| `.github/workflows/site.yml` | Testes e publicação no Pages | 6 |
| `LICENSE`, `LICENSE-codigo`, `README.md` | Licenças e apresentação | 6 |
| `tests/` | Um arquivo por tarefa | 1 a 6 |

Nenhum `.md` fica dentro de `conteudo/` além das páginas do site, porque o Zensical publica todo `.md` dessa pasta como página.

---

### Tarefa 1: ambiente Python e validador dos CSVs

**Arquivos:**
- Criar: `pyproject.toml`, `requirements-site.txt`, `requirements-dev.txt`, `.gitignore`, `scripts/__init__.py`, `scripts/validar.py`
- Teste: `tests/test_validar.py`

**Interfaces:**
- Produz, em `scripts/__init__.py`: `RAIZ: Path = Path(__file__).resolve().parent.parent`
- Produz, em `scripts/validar.py`:
  - `@dataclass(frozen=True) class Erro: arquivo: str; linha: int; mensagem: str`. `linha` 0 é o arquivo inteiro, 1 é o cabeçalho. `__str__` devolve `"arquivo:linha: mensagem"`.
  - `@dataclass class Relatorio: arquivos: int; linhas: int; erros: list[Erro]`. `linhas` conta as linhas de dados lidas.
  - `validar_arquivo(caminho: Path, ids_vistos: dict[str, tuple[str, int]]) -> Relatorio`: registra em `ids_vistos` cada `id` novo com `(str(caminho), linha)`.
  - `validar_pasta(pasta: Path) -> Relatorio`: valida os `*.csv` da pasta em ordem alfabética (sem subpastas), com um único `ids_vistos`.

**Regras** (as mensagens são em português e citam o nome da coluna):

- **Leitura:** decodificar com `utf-8-sig`. Se falhar, um erro na linha 0 com o texto "UTF-8". Arquivo sem cabeçalho dá erro na linha 0 com o texto "vazio". Linhas totalmente em branco são ignoradas. O número da linha é o `line_num` do leitor `csv`.
- **Cabeçalho:**
  - Se tiver uma coluna só e ela contiver `;`, um erro na linha 1 com o texto "vírgula".
  - Obrigatórias: `id`, `en`, `pt`, `fonte` e `licenca`, mais exatamente uma de `situacao` ou `faixa`. Opcionais: `silaba` e `autor`.
  - Coluna fora dessa lista dá um erro por coluna, e coluna obrigatória ausente também. Ambos ficam na linha 1. Ter as duas, ou nenhuma, de `situacao` e `faixa` gera um erro com o texto "situacao ou faixa".
  - Com erro no cabeçalho, as linhas não são conferidas.
- **Linha:**
  - Mais campos que o cabeçalho geram um erro com o texto "aspas" (frases com vírgula precisam ficar entre aspas). Menos campos geram um erro com o texto "menos colunas".
  - Campo obrigatório vazio ou só com espaços é erro.
  - `id`: segue `^[a-z0-9]+(?:-[a-z0-9]+)*$` e é único em todos os arquivos. Um `id` repetido gera erro na segunda ocorrência, citando `arquivo:linha` da primeira.
  - `situacao`: inteiro de 1 a 8. `faixa`: inteiro a partir de 1.
  - `fonte`: `ngsl`, `tatoeba:` seguido de dígitos, ou `projeto`.
  - `licenca`: fora das três aceitas, o erro diz "não permitida". Ela também precisa combinar com a fonte: `ngsl` e `projeto` só aceitam `CC BY-SA 4.0`; `tatoeba:` aceita `CC BY 2.0 FR` ou `CC0`. A mensagem cita a fonte.
  - `autor`: obrigatório quando a licença é `CC BY 2.0 FR`.
  - `silaba`, quando preenchida, precisa conter `·`. Sem os `·` e em minúsculas, ela precisa aparecer como palavra inteira em `en`, sem diferença de maiúsculas.
- Cada linha com problema gera **um** erro: o primeiro encontrado, na ordem das regras acima.

- [ ] **Passo 1: preparar o repositório (mantenedor)**

  Na pasta `~/www/ingles-com-evidencia`, rodar `git init -b main`. Depois, o commit dos documentos:
  ```bash
  git add docs && git commit -m "docs: desenho do projeto e plano da fase 0"
  ```

- [ ] **Passo 2: criar o ambiente**

  - Criar `requirements-site.txt` com a linha `zensical==0.1.1`.
  - Criar `requirements-dev.txt` com as linhas `-r requirements-site.txt` e `pytest==9.2.0`.
  - Criar `pyproject.toml` só com:
    ```toml
    [tool.pytest.ini_options]
    pythonpath = ["."]
    testpaths = ["tests"]
    ```
  - Criar o `.gitignore` do mapa e o `scripts/__init__.py` com `RAIZ`.

  Rodar: `python3.12 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt`
  Esperado: termina sem erro, e `.venv/bin/python -m zensical --version` mostra `0.1.1`.

- [ ] **Passo 3: escrever os testes que falham**

```python
import csv, io
import pytest
from scripts.validar import Erro, validar_arquivo, validar_pasta

CAB = ["id", "en", "pt", "silaba", "situacao", "fonte", "licenca", "autor"]
BASE = {"id": "reuniao-01", "en": "Can we schedule a call for Monday?",
        "pt": "Podemos marcar uma ligação para segunda?", "silaba": "SCHED·ule",
        "situacao": "6", "fonte": "projeto", "licenca": "CC BY-SA 4.0", "autor": ""}

def montar(*linhas, cab=CAB):
    s = io.StringIO()
    w = csv.writer(s, lineterminator="\n")
    w.writerow(cab)
    for l in linhas:
        w.writerow([l.get(c, "") for c in cab])
    return s.getvalue()

def gravar(tmp_path, texto, nome="teste.csv", codificacao="utf-8"):
    p = tmp_path / nome
    p.write_bytes(texto.encode(codificacao))
    return p

def erros(tmp_path, texto, **kw):
    return validar_arquivo(gravar(tmp_path, texto, **kw), {}).erros

def test_erro_formata_arquivo_linha_mensagem():
    assert str(Erro("kit/dados/a.csv", 3, "falta en")) == "kit/dados/a.csv:3: falta en"

def test_arquivo_valido(tmp_path):
    ids = {}
    r = validar_arquivo(gravar(tmp_path, montar(BASE)), ids)
    assert (r.arquivos, r.linhas, r.erros) == (1, 1, [])
    assert ids["reuniao-01"] == (str(tmp_path / "teste.csv"), 2)

@pytest.mark.parametrize("texto", [
    "﻿" + montar(BASE).replace("\n", "\r\n") + "\r\n\r\n",
    montar({**BASE, "fonte": "tatoeba:123", "licenca": "CC BY 2.0 FR", "autor": "CK"}),
    montar({**BASE, "fonte": "tatoeba:123", "licenca": "CC0"}),
    montar({"id": "ngsl-0001", "en": "time", "pt": "tempo", "faixa": "1",
            "fonte": "ngsl", "licenca": "CC BY-SA 4.0"},
           cab=["id", "en", "pt", "faixa", "fonte", "licenca"]),
])
def test_casos_validos(tmp_path, texto):
    assert erros(tmp_path, texto) == []

@pytest.mark.parametrize("texto, trecho", [
    (montar({**BASE, "en": "   "}), "en"),
    (montar({**BASE, "id": "Reuniao 01"}), "id"),
    (montar({**BASE, "situacao": "9"}), "situacao"),
    (montar({**BASE, "situacao": "seis"}), "situacao"),
    (montar({**BASE, "fonte": "tatoeba:"}), "fonte"),
    (montar({**BASE, "fonte": "wikipedia"}), "fonte"),
    (montar({**BASE, "licenca": "CC BY-NC 4.0"}), "não permitida"),
    (montar({**BASE, "fonte": "ngsl", "licenca": "CC0"}), "ngsl"),
    (montar({**BASE, "fonte": "tatoeba:123", "licenca": "CC BY 2.0 FR"}), "autor"),
    (montar({**BASE, "silaba": "va·CA·tion"}), "silaba"),
    (montar({**BASE, "silaba": "schedule"}), "·"),
    (",".join(CAB) + "\nreuniao-02,Hi, how are you?,Oi, tudo bem?,,6,projeto,CC BY-SA 4.0,\n", "aspas"),
    (",".join(CAB) + "\nreuniao-02,Hi\n", "menos colunas"),
])
def test_um_erro_na_linha_2(tmp_path, texto, trecho):
    e = erros(tmp_path, texto)
    assert len(e) == 1 and e[0].linha == 2 and trecho in e[0].mensagem

@pytest.mark.parametrize("texto, trecho", [
    ("id;en;pt;situacao;fonte;licenca\n", "vírgula"),
    (montar(BASE, cab=["id", "en", "pt", "situacao", "fonte"]), "licenca"),
    (montar(BASE, cab=[c.replace("licenca", "licença") for c in CAB]), "licença"),
    (montar(BASE, cab=CAB + ["faixa"]), "situacao ou faixa"),
    (montar(BASE, cab=[c for c in CAB if c != "situacao"]), "situacao ou faixa"),
])
def test_erro_no_cabecalho(tmp_path, texto, trecho):
    e = erros(tmp_path, texto)
    assert e and all(x.linha == 1 for x in e) and any(trecho in x.mensagem for x in e)

@pytest.mark.parametrize("texto, codificacao, trecho", [
    (montar(BASE), "latin-1", "UTF-8"),
    ("", "utf-8", "vazio"),
])
def test_erro_no_arquivo_inteiro(tmp_path, texto, codificacao, trecho):
    e = erros(tmp_path, texto, codificacao=codificacao)
    assert len(e) == 1 and e[0].linha == 0 and trecho in e[0].mensagem

def test_id_repetido_entre_arquivos(tmp_path):
    gravar(tmp_path, montar(BASE), "a.csv")
    gravar(tmp_path, montar(BASE), "b.csv")
    r = validar_pasta(tmp_path)
    assert r.arquivos == 2 and len(r.erros) == 1
    assert r.erros[0].arquivo.endswith("b.csv") and r.erros[0].linha == 2
    assert "a.csv:2" in r.erros[0].mensagem

def test_pasta_conta_linhas(tmp_path):
    gravar(tmp_path, montar(BASE, {**BASE, "id": "reuniao-02"}))
    r = validar_pasta(tmp_path)
    assert (r.arquivos, r.linhas, r.erros) == (1, 2, [])

def test_pasta_sem_csv(tmp_path):
    r = validar_pasta(tmp_path)
    assert len(r.erros) == 1 and r.erros[0].linha == 0 and "nenhum CSV" in r.erros[0].mensagem
```

- [ ] **Passo 4: conferir que falham**

  Rodar: `.venv/bin/python -m pytest tests/test_validar.py -q`
  Esperado: FALHA com `ModuleNotFoundError: No module named 'scripts.validar'`.

- [ ] **Passo 5: implementar `scripts/validar.py`** com as interfaces e regras acima, usando `csv.DictReader` (os campos a mais caem na chave `None`; os que faltam ficam `None`).

- [ ] **Passo 6: conferir que passam**

  Rodar: `.venv/bin/python -m pytest tests/test_validar.py -q`
  Esperado: todos passam.

- [ ] **Passo 7: commit (mantenedor)**
  ```bash
  git add pyproject.toml requirements-site.txt requirements-dev.txt .gitignore scripts tests/test_validar.py
  git commit -m "feat: validador dos CSVs de baralho"
  ```

### Tarefa 2: `construir.py` e CSV de exemplo

**Arquivos:**
- Criar: `scripts/construir.py`, `kit/dados/exemplo.csv`
- Teste: `tests/test_construir.py`

**Interfaces:**
- Consome: `validar_pasta`, `Erro` e `RAIZ`, da Tarefa 1.
- Produz: `main(argv: list[str] | None = None) -> int`, com a opção `--dados CAMINHO` (padrão `RAIZ / "kit" / "dados"`). Roda com `python -m scripts.construir`.
  - Com erros: imprime cada erro no stderr com o caminho relativo à pasta atual (`os.path.relpath`), depois `N problema(s) encontrado(s).`, e devolve 1.
  - Sem erros: imprime no stdout `Tudo certo: A arquivo(s), L linha(s).` e devolve 0.

O `exemplo.csv` tem exatamente estas três linhas da situação 6, com cabeçalho `id,en,pt,silaba,situacao,fonte,licenca,autor`. Os ids `exemplo-*` não são reaproveitados depois que o arquivo sair, na Fase 1.

```csv
id,en,pt,silaba,situacao,fonte,licenca,autor
exemplo-01,Can we schedule a quick call for Monday?,Podemos marcar uma ligação rápida para segunda?,SCHED·ule,6,projeto,CC BY-SA 4.0,
exemplo-02,Does 10 a.m. work for you?,Dez da manhã funciona para você?,,6,projeto,CC BY-SA 4.0,
exemplo-03,"Sorry, could you repeat that?","Desculpe, pode repetir?",re·PEAT,6,projeto,CC BY-SA 4.0,
```

- [ ] **Passo 1: escrever os testes que falham**

```python
from scripts.construir import main

def test_dados_do_repositorio_passam(capsys):
    assert main([]) == 0
    assert "Tudo certo: 1 arquivo(s), 3 linha(s)." in capsys.readouterr().out

def test_pasta_com_erro_devolve_1(tmp_path, capsys):
    (tmp_path / "ruim.csv").write_text("id,en,pt,situacao,fonte,licenca\nx-1,Hi,Oi,6,projeto,CC BY-NC 4.0\n", encoding="utf-8")
    assert main(["--dados", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert "ruim.csv:2:" in err and "1 problema(s) encontrado(s)." in err
```

- [ ] **Passo 2: conferir que falham**

  Rodar: `.venv/bin/python -m pytest tests/test_construir.py -q`
  Esperado: FALHA com `No module named 'scripts.construir'`.

- [ ] **Passo 3: implementar `scripts/construir.py`** (com `argparse`) e criar o `kit/dados/exemplo.csv`.

- [ ] **Passo 4: conferir que passam**

  Rodar: `.venv/bin/python -m pytest -q && .venv/bin/python -m scripts.construir`
  Esperado: testes passam, e a saída é `Tudo certo: 1 arquivo(s), 3 linha(s).`

- [ ] **Passo 5: commit (mantenedor)**
  ```bash
  git add scripts/construir.py kit tests/test_construir.py
  git commit -m "feat: construir.py validando o CSV de exemplo"
  ```

### Tarefa 3: Passaporte no repositório e `tokens.css` gerado

**Arquivos:**
- Copiar do design system Passaporte (a cópia local dos arquivos ou o artifact citado na seção 5.3 do desenho):
  - `tokens.json`, `README.md` e `components/<Comp>/README.md` dos 8 componentes, para `design/passaporte/` (mesmos caminhos);
  - `components/bundle.css`, para `conteudo/estilos/bundle.css`, sem alterar nada.
- Criar: `scripts/estilos.py`, `conteudo/estilos/tokens.css` (gerado)
- Teste: `tests/test_estilos.py`

**Interfaces:**
- Produz, em `scripts/estilos.py`:
  - `TOKENS_JSON = RAIZ / "design/passaporte/tokens.json"` e `TOKENS_CSS = RAIZ / "conteudo/estilos/tokens.css"`
  - `carregar_tokens(caminho: Path = TOKENS_JSON) -> dict`
  - `resolver_cores(tokens: dict) -> dict[str, dict[str, str]]`: `{"light": {nome: "#hex"}, "dark": {...}}`, com os apelidos `"{outro}"` resolvidos.
  - `gerar_tokens_css(tokens: dict) -> str`
  - `contraste(cor_a: str, cor_b: str) -> float`: razão de contraste WCAG 2.x, sem importar a ordem.
  - `main() -> int`: grava o `TOKENS_CSS`. Roda com `python -m scripts.estilos`.
- **Formato do `tokens.css`** (cada linha `  --nome: valor;`, blocos separados por uma linha em branco, arquivo terminando em `\n`):
  1. Comentário: `/* Gerado por scripts/estilos.py a partir de design/passaporte/tokens.json. Não edite à mão. */`
  2. `:root, [data-md-color-scheme="default"] {`: cores claras. Um apelido vira `var(--outro)`.
  3. `[data-md-color-scheme="slate"] {`: cores escuras, da mesma forma.
  4. `:root {`, nesta ordem:
     - `--font-<família>` com o valor de `type.families`;
     - para cada estilo de `type.groups[].styles`: `--<estilo>-tamanho`, `--<estilo>-altura`, `--<estilo>-peso`, e `--<estilo>-espacamento` só quando houver `letterSpacing`;
     - os tokens de `spacing`, `radius` e `medida` como `--<nome>`.

  Os temas seguem o atributo que o Zensical põe no `<body>`, para o botão de tema funcionar. O `tokens.css` não usa `prefers-color-scheme`: quem segue o sistema é o próprio Zensical.

- [ ] **Passo 1: escrever os testes que falham**

```python
import re
import pytest
from scripts import RAIZ
from scripts.estilos import carregar_tokens, contraste, gerar_tokens_css, resolver_cores

TOKENS = carregar_tokens()
CORES = resolver_cores(TOKENS)
CSS = gerar_tokens_css(TOKENS)

def bloco(seletor):
    return CSS.split(seletor + " {", 1)[1].split("}", 1)[0]

def test_apelidos_resolvidos():
    assert CORES["light"]["foco"] == "#0e5a49"
    assert CORES["dark"]["evidencia-nenhuma"] == "#93a89f"

def test_temas_seguem_o_atributo_do_zensical():
    claro = bloco(':root, [data-md-color-scheme="default"]')
    escuro = bloco('[data-md-color-scheme="slate"]')
    assert "--fundo: #f1f5f3;" in claro and "--fundo: #0c1613;" in escuro
    assert "--foco: var(--passaporte);" in escuro
    assert "prefers-color-scheme" not in CSS

def test_familias_tipos_e_medidas():
    for trecho in ['--font-texto: "Figtree", system-ui', "--corpo-tamanho: 17px;",
                   "--titulo-1-peso: 800;", "--etiqueta-espacamento: 0.08em;",
                   "--espaco-4: 16px;", "--raio-painel: 12px;", "--alvo-toque: 48px;",
                   "--largura-texto: 68ch;"]:
        assert trecho in CSS

def test_tokens_css_do_repositorio_em_dia():
    assert (RAIZ / "conteudo/estilos/tokens.css").read_text(encoding="utf-8") == CSS

def test_bundle_so_usa_variaveis_definidas():
    bundle = (RAIZ / "conteudo/estilos/bundle.css").read_text(encoding="utf-8")
    assert set(re.findall(r"var\(--([a-z0-9-]+)", bundle)) <= set(re.findall(r"--([a-z0-9-]+):", CSS))

def test_contraste_valores_conhecidos():
    assert contraste("#000000", "#ffffff") == pytest.approx(21.0)
    assert contraste("#ffffff", "#777777") == pytest.approx(4.48, abs=0.01)

PARES = [("tinta", "fundo"), ("tinta", "superficie"), ("tinta-suave", "fundo"),
         ("tinta-suave", "superficie"), ("passaporte", "fundo"), ("passaporte", "superficie"),
         ("sobre-passaporte", "passaporte"), ("evidencia-forte", "fundo"),
         ("evidencia-forte", "superficie"), ("evidencia-moderada", "fundo"),
         ("evidencia-moderada", "superficie"), ("evidencia-fraca", "fundo"),
         ("evidencia-fraca", "superficie"), ("evidencia-nenhuma", "superficie")]

@pytest.mark.parametrize("tema", ["light", "dark"])
@pytest.mark.parametrize("texto, fundo", PARES)
def test_contraste_aa(tema, texto, fundo):
    assert contraste(CORES[tema][texto], CORES[tema][fundo]) >= 4.5
```

  Os valores saem do `tokens.json` como estão escritos nele (`letterSpacing` da etiqueta é `"0.08em"`; `lineHeight` 1.1 vira `1.1`).

- [ ] **Passo 2: conferir que falham**

  Rodar: `.venv/bin/python -m pytest tests/test_estilos.py -q`
  Esperado: FALHA com `No module named 'scripts.estilos'`.

- [ ] **Passo 3: implementar `scripts/estilos.py`** e gerar o arquivo com `.venv/bin/python -m scripts.estilos`.

- [ ] **Passo 4: conferir que passam**

  Rodar: `.venv/bin/python -m pytest -q`
  Esperado: todos passam. Hoje o par mais justo é `evidencia-moderada` sobre `fundo` no tema claro (4,55).

- [ ] **Passo 5: commit (mantenedor)**
  ```bash
  git add design scripts/estilos.py conteudo/estilos/tokens.css conteudo/estilos/bundle.css tests/test_estilos.py
  git commit -m "feat: design system Passaporte e tokens.css gerado"
  ```

### Tarefa 4: fontes servidas pelo próprio site

**Antes de começar:** pedir o OK do mantenedor para a lista de "Downloads da fase". Sem OK, a tarefa para aqui.

**Arquivos:**
- Baixar, para `conteudo/estilos/fontes/`, os quatro `.woff2` da lista, com o mesmo nome.
- Baixar, para `conteudo/estilos/fontes/LICENCAS/`, os `LICENSE` dos pacotes, com os nomes `archivo-OFL.txt`, `figtree-OFL.txt` e `ibm-plex-mono-OFL.txt`.
- Criar: `conteudo/estilos/fontes.css` e `design/passaporte/fontes.md` (de onde veio cada arquivo: pacote, versão, URL e `sha256sum`).
- Teste: `tests/test_fontes.py`

**Interfaces:**
- Consome: `carregar_tokens` (Tarefa 3).
- Produz: as famílias `"Archivo"` (pesos 100 a 900), `"Figtree"` (300 a 900) e `"IBM Plex Mono"` (500 e 600), cada `@font-face` com `font-display: swap;` e `src: url("fontes/<arquivo>.woff2") format("woff2");`. O caminho é relativo ao `fontes.css`.

- [ ] **Passo 1: escrever os testes que falham**

```python
import re
from scripts import RAIZ
from scripts.estilos import carregar_tokens

ESTILOS = RAIZ / "conteudo/estilos"

def css():
    return (ESTILOS / "fontes.css").read_text(encoding="utf-8")

def test_urls_relativas_e_existentes():
    urls = re.findall(r'url\("([^"]+)"\)', css())
    assert len(urls) == 4
    for u in urls:
        assert not u.startswith(("/", "http:", "https:"))
        assert (ESTILOS / u).is_file()

def test_arquivos_sao_woff2():
    arquivos = list((ESTILOS / "fontes").glob("*.woff2"))
    assert len(arquivos) == 4
    assert all(a.read_bytes()[:4] == b"wOF2" for a in arquivos)

def test_cada_familia_do_passaporte_tem_font_face():
    familias = {v.split(",")[0].strip().strip('"') for v in carregar_tokens()["type"]["families"].values()}
    assert familias == set(re.findall(r'font-family:\s*"([^"]+)"', css())) == {"Archivo", "Figtree", "IBM Plex Mono"}
    assert css().count("font-display: swap;") == 4

def test_cada_fonte_tem_licenca_ofl():
    for nome in ["archivo", "figtree", "ibm-plex-mono"]:
        texto = (ESTILOS / f"fontes/LICENCAS/{nome}-OFL.txt").read_text(encoding="utf-8")
        assert "SIL OPEN FONT LICENSE" in texto.upper()
```

- [ ] **Passo 2: conferir que falham**

  Rodar: `.venv/bin/python -m pytest tests/test_fontes.py -q`
  Esperado: FALHA com `FileNotFoundError` do `fontes.css`.

- [ ] **Passo 3: baixar os arquivos** com `curl -fsSL <URL> -o <destino>` (um por arquivo), depois `sha256sum conteudo/estilos/fontes/*.woff2 conteudo/estilos/fontes/LICENCAS/*`. Registrar o resultado em `design/passaporte/fontes.md`.

- [ ] **Passo 4: escrever o `fontes.css`** conforme a interface.

- [ ] **Passo 5: conferir que passam**

  Rodar: `.venv/bin/python -m pytest -q`
  Esperado: todos passam.

- [ ] **Passo 6: commit (mantenedor)**
  ```bash
  git add conteudo/estilos/fontes conteudo/estilos/fontes.css design/passaporte/fontes.md tests/test_fontes.py
  git commit -m "feat: fontes Archivo, Figtree e IBM Plex Mono servidas pelo site"
  ```

### Tarefa 5: site Zensical com o Passaporte

**Arquivos:**
- Criar: `zensical.toml`, `conteudo/index.md`, `conteudo/sobre.md`, `conteudo/estilos/ponte.css`
- Teste: `tests/test_site.py`

**Interfaces:**
- Consome: `tokens.css` e `bundle.css` (Tarefa 3) e `fontes.css` (Tarefa 4).
- Produz: o site em `site/` com `python -m zensical build --clean --strict`.

**`zensical.toml`** (valores decididos):
- `[project]`:
  - `site_name = "Inglês com Evidência"`
  - `site_description = "Guia aberto e gratuito que confere com a pesquisa as técnicas vendidas pelos cursos de inglês, com um kit para praticar."`
  - `site_url = "https://angeloreis.github.io/ingles-com-evidencia/"`
  - `copyright = "Conteúdo sob CC BY-SA 4.0 · código sob MIT"`
  - `docs_dir = "conteudo"`
  - `extra_css = ["estilos/fontes.css", "estilos/tokens.css", "estilos/bundle.css", "estilos/ponte.css"]`, nesta ordem
  - `nav = [{ "Início" = "index.md" }, { "Sobre e créditos" = "sobre.md" }]`
  - **Sem `repo_url`:** o cabeçalho do tema buscaria dados na API do GitHub pelo navegador de quem visita. O link para o repositório fica na página Sobre.
- `[project.theme]`:
  - `language = "pt-BR"` (o HTML sai com `lang="pt"`)
  - `font = false`
  - `features = ["navigation.instant", "navigation.top", "navigation.footer", "search.highlight"]`
- Duas entradas `[[project.theme.palette]]`, ambas com `primary = "custom"` e `accent = "custom"`:
  - claro: `media = "(prefers-color-scheme: light)"`, `scheme = "default"`, `toggle.icon = "lucide/moon"`, `toggle.name = "Mudar para o tema escuro"`;
  - escuro: `media = "(prefers-color-scheme: dark)"`, `scheme = "slate"`, `toggle.icon = "lucide/sun"`, `toggle.name = "Mudar para o tema claro"`.
- `[project.markdown_extensions]`: `admonition = {}`, `attr_list = {}`, `md_in_html = {}`, `toc.permalink = true`.

**`ponte.css`** (só usa variáveis do `tokens.css` e do tema):
- **Cores do tema**, no seletor `[data-md-color-scheme]`. O seletor fica no `<body>`, onde os tokens de cada tema valem. Ligações:

  | Variável do tema | Token |
  |---|---|
  | `--md-default-bg-color` | `var(--fundo)` |
  | `--md-default-fg-color` e `--md-typeset-color` | `var(--tinta)` |
  | `--md-default-fg-color--light` | `var(--tinta-suave)` |
  | `--md-primary-fg-color`, `--md-accent-fg-color` e `--md-typeset-a-color` | `var(--passaporte)` |
  | `--md-primary-bg-color` e `--md-accent-bg-color` | `var(--sobre-passaporte)` |
  | `--md-code-bg-color` e `--md-footer-bg-color` | `var(--superficie)` |

- **Fontes**, em `:root`: `--md-text-font: "Figtree"` e `--md-code-font: "IBM Plex Mono"`.
- **Títulos:** `[data-md-color-scheme] .md-typeset h1, h2, h3` com `font-family: var(--font-titulo)` e `color: var(--tinta)`, e tamanho, altura e peso dos estilos `titulo-1`, `titulo-2` e `titulo-3`. A especificidade precisa vencer a regra do tema escuro que pinta títulos de branco.
- **Texto:** `.md-typeset` com `font-size: var(--corpo-tamanho)`, `line-height: var(--corpo-altura)` e `overflow-wrap: break-word`.
- **Foco:** `:focus-visible` com `outline: 3px solid var(--foco)` e `outline-offset: 2px`.
- **Toque:** na gaveta do menu (`@media screen and (max-width: 76.234375em)`), `.md-nav__link` com `min-height: var(--alvo-toque)` e `display: flex; align-items: center`.

**Página inicial (`conteudo/index.md`)**, nesta ordem, com os componentes do Passaporte em HTML e links sempre relativos:
1. Faixa `<div class="pp-faixa"><span>Início</span><span>Em construção</span></div>` e o título "Inglês com Evidência".
2. "O que é": um parágrafo sobre as duas partes (guia e kit), dizendo que tudo é aberto e gratuito.
3. "Para quem": as duas trilhas (Destravar a fala; Do zero ao A2), com uma frase cada e a indicação "em construção".
4. "O que significam os selos": os quatro **Carimbos** (`data-nivel` 3, 2, 1 e 0, com o texto "Evidência forte", "Evidência moderada", "Evidência fraca" e "Sem evidência"), cada um com o critério da tabela da seção 5.1 do desenho.
5. Aviso honesto de que ainda não há capítulos nem situações publicados, e um **Botao** primário "Conhecer o projeto" com `href="sobre/"`.

**`conteudo/sobre.md`**:
- Licenças: CC BY-SA 4.0 para o conteúdo, explicando que é a licença exigida pela NGSL; MIT para o código.
- Fontes: Archivo, Figtree e IBM Plex Mono sob SIL Open Font License 1.1, com link para cada arquivo em `estilos/fontes/LICENCAS/`.
- Privacidade: sem rastreadores, fontes servidas pelo próprio site, e o progresso, quando existir, fica só no aparelho.
- Links para o repositório e para abrir uma issue ao reportar um erro no inglês ou no texto.
- Nenhum nome ou dado pessoal.

- [ ] **Passo 1: escrever os testes que falham**

```python
import re, subprocess, sys
import pytest
from scripts import RAIZ

@pytest.fixture(scope="session")
def site():
    subprocess.run([sys.executable, "-m", "zensical", "build", "--clean", "--strict"], cwd=RAIZ, check=True)
    return RAIZ / "site"

def paginas(site):
    return {p: p.read_text(encoding="utf-8") for p in site.rglob("*.html")}

def test_pagina_inicial_em_portugues(site):
    html = (site / "index.html").read_text(encoding="utf-8")
    assert '<html lang="pt"' in html and "Pular para conteúdo" in html
    assert (site / "sobre/index.html").is_file() and "Sobre e créditos" in html

def test_docs_do_projeto_fora_do_site(site):
    assert not (site / "superpowers").exists()
    assert "desenho do projeto" not in (site / "search.json").read_text(encoding="utf-8")

def test_estilos_na_ordem_e_relativos(site):
    html = (site / "index.html").read_text(encoding="utf-8")
    posicoes = [html.index(f'href="./estilos/{n}.css"') for n in ["fontes", "tokens", "bundle", "ponte"]]
    assert posicoes == sorted(posicoes)

def test_nada_de_terceiros_nem_caminho_absoluto(site):
    for caminho, html in paginas(site).items():
        for proibido in ["fonts.googleapis.com", "fonts.gstatic.com", "api.github.com"]:
            assert proibido not in html, caminho
        assert not re.findall(r'<script[^>]+src="(?:https?:)?//', html), caminho
        assert not re.findall(r'<link rel="(?:stylesheet|preload|modulepreload|icon)"[^>]+href="(?:https?:)?//', html), caminho
        assert not re.findall(r'(?:href|src)="/(?!/|ingles-com-evidencia/)', html), caminho

def test_dois_temas_com_botao(site):
    html = (site / "index.html").read_text(encoding="utf-8")
    for trecho in ['data-md-color-scheme="slate"', 'data-md-color-media="(prefers-color-scheme: dark)"',
                   'aria-label="Mudar para o tema escuro"', 'aria-label="Mudar para o tema claro"']:
        assert trecho in html

def test_fontes_publicadas(site):
    assert (site / "estilos/fontes/figtree-latin-wght-normal.woff2").is_file()

def test_ponte_liga_o_passaporte():
    ponte = (RAIZ / "conteudo/estilos/ponte.css").read_text(encoding="utf-8")
    tokens = (RAIZ / "conteudo/estilos/tokens.css").read_text(encoding="utf-8")
    assert "--md-default-bg-color: var(--fundo);" in ponte and "--md-typeset-a-color: var(--passaporte);" in ponte
    usadas = {v for v in re.findall(r"var\(--([a-z0-9-]+)", ponte) if not v.startswith("md-")}
    assert usadas <= set(re.findall(r"--([a-z0-9-]+):", tokens))
```

  O teste de links externos olha só para scripts e para `<link>` que carregam algo. O `<link rel="canonical">` (endereço completo do site) e os links de texto para o GitHub e para as licenças são permitidos. A página 404 usa caminhos que começam com `/ingles-com-evidencia/`, e isso está certo para a subpasta. Qualquer outro caminho começando com `/` é erro.

- [ ] **Passo 2: conferir que falham**

  Rodar: `.venv/bin/python -m pytest tests/test_site.py -q`
  Esperado: FALHA (sem `zensical.toml`, o build sai com erro).

- [ ] **Passo 3: criar o `zensical.toml`, o `ponte.css` e as duas páginas** conforme acima.

- [ ] **Passo 4: conferir que passam**

  Rodar: `.venv/bin/python -m pytest -q`
  Esperado: todos passam, e o build mostra `No issues found`.

- [ ] **Passo 5: commit (mantenedor)**
  ```bash
  git add zensical.toml conteudo/index.md conteudo/sobre.md conteudo/estilos/ponte.css tests/test_site.py
  git commit -m "feat: site Zensical com o Passaporte e página inicial"
  ```

### Tarefa 6: licenças, README e Action do Pages

**Antes de começar:** o mantenedor confirma o nome do repositório (`ingles-com-evidencia`) e confere se está livre na conta dele. Se o nome mudar, trocar `site_url`, os links da página Sobre e o prefixo `/ingles-com-evidencia/` do teste da Tarefa 5. O desenho também pede conferir o nome como domínio, mas isso não impede publicar no `github.io`.

**Arquivos:**
- Criar:
  - `LICENSE`: o `legalcode.txt` da lista de downloads, sem alterações.
  - `LICENSE-codigo`: texto padrão da MIT, com `Copyright (c) 2026 Contribuidores do Inglês com Evidência`. Diz que vale para `scripts/` e `tests/`.
  - `README.md`, em português:
    - o que é e o link do site;
    - como rodar localmente (`python3.12 -m venv .venv`, `.venv/bin/pip install -r requirements-dev.txt`, `.venv/bin/python -m zensical serve`);
    - como validar os dados (`.venv/bin/python -m scripts.construir`) e regenerar o `tokens.css` (`.venv/bin/python -m scripts.estilos`);
    - licenças, e como reportar erro por issue.
  - `.github/workflows/site.yml`
- Teste: `tests/test_repositorio.py`

**Workflow `site.yml`:**
- Nome "Site". Roda em `push` na `main` e em `pull_request`. No topo, `permissions: contents: read`.
- `concurrency: { group: pages, cancel-in-progress: false }`.
- Job `verificar`, em `ubuntu-latest`: `actions/checkout@v7`, `actions/setup-python@v6` com `python-version: "3.12"` e `cache: pip`, `pip install -r requirements-dev.txt`, `python -m pytest -q` e `python -m scripts.construir`.
- Job `publicar`:
  - `needs: verificar` e `if: github.event_name == 'push'`;
  - `permissions` com `pages: write` e `id-token: write`;
  - `environment` com `name: github-pages` e `url: ${{ steps.deployment.outputs.page_url }}`;
  - passos: `actions/configure-pages@v6`, `actions/checkout@v7`, `actions/setup-python@v6` (3.12), `pip install -r requirements-site.txt`, `zensical build --clean --strict`, `actions/upload-pages-artifact@v5` com `path: site` e `actions/deploy-pages@v5` com `id: deployment`.

- [ ] **Passo 1: escrever os testes que falham**

```python
from scripts import RAIZ

def ler(nome):
    return (RAIZ / nome).read_text(encoding="utf-8")

def test_licencas():
    assert "Attribution-ShareAlike 4.0 International" in ler("LICENSE")
    assert ler("LICENSE-codigo").startswith("MIT License")

def test_readme_cita_licencas_e_comandos():
    readme = ler("README.md")
    for trecho in ["CC BY-SA 4.0", "MIT", "python -m scripts.construir", "python -m zensical serve"]:
        assert trecho in readme

def test_workflow_testa_antes_de_publicar():
    wf = ler(".github/workflows/site.yml")
    assert wf.index("python -m pytest") < wf.index("zensical build --clean --strict")
    assert "needs: verificar" in wf and "actions/deploy-pages@v5" in wf
```

- [ ] **Passo 2: conferir que falham**

  Rodar: `.venv/bin/python -m pytest tests/test_repositorio.py -q`
  Esperado: FALHA com `FileNotFoundError`.

- [ ] **Passo 3: baixar o `LICENSE`, escrever os demais arquivos** e conferir que passam (`.venv/bin/python -m pytest -q`: todos passam).

- [ ] **Passo 4: commit e publicação (mantenedor)**

  ```bash
  git add LICENSE LICENSE-codigo README.md .github tests/test_repositorio.py
  git commit -m "chore: licenças, README e Action do GitHub Pages"
  ```

  Depois:
  1. Criar o repositório público `ingles-com-evidencia` no GitHub, sem README nem licença.
  2. `git remote add origin` e `git push -u origin main`.
  3. Em **Settings → Pages**, escolher **Source: GitHub Actions**.
  4. Se a primeira execução falhou antes disso, rodar de novo pela aba Actions.

  Esperado: a Action "Site" fica verde nos dois jobs.

### Tarefa 7: conferência no navegador e registro no desenho

**Arquivos:**
- Modificar: `docs/superpowers/specs/2026-11-12-ingles-com-evidencia-design.md`
- Criar, fora do repositório: uma entrada `ingles-site` no `.claude/launch.json` da pasta de trabalho do agente. Mantenha as outras entradas, se já houver. A entrada roda o Python do `.venv` do repositório com `-m zensical serve -f <repositório>/zensical.toml -a localhost:<porta livre>`.

- [ ] **Passo 1: abrir o site local** com `preview_start` (nome `ingles-site`) e esperar a página inicial carregar.

- [ ] **Passo 2: medir em seis combinações**

  Larguras 320×640, 375×812 e 1280×800, cada uma com `colorScheme` claro e escuro (`resize_window`, depois recarregar). Em cada uma, rodar no `javascript_tool`:
  ```js
  ({ semRolagemLateral: document.documentElement.scrollWidth <= innerWidth,
     esquema: document.body.dataset.mdColorScheme,
     fundo: getComputedStyle(document.body).backgroundColor,
     titulo: getComputedStyle(document.querySelector(".md-typeset h1")).color,
     fontes: [...document.fonts].filter(f => f.status === "loaded").map(f => f.family),
     externos: performance.getEntriesByType("resource").map(r => new URL(r.name).host).filter(h => h !== location.host) })
  ```
  Esperado:
  - `semRolagemLateral: true`;
  - claro: `esquema "default"`, `fundo "rgb(241, 245, 243)"`, `titulo "rgb(15, 35, 30)"`;
  - escuro: `esquema "slate"`, `fundo "rgb(12, 22, 19)"`, `titulo "rgb(226, 236, 232)"`;
  - `fontes` com `Figtree` e `Archivo`, e `externos: []`.

- [ ] **Passo 3: botão de tema contra o sistema**

  Com `colorScheme` escuro, clicar no botão "Mudar para o tema claro" e repetir a medição. Esperado: `esquema "default"` e `fundo "rgb(241, 245, 243)"`.

- [ ] **Passo 4: busca em português**

  Buscar "evidência" e depois "evidencia" (sem acento). Anotar se as duas encontram a página inicial.

- [ ] **Passo 5: capturas para o mantenedor**

  Tirar capturas do celular a 375 px nos dois temas e do computador a 1280 px no tema claro. Mandar com `SendUserFile`.

- [ ] **Passo 6: repetir no endereço publicado**

  Depois do push e da Action verde, repetir os Passos 2 e 3 em `https://angeloreis.github.io/ingles-com-evidencia/` (celular a 375 px e computador). Esperado: os mesmos valores, o que confirma que a publicação em subpasta funciona.

- [ ] **Passo 7: registrar no desenho**

  - "Situação: aprovado em 12/11/2026".
  - Na seção 5.4, a árvore ganha `design/passaporte/`, `.github/workflows/site.yml`, `requirements-*.txt`, `pyproject.toml` e `tests/`.
  - Na seção 5.3, o resultado da busca do Passo 4. Se a busca sem acento falhar, registrar como pendência da Fase 1.
  - Também na seção 5.3, a decisão de não usar `repo_url`, por privacidade.

- [ ] **Passo 8: validação do mantenedor (fim da fase)**

  O mantenedor e pelo menos uma pessoa do público iniciante abrem o site no próprio celular, nos dois temas. Commit dele:
  ```bash
  git add docs && git commit -m "docs: registra decisões da fase 0"
  ```
  Esperado: o critério da Fase 0 ("o site está no ar com a página inicial, no celular e no computador, nos dois temas") está cumprido.
