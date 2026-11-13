# Inglês com Evidência: desenho do projeto

- **Data:** 12/11/2026
- **Situação:** aprovado em 12/11/2026; Fase 0 (esqueleto) construída em 13/11/2026
- **Nome:** provisório ("Inglês com Evidência"); conferir se o nome está livre no GitHub e como domínio antes de publicar.

## 1. Intenção

Um material **aberto, gratuito e em português do Brasil** para quem estuda inglês por conta própria. Ele pega as técnicas que cursos de "poliglotas" vendem (vocabulário de alta frequência, repetição espaçada, memorização por associação, frases-chave, shadowing, aprender dois idiomas ao mesmo tempo), cruza cada uma com a pesquisa sobre aprendizagem de línguas e diz, sem rodeio, o quanto a ciência sustenta cada promessa.

São duas partes:

1. **O guia**: um capítulo por técnica, com o que os cursos dizem, o que a pesquisa diz, um selo de evidência e como praticar.
2. **O kit de prática**: situações de treino, baralhos do Anki gerados a partir de dados, planos de estudo e ficha de progresso.

Tudo publicado como **site** (GitHub Pages), porque boa parte do público não é técnica: abrir no celular e seguir os passos precisa bastar. O repositório no GitHub guarda os dados, os scripts e os textos.

### Para quem

- **Quem entende, mas não fala.** Já estudou ou morou fora, entende vídeos sem legenda, mas a fala enferrujou e falta confiança. Trilha **Destravar a fala**.
- **Quem está começando.** Sabe pouco além do "verb to be". Trilha **Do zero ao A2**.
- Os dois públicos têm objetivos práticos: **viajar** (EUA ou Canadá) e **trabalhar remoto** para empresas de fora, em especial na área de tecnologia.

## 2. Objetivos, não objetivos e anti-objetivos

### Objetivos

- Guia com os capítulos da seção 5.1, todos no mesmo formato e com referências conferidas.
- Kit com as duas trilhas, oito situações de treino, planos de estudo e ficha de progresso.
- Baralhos do Anki **gerados por script** a partir de arquivos CSV, com áudio e créditos automáticos.
- Site em **Zensical** com o design system **Passaporte**, feito primeiro para o celular.
- Licenças limpas: cada frase, palavra e áudio com fonte e licença registradas.

### Não objetivos (agora)

- Login, contas, progresso salvo em servidor ou qualquer parte paga.
- Outros idiomas além do inglês.
- Aulas ao vivo ou correção por pessoas.
- Aplicativo de celular.

### Anti-objetivos (seria um fracasso mesmo funcionando)

- Copiar conteúdo de cursos pagos (textos, listas de frases, vídeos, áudios) ou usar nome e marca de cursos ou pessoas como chamariz.
- Prometer prazo ("fluente em 3 meses") ou resultado.
- Afirmar algo sobre evidência sem citar a pesquisa.
- Exigir instalação ou conhecimento técnico para o uso básico: ler o guia, ouvir as frases e seguir o plano do dia têm que funcionar só no navegador.
- Rolagem para os lados no celular.
- Usar material com licença "não comercial" (NC), que impediria reutilizações que a licença do projeto permite.

## 3. Restrições

- **Licença do conteúdo: CC BY-SA 4.0.** É obrigatória, porque a lista NGSL (base do vocabulário) é CC BY-SA 4.0 e exige a mesma licença nas obras derivadas. **Scripts: MIT.**
- **Fontes de dados permitidas:** NGSL e NGSL-Spoken (CC BY-SA 4.0), frases do Tatoeba (CC BY 2.0 FR ou CC0), textos e áudios gerados pelo próprio projeto. Áudio de terceiros só com CC0, CC BY ou CC BY-SA, nunca NC nem "sem licença".
- **Créditos:** `CREDITOS.md` gerado pelo script a partir das colunas de fonte e licença dos CSVs. Nenhuma linha de dado entra sem fonte e licença.
- **Ferramentas:** Python 3.12, Zensical (instalado via pip), genanki (MIT) e um sintetizador de voz com licença aberta (ver 4.3). **Sem Node** no repositório.
- **Publicação:** GitHub Pages via GitHub Actions.
- **Celular primeiro:** valem as regras do Passaporte: texto com 17 px ou mais, áreas de toque com 48 px ou mais, uma coluna até 768 px, tabelas que viram cartões, tema escuro automático.
- **Idioma:** tudo em português do Brasil. Toda frase em inglês vem com tradução.
- **Privacidade:** nenhum dado pessoal dos mantenedores no repositório. O site não usa rastreadores e não carrega fontes de servidores de terceiros (ver 5.3).
- **Git:** o mantenedor faz commit, push e deploy. Nada é commitado automaticamente.

