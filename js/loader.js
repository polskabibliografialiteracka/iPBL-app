"use strict";
(async function () {
  const root = document.getElementById("root");
  try {
    const [sources,catalog,catalogTypes,catalogFields,config] = await Promise.all([
      fetch("data/sources.json").then(check).then(r=>r.json()),
      fetch("data/catalog.json").then(check).then(r=>r.json()),
      fetch("data/catalog-types.json").then(check).then(r=>r.json()),
      fetch("data/catalog-fields.json").then(check).then(r=>r.json()),
      fetch("config/app.json").then(check).then(r=>r.json())
    ]);
    window.IPBL_DATA={sources,catalog,catalogTypes,catalogFields};
    window.IPBL_CONFIG=config;
    await loadScript("js/search-utils.js");
    await loadScript("js/app.bundle.js");
    await loadScript("js/tooltip.js");
  } catch(error) {
    console.error("Nie udało się uruchomić aplikacji iPBL:",error);
    if(root)root.innerHTML='<div style="max-width:760px;margin:80px auto;padding:24px;font:16px/1.5 Arial,sans-serif;background:#fff;border:1px solid #d9cfc0;border-radius:12px">'+
      '<h1 style="font-size:24px;margin-top:0">Nie udało się wczytać aplikacji iPBL</h1>'+
      '<p>Wersja modułowa wymaga serwera WWW (np. GitHub Pages), a nie dwukrotnego kliknięcia index.html.</p>'+
      '<p>Lokalnie uruchom tools/start_local.bat lub python -m http.server 8000.</p></div>';
  }
  function check(response) {
    if(!response.ok)throw new Error(response.status+" "+response.statusText+" — "+response.url);
    return response;
  }
  function loadScript(src) {
    return new Promise((resolve,reject)=>{
      const script=document.createElement("script");
      script.src=src;
      script.onload=resolve;
      script.onerror=()=>reject(new Error("Nie udało się wczytać: "+src));
      document.body.appendChild(script);
    });
  }
})();
