# RoteiroIA

Um roteiro pronto para copiar e colar num assistente de IA com modo de voz, que faz o papel do outro lado da conversa.

Use no fim de cada situação de treino, depois das frases-chave. O roteiro fica em inglês (é o que a IA vai seguir) e pede a correção em português.

## O que você fornece

```html
<div class="pp-roteiro">
  <span class="pp-roteiro__rotulo">Treinar com IA no modo de voz</span>
  <p class="pp-roteiro__texto">You are an immigration officer…</p>
  <button type="button" class="pp-botao">Copiar roteiro</button>
</div>
```

- O rótulo, o texto do roteiro e o botão de copiar. O botão troca para "Copiado" por dois segundos; se o navegador não deixar copiar, o texto fica selecionado para a pessoa copiar.

## Faça e não faça

- Faça: diga à IA quantas perguntas fazer, uma por vez, e quando corrigir.
- Não faça: roteiros que peçam para a IA responder pela pessoa.
