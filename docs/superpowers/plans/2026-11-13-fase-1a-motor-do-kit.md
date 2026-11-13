# Fase 1A (motor do kit): plano de implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: use superpowers:subagent-driven-development (recomendada) ou superpowers:executing-plans para executar este plano tarefa por tarefa. Os passos usam caixas (`- [ ]`) para acompanhamento.

**Objetivo:** construir o motor do kit de prática e pôr a situação 6 inteira no ar como piloto:
- frases e diálogo com áudio;
- treino de cartas no próprio site;
- página "Hoje" com o plano da trilha "Destravar a fala";
- ficha de progresso;
- baralho do Anki publicado nas Releases.

**Arquitetura:** os CSVs de `kit/` são a única fonte dos dados. `scripts/construir.py` valida esses arquivos e gera:
- trechos HTML em `kit/gerado/`, incluídos nas páginas escritas à mão pelo `pymdownx.snippets`;
- dados JSON em `conteudo/dados/`;
- o `CREDITOS.md`;
- com `--audio`, os áudios (Kokoro, via `kokoro-onnx`);
- com `--baralhos`, os baralhos (genanki).

No site, um JavaScript sem dependências faz a parte de cada aparelho (áudio, treino, "Hoje", ficha) e guarda o progresso só no `localStorage`. A lógica pura desse JavaScript é testada no pytest com o `mini-racer`.

**Tecnologias:**
- Python 3.12 e Zensical 0.1.1, como na Fase 0.
- `kokoro-onnx==0.6.1` (MIT), com o modelo Kokoro-82M v1.0 (Apache 2.0).
- `soundfile` (grava MP3 sem ffmpeg).
- `genanki==0.13.1` (MIT).
- `mini-racer==0.14.1` (ISC, só nos testes).
- GitHub Actions com `actions/cache@v5`.

**Desenho:** `docs/superpowers/specs/2026-11-12-ingles-com-evidencia-design.md`. Este plano cobre a primeira metade da Fase 1. O plano 1B cobre as situações 7 e 8, os capítulos 1, 6, 8, 9, 10 e 11 e as semanas 1 a 6.

**Decisão do mantenedor (13/11/2026):** o AnkiWeb não importa baralhos pelo navegador, então o site ganha o próprio **treino de cartas**, e o Anki vira opcional (AnkiDroid ou computador). O critério da Fase 1 passa a ser seguir a semana 1 **só pelo site**.

**Pronto quando:** no celular, só pelo site publicado, uma pessoa consegue seguir a semana 1 do piloto:
- abrir "Hoje" e marcar os passos;
- ouvir as frases e o diálogo da situação 6;
- treinar as cartas;
- registrar a ficha.

E a Release `v0.1.0` traz o baralho da situação 6 para quem usa o Anki.

## Restrições gerais

- Todas as da Fase 0 continuam valendo:
  - Python 3.12, sem Node;
  - conteúdo CC BY-SA 4.0 e código MIT, nada com licença NC;
  - pt-BR, e toda frase em inglês com tradução;
  - texto com 17 px ou mais, áreas de toque com 48 px ou mais, sem rolagem lateral;
  - contraste AA nos dois temas;
  - nada de servidores de terceiros nem rastreadores;
  - nenhum dado pessoal no repositório;
  - nenhum caminho começando com `/`.
- Progresso **só no aparelho** (`localStorage`), sem login. Toda leitura e gravação fica dentro de `try/catch`, e a página funciona mesmo sem armazenamento.
- Toda frase em inglês no HTML leva `lang="en"`.
- Áudio de frase e da pessoa A do diálogo: voz `af_heart`. Pessoa B: voz `am_michael`. Velocidade 0.9. Arquivos `ice-<id>.mp3`.
- A trilha "Destravar a fala" usa só cartas do tipo "produzir": português na frente, resposta falada.
- Limites da trilha `destravar`: 12 semanas e de 20 a 30 minutos por dia com passos. Dia sem passos é dia de descanso.
- **Git é do mantenedor:** cada tarefa sugere um commit, sem `Co-Authored-By`. Quem executa não roda git.
- **Downloads só com OK do mantenedor:** os arquivos do modelo Kokoro (Tarefa 7) pedem confirmação antes.

## Pontos de atenção na revisão

1. **Navegador sem armazenamento** (aba anônima, Safari que apaga dados de site não visitado em 7 dias): "Hoje", treino e ficha abrem, mostram um aviso e funcionam na sessão. *Testes de `ler` tolerante nas Tarefas 4 a 6, mais conferência no navegador na Tarefa 12.*
2. **Data local à noite:** depois das 21h no Brasil, `toISOString()` já é o dia seguinte. "Hoje" e o treino usam a data local. *Teste de `ICE.datas.iso` na Tarefa 4.*
3. **Plano fora do intervalo publicado:** depois da semana 12; semanas 7 a 12 ainda sem passos na Fase 1; relógio do aparelho voltando no tempo. "Hoje" mostra uma mensagem coerente, sem tela vazia. *Testes de `posicao` e `passosDoDia` na Tarefa 6.*
4. **Frase sem áudio** (frase nova antes de rodar `--audio`, ou falha na Action): o botão aparece desabilitado com "Sem áudio aqui", e o resto da página funciona. No baralho, a falta de áudio é erro. *Teste de `estadoDoBotao` na Tarefa 4 e de `baralhos` na Tarefa 8.*
5. **Troca de página sem recarregar** (`navigation.instant`): botões e componentes continuam funcionando depois de navegar pelo menu. *Conferência no navegador na Tarefa 12, porque o pytest não tem DOM.*

