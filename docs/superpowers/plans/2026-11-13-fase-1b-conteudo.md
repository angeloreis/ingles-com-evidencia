# Fase 1B (conteúdo): plano de implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: use superpowers:subagent-driven-development (recomendada) ou superpowers:executing-plans para executar este plano tarefa por tarefa. Os passos usam caixas (`- [ ]`) para acompanhamento.

**Objetivo:** completar a Fase 1 sobre o motor da 1A:
- situações 7 (programação, IA e frameworks) e 8 (entrevista para trabalho remoto), com frases, diálogo, áudio, cartas, roteiro de IA e notas culturais;
- o guia, com os capítulos 1, 6, 8, 9, 10 e 11, cada um com selo de evidência e referências lidas;
- as semanas 1 a 6 da trilha "Destravar a fala", usando só as situações 6, 7 e 8;
- os baralhos das três situações na Release `v0.2.0`.

**Arquitetura:** o motor da 1A não muda de forma. Os CSVs de `kit/` continuam sendo a fonte das situações e do plano, e as páginas escritas à mão incluem os trechos gerados. Entram três peças novas:
- a coluna opcional `leitura`, com o texto que a voz sintética lê quando a escrita engana a voz (PostgreSQL, regex, async);
- `scripts/guia.py`, que confere a estrutura de cada capítulo e se toda citação tem referência e registro de leitura. O `construir` roda essa conferência, então a Action barra um capítulo com citação solta;
- `docs/pesquisa/referencias.md`, o registro de leitura: uma entrada por estudo, com link e o que o resumo diz, em palavras próprias.

**Tecnologias:** as mesmas da 1A (Python 3.12, Zensical 0.1.1, kokoro-onnx 0.6.1, genanki 0.13.1, mini-racer nos testes). Nenhuma dependência nova.

**Desenho:** `docs/superpowers/specs/2026-11-12-ingles-com-evidencia-design.md` (seções 5.1, 5.2, 5.3 e 5.5). Plano anterior: `docs/superpowers/plans/2026-11-13-fase-1a-motor-do-kit.md`.

**Pronto quando:** no site publicado, pelo celular:
- as situações 6, 7 e 8 têm frases e diálogo com áudio e treino de cartas;
- os capítulos 1, 6, 8, 9, 10 e 11 estão no menu "Guia", cada capítulo de técnica com selo e referências;
- "Hoje" e a lista de semanas trazem as semanas 1 a 6;
- a Release `v0.2.0` traz os baralhos das situações 6, 7 e 8.

O mantenedor valida no celular, seguindo um dia de uma semana que use a situação 7 ou 8, e ouve os áudios novos.

## Restrições gerais

- Todas as da Fase 1A continuam valendo:
  - pt-BR, e toda frase em inglês com tradução e com `lang="en"` no HTML;
  - texto com 17 px ou mais, toque com 48 px ou mais, sem rolagem lateral;
  - contraste AA nos dois temas;
  - nada de terceiros nem rastreadores;
  - nenhum dado pessoal no repositório;
  - nenhum caminho começando com `/`;
  - progresso só no `localStorage`, dentro de `try/catch`;
  - vozes `af_heart` (frases e pessoa A) e `am_michael` (pessoa B), velocidade 0.9, arquivos `ice-<id>.mp3`;
  - só cartas "produzir" na trilha;
  - trilha `destravar` com de 20 a 30 minutos por dia com passos; dia sem passos é descanso.
- **Guia, estrutura de cada capítulo de técnica (desenho 5.1), nesta ordem:**
  - Faixa, título e Carimbo;
  - SecaoDoGuia "O que os cursos dizem", "O que a pesquisa diz" e "Como praticar";
  - `## Armadilhas`;
  - `## Referências`, a última seção.
  - Capítulo com mais de uma técnica (o 9) põe, logo abaixo do título, uma lista de carimbos retos, um por técnica.
- **Critério dos selos (desenho 5.1):**
  - **Forte:** metanálises ou muitos estudos controlados com resultado na mesma direção;
  - **Moderada:** vários estudos a favor, com limitações (amostras pequenas, contexto restrito);
  - **Fraca:** poucos estudos, estudos indiretos ou resultados mistos;
  - **Sem evidência:** nenhum estudo, ou estudos contra a promessa.
- **Nenhuma referência entra no guia sem que o resumo do estudo tenha sido lido.** Se ela não disser o que se esperava, o texto muda, não a referência.
  - Cada referência tem uma entrada no registro `docs/pesquisa/referencias.md`.
  - Citação no texto só nestas formas: `Sobrenome (AAAA)`, `Sobrenome e Sobrenome (AAAA)` ou `Sobrenome et al. (AAAA)`.
  - Resumo sempre com palavras próprias; trecho literal de estudo, no máximo uma expressão curta entre aspas.
