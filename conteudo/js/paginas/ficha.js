/* Ficha de progresso (#ice-ficha[data-trilha]): um registro por semana, só no aparelho. */
(function (ICE) {
  "use strict";

  function el(tag, classe, texto) {
    var e = document.createElement(tag);
    if (classe) e.className = classe;
    if (texto !== undefined) e.textContent = texto;
    return e;
  }

  function campo(rotuloTexto, entrada) {
    var rotulo = el("label", "ice-ficha__campo");
    rotulo.appendChild(el("span", "", rotuloTexto));
    rotulo.appendChild(entrada);
    return rotulo;
  }

  function dois(n) { return (n < 10 ? "0" : "") + n; }

  /* Tempo em dois campos só de números: o teclado numérico do celular não tem ":". */
  function campoTempo(legenda, idErro) {
    var grupo = el("fieldset", "ice-ficha__tempo");
    grupo.appendChild(el("legend", "", legenda));
    var linha = el("div", "ice-ficha__tempo-linha");
    function unidade(nome) {
      var entrada = el("input");
      entrada.type = "text";
      entrada.inputMode = "numeric";
      entrada.pattern = "[0-9]*";
      entrada.maxLength = 2;
      entrada.autocomplete = "off";
      entrada.setAttribute("aria-describedby", idErro);
      var rotulo = el("label", "ice-ficha__unidade");
      rotulo.appendChild(entrada);
      rotulo.appendChild(el("span", "", nome));
      linha.appendChild(rotulo);
      return entrada;
    }
    var tempo = { grupo: grupo, minutos: unidade("min"), segs: unidade("seg"), erro: el("p", "ice-ficha__erro") };
    tempo.erro.id = idErro;
    tempo.erro.hidden = true;
    grupo.appendChild(linha);
    grupo.appendChild(tempo.erro);
    grupo.addEventListener("input", function () { marcarErro(tempo, null); });
    return tempo;
  }

  function marcarErro(tempo, mensagem) {
    [tempo.minutos, tempo.segs].forEach(function (e) {
      if (mensagem) e.setAttribute("aria-invalid", "true");
      else e.removeAttribute("aria-invalid");
    });
    tempo.erro.textContent = mensagem || "";
    tempo.erro.hidden = !mensagem;
  }

  function mostrarTempo(tempo, s) {
    tempo.minutos.value = s != null ? String(Math.floor(s / 60)) : "";
    tempo.segs.value = s != null ? dois(s % 60) : "";
    marcarErro(tempo, null);
  }

  ICE.aoAbrirPagina(function () {
    var alvo = document.getElementById("ice-ficha");
    if (!alvo) return;
    var trilha = alvo.dataset.trilha;
    var chave = ICE.ficha.chave(trilha);
    var guarda = ICE.armazenamento.disponivel();
    var estado = ICE.ficha.ler(ICE.armazenamento.ler(chave));
    var plano = ICE.plano.ler(ICE.armazenamento.ler(ICE.plano.chave(trilha)));
    var semanaAtual = 1;
    if (plano.inicio) {
      semanaAtual = Math.min(12, ICE.plano.posicao(plano.inicio, ICE.datas.iso(new Date()), 12).semana);
    }

    alvo.textContent = "";
    alvo.classList.add("ice-ficha");
    if (!guarda) alvo.appendChild(ICE.avisoSemArmazenamento());

    var form = el("form", "ice-ficha__form");
    var semana = el("select");
    for (var s = 1; s <= 12; s++) semana.appendChild(new Option("Semana " + s, String(s)));
    semana.value = String(semanaAtual);
    var gravacao = el("input");
    gravacao.type = "date";
    var t4 = campoTempo("4/3/2 — quanto você falou na rodada de 4 min", "ice-ficha-erro-4");
    var t3 = campoTempo("Rodada de 3 min", "ice-ficha-erro-3");
    var t2 = campoTempo("Rodada de 2 min", "ice-ficha-erro-2");
    var conversa = el("input");
    conversa.type = "checkbox";
    var confianca = el("select");
    confianca.appendChild(new Option("Escolha", ""));
    ["1 — nada confiante", "2", "3", "4", "5 — muito confiante"].forEach(function (texto, i) {
      confianca.appendChild(new Option(texto, String(i + 1)));
    });

    form.appendChild(campo("Semana", semana));
    form.appendChild(campo("Data da gravação da voz", gravacao));
    form.appendChild(t4.grupo);
    form.appendChild(t3.grupo);
    form.appendChild(t2.grupo);
    var rotuloConversa = el("label", "ice-ficha__campo ice-ficha__marcar");
    rotuloConversa.appendChild(conversa);
    rotuloConversa.appendChild(el("span", "", "Fiz uma conversa real nesta semana"));
    form.appendChild(rotuloConversa);
    form.appendChild(campo("Confiança para falar (1 a 5)", confianca));
    var salvar = el("button", "pp-botao pp-botao--primario", "Salvar a semana");
    salvar.type = "submit";
    form.appendChild(salvar);
    var situacao = el("p", "ice-ficha__status");
    situacao.setAttribute("role", "status");
    form.appendChild(situacao);
    alvo.appendChild(form);

    var tabela = el("table", "pp-tabela");
    alvo.appendChild(tabela);

    function preencher() {
      var r = estado.semanas[semana.value] || {};
      gravacao.value = r.gravacao || "";
      mostrarTempo(t4, r.tempo4);
      mostrarTempo(t3, r.tempo3);
      mostrarTempo(t2, r.tempo2);
      conversa.checked = !!r.conversa;
      confianca.value = r.confianca ? String(r.confianca) : "";
    }

    function desenharTabela() {
      tabela.textContent = "";
      var semanas = Object.keys(estado.semanas).map(Number).sort(function (a, b) { return a - b; });
      if (!semanas.length) return;
      var colunas = ["Semana", "Gravação", "4 min", "3 min", "2 min", "Conversa real", "Confiança"];
      var cabeca = el("thead");
      var linha = el("tr");
      colunas.forEach(function (c) { linha.appendChild(el("th", "", c)); });
      cabeca.appendChild(linha);
      tabela.appendChild(cabeca);
      var corpo = el("tbody");
      semanas.forEach(function (s) {
        var r = estado.semanas[String(s)];
        var valores = [String(s), r.gravacao || "—", ICE.ficha.formatarTempo(r.tempo4),
                       ICE.ficha.formatarTempo(r.tempo3), ICE.ficha.formatarTempo(r.tempo2),
                       r.conversa ? "Sim" : "Não", r.confianca ? String(r.confianca) : "—"];
        var tr = el("tr");
        valores.forEach(function (v, i) {
          var td = el("td", "", v);
          td.setAttribute("data-rotulo", colunas[i]);
          tr.appendChild(td);
        });
        corpo.appendChild(tr);
      });
      tabela.appendChild(corpo);
    }

    semana.addEventListener("change", function () {
      situacao.textContent = "";
      preencher();
    });
    form.addEventListener("submit", function (evento) {
      evento.preventDefault();
      var tempos = [t4, t3, t2].map(function (t) {
        var lido = ICE.ficha.tempo(t.minutos.value, t.segs.value);
        marcarErro(t, lido.erro);
        return lido;
      });
      var primeiroErro = tempos.findIndex(function (lido) { return lido.erro; });
      if (primeiroErro >= 0) {
        situacao.textContent = "Nada foi salvo: confira o tempo marcado.";
        [t4, t3, t2][primeiroErro].minutos.focus();
        return;
      }
      estado = ICE.ficha.registrar(estado, Number(semana.value), {
        gravacao: gravacao.value, tempo4: tempos[0].segundos, tempo3: tempos[1].segundos,
        tempo2: tempos[2].segundos, conversa: conversa.checked, confianca: confianca.value
      });
      ICE.armazenamento.gravar(chave, JSON.stringify(estado));
      preencher();
      desenharTabela();
      situacao.textContent = "Semana " + semana.value + " salva.";
    });
    preencher();
    desenharTabela();
  });
})(globalThis.ICE = globalThis.ICE || {});
