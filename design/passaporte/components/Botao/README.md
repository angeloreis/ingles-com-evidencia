# Botao

Botão de ação: preenchido para a ação principal da tela, contornado para as demais.

Use `pp-botao--primario` uma vez por tela, para o que a pessoa veio fazer ("Marcar o próximo passo"). As outras ações ("Ouvir", "Copiar roteiro") usam o botão contornado. No celular, o primário ocupa a largura toda e fica com 56 px de altura.

## O que você fornece

```html
<button type="button" class="pp-botao pp-botao--primario">Marcar o próximo passo</button>
<button type="button" class="pp-botao">Ouvir</button>
<a class="pp-botao" href="/situacoes/restaurante/">Próxima situação</a>
```

- Um verbo que diga o que acontece. Depois da ação, troque o texto para confirmar ("Copiado").
- `pp-botao--largo` força a largura toda também no computador.
- Desabilitado: atributo `disabled` e o motivo no texto ("Sem áudio aqui").

## Faça e não faça

- Faça: um primário por tela.
- Não faça: dois primários lado a lado, ou texto genérico como "Clique aqui".
