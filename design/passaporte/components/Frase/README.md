# Frase

Uma frase-chave em inglês com a tradução, a sílaba forte da palavra difícil e o botão de ouvir.

Use em listas `pp-frases` dentro de cada situação de treino (imigração, restaurante, táxi, polícia, reunião). No celular estreito, o botão desce para baixo do texto e ocupa a largura toda.

## O que você fornece

```html
<ul class="pp-frases">
  <li class="pp-frase">
    <p class="pp-frase__en" lang="en">I'm here on <mark class="pp-marca">vacation</mark> for two weeks.</p>
    <p class="pp-frase__pt">Estou aqui de férias por duas semanas.</p>
    <p class="pp-frase__silaba">Sílaba forte: va·<b>CA</b>·tion</p>
    <button type="button" class="pp-botao" data-audio="ice-imigracao-01.mp3">Ouvir</button>
  </li>
</ul>
```

- A frase em inglês, a tradução e, quando houver palavra difícil, a sílaba forte dela.
- O áudio: só o nome do arquivo gerado pelo kit (`ice-<id>.mp3`); o JavaScript procura em `audio/` a partir da raiz do site. No site, esse HTML é gerado por `scripts/paginas.py`.
- O áudio: o site toca o arquivo gerado pelo kit. Sem arquivo, o botão fica `disabled` com "Sem áudio aqui".

## Faça e não faça

- Faça: frases curtas que a pessoa realmente diria na situação.
- Não faça: mais de uma palavra marcada por frase.
