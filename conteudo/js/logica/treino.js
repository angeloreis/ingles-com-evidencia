/* Treino de cartas com caixas (sistema de Leitner). Lógica pura, testada no pytest.
   Estado guardado no aparelho: {versao: 1, cartas: {id: {caixa, proxima}}, novas: {dia, quantidade}}.
   Caixa 0: carta errada, volta no mesmo dia. */
(function (ICE) {
  "use strict";

  var INTERVALOS = { 1: 1, 2: 3, 3: 7, 4: 14, 5: 30 }; // dias até a carta voltar
  var LIMITE_NOVAS = 10; // cartas novas por dia

  function estadoVazio() {
    return { versao: 1, cartas: {}, novas: { dia: null, quantidade: 0 } };
  }

  ICE.treino = {
    INTERVALOS: INTERVALOS,
    LIMITE_NOVAS: LIMITE_NOVAS,
    CHAVE: "ice:treino:v1",
    estadoVazio: estadoVazio,

    ler: function (texto) {
      if (texto === null || texto === undefined) return estadoVazio();
      try {
        var estado = JSON.parse(texto);
        if (!estado || estado.versao !== 1 || typeof estado.cartas !== "object" || !estado.novas) {
          return estadoVazio();
        }
        return estado;
      } catch (e) {
        return estadoVazio();
      }
    },

    /* Errar leva a carta para a caixa 0 (volta hoje): o acerto seguinte a põe na caixa 1,
       igual a uma carta acertada de primeira. */
    responder: function (estadoCarta, acertou, hoje) {
      if (!acertou) return { caixa: 0, proxima: hoje };
      var caixa = Math.min(((estadoCarta && estadoCarta.caixa) || 0) + 1, 5);
      return { caixa: caixa, proxima: ICE.datas.somarDias(hoje, INTERVALOS[caixa]) };
    },

    /* Primeiro as vencidas (pela data, depois pela ordem do arquivo); depois as novas até o limite do dia. */
    fila: function (ids, cartas, hoje, novasHoje, limite) {
      if (limite === undefined || limite === null) limite = LIMITE_NOVAS;
      var posicao = {};
      ids.forEach(function (id, i) { posicao[id] = i; });
      var vencidas = ids.filter(function (id) { return cartas[id] && cartas[id].proxima <= hoje; });
      vencidas.sort(function (a, b) {
        if (cartas[a].proxima !== cartas[b].proxima) return cartas[a].proxima < cartas[b].proxima ? -1 : 1;
        return posicao[a] - posicao[b];
      });
      var novas = ids.filter(function (id) { return !cartas[id]; }).slice(0, Math.max(0, limite - novasHoje));
      return vencidas.concat(novas);
    }
  };
})(globalThis.ICE = globalThis.ICE || {});
