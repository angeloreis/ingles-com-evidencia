# Fase 2A (viagem): plano de implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: use superpowers:subagent-driven-development (recomendada) ou superpowers:executing-plans para executar este plano tarefa por tarefa. Os passos usam caixas (`- [ ]`) para acompanhamento.

**Objetivo:** completar as oito situações e as doze semanas:
- situações 1 a 5 (imigração, restaurante, táxi ou carro de aplicativo, polícia, puxar conversa), com frases, diálogo, áudio, cartas, roteiro de IA e notas culturais;
- semanas 7 a 12 da trilha "Destravar a fala";
- as pendências que o mantenedor escolheu para a 2A:
  - acessibilidade da página "Hoje" e do treino;
  - robustez do build e da publicação;
  - ajustes de texto da 1B;
- a Release `v0.3.0` com os oito baralhos.

**Arquitetura:** o motor da 1A e da 1B não muda de forma. Os CSVs de `kit/` continuam sendo a fonte, e as páginas escritas à mão incluem os trechos gerados. Entram três peças novas:
- o crédito das frases do Tatoeba na página, na carta e em `CREDITOS.md`;
- `scripts/tatoeba.py`, que confere cada frase `tatoeba:<n>` dos CSVs na API pública do Tatoeba. Roda à mão, fora do build e da Action, porque o build não pode depender da rede;
- a conferência de `?situacao=` e de `#âncora` nos links do plano.

**Tecnologias:** as mesmas da 1B (Python 3.12, Zensical 0.1.1, kokoro-onnx 0.6.1, genanki 0.13.1, mini-racer nos testes). Nenhuma dependência nova. As transitivas passam a ter versão fixa num arquivo de restrições (Tarefa 1).

**Desenho:** `docs/superpowers/specs/2026-11-12-ingles-com-evidencia-design.md` (seções 5.2, 5.3 e 5.5; a decisão do Tatoeba está em 5.2 "Dados"). Plano anterior: `docs/superpowers/plans/2026-11-13-fase-1b-conteudo.md`. Pendências na memória do projeto: M2 a M6, M10, M12 e M13 da 1A e os menores da 1B.

**Pronto quando:** no site publicado, pelo celular:
- as oito situações têm frases e diálogo com áudio e treino de cartas;
- "Hoje" e a lista de semanas trazem as semanas 1 a 12;
- depois da semana 12, "Hoje" mostra o fim do plano com saídas;
- a Release `v0.3.0` traz os oito baralhos.

O mantenedor valida no celular: segue um dia de uma semana de viagem (7 a 11), ouve os áudios novos e usa "Hoje" só pelo teclado ou pelo leitor de tela.

## Restrições gerais

- Todas as da 1B continuam valendo:
  - pt-BR, e toda frase em inglês com tradução e com `lang="en"` no HTML;
  - texto com 17 px ou mais (a tradução e a sílaba seguem menores, por decisão do mantenedor), toque com 48 px ou mais, sem rolagem lateral;
  - contraste AA nos dois temas;
  - nada de terceiros nem rastreadores;
  - nenhum dado pessoal no repositório (`test_repositorio_sem_dados_pessoais`);
  - nenhum caminho começando com `/`;
  - progresso só no `localStorage`, dentro de `try/catch`;
  - vozes `af_heart` (frases e pessoa A) e `am_michael` (pessoa B), velocidade 0.9, arquivos `ice-<id>.mp3`;
  - trilha `destravar` com de 20 a 30 minutos por dia com passos; dia sem passos é descanso.
- **Frases do Tatoeba** (desenho 5.2, decidido na 2A):
  - nas situações de viagem, a frase vem do Tatoeba quando existe uma que sirva, lida frase a frase na API pública, sem baixar o arquivo completo;
  - `fonte` `tatoeba:<id>`, a licença e o autor; o que não existir lá, o projeto escreve (`projeto`, CC BY-SA 4.0).
  - Regras de escolha, decididas neste plano:
    - o `en` é idêntico ao texto do Tatoeba; quem quiser outra redação escreve a frase como `projeto`;
    - só frase aprovada (`is_unapproved` falso) e com dono (`owner` preenchido); o dono vai na coluna `autor`;
    - licença `CC BY 2.0 FR` ou `CC0 1.0`, gravada como `CC0` no CSV;
    - inglês dos Estados Unidos e do Canadá;
    - o `pt` é sempre do projeto, em português do Brasil. As traduções do Tatoeba não entram: muitas são de Portugal, e cada uma teria outro autor e outra licença.
- **Imigração e polícia (desenho 5.2), copiado do desenho:**
  - "o comportamento recomendado (por exemplo, mãos no volante numa abordagem) vem **só de fonte oficial** (manuais de trânsito dos estados ou províncias, sites do CBP e da CBSA), com o link";
  - "A página avisa que o material treina o idioma e **não é orientação jurídica nem migratória**";
  - "Na imigração, o treino é responder **com clareza e com a verdade**. O kit não ensina o que dizer sobre planos de imigração."
  - Desta fase:
    - recomendação de segurança também só com fonte oficial, e só nas situações 1 e 4;
    - nas outras situações, as notas culturais tratam de idioma e costume;
    - o kit não ensina táticas jurídicas (direitos, recusar revista, pedir advogado);
    - número que precise de fonte (porcentagem de gorjeta, multa, prazo) não entra sem a fonte.
- **Fontes oficiais de partida**, todas abertas em 13/11/2026 (quem executa lê cada página antes de citar):
  - CBP:
    - <https://www.cbp.gov/travel/international-visitors/know-before-you-visit>
    - <https://www.cbp.gov/travel/international-visitors/applying-admission-united-states>
    - <https://www.cbp.gov/travel/international-visitors/agricultural-items>
    - O site do CBP recusa leitura por `curl` (403). Leia pelo navegador do app.
  - CBSA: <https://www.cbsa-asfc.gc.ca/travel-voyage/ivc-rnc-eng.html>
  - Manual de trânsito da Califórnia, seção "Law Enforcement Stops": <https://www.dmv.ca.gov/portal/handbook/california-driver-handbook/navigating-the-roads-cont1/>
  - Manual de trânsito de Ontário, "Emergency vehicles" e a parada pedida pela polícia: <https://www.ontario.ca/document/official-mto-drivers-handbook/dealing-particular-situations>
  - 911 nos Estados Unidos: <https://www.911.gov/>
  - A página do CRTC sobre o 911 no Canadá pede verificação humana. Não contornar: procure outra página oficial do governo canadense, e, se nenhuma abrir, a página cita só a fonte americana.