## Mapa dos arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `scripts/validar.py` | Esquemas `BARALHO` e `DIALOGO` | 1 |
| `scripts/situacoes.py` | Número, slug e título das 8 situações | 1 |
| `kit/dialogos/` | CSVs dos diálogos | 1 e 11 |
| `scripts/planos.py` | Validação dos planos e `conteudo/dados/<trilha>.json` | 2 |
| `scripts/paginas.py` | Trechos HTML de frases, diálogo e semanas; `conteudo/dados/cartas.json` | 3 |
| `conteudo/js/nucleo.js` | Endereço da raiz, armazenamento seguro, gancho de troca de página | 4 |
| `conteudo/js/logica/{datas,audio,treino,plano,ficha}.js` | Lógica pura, testada no `mini-racer` | 4 a 6 |
| `conteudo/js/paginas/{audio,roteiro,treino,hoje,ficha}.js` | Ligação com o DOM | 4 a 6 |
| `tests/js.py` | Ajudante que roda o JavaScript no pytest | 4 |
| `scripts/audio.py` | Áudio com Kokoro, manifesto e modelo em cache | 7 |
| `scripts/baralhos.py` | Baralhos `.apkg` | 8 |
| `scripts/creditos.py` e `CREDITOS.md` | Créditos gerados | 9 |
| `.github/workflows/site.yml` | Áudio no deploy, baralhos nas tags `v*` | 10 |
| `conteudo/situacoes/`, `conteudo/trilhas/destravar/`, `conteudo/treinar.md` | Páginas | 11 |
| `kit/dados/situacao-06.csv`, `kit/planos/destravar.csv` | Conteúdo do piloto | 11 |

São arquivos gerados e versionados: `kit/gerado/*.md`, `conteudo/dados/*.json` e `CREDITOS.md`. Cada um tem um teste "em dia", como o `tokens.css`. `conteudo/audio/` e `dist/` são gerados e ficam fora do git.

---

### Tarefa 1: esquemas de CSV, diálogos e ajustes do validador

**Arquivos:**
- Modificar: `scripts/validar.py`, `scripts/construir.py`, `tests/test_validar.py`, `tests/test_construir.py`.
- Criar: `scripts/situacoes.py`.

**Interfaces:**
- Produz, em `scripts/validar.py`:
  - `@dataclass(frozen=True) class Esquema: nome: str; obrigatorias: tuple[str, ...]; grupo: tuple[str, ...]; opcionais: tuple[str, ...]`.
  - `BARALHO`: as colunas atuais, com `grupo=("situacao", "faixa")`.
  - `DIALOGO`: obrigatórias `id, situacao, ordem, falante, en, pt, fonte, licenca`, sem grupo e com `autor` opcional.
  - `validar_arquivo(caminho, ids_vistos, esquema=BARALHO)` e `validar_pasta(pasta, esquema=BARALHO, ids_vistos=None)`.
  - Os ids são únicos entre baralhos e diálogos, porque viram nome de arquivo de áudio. `validar_pasta` recebe e devolve o mesmo dicionário.
- Regras do `DIALOGO`:
  - `falante` é `A` ou `B`;
  - `ordem` é um inteiro a partir de 1, único por situação no arquivo;
  - `situacao` vai de 1 a 8;
  - as demais regras são as do baralho.
- Ajustes adiados da Fase 0, todos aqui:
  - número só com `[0-9]` (`re.ASCII`);
  - nome de coluna vazio gera erro "coluna sem nome (vírgula sobrando no cabeçalho?)";
  - coluna repetida gera erro "coluna repetida: X";
  - `--dados` apontando para um arquivo valida só esse arquivo.
- Produz, em `scripts/situacoes.py`: `SITUACOES: dict[int, tuple[str, str]]`, com número → (slug, título). Os títulos são os da tabela 5.2 do desenho. Slugs: `imigracao`, `restaurante`, `taxi`, `policia`, `conversa`, `telefonar`, `tecnologia`, `entrevista`.
- `construir.main` valida `kit/dados` com `BARALHO` e `kit/dialogos` com `DIALOGO`. Pasta sem CSV não é erro para os diálogos, mas continua sendo erro para os baralhos.

- [ ] **Passo 1: testes que falham.** Em `tests/test_validar.py`:
  - `test_dialogo_valido(tmp_path)`: cabeçalho do `DIALOGO`, duas linhas (A ordem 1, B ordem 2) → `erros == []`.
  - `test_dialogo_erros`, parametrizado:
    - `falante` = `C` → mensagem com "falante";
    - `ordem` repetida → "ordem";
    - `ordem` = `0` → "ordem".
  - `test_id_repetido_entre_baralho_e_dialogo(tmp_path)`: o mesmo id numa pasta de baralho e numa de diálogo, com o mesmo `ids_vistos` → um erro com "id repetido".
  - `test_cabecalho_coluna_sem_nome_e_repetida`, parametrizado:
    - `CAB + [""]` → "sem nome";
    - `CAB + ["en"]` → "repetida".
  - `test_digito_de_outro_alfabeto_nao_vale`: `situacao` = `"６"` → erro com "situacao".

  Em `tests/test_construir.py`:
  - `test_dados_apontando_para_arquivo(tmp_path, capsys)`: um CSV válido passado direto em `--dados` → retorno 0 e "1 arquivo(s)".

- [ ] **Passo 2:** `.venv/bin/python -m pytest -q tests/test_validar.py tests/test_construir.py`. Esperado: os testes novos falham.
- [ ] **Passo 3:** implementar. O `exemplo.csv` continua até a Tarefa 11.
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q`. Esperado: tudo passa.
- [ ] **Passo 5 (mantenedor):** `git add scripts tests && git commit -m "feat: esquemas de baralho e diálogo no validador"`.

### Tarefa 2: planos das trilhas

**Arquivos:**
- Criar: `scripts/planos.py` e `tests/test_planos.py`.
- Modificar: `scripts/construir.py`.

**Interfaces:**
- Produz:
  - `TRILHAS = {"destravar": {"titulo": "Destravar a fala", "semanas": 12, "minutos": (20, 30)}}`.
  - `validar_plano(caminho: Path, trilha: str, raiz_conteudo: Path) -> list[Erro]`.
  - `dados_do_plano(caminho: Path, trilha: str) -> dict`, que devolve `{"trilha", "titulo", "semanas", "passos": [{"semana", "dia", "ordem", "passo", "minutos", "link"}]}`, com os passos ordenados.
- Colunas: `semana, dia, ordem, passo, minutos, link`. Regras:
  - `semana` de 1 a 12, `dia` de 1 a 7, `minutos` de 1 a 30;
  - `ordem` única no dia;
  - `passo` não vazio;
  - soma de minutos do dia entre 20 e 30;
  - `link` vazio, ou um caminho relativo do site sem `/` inicial e sem `http`. Tirando `?…` e `#…`, ele precisa existir como `conteudo/<link>.md`, `conteudo/<link>/index.md` ou `conteudo/<link sem barra final>.md`.
