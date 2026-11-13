/* Página "Treinar cartas" (#ice-treino): português na frente, a pessoa fala em inglês e confere. */
(function (ICE) {
  "use strict";

  function el(tag, classe, texto) {
    var e = document.createElement(tag);
    if (classe) e.className = classe;
    if (texto !== undefined) e.textContent = texto;
    return e;
  }

  function botao(texto, primario) {
    var b = el("button", "pp-botao" + (primario ? " pp-botao--primario" : ""), texto);
    b.type = "button";
    return b;
  }

  /* "va·CA·tion" com a sílaba em maiúsculas em negrito, sem usar innerHTML. */
  function silaba(texto) {
    var p = el("p", "pp-frase__silaba", "Sílaba forte: ");
    var palavra = el("span");
    palavra.lang = "en";
    texto.split("·").forEach(function (parte, i) {
      if (i > 0) palavra.appendChild(document.createTextNode("·"));
      palavra.appendChild(parte === parte.toUpperCase() && /[A-Z]/.test(parte) ? el("b", "", parte) : document.createTextNode(parte));
    });
    p.appendChild(palavra);
    return p;
  }

  function montar(alvo, cartas, manifesto, titulos) {
    var guarda = ICE.armazenamento.disponivel();
    var estado = ICE.treino.ler(ICE.armazenamento.ler(ICE.treino.CHAVE));
    var hoje = ICE.datas.iso(new Date());
    if (estado.novas.dia !== hoje) estado.novas = { dia: hoje, quantidade: 0 };

    var parametros = new URLSearchParams(location.search);
    var situacoes = [];
    cartas.forEach(function (c) { if (situacoes.indexOf(c.situacao) < 0) situacoes.push(c.situacao); });
    situacoes.sort(function (a, b) { return a - b; });
    var escolhida = Number(parametros.get("situacao")) || 0;
    if (situacoes.indexOf(escolhida) < 0) escolhida = 0;

    alvo.textContent = "";
    if (!guarda) alvo.appendChild(ICE.avisoSemArmazenamento());

    var rotulo = el("label", "ice-treino__filtro", "Cartas de ");
    var seletor = el("select");
    seletor.appendChild(new Option("todas as situações", "0"));
    situacoes.forEach(function (s) {
      var titulo = titulos && typeof titulos[String(s)] === "string" ? ": " + titulos[String(s)] : "";
      seletor.appendChild(new Option("Situação " + s + titulo, String(s)));
    });
    seletor.value = String(escolhida);
    rotulo.appendChild(seletor);
    alvo.appendChild(rotulo);

    var area = el("div", "ice-carta");
    alvo.appendChild(area);

    var porId = {};
    cartas.forEach(function (c) { porId[c.id] = c; });

    function salvar() {
      ICE.armazenamento.gravar(ICE.treino.CHAVE, JSON.stringify(estado));
    }

    function comecar() {
      var ids = cartas.filter(function (c) { return !escolhida || c.situacao === escolhida; })
                      .map(function (c) { return c.id; });
      var fila = ICE.treino.fila(ids, estado.cartas, hoje, estado.novas.quantidade);
      var repetidas = {};
      var feitas = 0;
      var total = fila.length;

      function fim() {
        area.textContent = "";
        area.appendChild(el("p", "ice-carta__pt",
          feitas ? "Treino de hoje feito. Volte amanhã." : "Nenhuma carta para hoje. Volte amanhã."));
      }

      function mostrar() {
        area.textContent = "";
        if (!fila.length) { fim(); return; }
        var carta = porId[fila[0]];
        area.appendChild(el("p", "ice-carta__progresso", "Carta " + (feitas + 1) + " de " + total));
        area.appendChild(el("p", "ice-carta__pt", carta.pt));
        area.appendChild(el("p", "ice-carta__dica", "Fale em inglês, em voz alta."));
        var revelar = botao("Mostrar a resposta", true);
        area.appendChild(revelar);
        revelar.addEventListener("click", function () {
          revelar.remove();
          var en = el("p", "ice-carta__en", carta.en);
          en.lang = "en";
          area.appendChild(en);
          if (carta.silaba) area.appendChild(silaba(carta.silaba));
          var acoes = el("div", "ice-carta__acoes");
          var ouvir = botao("Ouvir");
          var som = ICE.audio.estadoDoBotao(manifesto, carta.audio);
          ouvir.disabled = !som.habilitado;
          ouvir.textContent = som.rotulo;
          ouvir.addEventListener("click", function () { if (ICE.tocar) ICE.tocar([carta.audio]); });
          var acertei = botao("Acertei", true);
          var errei = botao("Errei");
          acoes.appendChild(ouvir);
          acoes.appendChild(acertei);
          acoes.appendChild(errei);
          area.appendChild(acoes);
          acertei.focus();
          function responder(acertou) {
            if (!estado.cartas[carta.id]) estado.novas.quantidade += 1;
            estado.cartas[carta.id] = ICE.treino.responder(estado.cartas[carta.id], acertou, hoje);
            salvar();
            fila.shift();
            if (!acertou && !repetidas[carta.id]) {
              repetidas[carta.id] = true;
              fila.push(carta.id);
              total += 1;
            }
            feitas += 1;
            mostrar();
          }
          acertei.addEventListener("click", function () { responder(true); });
          errei.addEventListener("click", function () { responder(false); });
        });
      }
      mostrar();
    }

    seletor.addEventListener("change", function () {
      escolhida = Number(seletor.value);
      comecar();
    });
    comecar();
  }

  ICE.aoAbrirPagina(function () {
    var alvo = document.getElementById("ice-treino");
    if (!alvo) return;
    alvo.textContent = "Carregando as cartas…";
    Promise.all([
      ICE.json("dados/cartas.json"),
      ICE.json("audio/manifesto.json").catch(function () { return null; }),
      ICE.json("dados/situacoes.json").catch(function () { return null; })
    ]).then(function (r) { montar(alvo, r[0], r[1], r[2]); }, function () {
      alvo.textContent = "Não foi possível carregar as cartas. Confira a conexão e recarregue a página.";
    });
  });
})(globalThis.ICE = globalThis.ICE || {});