- **Roteiros de IA:**
  - em inglês, sem nome de produto de IA;
  - aviso para não colar nem dizer na conversa nome completo, número de passaporte ou de documento, endereço, placa ou dados de cartão;
  - na imigração e na polícia, o roteiro pede à IA que, no fim, aponte só frases menos claras, nunca o que responder.
- **Frases e falas:**
  - de 8 a 12 frases por situação e de 10 a 14 falas por diálogo;
  - sílaba forte na palavra difícil;
  - `leitura` quando o fonema da voz não bate com o IPA americano do Oxford Learner's Dictionaries (o Cambridge pede verificação humana);
  - nomes neutros nos diálogos, diferentes dos já usados (Alex, Sam, Jordan, Riley, Morgan, Ariel); agente e policial sem nome;
  - o mantenedor revisa o inglês antes da tag.
- **Downloads:**
  - nenhum previsto;
  - ler páginas e o JSON da API para a pesquisa pode;
  - baixar PDF, a exportação do Tatoeba ou qualquer arquivo pede OK do mantenedor;
  - página com CAPTCHA ou verificação humana não se contorna.
- **Git é do mantenedor:** cada tarefa sugere um commit, sem `Co-Authored-By`. Quem executa não roda git que muda estado.

## Pontos de atenção na revisão

1. **Frase do Tatoeba com texto, licença ou autor diferente da origem:**
   - casos: erro de digitação, frase editada depois, `CC0 1.0` gravado como veio, frase sem dono;
   - o crédito sai errado, e a licença do projeto fica comprometida.
   - *Testes de `conferir_linhas` e do autor obrigatório na Tarefa 4; `python -m scripts.tatoeba` em cada situação (Tarefas 6 a 10) e na Tarefa 12.*
2. **Pessoa que passa da semana 12** (dia 85 em diante): com o plano completo, o aviso de "semanas não publicadas" some. "Hoje" mostra o fim do plano com o que fazer, e não uma frase sem saída.
   - *Teste de `depoisDoPublicado` na Tarefa 2; conferência no navegador na Tarefa 12.*
3. **Quem usa teclado ou leitor de tela:**
   - depois de "Começar hoje", de marcar um passo ou de "Acertei" e "Errei", o foco não cai no `body`;
   - o leitor ouve o resultado (passo marcado, dia concluído).
   - *Testes de `resumoDoDia` e `proximoAberto` na Tarefa 2; `document.activeElement` conferido no navegador nas Tarefas 2 e 12.*
4. **Link do plano para uma âncora que não existe, ou `?situacao=` de uma situação sem cartas:** as semanas 7 a 12 trazem dezenas de links novos, e o `construir` acusa.
   - *Testes de `validar_plano` e `ancoras` na Tarefa 5, mais o teste das semanas na Tarefa 11.*
5. **Rodar de novo a publicação ou a tag:**
   - o job da Release não falha na segunda vez;
   - o cache do áudio volta, e só as frases que mudaram são sintetizadas.
   - *Testes da Action na Tarefa 1.*

## Mapa dos arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `scripts/construir.py`, `scripts/audio.py`, `.github/workflows/site.yml`, `requirements-travado.txt` | Build que só confere com dados de fora, tempo limite no download, caches, Release repetível, versões travadas (M2, M12, M13) | 1 |
| `conteudo/js/logica/plano.js`, `conteudo/js/paginas/{hoje,treino}.js`, `conteudo/estilos/ponte.css` | Acessibilidade e mensagens de "Hoje" e do treino (M3, M4, M5, M6, M10) e fim do plano | 2 |
| `kit/dados/situacao-07.csv`, `conteudo/situacoes/tecnologia.md`, `conteudo/guia/*.md`, desenho | Ajustes de texto da 1B | 3 |
| `scripts/{validar,paginas,baralhos,creditos,tatoeba}.py`, `conteudo/estilos/ponte.css`, README do Frase | Crédito e conferência das frases do Tatoeba | 4 |
| `scripts/planos.py`, `scripts/construir.py` | `?situacao=` e âncoras nos links do plano | 5 |
| `kit/dados/situacao-0{1..5}.csv`, `kit/dialogos/situacao-0{1..5}.csv`, `conteudo/situacoes/{imigracao,restaurante,taxi,policia,conversa}.md`, `zensical.toml`, `conteudo/situacoes/index.md` | Situações 1 a 5 | 6 a 10 |
| `kit/planos/destravar.csv` | Semanas 7 a 12 e gravação comparável | 11 |
| `conteudo/{index,sobre}.md`, `conteudo/trilhas/index.md`, `conteudo/guia/{frases-chave,ia-modo-de-voz}.md`, desenho | Textos de entrada e fechamento | 12 |

**Fora desta fase:**
- Fase 2B:
  - capítulos 2, 3, 4, 5, 7, 12 e 13;
  - `guia.py` pronto para eles: sobrenome composto sem partícula (Montero Perez), carimbo × texto, Armadilhas, Faixa, linha do erro, título malformado do registro;
  - trocar os passos de leitura das semanas 7 a 12 por capítulos novos onde couber.
- Da 1A: M14 (tabela da ficha com 7 colunas).
- Da 1B:
  - testes de CSS que conferem texto e não cascata;
  - `objeto()` repetido em três scripts;
  - "Repetir a semana N" sem função pura: deixa de aparecer com as 12 semanas publicadas;
  - as duas decisões do mantenedor (tamanho da tradução e da sílaba; roteiros sem resumo em português).
- Pendências da Fase 0 que não são do build.

---

### Tarefa 1: Robustez do build e da publicação (M2, M12, M13)

**Arquivos:**
- Modificar: `scripts/construir.py`, `scripts/audio.py` (`baixar_modelos`), `.github/workflows/site.yml`, `README.md` (uso do `construir`)
- Criar: `requirements-travado.txt`, `tests/test_publicacao.py`
- Testes: `tests/test_construir.py`, `tests/test_audio.py`, `tests/test_publicacao.py`