## 4. Abordagens consideradas

### 4.1 Estrutura do projeto

| Abordagem | Como é | Ganha | Perde |
|---|---|---|---|
| A. Guia em Markdown e baralhos feitos à mão | `.md` no GitHub e `.apkg` exportado do Anki | Começa mais rápido | `.apkg` é binário: sem diff, sem contribuição por PR, licença de cada frase controlada à mão |
| B. Guia em Markdown e kit gerado de dados | CSV por baralho e script que gera `.apkg`, áudio e créditos | Tudo revisável no diff, créditos automáticos, contribuição por PR | Mais trabalho no início e um script para manter |
| **C. B mais um site (escolhida)** | O mesmo Markdown vira um site no GitHub Pages | Quem não é técnico usa sem GitHub nem Anki | Mais uma peça para configurar |

**Escolha: C.** O público inclui pessoas com pouca familiaridade com tecnologia, e para elas o site é a porta de entrada.

### 4.2 Ferramenta do site

| Opção | Situação |
|---|---|
| Material for MkDocs | Em manutenção desde novembro de 2025; o suporte terminou em 5/11/2026. Descartada. |
| Astro Starlight | Boa e mantida, mas traz Node para o repositório. Descartada. |
| **Zensical (escolhida)** | Sucessor do Material, da mesma equipe, licença MIT, configuração em `zensical.toml`, aceita CSS próprio (`extra_css`), JavaScript próprio e substituição de templates (`custom_dir`). Roda em Python, a mesma linguagem dos scripts. |

### 4.3 Áudio

| Opção | Ganha | Perde |
|---|---|---|
| **Voz sintética aberta (escolhida)**, a começar pelo Kokoro | Áudio para toda frase, voz consistente, licença clara | Não é voz de nativo; entonação menos natural |
| Áudios do Tatoeba | Vozes humanas | Cobertura irregular, licença por pessoa (muitas NC) |
| Só a voz do sistema (TTS do Anki ou do navegador) | Zero arquivos | Qualidade e voz variam por aparelho; nada funciona igual para todos |

**Escolha:** voz sintética aberta para frases e diálogos. Para shadowing com fala natural, o guia indica conteúdos externos **só com link**, sem copiar áudio. **Antes de gerar qualquer áudio**, conferir a licença do modelo e de cada voz usada. Se o Kokoro não servir, trocar por outro modelo com licença que permita uso comercial e registrar a troca neste documento.

*Decidido na Fase 1A (13/11/2026):* modelo Kokoro-82M v1.0 (Apache 2.0) pela biblioteca `kokoro-onnx` (MIT), arquivo fp32 com sha256 conferido. Vozes `af_heart` (frases e pessoa A dos diálogos) e `am_michael` (pessoa B), na velocidade 0.9. Arquivos `ice-<id>.mp3`, gravados pelo `soundfile` sem ffmpeg. A conversão de texto em fonemas usa o espeak-ng (GPL-3.0) só durante a geração.

## 5. O que foi decidido

### 5.1 Guia

Capítulos, nesta ordem:

1. Como usar este guia e o que significam os selos
2. Vocabulário de alta frequência ("pular o básico")
3. Repetição espaçada
4. Testar a própria memória (recordação ativa)
5. Memorização por associação
6. Frases-chave e blocos prontos
7. Escuta: conteúdo que você quase entende e legendas em degraus
8. Shadowing
9. Fluência na fala: técnica 4/3/2, gravar a própria voz e cartas ao contrário
10. Medo de falar e confiança
11. Treinar com IA no modo de voz
12. Dois idiomas ao mesmo tempo
13. Rotina, motivação e promessas que a pesquisa não sustenta