- `construir.main` valida `kit/planos/<trilha>.csv` (o arquivo pode faltar) e grava `conteudo/dados/<trilha>.json` (UTF-8, `ensure_ascii=False`, indentação 2).

- [ ] **Passo 1: testes que falham.**
  - `test_plano_valido_gera_dados(tmp_path)`: dia 1 com passos de 10 e 15 minutos; o link aponta para uma página criada em `tmp_path/conteudo` → sem erros, e os dados vêm ordenados.
  - `test_plano_erros`, parametrizado:
    - dia somando 35 → "minutos";
    - dia somando 15 → "minutos";
    - `dia` = 8 → "dia";
    - `ordem` repetida → "ordem";
    - link `/situacoes/x/` → "link";
    - link `https://exemplo.com` → "link";
    - link para página inexistente → "não existe".
  - `test_dados_do_plano_do_repositorio_em_dia`: se `kit/planos/destravar.csv` existir, o JSON do repositório é igual ao gerado.
- [ ] **Passo 2:** rodar `tests/test_planos.py`. Esperado: falha por import.
- [ ] **Passo 3:** implementar, reaproveitando `Erro` e a leitura tolerante do `validar.py` (BOM, aspas).
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q`. Esperado: tudo passa.
- [ ] **Passo 5 (mantenedor):** `git add scripts/planos.py scripts/construir.py tests/test_planos.py && git commit -m "feat: validação e dados dos planos das trilhas"`.

### Tarefa 3: trechos gerados (frases, diálogo, semanas) e cartas

**Arquivos:**
- Criar: `scripts/paginas.py` e `tests/test_paginas.py`.
- Modificar: `scripts/construir.py`, `zensical.toml` e `conteudo/estilos/ponte.css`. O `ponte.css` ganha a regra de `.pp-frase__falante`, na fonte de etiqueta e com a cor `tinta-suave`.

**Interfaces:**
- Consome `SITUACOES` e os esquemas (Tarefa 1) e `dados_do_plano` (Tarefa 2).
- Produz:
  - `nome_audio(id: str) -> str`, que devolve `f"ice-{id}.mp3"`.
  - `silaba_html(silaba: str) -> str`: `va·CA·tion` vira `va·<b>CA</b>·tion`. A parte toda em maiúsculas vai em `<b>`.
  - `trecho_frases(linhas: list[dict]) -> str`: um `<ul class="pp-frases">` com um `<li class="pp-frase">` por linha, no formato do README do Frase. Diferenças:
    - `<p class="pp-frase__en" lang="en">`;
    - `<p class="pp-frase__silaba">Sílaba forte: …</p>` só quando houver;
    - botão `<button type="button" class="pp-botao" data-audio="ice-<id>.mp3">Ouvir</button>`.
  - `trecho_dialogo(linhas: list[dict]) -> str`: na ordem, cada fala com `<span class="pp-frase__falante">Pessoa A</span>` ou `Pessoa B` antes do inglês. No fim, `<button type="button" class="pp-botao pp-botao--largo" data-audio-sequencia="ice-a.mp3 ice-b.mp3 …">Ouvir o diálogo inteiro</button>`.
  - `trecho_semanas(dados_plano: dict) -> str`: Markdown com `### Semana N`, uma lista por dia ("Dia D — X min") e os passos, cada um com link relativo quando houver.
  - `cartas(linhas_baralho: list[dict]) -> list[dict]`: `{"id", "en", "pt", "silaba", "situacao", "audio"}`.
  - `gerar_tudo(raiz: Path) -> list[Path]`. Grava:
    - `kit/gerado/frases-NN.md` e `kit/gerado/dialogo-NN.md`, onde `NN` é a situação com dois dígitos;
    - `kit/gerado/semanas-<trilha>.md`;
    - `conteudo/dados/cartas.json`.

    Devolve os caminhos gravados. `construir.main` chama depois de validar, e só se não houver erro.
- Todo texto vai escapado com `html.escape(…, quote=True)`.
- `zensical.toml`: adicionar em `[project.markdown_extensions]` as chaves `pymdownx.snippets.base_path = ["."]` e `pymdownx.snippets.check_paths = true`. Trecho ausente derruba o build.

- [ ] **Passo 1: testes que falham.**
  - `test_trecho_frases_escapa_e_marca_ingles`: `en` = `I'm "fine" & you?` → saída contém `lang="en"`, `&quot;fine&quot; &amp; you?` e `data-audio="ice-x-01.mp3"`, e não contém `<script`.
  - `test_silaba_html`: `"va·CA·tion"` → `"va·<b>CA</b>·tion"`.
  - `test_trecho_dialogo_em_ordem_com_sequencia`: linhas fora de ordem saem em ordem; `data-audio-sequencia` lista os arquivos nessa ordem; aparecem "Pessoa A" e "Pessoa B".
  - `test_trecho_semanas`: um plano com 2 dias → contém `### Semana 1`, "Dia 1 — 25 min" e `[texto](../../situacoes/telefonar/)`. Os links ficam relativos a `trilhas/destravar/`, onde o trecho é incluído.
  - `test_gerados_do_repositorio_em_dia`: para cada arquivo de `gerar_tudo` num diretório temporário, cópia de `kit/` e `conteudo/` → igual ao versionado.