**Interfaces:**
- `construir`: a raiz do projeto é `args.conteudo.parent`.
  - `--dados`, `--dialogos` e `--planos` passam a ter padrão `None` e, sem eles, valem `<raiz>/kit/dados`, `<raiz>/kit/dialogos` e `<raiz>/kit/planos`.
  - Se algum deles aponta para fora desses três caminhos (comparando com `resolve()`), o `construir` só confere e não grava nada:
    - nada de dados do plano, trechos, créditos, áudio ou baralhos;
    - termina com `Só conferência: os dados vêm de fora de <raiz>/kit, então nada foi gerado.` e código 0, ou 1 se houver erro.
  - `--audio` ou `--baralhos` com dados de fora: `parser.error("--audio e --baralhos geram arquivos e precisam dos dados do próprio projeto, sem --dados, --dialogos ou --planos de fora")`.
- `scripts/audio.py`: `TEMPO_LIMITE = 60`, e `urllib.request.urlopen(a["url"], timeout=TEMPO_LIMITE)`.
- `requirements-travado.txt`:
  - saída de `.venv/bin/python -m pip freeze --exclude-editable`, em ordem alfabética, sem as linhas com ` @ ` (instalação local, que levaria o caminho da máquina);
  - na primeira linha, o comentário `# Versões de todas as dependências, do pip freeze do ambiente do projeto em AAAA-MM-DD. Refaça ao mudar um requirements-*.txt.`
- `site.yml`:
  - todo `pip install` ganha `-c requirements-travado.txt`;
  - a chave do cache do Kokoro passa a ser `kokoro-v1.0-<MODELO["sha256"]>-<VOZES["sha256"]>`;
  - os jobs `publicar` e `baralhos` ganham, antes do `construir --audio`, um `actions/cache@v5`:
    - `path: conteudo/audio`;
    - `key: audio-${{ hashFiles('kit/dados/*.csv', 'kit/dialogos/*.csv', 'scripts/audio.py', 'requirements-travado.txt') }}`;
    - `restore-keys: audio-`;
    - o `gerar_audios` já pula o que não mudou e apaga os órfãos;
  - o passo da Release vira:

```bash
if gh release view "$GITHUB_REF_NAME" >/dev/null 2>&1; then
  gh release upload "$GITHUB_REF_NAME" dist/baralhos/*.apkg --clobber
else
  gh release create "$GITHUB_REF_NAME" dist/baralhos/*.apkg --title "Baralhos $GITHUB_REF_NAME" --generate-notes
fi
```

- [ ] **Passo 1: testes que falham**
  - `test_dados_de_fora_so_conferem`:
    - projeto em `tmp_path` (`kit/dados` com um CSV válido e `conteudo/treinar.md`), mais um CSV válido em `tmp_path/fora`;
    - `main(["--conteudo", tmp/conteudo, "--dados", tmp/fora])` devolve 0;
    - a saída tem "Só conferência", e `tmp/kit/gerado` e `tmp/CREDITOS.md` não existem.
  - `test_dados_de_fora_com_audio_e_erro`: o mesmo com `--audio` → `SystemExit`, com a mensagem acima.
  - `test_outra_raiz_le_o_proprio_kit`: o projeto de `tmp_path` sem `--dados` → 0, e `tmp/kit/gerado/frases-06.md` e `tmp/CREDITOS.md` existem.
  - Ajustar `test_plano_valido_grava_os_dados` e os outros testes de `test_construir.py` que passam `--dados` e esperam arquivos gravados, para montarem o projeto em `tmp_path`.
  - `test_construir_acusa_capitulo_com_problema` (`test_guia.py`) continua passando sem mudança: a pasta de dados ausente em `tmp_path/kit/dados` vira mais um erro, e o do capítulo segue na saída.
  - `test_baixar_usa_tempo_limite`:
    - `monkeypatch` de `urllib.request.urlopen` por uma função que guarda o `timeout` e devolve um `io.BytesIO(b"x")` como gerenciador de contexto;
    - `baixar_modelos(tmp_path, ({"arquivo": "m", "url": "https://exemplo", "sha256": sha256(b"x")},))` → `timeout == 60`.
  - Em `tests/test_publicacao.py`, lendo `site.yml` como texto:
    - `test_pip_com_versoes_travadas`: toda linha com `pip install` tem `-c requirements-travado.txt`;
    - `test_requisitos_dentro_das_restricoes`: cada `nome==versão` de `requirements-{site,kit,dev}.txt` aparece igual em `requirements-travado.txt`, e nenhuma linha dele tem ` @ `;
    - `test_cache_do_kokoro_com_os_dois_arquivos`: a chave tem `MODELO["sha256"]` e `VOZES["sha256"]` (importados de `scripts.audio`);
    - `test_cache_do_audio_nos_dois_jobs`: `path: conteudo/audio` aparece duas vezes, com `restore-keys: audio-`;
    - `test_release_pode_rodar_de_novo`: o texto tem `gh release upload` com `--clobber` e `gh release view`.
- [ ] **Passo 2:** `.venv/bin/python -m pytest -q tests/test_construir.py tests/test_audio.py tests/test_publicacao.py` → os novos falham.
- [ ] **Passo 3:** implementar. Gerar `requirements-travado.txt` com o comando acima e conferir à mão que nenhuma linha tem caminho de máquina. Atualizar a seção de uso do README.
- [ ] **Passo 4:** a suíte inteira passa, e `python -m scripts.construir` diz "Tudo certo".
- [ ] **Passo 5:** commit sugerido: `build: construir só confere com dados de fora, caches do áudio e do modelo, Release repetível e versões travadas`.

### Tarefa 2: "Hoje" e treino com teclado e leitor de tela (M3, M4, M5, M6, M10) e fim do plano

**Arquivos:**
- Modificar: `conteudo/js/logica/plano.js`, `conteudo/js/paginas/hoje.js`, `conteudo/js/paginas/treino.js`, `conteudo/estilos/ponte.css`, `design/passaporte/components/PassosDoDia/README.md`
- Testes: `tests/test_js_plano.py`, `tests/test_site.py`