Cada capítulo segue a mesma estrutura, com os componentes do Passaporte:

- título e **Carimbo** (selo de evidência);
- **O que os cursos dizem**: a promessa, com palavras próprias, sem copiar texto de curso;
- **O que a pesquisa diz**: resumo com autor e ano no texto;
- **Como praticar**: passos concretos, com tempo;
- **Armadilhas**;
- **Referências**: lista completa no fim.

**Critério dos selos:**

| Selo | Quando usar |
|---|---|
| Forte | Metanálises ou muitos estudos controlados com resultado na mesma direção |
| Moderada | Vários estudos a favor, com limitações (amostras pequenas, contexto restrito) |
| Fraca | Poucos estudos, estudos indiretos ou resultados mistos |
| Sem evidência | Nenhum estudo, ou estudos contra a promessa |

**Referências de partida (a conferir uma a uma antes de citar):** Cepeda et al. (2006), sobre prática espaçada; Karpicke e Roediger (2008), sobre recordação ativa; Atkinson e Raugh (1975), sobre a técnica da palavra-chave; Nation (2006), sobre tamanho de vocabulário para ouvir e ler; Browne, Culligan e Phillips (NGSL); Montero Perez, Van Den Noortgate e Desmet (2013), metanálise sobre legendas; Hamada, sobre shadowing; Nation (1989) e De Jong e Perfetti (2011), sobre a técnica 4/3/2; Horwitz, Horwitz e Cope (1986), sobre ansiedade em língua estrangeira; Swain (1985), sobre produção oral. **Nenhuma referência entra no guia sem que o resumo do estudo tenha sido lido.** Se uma delas não disser o que se espera, o texto muda, não a referência.

### 5.2 Kit de prática

#### Trilhas

**Destravar a fala** (prioridade 1)
- Cartas ao contrário: aparece a frase em português e a pessoa fala em inglês, em voz alta.
- Shadowing com os diálogos das situações.
- Técnica 4/3/2 com temas da vida real (o próprio trabalho, o fim de semana, um projeto).
- Gravar a própria voz uma vez por semana e comparar com a semana anterior.
- Uma conversa real por semana (tandem, amigo, colega) e os roteiros de IA nos outros dias.
- Plano de **12 semanas**, com 20 a 30 minutos por dia.

**Do zero ao A2**
- Pronúncia primeiro: os sons que o português não tem (th, vogais curtas e longas, finais de palavra).
- Vocabulário da NGSL em faixas de 500 palavras, em ordem de frequência: primeiro reconhecer (inglês para português), depois produzir (português para inglês).
- Leituras graduadas: usar as da NGSL só se a licença permitir (conferir); senão, textos curtos escritos pelo projeto com o vocabulário da faixa.
- Frases de sobrevivência das situações de viagem.
- Treino em dupla: uma pessoa faz o atendente e a outra pede.
- Plano por fases para cerca de **200 horas** (perto do nível A2), com 30 minutos por dia.

#### Situações de treino (oito na primeira versão)

| # | Situação | Grupo |
|---|---|---|
| 1 | Imigração no aeroporto ou na fronteira | Viagem |
| 2 | Restaurante: pedir, trocar algo, pedir a conta, gorjeta | Viagem |
| 3 | Táxi ou carro de aplicativo | Viagem |
| 4 | Polícia: pedir ajuda e abordagem no trânsito | Viagem |
| 5 | Puxar conversa sem ser inconveniente | Viagem |
| 6 | Telefonar para colegas e marcar reunião | Trabalho |
| 7 | Conversar sobre programação, IA e frameworks | Trabalho |
| 8 | Entrevista de emprego para trabalho remoto | Trabalho |

