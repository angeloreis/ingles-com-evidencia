# PassosDoDia

O plano do dia: tempo total, barra de progresso da trilha e os passos numerados para marcar.

Use na página "Hoje" de cada trilha. Cada passo tem a tarefa e os minutos; a ordem é a ordem em que a pessoa deve fazer.

## O que você fornece

```html
<h3 class="titulo-3">24 minutos de treino</h3>
<div class="pp-progresso" role="img" aria-label="17 de 84 dias concluídos"><span style="width:20%"></span></div>
<ol class="pp-passos">
  <li>
    <input type="checkbox" id="passo-1">
    <label for="passo-1"><span class="pp-passos__texto">Revisar as cartas no Anki</span><span class="pp-passos__tempo">10 min</span></label>
    <a class="pp-passos__abrir" href="treinar/" aria-label="Abrir: Revisar as cartas no Anki">Abrir</a>
  </li>
</ol>
<p class="ice-hoje__status" role="status">0 de 1 passos feitos.</p>
<button type="button" class="pp-botao pp-botao--primario">Marcar o próximo passo</button>
```

- O título com o total de minutos, a largura da barra e o rótulo dela, e os passos com `id` únicos.
- O botão primário marca o primeiro passo ainda aberto e fica desabilitado com o dia completo.
- O link do passo vem depois do `label`, nunca dentro: tocar no texto marca o passo, e "Abrir" leva à página.
- O status (`role="status"`) anuncia quantos passos estão feitos a cada marcação.

## Faça e não faça

- Faça: no máximo quatro passos por dia.
- Não faça: passos sem tempo, ou tempo total que não bata com a soma.
