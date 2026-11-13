/* Núcleo do JavaScript do site: raiz do site, armazenamento seguro e gancho de troca de página.
   Os scripts extras rodam uma vez, no carregamento completo; a troca de página sem recarregar
   (navigation.instant) chama de novo as funções registradas em ICE.aoAbrirPagina. */
(function (ICE) {
  "use strict";

  /* Raiz do site calculada uma vez, enquanto o endereço ainda é o da página carregada. */
  var raiz = (function () {
    try {
      var config = JSON.parse(document.getElementById("__config").textContent);
      var url = new URL(config.base, location.href);
      if (!/\/$/.test(url.pathname)) url.pathname += "/";
      return url.href;
    } catch (e) {
      return new URL("./", location.href).href;
    }
  })();

  ICE.url = function (caminho) {
    return new URL(String(caminho).replace(/^\/+/, ""), raiz).href;
  };

  ICE.armazenamento = {
    disponivel: function () {
      try {
        var chave = "ice:teste";
        localStorage.setItem(chave, "1");
        localStorage.removeItem(chave);
        return true;
      } catch (e) {
        return false;
      }
    },
    ler: function (chave) {
      try {
        return localStorage.getItem(chave);
      } catch (e) {
        return null;
      }
    },
    gravar: function (chave, texto) {
      try {
        localStorage.setItem(chave, texto);
        return true;
      } catch (e) {
        return false;
      }
    }
  };

  var cacheJson = {};
  ICE.json = function (caminho) {
    if (!cacheJson[caminho]) {
      cacheJson[caminho] = fetch(ICE.url(caminho), { cache: "no-cache" }).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      });
      cacheJson[caminho].catch(function () { delete cacheJson[caminho]; });
    }
    return cacheJson[caminho];
  };

  ICE.aoAbrirPagina = function (fn) {
    var rodar = function () {
      try { fn(); } catch (e) { if (window.console) console.error(e); }
    };
    if (window.document$ && typeof window.document$.subscribe === "function") {
      window.document$.subscribe(rodar);
    } else if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", rodar);
    } else {
      rodar();
    }
  };

  ICE.avisoSemArmazenamento = function () {
    var p = document.createElement("p");
    p.className = "pp-aviso-armazenamento";
    p.setAttribute("role", "status");
    p.textContent = "Seu navegador não está guardando o progresso: o que você marcar vale só para esta visita.";
    return p;
  };
})(globalThis.ICE = globalThis.ICE || {});