Cada situação tem: **Faixa**, 8 a 12 **Frases** (com tradução e sílaba forte quando houver palavra difícil), um diálogo-modelo com áudio, cartas no baralho da situação, um **RoteiroIA** e notas culturais.

Regras de conteúdo sensível:
- **Imigração e polícia:** o comportamento recomendado (por exemplo, mãos no volante numa abordagem) vem **só de fonte oficial** (manuais de trânsito dos estados ou províncias, sites do CBP e da CBSA), com o link. A página avisa que o material treina o idioma e **não é orientação jurídica nem migratória**.
- Na imigração, o treino é responder **com clareza e com a verdade**. O kit não ensina o que dizer sobre planos de imigração.
- Situação 7 inclui a pronúncia de termos técnicos que brasileiros costumam errar (cache, SQL, Nginx, GUI, entre outros), conferida em dicionário com pronúncia.

#### Dados

Um CSV por baralho em `kit/dados/`, UTF-8, com cabeçalho. Colunas:

| Coluna | Obrigatória | O que é |
|---|---|---|
| `id` | sim | Identificador estável (por exemplo `imigracao-01`); nunca reaproveitado |
| `en` | sim | Frase ou palavra em inglês |
| `pt` | sim | Tradução |
| `silaba` | não | Palavra com a sílaba forte marcada, como `va·CA·tion` |
| `situacao` ou `faixa` | sim | A situação (1 a 8) ou a faixa da NGSL |
| `fonte` | sim | `ngsl`, `tatoeba:<id da frase>` ou `projeto` |
| `licenca` | sim | `CC BY-SA 4.0`, `CC BY 2.0 FR`, `CC0` |
| `autor` | quando a licença pede | Usuário ou autor de origem |

O `id` alimenta o identificador da nota no Anki, para que uma correção de tradução atualize a carta de quem já importou o baralho, em vez de duplicar.

Os diálogos ficam em `kit/dialogos/`, um CSV por situação, com as colunas `id`, `situacao`, `ordem`, `falante` (`A` ou `B`), `en`, `pt`, `fonte`, `licenca` e `autor`; os ids são únicos entre baralhos e diálogos, porque viram nome de arquivo de áudio. *(Fase 1A.)*

Os planos ficam em `kit/planos/<trilha>.csv`, uma linha por passo: `semana`, `dia`, `ordem`, `passo`, `minutos`, `link` (página do site ou baralho usado). O script gera a partir deles as páginas "Hoje" e a lista de semanas, e confere se a soma dos minutos de cada dia bate com o limite da trilha.

#### Scripts

- `scripts/construir.py` roda tudo: valida os CSVs (colunas, licenças permitidas, `id` repetido), gera áudio, gera baralhos, gera créditos.
- Baralhos com dois tipos de carta: **reconhecer** (inglês na frente) e **produzir** (português na frente, resposta falada). A trilha Destravar a fala usa só "produzir".
- Os `.apkg` e os áudios são **gerados**, não versionados: os baralhos saem anexados às Releases do GitHub e os áudios vão junto com o site publicado.

#### Anki

- *Decidido pelo mantenedor na Fase 1A (13/11/2026):* o AnkiWeb não importa baralhos pelo navegador (é preciso o Anki no computador ou o AnkiDroid, e depois sincronizar). Por isso o **site tem o próprio treino de cartas**: português na frente, a pessoa fala em inglês, confere a resposta e ouve o áudio. As cartas voltam em 1, 3, 7, 14 ou 30 dias (caixas de Leitner), com até 10 cartas novas por dia, e o progresso fica só no aparelho.
- O **Anki é opcional**: os baralhos saem nas Releases para quem usa o AnkiDroid (Android, gratuito) ou o Anki no computador. O AnkiMobile do iPhone é pago, e o site diz isso, apontando o treino de cartas como alternativa gratuita.
- O uso básico não depende do Anki: no site, cada situação já tem as frases com áudio, o treino de cartas e o plano do dia.

### 5.3 Site