- [ ] **Passo 2:** rodar. Esperado: falha por import.
- [ ] **Passo 3:** implementar. Rodar `.venv/bin/python -m scripts.construir`, que gera os arquivos do `exemplo.csv` até a Tarefa 11.
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q`. Esperado: tudo passa, inclusive `test_site`, com o build `--strict`.
- [ ] **Passo 5 (mantenedor):** `git add scripts tests zensical.toml conteudo/estilos/ponte.css kit/gerado conteudo/dados && git commit -m "feat: trechos gerados de frases, diálogo, semanas e cartas"`.

### Tarefa 4: núcleo do JavaScript e botões de áudio

**Arquivos:**
- Criar:
  - `conteudo/js/nucleo.js`;
  - `conteudo/js/logica/datas.js` e `conteudo/js/logica/audio.js`;
  - `conteudo/js/paginas/audio.js` e `conteudo/js/paginas/roteiro.js`;
  - `tests/js.py` e `tests/test_js_nucleo.py`.
- Modificar: `zensical.toml` (`extra_javascript`), `requirements-dev.txt` (`mini-racer==0.14.1`) e `tests/test_site.py`.

**Interfaces:**
- Todos os arquivos registram funções em `globalThis.ICE`. Os de `logica/` não tocam em `window` nem em `document`.
- `tests/js.py`:
  - `contexto(*arquivos: str) -> MiniRacer`: avalia `conteudo/js/<arquivo>` em ordem.
  - `chamar(ctx, funcao: str, *args)`: passa os argumentos em JSON e devolve via `JSON.stringify`, lido com `json.loads`.
- `logica/datas.js`:
  - `ICE.datas.iso(d: Date) -> "AAAA-MM-DD"` com ano, mês e dia **locais**;
  - `ICE.datas.somarDias(iso, n) -> iso`;
  - `ICE.datas.diasEntre(isoA, isoB) -> int`, com `Date.UTC` dos componentes, imune ao horário de verão.
- `logica/audio.js`: `ICE.audio.estadoDoBotao(manifesto: object|null, arquivo: str) -> {"habilitado": bool, "rotulo": "Ouvir" | "Sem áudio aqui"}`. Com manifesto `null` (falha ao baixar), fica desabilitado.
- `nucleo.js`:
  - `ICE.url(caminho)`: resolve a partir de `JSON.parse(document.getElementById("__config").textContent).base`.
  - `ICE.armazenamento.ler(chave) -> string|null` e `ICE.armazenamento.gravar(chave, texto) -> bool`, os dois com `try/catch`.
  - `ICE.aoAbrirPagina(fn)`: usa `window.document$.subscribe(fn)` quando existir; senão, `DOMContentLoaded`.
- `paginas/audio.js`:
  - Baixa `audio/manifesto.json` uma vez por carga.
  - Liga `[data-audio]`, com um `Audio` por vez: tocar outro para o anterior.
  - Liga `[data-audio-sequencia]`, que toca os arquivos em fila.
  - Aplica `estadoDoBotao` com `disabled` e o rótulo.
- `paginas/roteiro.js`: o botão de `.pp-roteiro` copia `.pp-roteiro__texto` com `navigator.clipboard`, troca para "Copiado" por 2 s e, em caso de falha, seleciona o texto.
- `extra_javascript`, nesta ordem: `js/nucleo.js`, `js/logica/datas.js`, `js/logica/audio.js`, `js/logica/treino.js`, `js/logica/plano.js`, `js/logica/ficha.js`, `js/paginas/audio.js`, `js/paginas/roteiro.js`, `js/paginas/treino.js`, `js/paginas/hoje.js`, `js/paginas/ficha.js`. Os das Tarefas 5 e 6 entram na lista quando forem criados.

- [ ] **Passo 1: testes que falham.**
  - `test_iso_usa_data_local`: `ctx.eval("JSON.stringify(ICE.datas.iso(new Date(2026, 10, 13, 23, 30)))")` → `"2026-11-13"`.
  - `test_somar_dias`, parametrizado:
    - `("2026-10-31", 1) → "2026-11-01"`;
    - `("2026-12-31", 1) → "2027-01-01"`;
    - `("2026-11-13", -7) → "2026-11-06"`.
  - `test_dias_entre`: `("2026-11-13", "2026-11-20") → 7`.
  - `test_botao_de_audio`:
    - manifesto `{"ice-a.mp3": true}` → `ice-a.mp3` habilitado com "Ouvir" e `ice-b.mp3` desabilitado com "Sem áudio aqui";
    - manifesto `None` → desabilitado.
  - Em `tests/test_site.py`, `test_scripts_relativos_na_ordem`: `js/nucleo.js` vem antes de `js/paginas/audio.js` no HTML, e os dois saem com `src="./js/…"`.
- [ ] **Passo 2:** rodar. Esperado: falha (arquivos inexistentes).
- [ ] **Passo 3:** implementar e instalar `mini-racer` (`.venv/bin/pip install -r requirements-dev.txt`).
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q`. Esperado: tudo passa.
- [ ] **Passo 5 (mantenedor):** `git add conteudo/js tests requirements-dev.txt zensical.toml && git commit -m "feat: núcleo do JavaScript e botões de áudio"`.

### Tarefa 5: treino de cartas no site

**Arquivos:**
- Criar: `conteudo/js/logica/treino.js`, `conteudo/js/paginas/treino.js`, `conteudo/treinar.md` e `tests/test_js_treino.py`.
- Modificar: `zensical.toml` (`extra_javascript`).

**Interfaces:**
- `logica/treino.js` (`ICE.treino`):
  - `INTERVALOS = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}` (dias);
  - `LIMITE_NOVAS = 10` por dia;
  - `CHAVE = "ice:treino:v1"`.
  - `estadoVazio() -> {"versao": 1, "cartas": {}, "novas": {"dia": null, "quantidade": 0}}`.
  - `ler(texto|null) -> estado`: JSON inválido, `null` ou versão diferente de 1 viram `estadoVazio()`.
  - `responder(estadoCarta|null, acertou: bool, hoje: iso) -> {"caixa", "proxima"}`:
    - acertou: `caixa = min((caixa ou 0) + 1, 5)` e `proxima = somarDias(hoje, INTERVALOS[caixa])`;
    - errou: `{"caixa": 1, "proxima": hoje}`.
  - `fila(ids: list, cartas: dict, hoje: iso, novasHoje: int, limite=LIMITE_NOVAS) -> list`: primeiro as vencidas (`proxima <= hoje`), por `proxima` e depois pela ordem de `ids`. Depois as novas (sem estado), na ordem de `ids`, até `max(0, limite - novasHoje)`.
- `paginas/treino.js`, no elemento `#ice-treino`:
  - Lê `dados/cartas.json` e o filtro `?situacao=N` da URL, com seletor das situações presentes.
  - Mostra o português e "Fale em inglês, em voz alta.". Depois o botão primário "Mostrar a resposta" revela o inglês (`lang="en"`), a sílaba e o "Ouvir". Por fim, "Acertei" e "Errei".
  - Errar coloca a carta de novo no fim da fila da sessão, uma vez. Ao acabar: "Treino de hoje feito. Volte amanhã."
  - Sem armazenamento, mostra o aviso "Seu navegador não está guardando o progresso: o treino vale só para esta visita."