- **"O que os cursos dizem":** a promessa com palavras próprias, sem nome de curso, de pessoa ou de produto e sem copiar texto de curso.
- **IA:** nenhum nome de produto de IA (como na situação 6), e aviso para não colar dados pessoais na conversa.
- **Frases e falas escritas pelo projeto** (`fonte` `projeto`, CC BY-SA 4.0), como na 1A (ruling da Tarefa 11 da 1A):
  - de 8 a 12 frases por situação e de 10 a 14 falas por diálogo;
  - o mantenedor revisa o inglês antes da tag.
- **Situação 7:** a pronúncia de cada termo técnico é conferida no Cambridge Dictionary. Para nome de projeto que não está em dicionário, vale a documentação oficial do projeto. O link vai na página, e termo sem fonte que diga a pronúncia fica de fora.
- **Situação 8:** treina dizer a verdade com clareza. Nenhuma frase ensina inventar experiência ou esconder fatos.
- **Downloads:** nenhum previsto. Ler páginas na web para a pesquisa pode; baixar PDF ou qualquer arquivo pede OK do mantenedor.
- **Git é do mantenedor:** cada tarefa sugere um commit, sem `Co-Authored-By`. Quem executa não roda git.

## Pontos de atenção na revisão

1. **Termo técnico que a voz lê errado:** PostgreSQL sai "post-grer", regex sai "rih-jex" e async sai "uh-sink" (conferido no fonemizador do kokoro-onnx em 13/11/2026). O áudio tem de dizer o que o dicionário diz. *Teste de `leitura` na Tarefa 1; conferência dos fonemas de cada frase na Tarefa 13.*
2. **Pessoa que passa da última semana publicada** (semana 7 em diante): "Hoje" diz o que fazer, em vez de uma tela sem saída. *Teste de `ultimaSemana` na Tarefa 5, mais conferência no navegador na Tarefa 16.*
3. **Estado salvo com campo `null`** (versão antiga ou dado mexido à mão): a página abre como se fosse a primeira visita, sem quebrar. *Testes de `ler` na Tarefa 3.*
4. **Citação sem referência, referência sem citação ou referência sem registro de leitura:** o `construir` acusa, e a Action não publica. *Testes de `conferir_capitulo` na Tarefa 6.*
5. **Link do plano para página que não existe, ou `?situacao=` fora de 6 a 8:** o `construir` acusa. *`validar_plano` (1A) mais o teste das semanas na Tarefa 15.*

## Mapa dos arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `scripts/validar.py`, `scripts/audio.py` | Coluna opcional `leitura` | 1 |
| `scripts/paginas.py`, `conteudo/js/paginas/treino.js` | `conteudo/dados/situacoes.json` e títulos no treino | 2 |
| `tests/conftest.py`, `conteudo/js/logica/{plano,treino,ficha}.js` | Fuso dos testes, `ler` sem `null` | 3 |
| `scripts/paginas.py`, `scripts/baralhos.py`, `conteudo/js/paginas/{audio,treino}.js` | Sílaba com `lang="en"`, "Ouvir" desabilitado, descrição do baralho | 4 |
| `conteudo/js/logica/plano.js`, `conteudo/js/paginas/hoje.js` | "Hoje" depois da última semana | 5 |
| `scripts/guia.py`, `docs/pesquisa/referencias.md`, `scripts/construir.py` | Conferência do guia e registro de leitura | 6 |
| `conteudo/guia/index.md`, `conteudo/guia/como-usar.md` | Visão geral e capítulo 1 | 7 |
| `conteudo/guia/{frases-chave,shadowing,fluencia,medo-de-falar,ia-modo-de-voz}.md` | Capítulos 6, 8, 9, 10 e 11 | 8 a 12 |
| `kit/dados/situacao-0{7,8}.csv`, `kit/dialogos/situacao-0{7,8}.csv`, `conteudo/situacoes/{tecnologia,entrevista}.md` | Situações 7 e 8 | 13 e 14 |
| `kit/planos/destravar.csv` | Semanas 2 a 6 | 15 |
| `conteudo/{index,sobre}.md`, `conteudo/situacoes/index.md`, `conteudo/trilhas/index.md`, desenho | Textos de entrada e fechamento | 16 |

**Fora desta fase** (ficam na memória do projeto): os menores M2, M3, M4, M5, M6, M10, M12, M13 e M14 da 1A; capítulos 2 a 5, 7, 12 e 13 e situações 1 a 5 (Fase 2); semanas 7 a 12.

