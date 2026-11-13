/* Ficha de progresso semanal da trilha. Lógica pura.
   Estado: {versao: 1, semanas: {"1": {gravacao, tempo4, tempo3, tempo2, conversa, confianca}}}.
   Os tempos chegam ao registrar já em segundos (veja ICE.ficha.tempo). */
(function (ICE) {
  "use strict";

  /* Objeto de verdade: typeof null também é "object" (M11 da 1A). */
  function objeto(x) { return x !== null && typeof x === "object"; }

  var ERRO_TEMPO = "Use só números: até 2 algarismos nos minutos e de 0 a 59 nos segundos.";

  function segundos(valor) {
    return typeof valor === "number" && isFinite(valor) && valor >= 0 ? Math.round(valor) : null;
  }

  function data(texto) {
    var m = /^([0-9]{4})-([0-9]{2})-([0-9]{2})$/.exec(String(texto || ""));
    return m ? m[0] : null;
  }

  ICE.ficha = {
    chave: function (trilha) { return "ice:ficha:" + trilha + ":v1"; },

    ler: function (texto) {
      var vazio = { versao: 1, semanas: {} };
      if (texto === null || texto === undefined) return vazio;
      try {
        var estado = JSON.parse(texto);
        if (!objeto(estado) || estado.versao !== 1 || !objeto(estado.semanas)) return vazio;
        return estado;
      } catch (e) {
        return vazio;
      }
    },

    registrar: function (estado, semana, campos) {
      var confianca = /^[1-5]$/.test(String(campos.confianca)) ? Number(campos.confianca) : null;
      var semanas = {};
      Object.keys(estado.semanas).forEach(function (k) { semanas[k] = estado.semanas[k]; });
      semanas[String(semana)] = {
        gravacao: data(campos.gravacao),
        tempo4: segundos(campos.tempo4),
        tempo3: segundos(campos.tempo3),
        tempo2: segundos(campos.tempo2),
        conversa: campos.conversa === true,
        confianca: confianca
      };
      return { versao: 1, semanas: semanas };
    },

    /* Tempo em dois campos de texto (minutos, segundos). Os dois vazios: sem tempo.
       Um só vazio conta como zero. */
    tempo: function (minutos, segs) {
      var m = String(minutos === null || minutos === undefined ? "" : minutos).trim();
      var s = String(segs === null || segs === undefined ? "" : segs).trim();
      if (!m && !s) return { segundos: null, erro: null };
      if (!/^[0-9]{0,2}$/.test(m) || !/^[0-9]{0,2}$/.test(s) || Number(s) > 59) {
        return { segundos: null, erro: ERRO_TEMPO };
      }
      return { segundos: Number(m || 0) * 60 + Number(s || 0), erro: null };
    },

    formatarTempo: function (s) {
      if (s === null || s === undefined) return "—";
      return Math.floor(s / 60) + ":" + (s % 60 < 10 ? "0" : "") + (s % 60);
    }
  };
})(globalThis.ICE = globalThis.ICE || {});