- `conteudo/treinar.md`: título "Treinar cartas", um parágrafo explicando o treino (sem prometer resultado), `<div id="ice-treino"></div>` e `<noscript>` com o link para a lista de frases das situações.

- [ ] **Passo 1: testes que falham** em `tests/test_js_treino.py` (contexto `logica/datas.js` + `logica/treino.js`):
  - `test_acertar_carta_nova`: `responder(None, True, "2026-11-13")` → `{"caixa": 1, "proxima": "2026-11-14"}`.
  - `test_caixa_maxima`:
    - `responder({"caixa": 4, …}, True, "2026-11-13")` → `{"caixa": 5, "proxima": "2026-12-13"}`;
    - `responder({"caixa": 5, …}, True, "2026-11-13")` → `{"caixa": 5, "proxima": "2026-12-13"}`.
  - `test_errar_volta_para_hoje`: `responder({"caixa": 3, "proxima": "2026-11-01"}, False, "2026-11-13")` → `{"caixa": 1, "proxima": "2026-11-13"}`.
  - `test_fila_vencidas_antes_das_novas_com_limite`, com `ids` = `["a", "b", "c", "d", "e"]`:
    - cartas: `b` vence em 12/11, `e` em 10/11, `c` vence no futuro;
    - `novasHoje` = 9, limite 10;
    - resultado: `["e", "b", "a"]`.
  - `test_ler_tolerante`: `ler("{quebrado")`, `ler(None)` e `ler('{"versao": 99}')` são iguais a `estadoVazio()`.
- [ ] **Passo 2:** rodar. Esperado: falha.
- [ ] **Passo 3:** implementar a lógica, a página e o DOM.
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q`. Esperado: tudo passa.
- [ ] **Passo 5 (mantenedor):** `git add conteudo/js conteudo/treinar.md tests zensical.toml && git commit -m "feat: treino de cartas no próprio site"`.

### Tarefa 6: "Hoje", semanas e ficha da trilha

**Arquivos:**
- Criar:
  - `conteudo/js/logica/plano.js`, `conteudo/js/logica/ficha.js`;
  - `conteudo/js/paginas/hoje.js`, `conteudo/js/paginas/ficha.js`;
  - `conteudo/trilhas/index.md`;
  - `conteudo/trilhas/destravar/index.md` (lista das semanas, com `--8<-- "kit/gerado/semanas-destravar.md"`);
  - `conteudo/trilhas/destravar/hoje.md` e `conteudo/trilhas/destravar/ficha.md`;
  - `tests/test_js_plano.py`.

**Interfaces:**
- `logica/plano.js` (`ICE.plano`). A chave de armazenamento é `ice:plano:<trilha>:v1`.
  - `posicao(inicio, hoje, totalSemanas) -> {"semana", "dia", "terminou"}`:
    - `d = diasEntre(inicio, hoje)`; com `d < 0`, vale `d = 0`;
    - `semana = floor(d / 7) + 1` e `dia = d % 7 + 1`;
    - `terminou = semana > totalSemanas`.
  - `inicioParaSemana(hoje, semana) -> iso`.
  - `passosDoDia(plano, semana, dia) -> list`, ordenados.
  - `diasConcluidos(plano, feitos) -> int`: conta os dias com passos em que todas as `ordem` estão em `feitos["s<semana>d<dia>"]`.
  - `ler(texto) -> {"versao": 1, "inicio": null, "feitos": {}}`, tolerante como em `ICE.treino.ler`.
- `paginas/hoje.js`, no elemento `#ice-hoje[data-trilha]`:
  - Sem `inicio`: os botões "Começar hoje" e "Já estou na semana…", com um seletor de 1 a 12.
  - Com `inicio`: o PassosDoDia do dia (título "N minutos de treino", barra `diasConcluidos` do total de dias com passos, passos marcáveis e botão primário "Marcar o próximo passo").
  - Sem passos no dia: "Dia de descanso." Semana sem passos: "Esta semana do plano ainda não foi publicada." `terminou`: "Você chegou ao fim das 12 semanas."
  - Sempre: o aviso "O progresso fica só neste aparelho: trocar de aparelho ou limpar o navegador zera tudo.", um link para a lista das semanas e o botão "Recomeçar", com confirmação.
- `logica/ficha.js` (`ICE.ficha`):
  - `ler`, tolerante;
  - `registrar(estado, semana: int, campos) -> estado`, que normaliza:
    - `gravacao` como data ISO ou `null`;
    - `tempo4`, `tempo3` e `tempo2` de `"m:ss"` para segundos, ou `null`;
    - `conversa` como booleano;
    - `confianca` como inteiro de 1 a 5, ou `null`.
- `paginas/ficha.js`, no elemento `#ice-ficha[data-trilha]`: um formulário por semana (de 1 a 12, abrindo a semana atual quando houver `inicio`) e a tabela das semanas registradas com a classe `pp-tabela` (`data-rotulo` em cada célula). Usa o mesmo aviso de armazenamento.

- [ ] **Passo 1: testes que falham** em `tests/test_js_plano.py`:
  - `test_posicao`, parametrizado, com início `2026-11-01` e total 12:
    - hoje `2026-11-01` → semana 1, dia 1;
    - hoje `2026-11-15` → semana 3, dia 1;
    - hoje `2027-01-24` → `terminou: true`;
    - início `2026-11-20` e hoje `2026-11-13` → semana 1, dia 1.
  - `test_inicio_para_semana`: `("2026-11-13", 3) → "2026-10-30"`.
  - `test_passos_do_dia_e_semana_vazia`: um plano com três passos fora de ordem na semana 1, dia 2 → saem ordenados; `(7, 1)` → `[]`.
  - `test_dias_concluidos`: dois dias com passos; um com todas as ordens feitas e outro pela metade → 1.
  - `test_ficha_registrar`, com os campos:
    ```python
    {"gravacao": "2026-11-13", "tempo4": "3:40", "tempo3": "x", "tempo2": "2:00",
     "conversa": True, "confianca": "7"}
    ```
    Resultado: `{"gravacao": "2026-11-13", "tempo4": 220, "tempo3": None, "tempo2": 120, "conversa": True, "confianca": None}`.