---

### Tarefa 1: Texto de leitura para a voz sintética

**Arquivos:**
- Modificar: `scripts/validar.py` (`BARALHO`, `DIALOGO`), `scripts/audio.py` (`itens_de_audio`)
- Testes: `tests/test_validar.py`, `tests/test_audio.py`

**Interfaces:**
- Produz: coluna opcional `leitura` nos dois esquemas (`BARALHO.opcionais == ("silaba", "autor", "leitura")`, `DIALOGO.opcionais == ("autor", "leitura")`). `itens_de_audio(raiz)` usa `linha["leitura"]` quando não está vazia; se estiver, usa `linha["en"]`.

- [ ] **Passo 1: testes que falham**
  - `test_leitura_e_coluna_opcional`: CSV de baralho e de diálogo com a coluna `leitura` (uma linha preenchida, outra vazia) → `validar_arquivo` sem erros.
  - `test_itens_de_audio_usam_a_leitura`: em `tmp_path/kit/dados`, a linha `{"id": "t-01", "en": "We moved to PostgreSQL.", "leitura": "We moved to post gres Q L."}` gera `ItemAudio("t-01", "We moved to post gres Q L.", VOZ_PRINCIPAL)`; outra linha sem leitura usa o `en`. O mesmo vale para uma fala de diálogo da pessoa B.
- [ ] **Passo 2:** `.venv/bin/python -m pytest -q tests/test_validar.py tests/test_audio.py` → os dois falham (coluna desconhecida; texto do `en`).
- [ ] **Passo 3:** acrescentar `leitura` aos opcionais e usar `l.get("leitura") or l["en"]` em `itens_de_audio`. A assinatura do áudio já inclui o texto, então mudar a leitura regera o arquivo.
- [ ] **Passo 4:** a suíte inteira passa.
- [ ] **Passo 5:** commit sugerido: `feat(kit): coluna leitura para a voz sintética`.

### Tarefa 2: Títulos das situações no treino

**Arquivos:**
- Modificar: `scripts/paginas.py` (`gerar_tudo`), `conteudo/js/paginas/treino.js`
- Gerado e versionado: `conteudo/dados/situacoes.json`
- Testes: `tests/test_paginas.py`

**Interfaces:**
- Consome: `SITUACOES` (`scripts/situacoes.py`).
- Produz: `gerar_tudo` grava `conteudo/dados/situacoes.json`, um objeto `{"6": "Telefonar para colegas e marcar reunião"}` só com as situações que têm cartas, em ordem numérica.
  - O treino busca esse arquivo com `ICE.json` e mostra no seletor `"Situação 6: Telefonar para colegas e marcar reunião"`.
  - Se o arquivo faltar, o seletor volta a mostrar `"Situação 6"`.

- [ ] **Passo 1: teste que falha.** `test_titulos_das_situacoes_com_cartas`: com cartas das situações 6 e 8 em `tmp_path/kit/dados`, `gerar_tudo` grava `conteudo/dados/situacoes.json` igual a `{"6": SITUACOES[6][1], "8": SITUACOES[8][1]}` e o inclui na lista de gravados.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** implementar. No `treino.js`, buscar os dois JSON antes de montar o seletor; uma falha no `situacoes.json` não impede o treino.
- [ ] **Passo 4:** rodar `python -m scripts.construir`, depois a suíte inteira (o teste "em dia" cobre o arquivo novo).
- [ ] **Passo 5:** commit sugerido: `feat(site): títulos das situações no treino`.

### Tarefa 3: Fuso nos testes e estado com campos nulos (M1, M11)

**Arquivos:**
- Modificar: `tests/conftest.py`, `conteudo/js/logica/plano.js`, `conteudo/js/logica/treino.js`, `conteudo/js/logica/ficha.js`
- Testes: `tests/test_js_nucleo.py`, `tests/test_js_plano.py`, `tests/test_js_treino.py`

**Interfaces:** nenhuma nova. Os `ler` passam a devolver o estado vazio quando `feitos`, `cartas`, `novas` ou `semanas` não são um objeto (incluindo `null`).

- [ ] **Passo 1: testes que falham**
  - `test_fuso_dos_testes_e_o_do_brasil`: `avaliar(ctx, "new Date(2026, 10, 13, 23, 30).getTimezoneOffset()") == 180`.
  - `test_ler_plano_com_campo_nulo`: `'{"versao": 1, "inicio": null, "feitos": null}'` → `{"versao": 1, "inicio": None, "feitos": {}}`.
  - `test_ler_treino_com_campo_nulo`: `'{"versao": 1, "cartas": null, "novas": {"dia": null, "quantidade": 0}}'` → `estadoVazio()`.
  - `test_ler_ficha_com_campo_nulo`: `'{"versao": 1, "semanas": null}'` → `{"versao": 1, "semanas": {}}`.
