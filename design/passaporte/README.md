Passaporte é o visual do site **Inglês com Evidência**, um guia aberto e gratuito, em português, para brasileiros que estudam inglês por conta própria, com um kit de prática. O visual lembra um documento de viagem: verde de passaporte, etiquetas em letra de máquina e o nível de evidência de cada técnica como um carimbo. Ele precisa servir a quem não gosta de tecnologia: letra grande, um passo por vez e nada para instalar.

## Voz e texto

- Fale com o leitor por "você", em português do Brasil, com frases curtas e na voz ativa.
- Toda frase em inglês vem seguida da tradução, nesta ordem: inglês em `corpo-forte` com `tinta`, português em `apoio` com `tinta-suave`.
- Diga o que a pesquisa sustenta e o que não sustenta, usando os quatro níveis do `Carimbo`. Nunca prometa prazo, como "fluente em 3 meses".
- Botões dizem a ação: "Ouvir", "Copiar roteiro", "Marcar o próximo passo". Depois da ação, o próprio botão confirma: "Copiado".
- Sem emoji, sem ponto de exclamação e sem caixa alta fora das etiquetas e do carimbo.
- Exemplo do tom: "Revisar em intervalos cada vez maiores faz a memória durar mais do que estudar tudo de uma vez."

## Cores

- Pinte a página com `fundo` e os blocos (frases, passos, roteiros, cartões) com `superficie`.
- Texto principal em `tinta`. Tradução, etiquetas, minutos e apoio em `tinta-suave`. Os dois passam de 4,5:1 sobre `fundo` e `superficie` nos dois temas.
- `passaporte` é a cor da marca e da ação: faixa do topo, botões, borda de controles, palavra-chave marcada e barra de progresso. Texto sobre ela é sempre `sobre-passaporte`, nunca branco fixo.
- `linha` só separa e contorna cartões. Borda de controle usa `passaporte`.
- As cores de evidência (`evidencia-forte`, `evidencia-moderada`, `evidencia-fraca`, `evidencia-nenhuma`) aparecem só no `Carimbo`. O nível também vem escrito e nas barras, então a cor nunca é o único sinal, inclusive para quem não distingue verde de vermelho.
- O tema escuro segue o celular automaticamente. Confira toda tela nova nos dois temas.

## Tipografia

- Três famílias: `titulo` (Archivo) para títulos, `texto` (Figtree) para leitura e `etiqueta` (IBM Plex Mono) para faixas, rótulos, carimbos, sílaba forte e minutos.
- Texto corrido em `corpo` (17 px). Nenhum texto de leitura abaixo de `apoio` (15 px).
- Um `titulo-1` por página, seções em `titulo-2`, cartões e blocos em `titulo-3`.
- `etiqueta` e `carimbo` vão sempre em maiúsculas, com o espaçamento do estilo.
- Sílaba forte em `pronuncia`, com a sílaba tônica em negrito e maiúsculas: va·**CA**·tion.
- As fontes (Archivo, Figtree e IBM Plex Mono) são servidas pelo próprio site, nunca pelo Google Fonts; origem e licenças em [fontes.md](fontes.md). Sem elas, as pilhas caem nas fontes do sistema.

## Espaço, forma e celular primeiro

- Espaçamento em passos de 4 px: `espaco-3` entre itens de uma lista, `espaco-4` dentro de cartões e na margem lateral do celular, `espaco-8` entre seções.
- Cantos quase retos, como documento: `raio` em cartões e botões, `raio-carimbo` no carimbo, `raio-painel` em painéis grandes. Não use sombra; separe com `linha`.
- Desenhe primeiro para 375 px de largura. Até `quebra-celular` (768 px) tudo fica em uma coluna; texto corrido nunca passa de `largura-texto`.
- Nada rola para os lados. Tabela vira cartões até 768 px com `TabelaCartoes`, cada valor com seu rótulo empilhado acima.
- Tudo que se toca tem pelo menos `alvo-toque` (48 px) de altura. A ação principal no celular usa `alvo-toque-grande` (56 px) e a largura toda.

## Estados e foco

- Foco do teclado: anel sólido de 3 px em `foco`, afastado 2 px do elemento. Nunca remova o anel.
- Botão desabilitado fica com 55% de opacidade e explica o motivo no próprio texto, como "Sem áudio aqui".
- Passo concluído: círculo preenchido com ✓ e texto riscado em `tinta-suave`.
- O sistema não usa animação. A única inclinação é a do carimbo, que é fixa.

## Iconografia

Não há biblioteca de ícones nem logotipo: o nome do site vai escrito em `titulo` e as ações são escritas nos botões. Os únicos sinais gráficos são as três barras do `Carimbo`, a perfuração tracejada da `Faixa` e o ✓ do passo concluído. Não use emoji como ícone.

## Componentes

Os componentes são classes CSS de `components/bundle.css`, com prefixo `pp-`, feitas para usar dentro de páginas em Markdown com HTML. Carregue `tokens.css` primeiro e `bundle.css` depois.

- `Faixa`: topo de cada página e de cada situação de treino.
- `Carimbo`: nível de evidência de uma técnica.
- `SecaoDoGuia`: os blocos "O que os cursos dizem", "O que a pesquisa diz" e "Como praticar".
- `Frase`: frase-chave com tradução, sílaba forte e botão de ouvir.
- `RoteiroIA`: roteiro para treinar com um assistente de IA no modo de voz.
- `PassosDoDia`: plano do dia, com progresso e passos para marcar.
- `Botao`: ações.
- `TabelaCartoes`: tabela que vira cartões no celular.
