# Carimbo

Mostra o nível de evidência de uma técnica como um carimbo de passaporte: forte, moderada, fraca ou sem evidência.

Use logo abaixo do título de cada capítulo do guia. Em listas e tabelas que comparam técnicas, use a versão reta (`pp-carimbo--reto`).

## O que você fornece

```html
<span class="pp-carimbo" data-nivel="3">
  <span class="pp-carimbo__barras" aria-hidden="true"><i></i><i></i><i></i></span>
  Evidência forte
</span>
```

- `data-nivel`: `3` forte, `2` moderada, `1` fraca, `0` sem evidência.
- O texto é obrigatório. As barras e a cor repetem o nível, nunca o substituem.

## Faça e não faça

- Faça: um carimbo por técnica, com a referência da pesquisa no texto do capítulo.
- Não faça: carimbo como enfeite, dentro de botão ou de título.
