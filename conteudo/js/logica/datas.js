/* Datas no formato "AAAA-MM-DD", sempre pelo calendário local do aparelho.
   Lógica pura: não toca em window nem em document (testada no pytest). */
(function (ICE) {
  "use strict";

  function doisDigitos(n) {
    return (n < 10 ? "0" : "") + n;
  }

  function partes(iso) {
    var p = String(iso).split("-");
    return [Number(p[0]), Number(p[1]), Number(p[2])];
  }

  ICE.datas = {
    /* Data local (não UTC): depois das 21h no Brasil, toISOString() já seria o dia seguinte. */
    iso: function (d) {
      return d.getFullYear() + "-" + doisDigitos(d.getMonth() + 1) + "-" + doisDigitos(d.getDate());
    },
    somarDias: function (iso, n) {
      var p = partes(iso);
      return ICE.datas.iso(new Date(p[0], p[1] - 1, p[2] + n, 12));
    },
    /* Diferença em dias de calendário, imune ao horário de verão. */
    diasEntre: function (isoA, isoB) {
      var a = partes(isoA), b = partes(isoB);
      return Math.round((Date.UTC(b[0], b[1] - 1, b[2]) - Date.UTC(a[0], a[1] - 1, a[2])) / 86400000);
    }
  };
})(globalThis.ICE = globalThis.ICE || {});
