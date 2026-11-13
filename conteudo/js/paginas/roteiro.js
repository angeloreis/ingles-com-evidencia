/* Botão "Copiar roteiro" dos blocos .pp-roteiro. */
(function (ICE) {
  "use strict";

  function selecionar(elemento) {
    var faixa = document.createRange();
    faixa.selectNodeContents(elemento);
    var selecao = window.getSelection();
    selecao.removeAllRanges();
    selecao.addRange(faixa);
  }

  ICE.aoAbrirPagina(function () {
    document.querySelectorAll(".pp-roteiro").forEach(function (bloco) {
      var botao = bloco.querySelector("button");
      var texto = bloco.querySelector(".pp-roteiro__texto");
      if (!botao || !texto || botao.dataset.ligado) return;
      botao.dataset.ligado = "1";
      var rotulo = botao.textContent;
      botao.addEventListener("click", function () {
        var feito = function () {
          botao.textContent = "Copiado";
          setTimeout(function () { botao.textContent = rotulo; }, 2000);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(texto.textContent.trim()).then(feito, function () { selecionar(texto); });
        } else {
          selecionar(texto);
        }
      });
    });
  });
})(globalThis.ICE = globalThis.ICE || {});