**Interfaces (lógica pura, `ICE.plano`):**
- `ler(texto)` também devolve o estado vazio quando `inicio` não é `null` nem uma data `AAAA-MM-DD` de verdade. Valer quer dizer casar com `/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/` e `ICE.datas.somarDias(inicio, 0) === inicio`.
- `proximoAberto(passos, feitos) -> number | null`: a `ordem` do primeiro passo, por ordem, que não está em `feitos`. Devolve `null` quando todos estão marcados.
- `resumoDoDia(passos, feitos) -> string`:
  - `"{k} de {n} passos feitos."`;
  - com todos marcados, `"Dia concluído: todos os passos de hoje estão feitos."`.
- `mensagemDeFalha(erro) -> string`:
  - erro com `message === "HTTP 404"` → `"O plano desta trilha ainda não foi publicado."`;
  - qualquer outro → `"Não foi possível carregar o plano. Confira a conexão e recarregue a página."` (M6).

**Página "Hoje":**
- **Primeira visita (M3):** o seletor fica num `div.ice-treino__filtro` com `<label for="ice-hoje-semana">Já estou na semana</label>`, o `<select id="ice-hoje-semana">` e o botão "Continuar dessa semana" fora do `label`.
- **Passo com link (M5):**
  - o `label` leva só o texto e o tempo, então tocar no texto marca a caixa;
  - o link vem depois do `label`: `<a class="pp-passos__abrir" href="…" aria-label="Abrir: {passo}">Abrir</a>`;
  - em `ponte.css`, `.pp-passos__abrir` tem `min-height: var(--alvo-toque)` e `display: inline-flex`, e a 320 px não cria rolagem lateral;
  - o README do PassosDoDia mostra o link.
- **Status (M10):**
  - um `<p class="ice-hoje__status" role="status">` abaixo da lista, atualizado com `resumoDoDia` a cada marcação;
  - "Marcar o próximo passo" fica `disabled` quando `proximoAberto` é `null`.
- **Foco (M4 e herdado da 1B):**
  - todo estado desenhado começa por um elemento com `tabindex="-1"` e a classe `ice-hoje__inicio`: o `h2` "Semana N, dia D", ou o primeiro parágrafo nos outros estados;
  - depois de uma ação da pessoa ("Começar hoje", "Continuar dessa semana", "Recomeçar o plano", "Repetir a semana"), `desenhar` foca esse elemento;
  - na abertura da página, nada recebe foco.
- **Falha ao carregar:** usa `mensagemDeFalha`.
- **Fim do plano:**
  - quando `pos.terminou` e não `depoisDoPublicado`, a página mostra: "Você chegou ao fim das {semanas} semanas. Para manter a fala em dia, siga no treino de cartas, faça uma conversa real por semana e grave a sua voz de vez em quando para comparar com a da semana 1.";
  - o botão-link primário "Treinar as cartas" (`treinar/`) e o link "Abrir a ficha de progresso" (`trilhas/<trilha>/ficha/`);
  - o "Recomeçar o plano" do rodapé continua.

**Treino (M4):**
- depois de "Acertei" ou "Errei", o foco vai para o "Mostrar a resposta" da carta seguinte;
- no fim, vai para a mensagem final, que ganha `tabindex="-1"`;
- na abertura e na troca do filtro, nada é focado.

- [ ] **Passo 1: testes que falham**, em `tests/test_js_plano.py`:
  - `test_ler_plano_com_inicio_invalido`: `"13/11/2026"`, `"2026-02-30"` e `20261113` → `{"versao": 1, "inicio": None, "feitos": {}}`; `"2026-11-13"` fica.
  - `test_proximo_aberto`: os passos de ordem 1, 2 e 3 com `feitos` `[]`, `[1]`, `[2]` e `[1, 2, 3]` → `1`, `2`, `1` e `None`.
  - `test_resumo_do_dia`: `[]` → `"0 de 3 passos feitos."`; `[1, 3]` → `"2 de 3 passos feitos."`; `[1, 2, 3]` → o texto de dia concluído.
  - `test_mensagem_de_falha`: `avaliar(ctx, 'ICE.plano.mensagemDeFalha(new Error("HTTP 404"))')` e o mesmo com `new TypeError("Failed to fetch")` dão as duas mensagens (o `chamar` passa os argumentos por JSON, que não leva um `Error`).
  - `test_depois_do_publicado_com_o_plano_completo`: um plano com passos na semana 12 → `depoisDoPublicado(plano, 13)` é falso.
  - Em `tests/test_site.py`, `test_link_do_passo_com_area_de_toque`: `ponte.css` tem a regra `.pp-passos__abrir` com `min-height: var(--alvo-toque)`.
- [ ] **Passo 2:** rodar e ver falhar (o de `depoisDoPublicado` já passa: ele protege o fim do plano contra mudança futura).
- [ ] **Passo 3:** implementar a lógica e as páginas.
- [ ] **Passo 4:** a suíte inteira passa. Rodar `construir`.
- [ ] **Passo 5: conferência no navegador** (servidor `ingles-site`, porta 8010):
  - em "Hoje" com o armazenamento limpo, Tab até "Começar hoje" e Enter → `document.activeElement` é o `h2` "Semana 1, dia N";
  - tocar no texto de um passo marca a caixa, e o status diz "1 de N passos feitos.";
  - "Abrir" navega;
  - com todos marcados, o botão fica desabilitado e o status diz o texto de dia concluído;
  - com `inicio` 84 dias atrás, aparece o fim do plano (enquanto as semanas 7 a 12 não saem, a mensagem continua a da 1B);
  - no treino, depois de "Acertei", `document.activeElement` é "Mostrar a resposta";
  - a 320 px, sem rolagem lateral.
- [ ] **Passo 6:** commit sugerido: `fix(site): Hoje e treino com foco, status e rótulos acessíveis, falha de rede e fim do plano`.

### Tarefa 3: Ajustes de texto da 1B

**Arquivos:**
- Modificar:
  - `kit/dados/situacao-07.csv`;
  - `conteudo/situacoes/tecnologia.md`;
  - `conteudo/guia/{ia-modo-de-voz,fluencia,frases-chave,shadowing,medo-de-falar}.md`;
  - desenho, seção 5.2, nota da situação 7.
- Testes: `tests/test_audio.py`, `tests/test_site.py`, `tests/test_guia.py`

**Mudanças:**
- `tecnologia-04` ganha a leitura `This queery is slow because the table has no index.`, já conferida na 1B contra o IPA americano do Oxford.
- Tabela "Pronúncia dos termos":
  - sai a linha do Linux, que tem duas pronúncias americanas, como o router e o GUI;
  - o texto acima da tabela diz que termos com duas pronúncias americanas ficaram de fora.
