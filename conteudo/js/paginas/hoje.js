/* Página "Hoje" (#ice-hoje[data-trilha]): os passos do dia, guardados só no aparelho. */
(function (ICE) {
  "use strict";

  var AVISO = "O progresso fica só neste aparelho: trocar de aparelho ou limpar o navegador zera tudo.";

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

  function montar(alvo, trilha, plano) {
    var chave = ICE.plano.chave(trilha);
    var guarda = ICE.armazenamento.disponivel();
    var estado = ICE.plano.ler(ICE.armazenamento.ler(chave));
    var hoje = ICE.datas.iso(new Date());

    function salvar() { ICE.armazenamento.gravar(chave, JSON.stringify(estado)); }

    function rodape() {
      var p = el("p", "ice-hoje__rodape");
      p.appendChild(document.createTextNode(AVISO + " "));
      var semanas = el("a", "", "Ver todas as semanas");
      semanas.href = ICE.url("trilhas/" + trilha + "/");
      p.appendChild(semanas);
      alvo.appendChild(p);
      if (estado.inicio) {
        var recomecar = botao("Recomeçar o plano");
        recomecar.addEventListener("click", function () {
          if (window.confirm("Apagar o progresso deste aparelho e escolher de novo o começo do plano?")) {
            estado = { versao: 1, inicio: null, feitos: {} };
            salvar();
            desenhar();
          }
        });
        alvo.appendChild(recomecar);
      }
    }

    function escolherInicio() {
      alvo.appendChild(el("p", "", "Escolha quando o plano começa para você. O site calcula o dia do plano a partir dessa data."));
      var acoes = el("div", "ice-carta__acoes");
      var hojeBotao = botao("Começar hoje", true);
      hojeBotao.addEventListener("click", function () {
        estado.inicio = hoje;
        salvar();
        desenhar();
      });
      acoes.appendChild(hojeBotao);
      alvo.appendChild(acoes);

      var rotulo = el("label", "ice-treino__filtro", "Já estou na semana ");
      var seletor = el("select");
      for (var s = 1; s <= plano.semanas; s++) seletor.appendChild(new Option(String(s), String(s)));
      rotulo.appendChild(seletor);
      var continuar = botao("Continuar dessa semana");
      continuar.addEventListener("click", function () {
        estado.inicio = ICE.plano.inicioParaSemana(hoje, Number(seletor.value));
        salvar();
        desenhar();
      });
      rotulo.appendChild(continuar);
      alvo.appendChild(rotulo);
    }

    /* Semana atual depois da última publicada: repetir a última ou seguir no treino (M9 da 1A). */
    function depoisDaUltima(ultima) {
      var faltam = ultima + 1 === plano.semanas
        ? "A semana " + plano.semanas + " ainda não foi publicada."
        : "As semanas " + (ultima + 1) + " a " + plano.semanas + " ainda não foram publicadas.";
      alvo.appendChild(el("p", "ice-carta__pt",
        faltam + " Enquanto isso, repita a semana " + ultima + " ou siga no treino de cartas."));
      var acoes = el("div", "ice-carta__acoes");
      var repetir = botao("Repetir a semana " + ultima, true);
      repetir.addEventListener("click", function () {
        estado.inicio = ICE.plano.inicioParaSemana(hoje, ultima);
        Object.keys(estado.feitos).forEach(function (chaveDia) {
          if (chaveDia.indexOf("s" + ultima + "d") === 0) delete estado.feitos[chaveDia];
        });
        salvar();
        desenhar();
      });
      acoes.appendChild(repetir);
      var treinar = el("a", "pp-botao", "Treinar as cartas");
      treinar.href = ICE.url("treinar/");
      acoes.appendChild(treinar);
      alvo.appendChild(acoes);
    }

    function dia() {
      var pos = ICE.plano.posicao(estado.inicio, hoje, plano.semanas);
      if (pos.terminou) {
        if (ICE.plano.depoisDoPublicado(plano, pos.semana)) { depoisDaUltima(ICE.plano.ultimaSemana(plano)); return; }
        alvo.appendChild(el("p", "ice-carta__pt", "Você chegou ao fim das " + plano.semanas + " semanas."));
        return;
      }
      alvo.appendChild(el("h2", "", "Semana " + pos.semana + ", dia " + pos.dia));
      var passos = ICE.plano.passosDoDia(plano, pos.semana, pos.dia);
      if (!passos.length) {
        if (ICE.plano.depoisDoPublicado(plano, pos.semana)) { depoisDaUltima(ICE.plano.ultimaSemana(plano)); return; }
        var semanaTem = plano.passos.some(function (p) { return p.semana === pos.semana; });
        alvo.appendChild(el("p", "ice-carta__pt",
          semanaTem ? "Dia de descanso." : "Esta semana do plano ainda não foi publicada."));
        return;
      }
      var chaveDia = "s" + pos.semana + "d" + pos.dia;
      var feitos = estado.feitos[chaveDia] = estado.feitos[chaveDia] || [];
      var minutos = passos.reduce(function (t, p) { return t + p.minutos; }, 0);
      alvo.appendChild(el("h3", "", minutos + " minutos de treino"));

      var barra = el("div", "pp-progresso");
      barra.setAttribute("role", "img");
      var preenchido = el("span");
      barra.appendChild(preenchido);
      alvo.appendChild(barra);
      function atualizarBarra() {
        var total = ICE.plano.totalDeDias(plano);
        var feitosDias = ICE.plano.diasConcluidos(plano, estado.feitos);
        barra.setAttribute("aria-label", feitosDias + " de " + total + " dias concluídos");
        preenchido.style.width = (total ? Math.round(100 * feitosDias / total) : 0) + "%";
      }

      var lista = el("ol", "pp-passos");
      var caixas = [];
      passos.forEach(function (p) {
        var li = el("li");
        var id = "passo-" + pos.semana + "-" + pos.dia + "-" + p.ordem;
        var caixa = el("input");
        caixa.type = "checkbox";
        caixa.id = id;
        caixa.checked = feitos.indexOf(p.ordem) >= 0;
        var rotulo = el("label");
        rotulo.htmlFor = id;
        var texto = el("span", "pp-passos__texto");
        if (p.link) {
          var a = el("a", "", p.passo);
          a.href = ICE.url(p.link);
          texto.appendChild(a);
        } else {
          texto.textContent = p.passo;
        }
        rotulo.appendChild(texto);
        rotulo.appendChild(el("span", "pp-passos__tempo", p.minutos + " min"));
        caixa.addEventListener("change", function () {
          var i = feitos.indexOf(p.ordem);
          if (caixa.checked && i < 0) feitos.push(p.ordem);
          if (!caixa.checked && i >= 0) feitos.splice(i, 1);
          salvar();
          atualizarBarra();
        });
        li.appendChild(caixa);
        li.appendChild(rotulo);
        lista.appendChild(li);
        caixas.push(caixa);
      });
      alvo.appendChild(lista);
      var proximo = botao("Marcar o próximo passo", true);
      proximo.addEventListener("click", function () {
        var aberta = caixas.filter(function (c) { return !c.checked; })[0];
        if (aberta) {
          aberta.checked = true;
          aberta.dispatchEvent(new Event("change"));
        }
      });
      alvo.appendChild(proximo);
      atualizarBarra();
    }

    function desenhar() {
      alvo.textContent = "";
      if (!guarda) alvo.appendChild(ICE.avisoSemArmazenamento());
      if (!estado.inicio) escolherInicio(); else dia();
      rodape();
    }
    desenhar();
  }

  ICE.aoAbrirPagina(function () {
    var alvo = document.getElementById("ice-hoje");
    if (!alvo) return;
    var trilha = alvo.dataset.trilha;
    alvo.textContent = "Carregando o plano…";
    ICE.json("dados/" + trilha + ".json").then(function (plano) { montar(alvo, trilha, plano); }, function () {
      alvo.textContent = "O plano desta trilha ainda não foi publicado.";
    });
  });
})(globalThis.ICE = globalThis.ICE || {});