- [ ] **Passo 2:** rodar. Esperado: falha.
- [ ] **Passo 3:** implementar e incluir os scripts em `extra_javascript`.
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q`. Esperado: tudo passa.
- [ ] **Passo 5 (mantenedor):** `git add conteudo/js conteudo/trilhas tests zensical.toml && git commit -m "feat: página Hoje, lista de semanas e ficha da trilha"`.

### Tarefa 7: áudio com Kokoro

**Antes de começar:** pedir o OK do mantenedor para baixar o modelo. São dois arquivos, `kokoro-v1.0.onnx` (326 MB) e `voices-v1.0.bin` (28 MB), da release `model-files-v1.1` de `github.com/thewh1teagle/kokoro-onnx`. Sem OK, os testes com sintetizador falso seguem, e só o Passo 6 espera.

**Arquivos:**
- Criar: `requirements-kit.txt` (`kokoro-onnx==0.6.1`, `soundfile`, `genanki==0.13.1`, com as versões que o pip instalar fixadas), `scripts/audio.py` e `tests/test_audio.py`.
- Modificar: `requirements-dev.txt` (`-r requirements-kit.txt`), `scripts/construir.py` (`--audio`) e `.gitignore` (`conteudo/audio/`, `dist/`).

**Interfaces:**
- `MODELO` e `VOZES`: dicionários com `arquivo`, `url` e `sha256`. O `sha256` é registrado no primeiro download e conferido a cada download.
- `pasta_modelos() -> Path`: a variável `ICE_MODELOS` ou `~/.cache/ingles-com-evidencia/kokoro`.
- Consome `nome_audio` (Tarefa 3) e os esquemas (Tarefa 1).
- `baixar_modelos(pasta, arquivos=(MODELO, VOZES)) -> tuple[Path, ...]`: só baixa o que falta e confere o sha256. Se o arquivo não bater, apaga e levanta um erro com a mensagem em português. O parâmetro `arquivos` deixa o teste apontar para o servidor local.
- `@dataclass(frozen=True) class ItemAudio: id: str; texto: str; voz: str`.
- `itens_de_audio(raiz) -> list[ItemAudio]`:
  - frases dos baralhos com `af_heart`;
  - falas do diálogo com `af_heart` para A e `am_michael` para B.
- `gerar_audios(itens, destino: Path, sintetizar: Callable[[str, str], tuple[ndarray, int]]) -> dict`:
  - grava `ice-<id>.mp3` com `soundfile` (`format="MP3"`);
  - mantém `destino/manifesto.json` com `{arquivo: hash}`, onde o hash é o sha256 de `texto|voz|velocidade|modelo`;
  - pula o que não mudou;
  - apaga `.mp3` órfãos;
  - devolve o manifesto.
- `sintetizador_kokoro(modelo, vozes)`: devolve a função que chama `Kokoro(...).create(texto, voice=voz, speed=0.9, lang="en-us")`.
- `construir.main --audio`: chama `baixar_modelos` e depois `gerar_audios` em `conteudo/audio/`.

- [ ] **Passo 1: testes que falham**, com um sintetizador falso que devolve 0,2 s de seno e conta as chamadas:
  - `test_gera_mp3_e_manifesto`: 2 itens → 2 arquivos `.mp3` que o `soundfile.info` lê como MP3, e o manifesto com 2 entradas.
  - `test_nao_regera_o_que_nao_mudou`: segunda rodada → 0 chamadas.
  - `test_regera_quando_o_texto_muda`: muda 1 texto → 1 chamada.
  - `test_apaga_orfaos`: remove 1 item → o arquivo some e sai do manifesto.
  - `test_vozes_do_dialogo`: falante B → `am_michael`; frase → `af_heart`.
  - `test_sha256_errado_apaga_e_avisa`: um servidor local de teste (`http.server` em thread) serve um arquivo com o conteúdo errado → erro com "sha256" e nenhum arquivo deixado na pasta.
- [ ] **Passo 2:** rodar. Esperado: falha.
- [ ] **Passo 3:** implementar.
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q`. Esperado: tudo passa.
- [ ] **Passo 5 (mantenedor):** `git add requirements-*.txt .gitignore scripts tests && git commit -m "feat: áudio das frases com Kokoro"`.
- [ ] **Passo 6 (com OK):** `.venv/bin/python -m scripts.construir --audio`. Registrar os dois `sha256` em `scripts/audio.py`. Ouvir 3 áudios e conferir que soam como inglês americano, na velocidade combinada.

### Tarefa 8: baralhos do Anki

**Arquivos:**
- Criar: `scripts/baralhos.py` e `tests/test_baralhos.py`.
- Modificar: `scripts/construir.py` (`--baralhos`, que exige `--audio`).

**Interfaces:**
- Consome `nome_audio` (Tarefa 3) e `SITUACOES` (Tarefa 1).
- Constantes:
  - `MODELO_ID` e `BARALHO_BASE_ID`: gerar **uma vez** com `random.randrange(1 << 30, 1 << 31)` e fixar no código;
  - o id do baralho é `BARALHO_BASE_ID + situacao`.
- Modelo "Inglês com Evidência — Produzir":
  - campos `Id`, `Portugues`, `Ingles`, `Silaba`, `Audio`, `Credito`;
  - frente: `{{Portugues}}` e "Fale em inglês, em voz alta.";
  - verso: `{{FrontSide}}<hr id=answer>`, depois `<div lang="en">{{Ingles}}</div>`, `{{#Silaba}}…{{/Silaba}}` e `{{Audio}}`;
  - CSS com as cores do Passaporte (tema claro).
- A nota é uma subclasse de `genanki.Note` com `guid = genanki.guid_for(id)`. `Audio` = `[sound:ice-<id>.mp3]`. `Credito` = fonte, licença e autor.
- `gerar_baralho(situacao: int, linhas: list[dict], pasta_audio: Path, destino: Path) -> Path`:
  - grava `ice-destravar-situacao-NN.apkg`;
  - nome do baralho: `Inglês com Evidência::Destravar a fala::NN <título>`;
  - frase sem áudio gera erro "sem áudio: <id>".