- Desenho, 5.2:
  - os exemplos da nota passam a ser "cache, deploy, query, Nginx, entre outros";
  - o fim diz "o que tem duas pronúncias americanas (router, GUI e Linux)".
- Capítulo 11, "O que a pesquisa diz": a frase "Uma IA que conversa por voz dá muitas chances de tropeçar e refazer, a qualquer hora." vira "Daqui o guia tira uma conclusão própria, que os estudos não testaram: uma IA que conversa por voz dá muitas chances de tropeçar e refazer, a qualquer hora."
- Capítulo 9: "há estudos controlados a favor da fluência" vira "há estudos comparativos a favor da fluência".
- Passos sem tempo em "Como praticar":
  - frases-chave 4 vira "**Uma vez por semana, numa conversa real (20 minutos).**";
  - fluencia 2 vira "**Ajuste antes de acelerar (5 minutos).**";
  - ia-modo-de-voz 4 vira "**Use a IA nos dias sem conversa real (15 minutos).**".
- "O que os cursos dizem", nos capítulos 6, 8, 9, 10 e 11:
  - a promessa deixa de vir entre aspas, que pareciam citação literal, e passa a ser dita como paráfrase, por exemplo "A promessa é que, decorando algumas centenas de frases prontas, você vai falar com desenvoltura…";
  - o sentido não muda.

- [ ] **Passo 1: testes que falham**
  - `test_leitura_segue_o_dicionario` ganha o caso `("dados/situacao-07.csv", "tecnologia-04", "queery")`.
  - `test_situacao_7_publicada` ganha `assert "linux" not in tabela.lower()`.
  - Em `tests/test_guia.py`:
    - `test_trecho_corrigido_na_revisao_final` ganha `("fluencia", "estudos controlados")` e `("ia-modo-de-voz", "Uma IA que conversa por voz dá muitas")`;
    - `test_inferencia_do_guia_marcada`: a seção "O que a pesquisa diz" do capítulo 11 tem "conclusão própria, que os estudos não testaram";
    - `test_passos_de_como_praticar_com_tempo`: em todo capítulo de `CAPITULOS` com "Como praticar", cada item `^[0-9]+\. \*\*(.+?)\*\*` tem `\([0-9]+ minutos?` dentro do negrito;
    - `test_cursos_dizem_sem_aspas`: sem as tags HTML, o texto da seção "O que os cursos dizem" de cada capítulo não tem `"`, `“` nem `”`.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** fazer as mudanças. Conferir com `Tokenizer().phonemize(texto, "en-us")` que a leitura de `tecnologia-04` sai com a vogal de "queery".
- [ ] **Passo 4:** rodar `construir`, `zensical build --clean --strict` e a suíte inteira.
- [ ] **Passo 5:** commit sugerido: `fix(guia,kit): ajustes de texto da revisão da 1B`.

### Tarefa 4: Crédito e conferência das frases do Tatoeba

**Arquivos:**
- Modificar:
  - `scripts/validar.py` (`_conferir_linha`), `scripts/paginas.py` (`_frase_li`), `scripts/baralhos.py` (`_credito`), `scripts/creditos.py` (`gerar_creditos`);
  - `conteudo/estilos/ponte.css`, `design/passaporte/components/Frase/README.md`.
- Criar: `scripts/tatoeba.py`, `tests/test_tatoeba.py`
- Testes: `tests/test_validar.py`, `tests/test_paginas.py`, `tests/test_baralhos.py`, `tests/test_creditos.py`

**Interfaces:**
- `validar.py`: linha com `fonte` `tatoeba:<n>` e `autor` vazio, qualquer que seja a licença, é erro: `"frase do Tatoeba precisa do autor na coluna autor (o usuário dono da frase no Tatoeba)"`.
- `paginas._frase_li`: em linha do Tatoeba, depois da sílaba e antes do botão:
  - CC BY 2.0 FR: `<p class="pp-frase__fonte">Frase do <a href="https://tatoeba.org/pt-br/sentences/show/{n}">Tatoeba nº {n}</a>, de {autor}, sob CC BY 2.0 FR. Tradução do projeto.</p>`;
  - CC0: termina em `, de {autor}, em domínio público (CC0). Tradução do projeto.`;
  - autor escapado com `_e`;
  - vale para frases e falas, porque o diálogo usa o mesmo `_frase_li`.
- `baralhos._credito`: em linha do Tatoeba, `"Tatoeba nº {n}, de {autor}, {licenca}. Tradução do projeto."`; as outras linhas ficam como estão.
- `creditos.gerar_creditos`: logo abaixo de `### Frases do Tatoeba`, o parágrafo "O texto em inglês destas frases vem do [Tatoeba](https://tatoeba.org/pt-br/), sob [CC BY 2.0 FR](https://creativecommons.org/licenses/by/2.0/fr/) ou CC0, como indicado em cada uma. A tradução para o português é do projeto, sob CC BY-SA 4.0."
- `.pp-frase__fonte` em `ponte.css`: `font-size: var(--apoio-tamanho)` e `color: var(--tinta-suave)`, o mesmo tamanho da tradução.
- `scripts/tatoeba.py`:
  - `API = "https://api.tatoeba.org/unstable/sentences/"` e `TEMPO_LIMITE = 20`;
  - `LICENCAS = {"CC BY 2.0 FR": "CC BY 2.0 FR", "CC0 1.0": "CC0"}`, a licença da API e como ela fica no CSV;
  - `buscar_frase(numero: int) -> dict | None`:
    - GET em `API + str(numero)`, com `timeout=TEMPO_LIMITE` e `User-Agent: ingles-com-evidencia (conferencia de frases)`;
    - devolve o `data` da resposta, ou `None` no 404.
  - `conferir_linhas(linhas: list[dict], buscar: Callable[[int], dict | None]) -> list[str]`: para cada linha `tatoeba:<n>`, uma mensagem `"{id}: …"` por problema:
    - `não existe mais no Tatoeba`;
    - `texto diferente do Tatoeba ("{csv}" × "{tatoeba}")`;
    - `licença diferente (CSV {x}, Tatoeba {y})`, com a de cima já convertida pelo `LICENCAS`;
    - `autor diferente (CSV {x}, Tatoeba {y})`;
    - `frase ainda não aprovada no Tatoeba`;
    - `frase sem dono no Tatoeba`.
  - `main(argv: list[str] | None = None) -> int`:
    - lê `kit/dados` e `kit/dialogos` com `_ler_csvs` e confere com `buscar_frase`;
    - imprime os problemas e devolve 1, ou imprime `Frases do Tatoeba conferidas: {N}.` e devolve 0;
    - não entra no `construir` nem na Action.