- [ ] **Passo 2:** rodar com `TZ=UTC .venv/bin/python -m pytest -q tests/test_js_nucleo.py tests/test_js_plano.py tests/test_js_treino.py` → os quatro falham. O do fuso só falha com `TZ=UTC`, que é o fuso da Action; na máquina do mantenedor o fuso já é o do Brasil.
- [ ] **Passo 3:** no `conftest.py`, fixar `os.environ["TZ"] = "America/Sao_Paulo"` e chamar `time.tzset()` antes de qualquer `MiniRacer`. Nos `ler`, conferir `x && typeof x === "object"`.
- [ ] **Passo 4:** `TZ=UTC .venv/bin/python -m pytest -q` passa inteiro.
- [ ] **Passo 5:** commit sugerido: `fix(site): fuso fixo nos testes e estado salvo com campos nulos`.

### Tarefa 4: Frases geradas e baralho (M7, M8, M16, M17)

**Arquivos:**
- Modificar: `scripts/paginas.py` (`silaba_html`, `_frase_li`, `trecho_dialogo`), `scripts/baralhos.py`, `conteudo/js/paginas/treino.js`, `design/passaporte/components/Frase/README.md`
- Testes: `tests/test_paginas.py`, `tests/test_baralhos.py`

**Interfaces:**
- `silaba_html("va·CA·tion") == '<span lang="en">va·<b>CA</b>·tion</span>'`.
- Os botões "Ouvir" e "Ouvir o diálogo inteiro" saem do gerador com `disabled`. O `paginas/audio.js` já faz `botao.disabled = !estado.habilitado` (linha 31), então habilita cada um quando o manifesto tem o arquivo; sem JavaScript, o botão fica desabilitado.
- O baralho ganha `description` com "Inglês com Evidência", o endereço do site (`https://angeloreis.github.io/ingles-com-evidencia/`) e "CC BY-SA 4.0".

- [ ] **Passo 1: testes que falham**
  - `test_silaba_html` atualizado para o valor acima.
  - `test_ouvir_nasce_desabilitado`: em `trecho_frases([FRASE])` e `trecho_dialogo(...)`, cada `<button` com `data-audio` ou `data-audio-sequencia` tem `disabled`.
  - `test_baralho_tem_descricao`: o `desc` do baralho no JSON de decks do `.apkg` contém as três partes.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** implementar.
  - No treino, a linha da sílaba recebe `lang="en"` no elemento da palavra.
  - No README do Frase, juntar os dois itens "O áudio:".
- [ ] **Passo 4:** rodar `construir`, depois a suíte inteira. No navegador, a página da situação 6 continua com os 24 botões habilitados.
- [ ] **Passo 5:** commit sugerido: `fix(kit): sílaba em inglês, Ouvir desabilitado até ter áudio e descrição do baralho`.

### Tarefa 5: "Hoje" depois da última semana publicada (M9)

**Arquivos:**
- Modificar: `conteudo/js/logica/plano.js`, `conteudo/js/paginas/hoje.js`
- Teste: `tests/test_js_plano.py`

**Interfaces:**
- Produz: `ICE.plano.ultimaSemana(plano) -> number`, a maior `semana` com passos, ou 0 sem passos.
- Em "Hoje", quando a semana atual passa de `ultimaSemana` (e vai até `total`), a página mostra:
  - o texto "As semanas {ultima+1} a {total} ainda não foram publicadas. Enquanto isso, repita a semana {ultima} ou siga no treino de cartas.";
  - o botão "Repetir a semana {ultima}", que grava `inicio = ICE.plano.inicioParaSemana(hoje, ultima)`;
  - o link "Treinar as cartas".
  - Essa mensagem substitui "Esta semana do plano ainda não foi publicada.".

- [ ] **Passo 1: teste que falha.** `test_ultima_semana`: o `PLANO` dos testes (só a semana 1) → 1; um plano com passos nas semanas 1 e 3 → 3; `{"passos": []}` → 0.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** implementar.
- [ ] **Passo 4:** a suíte inteira passa.
- [ ] **Passo 5:** commit sugerido: `feat(site): Hoje sugere o que fazer depois da última semana publicada`.

### Tarefa 6: Conferência do guia e registro de leitura

