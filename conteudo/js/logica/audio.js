/* Estado dos botões "Ouvir" a partir do manifesto dos áudios gerados. Lógica pura. */
(function (ICE) {
  "use strict";

  ICE.audio = {
    estadoDoBotao: function (manifesto, arquivo) {
      var tem = !!(manifesto && Object.prototype.hasOwnProperty.call(manifesto, arquivo) && manifesto[arquivo]);
      return tem ? { habilitado: true, rotulo: "Ouvir" } : { habilitado: false, rotulo: "Sem áudio aqui" };
    }
  };
})(globalThis.ICE = globalThis.ICE || {});