- **Zensical** publicado no **GitHub Pages** por uma GitHub Action a cada push na `main`.
- **Visual:** design system **Passaporte** (`tokens.css` e `bundle.css`, prefixo `pp-`) carregado como `extra_css`. Componentes: Faixa, Carimbo, SecaoDoGuia, Frase, RoteiroIA, PassosDoDia, Botao, TabelaCartoes. Referência completa: <https://claude.ai/artifact/7xV6BDaYQkmtbYdw7Mv2Bt> (link privado; uma cópia dos arquivos entra no repositório em `conteudo/estilos/`).
- **Fontes servidas pelo próprio site** (Archivo, Figtree e IBM Plex Mono, todas com licença OFL), em vez do Google Fonts, para o site não enviar dados de visitantes a terceiros.
- **Menu:** Início ("Por onde começar", com a escolha da trilha), Guia, Situações, Trilhas e planos, Sobre e créditos.
- **Plano do dia:** página "Hoje" de cada trilha com **PassosDoDia**. Na primeira visita, a pessoa escolhe "começar hoje" ou a semana em que está; o site guarda essa data e os passos marcados **só no aparelho** (localStorage), sem login, e calcula o dia do plano. A página avisa que trocar de aparelho ou limpar o navegador zera o progresso, e oferece também a lista completa das semanas para quem preferir seguir sem o "Hoje".
- **Ficha de progresso:** página da trilha com um registro por semana (data da gravação da voz, tempos da técnica 4/3/2, conversa real feita ou não, confiança de 1 a 5), salvo da mesma forma, só no aparelho.
- **Áudio:** o botão "Ouvir" toca o arquivo gerado. Sem arquivo, o botão aparece desabilitado com "Sem áudio aqui".
- **Busca** do próprio Zensical, conferindo se funciona bem em português. *Conferido na Fase 0:* acha com e sem acento ("evidencia" acha "evidência", "licenca" acha "licença"). Pendência conhecida: o contador de resultados aparece em inglês ("4 results"), porque a interface da busca do Zensical 0.1.1 ainda não é traduzida.
- **Tema:** o site começa seguindo o tema do aparelho (claro ou escuro); o botão alterna entre automático, claro e escuro, e a escolha vale para todas as páginas. *Decidido na Fase 0:* com só duas opções (claro e escuro), o tema gravava o esquema do primeiro acesso e deixava de acompanhar o aparelho.
- **Trechos gerados nas páginas:** frases, diálogos e lista de semanas são gerados de `kit/` para `kit/gerado/` e entram nas páginas escritas à mão com `--8<-- "kit/gerado/arquivo.md"` (`pymdownx.snippets`); trecho ausente derruba o build. Link em HTML cru dentro de uma página aponta para o `.md` de origem (`../treinar.md?situacao=6`), porque o Zensical reescreve esses links a partir do arquivo de origem e confere no modo estrito. *Decidido na Fase 1A.*
- **Sem link do repositório no cabeçalho** (`repo_url`): o tema buscaria dados na API do GitHub pelo navegador de quem visita. O link fica na página "Sobre e créditos". *Decidido na Fase 0, por privacidade.*
- **Acessibilidade:** contraste WCAG AA nos dois temas, foco visível, textos alternativos, nenhuma informação só por cor.

### 5.4 Repositório

```
ingles-com-evidencia/
├── .github/workflows/site.yml  testes e publicação no GitHub Pages
├── conteudo/                 textos do site (guia, situações, trilhas, sobre)
│   ├── estilos/              tokens.css (gerado), bundle.css, ponte.css, fontes.css e fontes/
│   ├── js/                   núcleo, lógica pura (testada no pytest) e scripts de página
│   ├── dados/                cartas.json e planos em JSON (gerados)
│   └── audio/                MP3 e manifesto (gerados, fora do git)
├── design/passaporte/        fonte do design system: tokens.json, guia de componentes, origem das fontes
├── docs/                     documentos do projeto, fora do site
│   └── superpowers/          specs/ (este documento) e plans/ (planos por fase)
├── kit/
│   ├── dados/                CSVs dos baralhos
│   ├── dialogos/             CSVs dos diálogos
│   ├── planos/               CSVs dos planos das trilhas
│   └── gerado/               trechos HTML e Markdown incluídos nas páginas (gerados)
├── scripts/                  construir.py, validar.py, estilos.py
├── tests/                    testes (pytest)
├── zensical.toml             com docs_dir = "conteudo"
├── pyproject.toml            configuração do pytest
├── requirements-site.txt     Zensical (versão fixa)
├── requirements-dev.txt      o anterior mais o pytest
├── CREDITOS.md               gerado (a partir da Fase 1)
├── LICENSE                   CC BY-SA 4.0 (conteúdo)
├── LICENSE-codigo            MIT (scripts)
└── README.md
```