**Arquivos:**
- Criar: `scripts/guia.py`, `docs/pesquisa/referencias.md` (só o cabeçalho com o formato), `tests/test_guia.py`
- Modificar: `scripts/construir.py` (chama a conferência depois dos planos)

**Interfaces:**
- `CAPITULOS: dict[str, int]`: slug → número, só dos capítulos publicados. Começa vazio; cada tarefa de capítulo acrescenta o seu.
- `SEM_CARIMBO = {"como-usar"}`: capítulo sem técnica, dispensado de carimbo e SecaoDoGuia, mas com `## Referências` se citar alguém.
- `ler_registro(caminho: Path) -> dict[tuple[str, str], dict[str, str]]`: chave (primeiro sobrenome, ano).
- `conferir_capitulo(caminho: Path, registro: dict) -> list[Erro]`, com o `Erro` de `scripts/validar.py`.
- `conferir_guia(pasta: Path, caminho_registro: Path) -> list[Erro]`:
  - pasta ausente: devolve `[]` sem conferir nada (os testes do `construir` usam um `--conteudo` sem guia);
  - confere todo `.md` da pasta, menos `index.md`;
  - slug fora de `CAPITULOS` é erro, e slug de `CAPITULOS` sem arquivo também.
- `construir` soma esses erros aos outros e sai com código 1 se houver algum.

Formato de uma entrada do registro:

```markdown
## Boers et al. (2006)

- Link: https://doi.org/…
- Lido em: 2026-11-14
- O que o resumo diz: (duas a quatro linhas, com palavras próprias)
- Usado em: capítulo 6, "O que a pesquisa diz"
```

Formato de uma referência no capítulo (a lista de `## Referências`):

```markdown
- Boers, F., Eyckmans, J., … (2006). Título. *Revista*, 10(3), 245–261. <https://doi.org/…>
```

A chave da referência é o texto antes da primeira vírgula mais o ano entre parênteses. A chave da citação no texto é o primeiro sobrenome mais o ano.

- [ ] **Passo 1: testes que falham.** Em `tests/test_guia.py`, cada teste escreve um capítulo e um registro em `tmp_path`, com um slug acrescentado a `CAPITULOS` por `monkeypatch`.
  - `test_capitulo_completo_sem_erros`
  - `test_falta_secao` (sem "Como praticar" → erro que cita "Como praticar")
  - `test_secoes_fora_de_ordem`
  - `test_sem_carimbo` (erro); `test_como_usar_sem_carimbo_pode`
  - `test_citacao_sem_referencia` (erro que cita "Hamada (2016)")
  - `test_referencia_sem_citacao`
  - `test_referencia_sem_link_https`
  - `test_referencia_fora_do_registro` (erro que cita "registro de leitura")
  - `test_registro_sem_resumo` (entrada sem "O que o resumo diz" → erro)
  - `test_slug_desconhecido`; `test_capitulo_listado_sem_arquivo`; `test_pasta_do_guia_ausente_sem_erros`
  - `test_construir_acusa_capitulo_com_problema` (pela linha de comando, com `--conteudo` em `tmp_path`)
  - `test_guia_do_repositorio_sem_problemas`: `conferir_guia(RAIZ / "conteudo/guia", RAIZ / "docs/pesquisa/referencias.md") == []`
- [ ] **Passo 2:** rodar e ver falhar (módulo não existe).
- [ ] **Passo 3:** implementar. Rótulos das seções lidos de `pp-secao__rotulo">…<`; carimbo por `class="pp-carimbo` com `data-nivel` de 0 a 3 antes do primeiro `pp-secao`; títulos por `^## `.
- [ ] **Passo 4:** a suíte inteira passa, e `python -m scripts.construir` diz "Tudo certo".
- [ ] **Passo 5:** commit sugerido: `feat(guia): conferência dos capítulos e registro de leitura`.

### Tarefa 7: Guia, visão geral e capítulo 1

**Arquivos:**
- Criar: `conteudo/guia/index.md`, `conteudo/guia/como-usar.md`
- Modificar: `zensical.toml` (seção "Guia" no menu, logo depois de "Início"), `scripts/guia.py` (`CAPITULOS["como-usar"] = 1`), `conteudo/index.md` (os selos saem da página inicial e viram um link para o capítulo 1)
- Testes: `tests/test_site.py`, `tests/test_guia.py`

**Conteúdo:**
- `index.md`: Faixa "Guia / 13 capítulos"; os 13 capítulos na ordem do desenho. Os publicados têm link; os outros aparecem como "Em breve", sem link.
- `como-usar.md`:
  - como ler um capítulo (as seções e o que cada uma traz);
  - o que significam os selos (a tabela do critério, com um carimbo reto por linha);
  - como as referências são conferidas (resumo lido; o selo muda se a pesquisa não sustentar);
  - como o guia se liga ao kit (situações, "Hoje", treino);
  - como reportar erro (issue).