- [ ] **Passo 1: testes que falham**
  - `test_tatoeba_exige_autor`: linha `tatoeba:21098`, `CC0`, autor vazio → erro com "autor".
  - `test_frase_do_tatoeba_traz_o_credito`: uma linha CC BY 2.0 FR com autor `CK` e uma CC0 com autor `a<b`:
    - o HTML tem o link `https://tatoeba.org/pt-br/sentences/show/21098`, "de CK", "Tradução do projeto." e `a&lt;b`;
    - uma linha `projeto` não tem `pp-frase__fonte`.
  - `test_credito_da_carta_do_tatoeba`: `_credito(linha)` == `"Tatoeba nº 21098, de CK, CC BY 2.0 FR. Tradução do projeto."`.
  - `test_creditos_explicam_a_traducao`: com uma linha do Tatoeba em `tmp_path/kit/dados`, o texto tem "A tradução para o português é do projeto" e o link da licença.
  - Em `tests/test_tatoeba.py`, com um `buscar` falso que devolve dicionários no formato da API (`{"id": 21098, "text": "Check, please.", "license": "CC BY 2.0 FR", "owner": "CK", "is_unapproved": False}`):
    - `test_frase_igual_sem_problemas`;
    - `test_cc0_da_api_bate_com_cc0_do_csv`;
    - `test_texto_diferente`;
    - `test_autor_diferente`;
    - `test_frase_que_sumiu` (o falso devolve `None`);
    - `test_frase_nao_aprovada`;
    - `test_frase_sem_dono`;
    - `test_linha_do_projeto_nao_e_buscada` (o falso falha se for chamado).
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** implementar. Atualizar o README do Frase com a linha da fonte.
- [ ] **Passo 4:** a suíte inteira passa. `python -m scripts.tatoeba` diz `Frases do Tatoeba conferidas: 0.`.
- [ ] **Passo 5:** commit sugerido: `feat(kit): crédito e conferência das frases do Tatoeba`.

### Tarefa 5: `?situacao=` e âncoras nos links do plano

**Arquivos:**
- Modificar: `scripts/planos.py` (`validar_plano`), `scripts/construir.py`
- Teste: `tests/test_planos.py`

**Interfaces:**
- `ancoras(pagina: Path) -> set[str]`:
  - as âncoras dos títulos (`^#{1,6} `) de uma página `.md`;
  - o slug segue o padrão do Python-Markdown:
    - tirar as tags HTML e os sinais `*` e `` ` ``;
    - `unicodedata.normalize("NFKD", …)` com `encode("ascii", "ignore")`;
    - tirar o que não é `[\w\s-]`, `strip()` e `lower()`;
    - trocar `[-\s]+` por `-`.
- `validar_plano(caminho, trilha, raiz_conteudo, situacoes: set[int] | None = None)`:
  - link com `?situacao=N` fora de `situacoes`, quando o conjunto vem: `"o link pede a situação N, que não tem cartas"`;
  - link com `#trecho` que não está em `ancoras` da página de destino: `"a página {caminho} não tem o trecho #{trecho}"`. A página de destino é a mesma que `_link_existe` encontra (`<caminho>.md` ou `<caminho>/index.md`);
  - link sem `#` ou para `treinar/` não muda.
- `construir` passa `situacoes`: os números da coluna `situacao` dos CSVs de baralho, depois da validação.

- [ ] **Passo 1: testes que falham**
  - `test_link_com_situacao_sem_cartas`: `treinar/?situacao=3` com `situacoes={6}` → erro com "situação 3".
  - `test_link_com_ancora_que_nao_existe`: `situacoes/telefonar/#nada` → erro com "#nada". A página do fixture ganha `## Diálogo`.
  - `test_link_com_ancora_que_existe`: `situacoes/telefonar/#dialogo` → sem erro.
  - `test_ancoras_das_paginas_do_repositorio`: `ancoras(RAIZ / "conteudo/situacoes/tecnologia.md")` contém `{"frases", "dialogo", "pronuncia-dos-termos", "treinar", "treinar-com-ia-no-modo-de-voz", "notas-culturais"}`.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** implementar.
- [ ] **Passo 4:** a suíte inteira passa, e `construir` diz "Tudo certo" com o plano atual (semanas 1 a 6).
- [ ] **Passo 5:** commit sugerido: `feat(kit): plano confere a situação e o trecho de cada link`.

### Tarefas 6 a 10: Situações 1 a 5

Uma tarefa por situação, nesta ordem, com os mesmos passos e a mesma página.

**Arquivos (cada tarefa):**
- Criar:
  - `kit/dados/situacao-0N.csv` (ids `<slug>-01` a `<slug>-12`);
  - `kit/dialogos/situacao-0N.csv` (`<slug>-d01` em diante);
  - `conteudo/situacoes/<slug>.md`.
- Modificar:
  - `zensical.toml`: o menu "Situações" fica em ordem numérica, 1 a 8, depois de "Visão geral";
  - `conteudo/situacoes/index.md`: o item da situação vira link, e o grupo "Viagem" passa a vir antes de "Trabalho".
- Testes: `tests/test_site.py`, `tests/test_validar.py`

**Página, nesta ordem:**
- Faixa "Situação N de 8 / Viagem" e introdução;
- nas situações 1 e 4:
  - logo depois da introdução, um `!!! warning "Treino de idioma, não orientação jurídica"` dizendo que o material treina o idioma e **não é orientação jurídica nem migratória**, e que as regras mudam e quem vale é a fonte oficial;
  - e a seção `## O que dizem as fontes oficiais`, com o que cada fonte diz, em palavras próprias, e o link;