- `construir.main --baralhos` grava em `dist/baralhos/`.

- [ ] **Passo 1: testes que falham**, com 2 linhas e 2 `.mp3` falsos:
  - `test_apkg_tem_notas_com_guid_estavel`: abre o zip e o `collection.anki2` com `sqlite3`. `select guid, flds from notes` → os guids são iguais a `genanki.guid_for(id)`, e `flds` contém o português.
  - `test_apkg_leva_os_audios`: o JSON `media` do zip lista `ice-<id>.mp3`.
  - `test_nome_do_baralho`: `select decks from col` contém "Destravar a fala::06".
  - `test_frase_sem_audio_e_erro`: `pytest.raises` com "sem áudio".
- [ ] **Passo 2:** rodar. Esperado: falha.
- [ ] **Passo 3:** implementar.
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q`. Esperado: tudo passa.
- [ ] **Passo 5 (mantenedor):** `git add scripts tests && git commit -m "feat: baralhos do Anki com cartas de produzir"`.

### Tarefa 9: créditos gerados

**Arquivos:**
- Criar: `scripts/creditos.py`, `tests/test_creditos.py` e `CREDITOS.md` (gerado).
- Modificar: `scripts/construir.py` e `conteudo/sobre.md`.

**Interfaces:**
- `gerar_creditos(raiz: Path) -> str`, em Markdown, com as seções:
  - **Dados:** contagem por fonte e licença. Para `tatoeba:N`, uma linha por frase com o link `https://tatoeba.org/pt-br/sentences/show/N`, o autor e a licença.
  - **Áudio:** Kokoro-82M (hexgrad, Apache 2.0), `kokoro-onnx` (MIT), as vozes `af_heart` e `am_michael`, e o aviso de que o áudio é voz sintética.
  - **Fontes:** as três, com licença OFL.
  - **Vocabulário:** NGSL (CC BY-SA 4.0), só quando houver linha `ngsl`.
- `construir.main` grava o `CREDITOS.md`. A página Sobre ganha um link para `CREDITOS.md` no GitHub e uma frase sobre a voz sintética.

- [ ] **Passo 1: testes que falham.**
  - `test_creditos_tatoeba_com_link_e_autor` (dados temporários).
  - `test_sem_ngsl_nao_cita_ngsl`.
  - `test_creditos_do_repositorio_em_dia`.
- [ ] **Passos 2 a 4:** rodar e ver falhar, implementar, rodar e ver tudo passar.
- [ ] **Passo 5 (mantenedor):** `git add scripts tests CREDITOS.md conteudo/sobre.md && git commit -m "feat: créditos gerados a partir dos dados"`.

### Tarefa 10: Action com áudio e baralhos

**Arquivos:**
- Modificar: `.github/workflows/site.yml` e `tests/test_repositorio.py`.

**Decisões:**
- `on`: `push` na `main`, `push` de tags `v*` e `pull_request`.
- `concurrency` sai do topo e vai só para o job `publicar` (ajuste adiado da Fase 0).
- `setup-python` com `cache-dependency-path: requirements-*.txt`.
- **Job `verificar`:** como hoje, mas instalando `requirements-dev.txt`.
- **Job `publicar`** (só em push na `main`):
  - `actions/cache@v5` em `~/.cache/ingles-com-evidencia/kokoro`, com chave `kokoro-v1.0-<sha256 do modelo>`;
  - `pip install -r requirements-site.txt -r requirements-kit.txt`;
  - `python -m scripts.construir --audio`;
  - `zensical build --clean --strict`;
  - upload e deploy, como hoje.
- **Job `baralhos`:**
  - `if: startsWith(github.ref, 'refs/tags/v')`;
  - `needs: verificar`;
  - `permissions: contents: write`;
  - mesmo cache e instalação do `publicar`;
  - `python -m scripts.construir --audio --baralhos`;
  - `gh release create "$GITHUB_REF_NAME" dist/baralhos/*.apkg --title "Baralhos $GITHUB_REF_NAME" --generate-notes`, com `GH_TOKEN: ${{ github.token }}`.

- [ ] **Passo 1: testes que falham** em `tests/test_repositorio.py`:
  - `test_publicar_gera_audio_antes_do_build`: no trecho do job `publicar`, o índice de `scripts.construir --audio` é menor que o de `zensical build`.
  - `test_job_baralhos_so_em_tag`: o trecho do job `baralhos` contém `startsWith(github.ref, 'refs/tags/v')`, `contents: write` e `gh release create`.
  - `test_concurrency_so_no_publicar`: `concurrency` aparece uma vez, dentro do trecho do `publicar`.
- [ ] **Passos 2 a 4:** rodar e ver falhar, implementar, rodar e ver tudo passar. Conferir que o YAML carrega.
- [ ] **Passo 5 (mantenedor):** `git add .github tests && git commit -m "ci: áudio no deploy e baralhos nas releases"`.

### Tarefa 11: piloto da situação 6 e ajustes adiados da Fase 0

**Arquivos:**
- Criar:
  - `kit/dados/situacao-06.csv`, com 10 a 12 frases;
  - `kit/dialogos/situacao-06.csv`, com 8 a 12 falas;
  - `kit/planos/destravar.csv` (só a semana 1);
  - `conteudo/situacoes/index.md` e `conteudo/situacoes/telefonar.md`.
- Apagar: `kit/dados/exemplo.csv`. Os ids `exemplo-*` ficam aposentados.
- Modificar:
  - `zensical.toml`;
  - `conteudo/index.md`;
  - `design/passaporte/README.md` e `design/passaporte/components/{Frase,Botao}/README.md`;
  - `tests/test_site.py` e `tests/test_construir.py`.

**Conteúdo do piloto** (o texto é de quem constrói; as regras ficam aqui):
- **Frases:**
  - Cobrem: se apresentar ao ligar; perguntar se é um bom momento; propor uma reunião; sugerir dia, hora e fuso; confirmar; remarcar; pedir para repetir ou falar mais devagar; mandar o convite; encerrar a ligação.
  - Preferir frases do Tatoeba (`fonte` = `tatoeba:N`, `licenca`, `autor`), conferindo a licença de cada uma. No resto, `projeto` com CC BY-SA 4.0.
  - Sílaba forte só em palavra difícil, como `SCHED·ule` e `a·VAIL·a·ble`.