Os textos do site ficam em `conteudo/` para que `docs/` (documentos do projeto, como este) não seja publicado. *Conferido na Fase 0:* o Zensical aceita `docs_dir`, e nada de `docs/` aparece no site. Nenhum `.md` além das páginas fica dentro de `conteudo/`, porque o Zensical publica todo `.md` dessa pasta como página: por isso a fonte do Passaporte fica em `design/passaporte/`.

### 5.5 Fases

Cada fase termina com a validação do mantenedor antes da próxima.

| Fase | Entrega | Pronto quando |
|---|---|---|
| 0. Esqueleto | Repositório, licenças, Zensical com Passaporte, Action do Pages, `construir.py` validando um CSV de exemplo | O site está no ar com a página inicial, no celular e no computador, nos dois temas |
| 1. Destravar a fala e trabalho | Situações 6, 7 e 8; capítulos 1, 6, 8, 9, 10 e 11; semanas 1 a 6 do plano, usando só essas situações; baralhos dessas situações | Uma pessoa consegue seguir a semana 1 inteira só pelo site (critério revisto na Fase 1A, porque o AnkiWeb não importa baralhos). Dividida em **1A, o motor** (áudio, baralhos, treino de cartas, "Hoje", ficha e a situação 6 como piloto) e **1B, o conteúdo** (situações 7 e 8, capítulos e semanas 1 a 6) |
| 2. Viagem | Situações 1 a 5; capítulos 2, 3, 4, 5, 7, 12 e 13; semanas 7 a 12 do plano | Todas as situações e capítulos publicados, com referências conferidas |
| 3. Do zero ao A2 | Pronúncia, faixas da NGSL (começando pelas primeiras 500), leituras, plano por fases | Uma pessoa iniciante consegue seguir as duas primeiras semanas sem ajuda |
| 4. Extras | Ideias para depois: baralho temático "inglês para fãs de doramas", versão para imprimir da ficha de progresso | A decidir |

## 6. O que fica para quem constrói

- O texto de cada capítulo, das frases e dos diálogos, seguindo as regras da seção 5 e o tom do Passaporte.
- Escolha das vozes sintéticas (pelo menos uma voz americana; uma segunda voz para diálogos) depois de conferir as licenças.
- Configuração do `zensical.toml`, do menu e da busca.
- Modelos de carta do Anki (layout, campos, uso de áudio).
- Detalhes da Action (cache do modelo de voz, onde os áudios ficam no site publicado).
- Se o conteúdo crescer além do previsto, propor a divisão em mais baralhos.

## 7. Riscos

- **Voz sintética no shadowing:** a entonação pode soar artificial. Mitigação: o guia combina o áudio do kit com conteúdo real externo.
- **Conteúdo de imigração e polícia:** erro pode causar dano real. Mitigação: só fonte oficial, link na página e aviso de que não é orientação jurídica.
- **Referência mal citada:** compromete a proposta do projeto. Mitigação: nenhuma citação sem leitura do resumo; selo revisto quando a pesquisa não sustentar.
- **Volume de escrita:** o grosso do trabalho é texto, não código. Mitigação: fases pequenas, cada uma publicável.
- **Erros no inglês das frases:** frases escritas pelo projeto podem soar artificiais. Mitigação: preferir frases do Tatoeba quando existirem; o mantenedor revisa cada situação; quando possível, um falante nativo lê as frases antes da publicação, e o site tem um link para reportar erros (issue no GitHub).
