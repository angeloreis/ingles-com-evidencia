/* Botões "Ouvir" ([data-audio]) e "Ouvir o diálogo inteiro" ([data-audio-sequencia]). */
(function (ICE) {
  "use strict";

  var tocando = null;

  function parar() {
    if (tocando) {
      tocando.onended = null;
      tocando.pause();
      tocando = null;
    }
  }

  function tocarFila(arquivos) {
    parar();
    var i = 0;
    var proximo = function () {
      if (i >= arquivos.length) { tocando = null; return; }
      tocando = new Audio(ICE.url("audio/" + arquivos[i++]));
      tocando.onended = proximo;
      tocando.play().catch(function () { tocando = null; });
    };
    proximo();
  }

  /* Para botões criados depois do carregamento (treino de cartas). */
  ICE.tocar = tocarFila;

  function aplicar(botao, estado) {
    botao.disabled = !estado.habilitado;
    botao.textContent = estado.habilitado ? botao.dataset.rotulo : estado.rotulo;
  }

  function ligar(manifesto) {
    document.querySelectorAll("[data-audio], [data-audio-sequencia]").forEach(function (botao) {
      if (!botao.dataset.rotulo) botao.dataset.rotulo = botao.textContent.trim();
      var arquivos = (botao.dataset.audio || botao.dataset.audioSequencia || "").split(/\s+/).filter(Boolean);
      var estados = arquivos.map(function (a) { return ICE.audio.estadoDoBotao(manifesto, a); });
      var todos = estados.length > 0 && estados.every(function (e) { return e.habilitado; });
      aplicar(botao, todos ? estados[0] : ICE.audio.estadoDoBotao(null, ""));
      if (botao.dataset.ligado) return;
      botao.dataset.ligado = "1";
      botao.addEventListener("click", function () { tocarFila(arquivos); });
    });
  }

  ICE.aoAbrirPagina(function () {
    parar();
    if (!document.querySelector("[data-audio], [data-audio-sequencia]")) return;
    ICE.json("audio/manifesto.json").then(ligar, function () { ligar(null); });
  });
})(globalThis.ICE = globalThis.ICE || {});