- [ ] **Passo 1: teste que falha.** `test_guia_no_menu`: o site gerado tem `guia/index.html` e `guia/como-usar/index.html`, e o menu tem "Guia" antes de "Situações".
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** escrever as páginas e o menu. Ajustar os testes da página inicial que conferem os selos.
- [ ] **Passo 4:** rodar a suíte inteira, `construir` e `zensical build --clean --strict`.
- [ ] **Passo 5:** commit sugerido: `feat(guia): visão geral e capítulo 1`.

### Tarefas 8 a 12: Capítulos de técnica

Uma tarefa por capítulo, nesta ordem, com os mesmos passos. As referências listadas são **de partida, a conferir**: quem executa busca cada uma, lê o resumo e acrescenta outras se o texto precisar.

| Tarefa | Arquivo (`conteudo/guia/`) | Capítulo | Referências de partida | Ligação obrigatória com o kit |
|---|---|---|---|---|
| 8 | `frases-chave.md` | 6. Frases-chave e blocos prontos | Boers et al. (2006), Language Teaching Research; Boers e Lindstromberg (2012), Annual Review of Applied Linguistics; Wood (2006) | As frases das situações 6, 7 e 8 |
| 9 | `shadowing.md` | 8. Shadowing | Hamada (2016), Language Teaching Research; Foote e McDonough (2017), Journal of Second Language Pronunciation; uma revisão ou metanálise recente, se houver | Os diálogos das situações. **Obrigatório:** dizer que a voz do kit é sintética e indicar fontes gratuitas de fala real para alternar (risco da seção 7 do desenho) |
| 10 | `fluencia.md` | 9. Fluência na fala: técnica 4/3/2, gravar a própria voz e cartas ao contrário | Nation (1989), System; De Jong e Perfetti (2011), Language Learning; Boers (2014), RELC Journal; Thai e Boers (2016), TESOL Quarterly; Webb (2009), RELC Journal (aprender de forma receptiva ou produtiva) | Ficha de progresso e treino de cartas. Um carimbo reto por técnica |
| 11 | `medo-de-falar.md` | 10. Medo de falar e confiança | Horwitz, Horwitz e Cope (1986), Modern Language Journal; Teimouri, Goetze e Plonsky (2019), Studies in Second Language Acquisition; MacIntyre et al. (1998), Modern Language Journal | Conversa real da trilha e ficha (confiança de 1 a 5) |
| 12 | `ia-modo-de-voz.md` | 11. Treinar com IA no modo de voz | Swain (1985), hipótese da produção; uma metanálise ou revisão de 2020 em diante sobre chatbots ou IA conversacional no aprendizado de segunda língua | Os roteiros de IA das situações 6, 7 e 8; aviso sobre dados pessoais |

**Arquivos (cada tarefa):** criar `conteudo/guia/<slug>.md`; acrescentar entradas em `docs/pesquisa/referencias.md`; modificar `scripts/guia.py` (`CAPITULOS`) e `zensical.toml` (menu, rótulo "N. Título"); testes em `tests/test_guia.py`.

- [ ] **Passo 1: teste que falha.** Acrescentar o slug a `CAPITULOS`. `test_guia_do_repositorio_sem_problemas` passa a falhar (capítulo listado sem arquivo). Acrescentar também `test_capitulo_<slug>_liga_o_kit`: o `.md` tem link para as páginas da coluna "Ligação obrigatória".
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3: pesquisa.** Ler o resumo de cada referência e registrar a entrada em `docs/pesquisa/referencias.md`. Referência cujo resumo não diz o que se esperava não entra, ou o texto muda.
- [ ] **Passo 4: selo.** Decidir o selo pelo critério e registrar no ledger: `Ruling: selo do capítulo N = <nível> — <estudos que pesam> — <custo se errado>`.
- [ ] **Passo 5: texto.** Escrever o capítulo na estrutura das Restrições gerais. "Como praticar" traz passos com tempo e links para o kit. "Armadilhas" traz de dois a quatro itens.
- [ ] **Passo 6:** rodar a suíte inteira, `construir` e `zensical build --clean --strict`.
- [ ] **Passo 7:** commit sugerido: `feat(guia): capítulo N, <título>`.

### Tarefa 13: Situação 7, conversar sobre programação, IA e frameworks