- "Frases" (`--8<-- "kit/gerado/frases-0N.md"`) e "Diálogo" (`--8<-- "kit/gerado/dialogo-0N.md"`);
- "Treinar": botão `../treinar.md?situacao=N` e link do baralho `…/releases/latest/download/ice-destravar-situacao-0N.apkg`, com o texto do Anki igual ao da situação 8;
- "Treinar com IA no modo de voz": aviso de privacidade (Restrições gerais) e RoteiroIA em inglês;
- "Notas culturais": inglês com `lang="en"` e tradução.

| Tarefa | N | Slug | Frases (temas) | Diálogo | RoteiroIA | Notas culturais | Teste extra |
|---|---|---|---|---|---|---|---|
| 6 | 1 | `imigracao` | Motivo da viagem, quanto tempo fica, onde vai ficar, volta marcada, profissão; pedir para repetir mais devagar; dizer que tem comida para declarar | Agente do CBP no aeroporto e a pessoa que chega a passeio; ela responde com fatos e declara um alimento | Agente faz as perguntas de chegada, uma por vez; a pessoa responde com a própria viagem, trocando dados por genéricos | Perguntas curtas e diretas; "<span lang="en">Next!</span>"; diferenças no Canadá, com o link da CBSA | Aviso e fontes; links externos só oficiais; nenhum `en` com `immigrate`, `asylum`, `green card`, `work permit`, `permanent resid` ou `for good` (a palavra "immigration", como lugar do aeroporto, pode) |
| 7 | 2 | `restaurante` | Mesa para dois, pedir, alergia, trocar o acompanhamento, prato errado, pedir a conta, dividir, gorjeta incluída?, levar o resto | Garçom e cliente num restaurante com serviço à mesa, do pedido à conta | Garçom de um restaurante nos EUA, com uma troca no pedido e uma pergunta sobre a conta | <span lang="en">check</span> nos EUA, <span lang="en">bill</span> no Canadá; a gorjeta é esperada em restaurante com serviço à mesa (sem porcentagem sem fonte); <span lang="en">refill</span>; <span lang="en">to go</span> | — |
| 8 | 3 | `taxi` | Confirmar o nome da corrida, dar o destino, perguntar quanto tempo, pedir para parar na entrada, ar-condicionado, "acho que passamos", pagar com cartão, gorjeta pelo aplicativo | Motorista e passageira do aeroporto ao hotel | Motorista de carro de aplicativo, com uma mudança de destino no caminho | <span lang="en">ride</span>, <span lang="en">pick-up</span> e <span lang="en">drop-off</span>; terminal e portão; nada de dica de segurança (Restrições gerais) | — |
| 9 | 4 | `policia` | Pedir ajuda, avisar que perdeu o celular ou foi roubado, onde fica a delegacia, não entendeu; na abordagem: cumprimentar, entregar habilitação e contrato do carro alugado, avisar antes de pegar algo no porta-luvas | Abordagem no trânsito de uma pessoa turista em carro alugado; o policial diz o motivo e dá uma advertência | Balcão de uma delegacia: registrar o celular perdido, com perguntas sobre onde e quando | O que fazer na abordagem só pelas fontes oficiais (manuais da Califórnia e de Ontário), dizendo que muda por estado e província; 911 com a fonte | Aviso e fontes; links externos só oficiais; nenhum `en` com `lawyer`, `attorney`, `my rights`, `free to go`, `search my car` ou `warrant` |
| 10 | 5 | `conversa` | Comentar o lugar ou o evento, perguntar de onde a pessoa é, o que a traz ali, devolver a pergunta, encerrar com gentileza, perceber que a pessoa quer parar | Duas pessoas na fila de um café num evento; uma puxa conversa, a outra responde e as duas encerram | Uma pessoa desconhecida no saguão de um hotel; a IA às vezes dá sinais de que quer encerrar | Temas que em geral se evitam com quem se acabou de conhecer; <span lang="en">small talk</span> curto; como sair da conversa | — |

**Links externos só oficiais (situações 1 e 4):** todo `href="https://…"` do artigo aponta para:
- um destes três: `github.com/angeloreis/ingles-com-evidencia` (baralho), `tatoeba.org` (crédito) ou `oxfordlearnersdictionaries.com`;
- ou um host que termina em `.gov`, `.gc.ca`, `canada.ca` ou `ontario.ca`, ou que casa com `gov\.[a-z]{2}\.ca`.

Outro domínio oficial precisa de ruling e da lista no teste.

- [ ] **Passo 1: teste que falha.** `test_situacao_N_publicada`:
  - `situacoes/<slug>/index.html` existe;
  - tem 18 ou mais `class="pp-frase"` (frases e falas), `data-audio-sequencia` e `pp-roteiro`;
  - mais a coluna "Teste extra":
    - o aviso tem "não é orientação jurídica";
    - as fontes ficam no artigo (`_artigo`);
    - a lista de palavras proibidas é conferida, em minúsculas e como trecho, no `en` do CSV de frases e do de diálogo.
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3: frases do Tatoeba.**
  - Para cada frase pensada, buscar na API, lendo só o JSON: `https://api.tatoeba.org/unstable/sentences?lang=eng&q=<palavras>&sort=relevance&limit=20`.
  - Escolher pelas Restrições gerais, sem mudar o texto.
  - Escrever os dois CSVs:
    - frase do Tatoeba com `tatoeba:<id>`, a licença e o autor;
    - o resto como `projeto`;
    - `pt` sempre do projeto.
  - Registrar no ledger, por id, `tatoeba:<n>` ou `projeto (busca: "<palavras>", nada que sirva)`.
- [ ] **Passo 4:** `python -m scripts.tatoeba` → `Frases do Tatoeba conferidas: N.`, sem problemas.
- [ ] **Passo 5: conferir os fonemas.**
  - Para cada frase e fala, imprimir `Tokenizer().phonemize(texto, "en-us")` (de `kokoro_onnx.tokenizer`) e comparar as palavras difíceis com o IPA americano do Oxford Learner's.
  - Onde não bater, preencher `leitura`.
  - Registrar no ledger os ids com leitura.
- [ ] **Passo 6: só nas situações 1 e 4:** ler cada fonte oficial pelo navegador. Escrever "O que dizem as fontes oficiais" e as notas só com o que a página diz. Registrar no ledger cada link e o que ele sustenta.
- [ ] **Passo 7:** escrever a página, o menu e o item do índice. Rodar `construir`, `zensical build --clean --strict` e a suíte inteira; o teste de `lang="en"` da 1A cobre as notas.
- [ ] **Passo 8:** `python -m scripts.construir --audio` e conferir que o manifesto tem os ids novos.
- [ ] **Passo 9:** commit sugerido: `feat(kit): situação N, <título curto>`.

