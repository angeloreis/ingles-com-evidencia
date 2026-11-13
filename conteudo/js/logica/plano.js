/* Plano da trilha: em que semana e dia a pessoa está, passos do dia e dias concluídos. Lógica pura.
   Estado guardado no aparelho: {versao: 1, inicio: "AAAA-MM-DD" | null, feitos: {"s1d2": [ordens]}}. */
(function (ICE) {
  "use strict";

  ICE.plano = {
    chave: function (trilha) { return "ice:plano:" + trilha + ":v1"; },

    ler: function (texto) {
      var vazio = { versao: 1, inicio: null, feitos: {} };
      if (texto === null || texto === undefined) return vazio;
      try {
        var estado = JSON.parse(texto);
        if (!estado || estado.versao !== 1 || typeof estado.feitos !== "object") return vazio;
        return estado;
      } catch (e) {
        return vazio;
      }
    },

    posicao: function (inicio, hoje, totalSemanas) {
      var d = Math.max(0, ICE.datas.diasEntre(inicio, hoje)); // relógio que voltou conta como o 1º dia
      var semana = Math.floor(d / 7) + 1;
      return { semana: semana, dia: (d % 7) + 1, terminou: semana > totalSemanas };
    },

    inicioParaSemana: function (hoje, semana) {
      return ICE.datas.somarDias(hoje, -(semana - 1) * 7);
    },

    passosDoDia: function (plano, semana, dia) {
      return plano.passos
        .filter(function (p) { return p.semana === semana && p.dia === dia; })
        .sort(function (a, b) { return a.ordem - b.ordem; });
    },

    diasConcluidos: function (plano, feitos) {
      var dias = {};
      plano.passos.forEach(function (p) {
        var chave = "s" + p.semana + "d" + p.dia;
        (dias[chave] = dias[chave] || []).push(p.ordem);
      });
      return Object.keys(dias).filter(function (chave) {
        var marcados = feitos[chave] || [];
        return dias[chave].every(function (ordem) { return marcados.indexOf(ordem) >= 0; });
      }).length;
    },

    totalDeDias: function (plano) {
      var dias = {};
      plano.passos.forEach(function (p) { dias["s" + p.semana + "d" + p.dia] = true; });
      return Object.keys(dias).length;
    }
  };
})(globalThis.ICE = globalThis.ICE || {});