**Arquivos:**
- Criar: `kit/dados/situacao-07.csv` (ids `tecnologia-01` a `tecnologia-12`), `kit/dialogos/situacao-07.csv` (ids `tecnologia-d01` em diante), `conteudo/situacoes/tecnologia.md`
- Modificar: `zensical.toml` (menu, depois de "Telefonar e marcar reunião"), `conteudo/situacoes/index.md`
- Testes: `tests/test_site.py`

**Conteúdo:**
- **Frases:** de 10 a 12, cada uma com um termo que brasileiros costumam errar, com `silaba` na palavra difícil e `leitura` quando o fonema da voz não bate com o dicionário. Temas: explicar um bug, pedir revisão de código, falar de deploy, de banco de dados e do uso de IA no trabalho.
- **Diálogo:** duas pessoas desenvolvedoras numa chamada, revisando uma mudança e decidindo como usar uma ferramenta de IA. Pessoa A e pessoa B com nomes neutros, diferentes dos da situação 6.
- **Página, nesta ordem:**
  - Faixa "Situação 7 de 8 / Trabalho" e introdução;
  - "Frases" (`--8<-- "kit/gerado/frases-07.md"`) e "Diálogo" (`--8<-- "kit/gerado/dialogo-07.md"`);
  - **"Pronúncia dos termos":** tabela "Termo | Sílaba forte | Fonte" com pelo menos 10 termos (ponto de partida: cache, SQL, Nginx, GUI, JSON, PostgreSQL, regex, async, Kubernetes, Azure, Linux, schema). O termo vai em `<span lang="en">`, e a fonte é o link do Cambridge Dictionary ou da documentação oficial;
  - "Treinar": botão `../treinar.md?situacao=7` e link do baralho `…/releases/latest/download/ice-destravar-situacao-07.apkg`;
  - RoteiroIA em inglês: uma pessoa colega pergunta, numa daily, o que você está fazendo e por que escolheu uma ferramenta;
  - "Notas culturais": por exemplo LGTM, "nit:" na revisão, daily curta, "let me check and get back to you". Inglês com `lang="en"` e tradução.

- [ ] **Passo 1: teste que falha.** `test_situacao_7_publicada`:
  - `situacoes/tecnologia/index.html` existe;
  - tem 20 ou mais `class="pp-frase"` (frases e falas), `data-audio-sequencia` e `pp-roteiro`;
  - a tabela de pronúncia tem 10 ou mais linhas, cada uma com um link `https://`.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** escrever os CSVs.
- [ ] **Passo 4: conferir os fonemas.** Para cada frase e fala, imprimir `Tokenizer().phonemize(texto, "en-us")` (de `kokoro_onnx.tokenizer`) e comparar o termo com o IPA americano do Cambridge. Onde não bater, preencher `leitura`. Registrar no ledger a lista de termos com leitura.
- [ ] **Passo 5:** escrever a página e o menu. Rodar `construir` e a suíte inteira; o teste de `lang="en"` da 1A cobre as notas.
- [ ] **Passo 6:** `python -m scripts.construir --audio` (o modelo já está no cache) e conferir que o manifesto tem os ids novos.
- [ ] **Passo 7:** commit sugerido: `feat(kit): situação 7, programação, IA e frameworks`.

### Tarefa 14: Situação 8, entrevista de emprego para trabalho remoto

**Arquivos:**
- Criar: `kit/dados/situacao-08.csv` (`entrevista-01` a `entrevista-12`), `kit/dialogos/situacao-08.csv` (`entrevista-d01` em diante), `conteudo/situacoes/entrevista.md`
- Modificar: `zensical.toml`, `conteudo/situacoes/index.md`
- Testes: `tests/test_site.py`

**Conteúdo:**
- **Frases:**
  - apresentar-se em poucas frases;
  - contar uma experiência com resultado;
  - falar de fuso horário e de horas em comum com o time;
  - falar de comunicação assíncrona e de expectativa salarial (faixa anual em dólar);
  - pedir para repetir;
  - perguntar sobre o time no fim.
- **Diálogo:** entrevista curta para uma vaga remota, com recrutador e candidato; o candidato responde com fatos.
- **Página:** a mesma ordem da situação 7, sem a tabela de pronúncia.
  - Faixa "Situação 8 de 8 / Trabalho".
  - RoteiroIA em inglês: entrevista simulada para uma vaga remota de desenvolvimento, uma pergunta por vez e, no fim, até três sugestões.
  - Notas culturais: resposta curta para "Tell me about yourself", exemplos concretos (situação, ação e resultado), salário em faixa anual, perguntas no fim, e-mail de agradecimento. Inglês com `lang="en"` e tradução.
  - Nota visível: o treino é para dizer a sua experiência real com clareza.

