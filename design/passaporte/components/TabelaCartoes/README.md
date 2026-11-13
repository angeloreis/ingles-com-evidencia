# TabelaCartoes

Tabela comum no computador que vira uma pilha de cartões até 768 px, com o rótulo de cada valor empilhado acima dele.

Use para comparar técnicas, resumir um plano por semana ou listar fontes. Nunca deixe uma tabela rolar para os lados no celular.

## O que você fornece

```html
<table class="pp-tabela">
  <thead><tr><th>Técnica</th><th>Evidência</th><th>Como praticar</th></tr></thead>
  <tbody>
    <tr>
      <td data-rotulo="Técnica">Repetição espaçada</td>
      <td data-rotulo="Evidência"><span class="pp-carimbo pp-carimbo--reto" data-nivel="3">…</span></td>
      <td data-rotulo="Como praticar">15 minutos de Anki por dia</td>
    </tr>
  </tbody>
</table>
```

- `data-rotulo` em toda célula, igual ao cabeçalho da coluna: é ele que aparece no cartão.

## Faça e não faça

- Faça: no máximo quatro colunas.
- Não faça: célula sem `data-rotulo`, ou tabela usada só para alinhar layout.