### Tarefa 11: Semanas 7 a 12 do plano

**Arquivos:**
- Modificar: `kit/planos/destravar.csv`
  - as semanas 1 a 6 ficam como estão;
  - exceção: o passo "Gravar a sua voz" das semanas 2 a 5 passa a ler também as frases da situação 6, como na semana 1, para a comparação valer (menor da 1B).
- Teste: `tests/test_planos.py`

**Foco de cada semana** (a leitura de 5 minutos relê um capítulo publicado; a 2B troca pelos capítulos novos onde couber):

| Semana | Foco | Situações | Leitura do guia |
|---|---|---|---|
| 7 | Chegada: imigração e o táxi do aeroporto ao hotel | 1, 3 | `guia/medo-de-falar/` |
| 8 | Restaurante: pedir, trocar e pagar | 2, revisão da 1 | `guia/frases-chave/` |
| 9 | Polícia: pedir ajuda e abordagem no trânsito | 4, revisão da 3 | `guia/shadowing/` |
| 10 | Puxar conversa | 5, revisão da 2 | `guia/fluencia/` |
| 11 | A viagem inteira, da imigração à conversa; IA em papéis diferentes | 1 a 5 | `guia/ia-modo-de-voz/` |
| 12 | Revisão das oito situações; gravar e comparar com as semanas 1 e 6; 4/3/2 com o tema da semana 1; ficha final | 1 a 8 | `guia/como-usar/` |

- [ ] **Passo 1: teste que falha.** `test_semanas_1_a_6_do_destravar` vira `test_semanas_1_a_12_do_destravar`:
  - semanas publicadas = {1, …, 12};
  - as regras por semana da 1B continuam;
  - `LEITURAS` ganha as semanas 7 a 12 da tabela;
  - todo `?situacao=` está em {1, …, 8}, e todo link `situacoes/` aponta para um slug de `SITUACOES`;
  - nas semanas 7 a 12, as situações ligadas pelos links (`?situacao=N` ou `situacoes/<slug>/`) contêm as da coluna "Situações";
  - nas semanas 2 a 12, o passo "Gravar a sua voz" tem "situação 6".
- [ ] **Passo 2:** rodar e ver falhar.
- [ ] **Passo 3:** escrever as semanas, com os textos dos passos no estilo das semanas 1 a 6. Os temas da 4/3/2 são de viagem: a viagem que você quer fazer, como foi chegar num lugar novo, um restaurante de que gosta.
- [ ] **Passo 4:** rodar `construir`; o `validar_plano` confere links, situações, trechos e minutos. Depois a suíte inteira.
- [ ] **Passo 5:** commit sugerido: `feat(kit): semanas 7 a 12 da trilha Destravar a fala`.

### Tarefa 12: Entrada do site, desenho e conferência final

**Arquivos:**
- Modificar:
  - `conteudo/index.md`:
    - "as semanas 1 a 6 já estão no ar" vira as 12 semanas;
    - o aviso "em construção" lista o que está no ar (seis capítulos, as oito situações, as 12 semanas) e o que falta (os outros capítulos e a trilha Do zero ao A2);
  - `conteudo/situacoes/index.md` (texto) e `conteudo/trilhas/index.md` ("as 12 semanas estão no ar");
  - `conteudo/guia/frases-chave.md` (passo 1) e `conteudo/guia/ia-modo-de-voz.md` (passo 1): depois das três situações de trabalho, "ou qualquer uma das [oito situações](../situacoes/index.md)";
  - `conteudo/sobre.md`: uma frase sobre o Tatoeba, um banco aberto de frases, e sobre o número e o autor que acompanham cada frase;
  - desenho, decisões da 2A:
    - 5.2: as regras de escolha do Tatoeba, a tradução do projeto, o crédito na frase e na carta, a regra de segurança e de táticas jurídicas, as fontes oficiais usadas;
    - 5.2, trilhas: semanas 7 a 12 publicadas, com a leitura relendo capítulos;
    - 5.3: foco, status e link separado em "Hoje", fim do plano;
    - 5.4: `requirements-travado.txt` e `scripts/tatoeba.py` na árvore;
    - 5.5: a 2A entregue.
- Testes: `tests/test_site.py`, `tests/test_guia.py`

- [ ] **Passo 1: teste que falha.** `test_entrada_cita_o_que_esta_no_ar` passa a conferir:
  - a página de situações liga os oito slugs de `SITUACOES`;
  - a página inicial não tem "semanas 1 a 6";
  - o `.md` dos capítulos 6 e 11 tem `../situacoes/index.md`;
  - "Sobre" tem `tatoeba.org`.
- [ ] **Passo 2:** rodar e ver falhar; escrever os textos; ver passar.
- [ ] **Passo 3:** rodar:
  - `python -m scripts.construir --audio --baralhos` → oito `.apkg` em `dist/baralhos/`;
  - `python -m scripts.tatoeba` sem problemas;
  - `zensical build --clean --strict` e a suíte inteira.
- [ ] **Passo 4: conferência no navegador** (servidor `ingles-site`, porta 8010):
  - as cinco páginas novas e as alteradas a 320, 375 e 1280 px, nos dois temas: sem rolagem lateral e sem requisição externa;
  - os botões "Ouvir" habilitados, e o crédito do Tatoeba legível nos dois temas;
  - o treino mostra os oito títulos e filtra `?situacao=1`;
  - "Hoje" com início 42 dias atrás mostra a semana 7;
  - "Hoje" com início 84 dias atrás mostra o fim do plano com os dois links;
  - a conferência de teclado da Tarefa 2, de novo.
- [ ] **Passo 5:** commit sugerido: `docs: entrada do site e desenho com a Fase 2A`.
- [ ] **Passo 6 (mantenedor):**
  - revisar o inglês das cinco situações (por falante nativo, se possível) e ouvir os áudios novos;
  - commit e push; depois, logo em seguida, a tag `v0.3.0`: até a tag sair, os links dos baralhos novos dão 404;
  - validar no celular.