- **Diálogo:** colega (A) liga para outro colega (B) e marca uma reunião. Tudo `projeto`.
- **Página `telefonar.md`:**
  - Faixa "Situação 6 de 8" / "Trabalho" e uma introdução de 2 frases.
  - "Frases", com `--8<-- "kit/gerado/frases-06.md"`.
  - "Diálogo", com `--8<-- "kit/gerado/dialogo-06.md"`.
  - "Treinar":
    - Botao primário "Treinar as cartas desta situação", com `href="../../treinar/?situacao=6"`.
    - Link para baixar o baralho em `https://github.com/angeloreis/ingles-com-evidencia/releases/latest/download/ice-destravar-situacao-06.apkg`.
    - Uma frase sobre o Anki ser opcional, dizendo que importa pelo AnkiDroid ou pelo Anki no computador e que o AnkiMobile do iPhone é pago.
  - Um RoteiroIA em inglês para o modo de voz de uma IA (pessoa colega de trabalho que liga para marcar uma reunião e corrige com gentileza no fim).
  - "Notas culturais", em 3 a 5 itens: fuso horário no convite, *small talk* curto, "Does that work for you?".
- **Plano da semana 1:** 7 dias, cada um com 20 a 30 min ou de descanso. Passos possíveis:
  - ouvir e repetir as frases;
  - shadowing do diálogo;
  - treinar as cartas;
  - 4/3/2 explicando o próprio trabalho;
  - gravar a voz;
  - roteiro de IA;
  - conversa real.

  Os links apontam para páginas que existem. O plano 1B revisa a semana 1 quando os capítulos existirem.
- **Menu** (`nav`):
  - Início;
  - Situações (Visão geral, Telefonar e marcar reunião);
  - Trilhas e planos (Visão geral, Destravar a fala: Hoje, Semanas e Ficha);
  - Treinar cartas;
  - Sobre e créditos.

  "Guia" entra no plano 1B.
- **Início:** "Por onde começar". O botão primário "Começar a trilha Destravar a fala" leva a `trilhas/destravar/hoje/`. "Do zero ao A2" continua "em construção". A frase "sem instalar nada" passa a falar só do uso básico (ler, ouvir e seguir o plano).
- **Ajustes adiados da Fase 0:**
  - `[project.extra] generator = false`;
  - `toc.permalink_title = "Link para esta seção"`;
  - `lang="en"` em "verb to be";
  - Carimbo `pp-carimbo--reto` na lista de selos;
  - `design/passaporte/README.md` sem citar o Google Fonts (apontar para `fontes.md`);
  - o exemplo de href do Botao vira relativo, e o exemplo do Frase ganha `lang="en"`.

- [ ] **Passo 1: testes que falham.**
  - Em `test_site.py`:
    - `test_situacao_6_publicada`: `site/situacoes/telefonar/index.html` tem ao menos 10 `class="pp-frase"`, `lang="en"`, `data-audio-sequencia` e `pp-roteiro`.
    - `test_paginas_da_trilha`: os `index.html` de `trilhas/destravar/hoje/`, `trilhas/destravar/ficha/` e `treinar/` existem.
    - `test_sem_textos_do_tema_em_ingles`: nenhum HTML contém "Made with" nem `title="Permanent link"`.
  - Em `test_construir.py`, atualizar a contagem para "1 arquivo(s), N linha(s)", com o N do CSV final.
- [ ] **Passo 2:** rodar. Esperado: falha.
- [ ] **Passo 3:** escrever o conteúdo, rodar `.venv/bin/python -m scripts.construir` e ajustar o resto.
- [ ] **Passo 4:** `.venv/bin/python -m pytest -q` e `.venv/bin/python -m scripts.construir --audio`. Esperado: tudo passa, e os áudios saem.
- [ ] **Passo 5 (mantenedor):** `git add -A kit conteudo design zensical.toml tests CREDITOS.md && git commit -m "feat: situação 6 como piloto e semana 1 da trilha"`.

### Tarefa 12: conferência no navegador e registro no desenho

- [ ] **Passo 1: celular a 375 px, nos dois temas.** Com `zensical serve` e os áudios gerados, abrir Início e tocar "Começar a trilha". Em "Hoje", "Começar hoje" mostra o dia 1. Marcar 2 passos, recarregar e conferir que continuam marcados.
- [ ] **Passo 2: troca de página sem recarregar** (ponto 5). Pelo menu, ir até "Telefonar e marcar reunião". "Ouvir" toca; "Ouvir o diálogo inteiro" toca em fila; "Copiar roteiro" vira "Copiado".
- [ ] **Passo 3: treino.** Abrir pelo botão da situação: o filtro da situação 6 já vem aplicado. Fazer 3 cartas (acertar, errar, acertar) e conferir que a errada volta no fim.
- [ ] **Passo 4: sem armazenamento** (ponto 1).
  1. No console da página, rodar `Storage.prototype.getItem = Storage.prototype.setItem = function () { throw new Error("bloqueado"); }`.
  2. Navegar pelo menu até "Hoje" e depois até "Treinar cartas". A troca de página sem recarregar roda os componentes de novo.
  3. Esperado: os dois mostram o aviso de armazenamento e funcionam durante a visita.
- [ ] **Passo 5: medição de 320, 375 e 1280 px nos dois temas.** Conferir:
  - `innerWidth` igual à largura simulada e `scrollWidth <= innerWidth`;
  - nenhuma requisição de fora;
  - botões com 48 px.
- [ ] **Passo 6: desenho.** Registrar:
  - a decisão do treino no site (seção 5.2, Anki);
  - o critério da Fase 1, que passa a ser "só pelo site";
  - a divisão em 1A e 1B;
  - o esquema dos diálogos;
  - as vozes e a velocidade;
  - os trechos gerados em `kit/gerado/`.
- [ ] **Passo 7 (mantenedor):** commit do desenho, push e tag `v0.1.0`. Conferir a Action: o site é publicado com áudio, e a Release traz `ice-destravar-situacao-06.apkg`.
