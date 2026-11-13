# SecaoDoGuia

Um bloco de texto do capítulo com rótulo em etiqueta: "O que os cursos dizem", "O que a pesquisa diz" e "Como praticar".

Todo capítulo de técnica tem esses três blocos, nessa ordem, logo depois do título e do `Carimbo`.

## O que você fornece

```html
<section class="pp-secao">
  <span class="pp-secao__rotulo">O que a pesquisa diz</span>
  <p class="pp-secao__texto">Revisar em intervalos cada vez maiores…</p>
</section>
```

- O rótulo (curto, a seção põe em maiúsculas) e um ou mais parágrafos `pp-secao__texto`.
- A promessa dos cursos vai entre aspas, para ficar claro que é citação.
- Para marcar a palavra-chave de um parágrafo, use `<mark class="pp-marca">`.

## Faça e não faça

- Faça: cite a pesquisa pelo nome e pelo ano no bloco "O que a pesquisa diz".
- Não faça: misture opinião e evidência no mesmo bloco.
