"use strict";
(async function () {
  const root = document.getElementById("root");
  try {
    const [sources, catalog, catalogTypes, catalogFields] = await Promise.all([
      fetch("data/sources.json").then(check).then(r => r.json()),
      fetch("data/catalog.json").then(check).then(r => r.json()),
      fetch("data/catalog-types.json").then(check).then(r => r.json()),
      fetch("data/catalog-fields.json").then(check).then(r => r.json())
    ]);

    window.IPBL_DATA = { sources, catalog, catalogTypes, catalogFields };

    await loadScript("js/app.bundle.js");
    await loadScript("js/tooltip.js");
  } catch (error) {
    console.error("Nie udało się uruchomić aplikacji iPBL:", error);
    if (root) {
      root.innerHTML = '<div style="max-width:760px;margin:80px auto;padding:24px;font:16px/1.5 Arial,sans-serif;background:#fff;border:1px solid #d9cfc0;border-radius:12px">' +
        '<h1 style="font-size:24px;margin-top:0">Nie udało się wczytać aplikacji iPBL</h1>' +
        '<p>Wersja modułowa musi być uruchamiana przez serwer WWW (np. GitHub Pages), a nie bezpośrednio przez dwukrotne kliknięcie pliku <code>index.html</code>.</p>' +
        '<p>Do pracy lokalnej uruchom <code>tools\\start_local.bat</code> w Windows albo <code>python -m http.server 8000</code> w katalogu aplikacji.</p>' +
        '</div>';
    }
  }

  function check(response) {
    if (!response.ok) throw new Error(response.status + " " + response.statusText + " — " + response.url);
    return response;
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = src;
      script.onload = resolve;
      script.onerror = () => reject(new Error("Nie udało się wczytać: " + src));
      document.body.appendChild(script);
    });
  }
})();