- [ ] **Passo 1: teste que falha.** `test_situacao_8_publicada`: `situacoes/entrevista/index.html` existe, tem 18 ou mais `class="pp-frase"` (frases e falas), `data-audio-sequencia` e `pp-roteiro`.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** escrever os CSVs, conferir os fonemas como na Tarefa 13 (Passo 4), e escrever a página e o menu.
- [ ] **Passo 4:** rodar `construir --audio` e a suíte inteira.
- [ ] **Passo 5:** commit sugerido: `feat(kit): situação 8, entrevista para trabalho remoto`.

### Tarefa 15: Semanas 2 a 6 do plano

**Arquivos:**
- Modificar: `kit/planos/destravar.csv` (a semana 1 fica como está, porque há gente seguindo)
- Teste: `tests/test_planos.py`

**Foco de cada semana:**

| Semana | Foco | Situações | Leitura do guia (um passo de 5 min) |
|---|---|---|---|
| 2 | Frases e diálogo de tecnologia; shadowing | 7, revisão da 6 | Capítulos 1 e 8 |
| 3 | Pronúncia dos termos; 4/3/2 explicando um projeto | 7 | Capítulo 9 |
| 4 | Entrevista: apresentar-se e contar experiências | 8, revisão da 6 | Capítulo 6 |
| 5 | Entrevista: perguntas difíceis e salário; IA como entrevistadora | 8 | Capítulo 10 |
| 6 | Revisão das três; entrevista simulada completa; gravar a voz e comparar com a semana 1 | 6, 7 e 8 | Capítulo 11 |

- [ ] **Passo 1: teste que falha.** `test_semanas_1_a_6_do_destravar`, lendo o CSV do repositório com `dados_do_plano`:
  - semanas publicadas = {1, …, 6};
  - em cada semana, os dias de 1 a 6 têm passos e o dia 7 não;
  - exatamente um passo com "Conversa real" e um com "Gravar a sua voz" (link para a ficha);
  - pelo menos um com "4/3/2" e um com "Shadowing"; nas semanas 2 a 6, pelo menos dois com "Roteiro de IA" (a semana 1 tem um e fica como está);
  - todo `?situacao=` está em {6, 7, 8}, e todo link `situacoes/` aponta para `telefonar/`, `tecnologia/` ou `entrevista/`.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** escrever as semanas 2 a 6, com os textos dos passos no estilo da semana 1.
- [ ] **Passo 4:** rodar `construir`; o `validar_plano` confere links e minutos. Depois a suíte inteira.
- [ ] **Passo 5:** commit sugerido: `feat(kit): semanas 2 a 6 da trilha Destravar a fala`.

### Tarefa 16: Entrada do site, desenho e conferência final

**Arquivos:**
- Modificar:
  - `conteudo/index.md` (aviso "em construção" com o que está no ar; o guia citado em "O que é");
  - `conteudo/situacoes/index.md` e `conteudo/trilhas/index.md` (textos);
  - `conteudo/sobre.md` (M15: o capítulo de shadowing é quem indica a fala real, com link);
  - desenho: decisões da 1B nas seções 5.1, 5.2, 5.3 e na árvore da 5.4 (`docs/pesquisa/`, `scripts/guia.py`, coluna `leitura`, `situacoes.json`).
- Testes: `tests/test_site.py`

- [ ] **Passo 1: teste que falha.** `test_entrada_cita_o_que_esta_no_ar`: a página inicial tem link para `guia/`, e a de situações tem links para as três situações publicadas.
- [ ] **Passo 2:** rodar e ver falhar; escrever os textos; ver passar.
- [ ] **Passo 3:** rodar `python -m scripts.construir --audio --baralhos` → três `.apkg` em `dist/baralhos/`. Depois `zensical build --clean --strict` e a suíte inteira.
- [ ] **Passo 4: conferência no navegador** (servidor `ingles-site`, porta 8010):
  - todas as páginas novas a 320, 375 e 1280 px, nos dois temas: sem rolagem lateral e sem requisição externa;
  - os botões "Ouvir" habilitados;
  - o treino mostra os títulos e filtra `?situacao=7`;
  - "Hoje" com início 7 dias atrás mostra a semana 2;
  - "Hoje" com início 42 dias atrás mostra a mensagem da Tarefa 5.
- [ ] **Passo 5:** commit sugerido: `docs: entrada do site e desenho com a Fase 1B`.
- [ ] **Passo 6 (mantenedor):**
  - revisar o inglês das situações 7 e 8 (por falante nativo, se possível) e ouvir os áudios novos;
  - commit e push; depois a tag `v0.2.0`;
  - validar no celular.
