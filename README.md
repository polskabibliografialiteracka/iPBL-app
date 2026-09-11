# iPBL app — wersja modułowa v0.3

To jest **bezpiecznie rozdzielona wersja aktualnej aplikacji iPBL**. Jej wygląd i logika zostały zachowane, ale ciężkie dane i zasoby nie siedzą już w jednym pliku HTML.

## Najważniejszy podział

```text
iPBL_app_modular_v0.3/
├── index.html                 # mały, czytelny punkt wejścia
├── css/
│   └── style.css              # cały wygląd aplikacji
├── js/
│   ├── loader.js              # ładuje dane i uruchamia aplikację
│   ├── app.bundle.js          # skompilowana logika obecnej aplikacji
│   ├── tooltip.js             # dymki informacyjne
│   └── analytics.js           # Google Analytics
├── data/
│   ├── sources.json           # 203 źródła z rekordami bibliograficznymi
│   ├── catalog.json           # 4003 pozycje Wykazu internetowych źródeł literackich
│   ├── catalog-types.json     # dane do filtrów/statystyk typów
│   ├── catalog-fields.json    # dane do filtrów/statystyk dziedzin
│   └── records.zip            # właściwe rekordy BibTeX używane przez aplikację
├── assets/
│   ├── iPBL_logo.png
│   ├── ibl_pan_logo.png
│   ├── pbl_logo.png
│   └── nprh_logo.png
├── tools/
│   ├── start_local.bat        # uruchomienie lokalne w Windows
│   ├── start_local.sh         # uruchomienie lokalne Linux/macOS
│   └── build_standalone.py    # buduje ponownie wersję jednoplikową
└── release/
    └── ...                    # tu powstaje samodzielny HTML
```

## Co zmieniono względem jednego HTML-a?

1. Metadane źródeł i katalog 4000 źródeł zostały wyjęte z kodu JavaScript do osobnych plików JSON.
2. Paczka z rekordami BibTeX została wyjęta z kodu do `data/records.zip`.
3. CSS został wyjęty do `css/style.css`.
4. Logotypy zostały wyjęte z base64 do `assets/`.
5. Dymki informacyjne i Analytics są osobnymi skryptami.
6. `index.html` jest mały i można go przeczytać bez przedzierania się przez kilkanaście megabajtów kodu.

## Ważne: `app.bundle.js`

`js/app.bundle.js` nadal jest **skompilowanym kodem obecnej aplikacji React**. Rozdzielenie go na prawdziwe moduły typu `search.js`, `analysis.js`, `records.js` i `export.js` wymaga osobnego refaktoringu kodu źródłowego. Celowo nie robiłem tego automatycznie w tej paczce, aby nie popsuć działającej wersji aplikacji.

To jest więc pierwszy, bezpieczny etap: **dane, rekordy, wygląd, zasoby i dodatki są już rozdzielone**, a działająca logika pozostaje nietknięta.

## Uruchamianie

### GitHub Pages

Cały katalog można umieścić w repozytorium. `index.html` pozostaje w katalogu głównym i GitHub Pages obsłuży go bez dodatkowej konfiguracji.

### Lokalnie w Windows

Uruchom:

```text
tools\start_local.bat
```

Powinna otworzyć się strona `http://localhost:8000`.

Nie należy uruchamiać wersji modułowej przez samo dwukrotne kliknięcie `index.html`, ponieważ przeglądarki blokują lokalne `fetch()` do plików JSON/ZIP.

## Jak zrobić ponownie wersję „jeden plik”?

W katalogu aplikacji uruchom:

```bash
python tools/build_standalone.py
```

Skrypt utworzy:

```text
release/iPBL_app_standalone.html
```

Ta wersja ponownie zawiera dane, ZIP i logotypy w środku i może być otwierana jako pojedynczy plik HTML.

## Co edytować najczęściej?

- zmiana wyglądu → `css/style.css`
- podmiana danych źródeł → `data/sources.json`
- podmiana katalogu 4000 → `data/catalog.json`
- podmiana rekordów → `data/records.zip`
- dymki → `js/tooltip.js`
- logotypy → `assets/`

## Kolejny sensowny etap

Następnym krokiem może być przebudowanie `app.bundle.js` do czytelnego katalogu źródłowego, np. `src/search.js`, `src/records.js`, `src/analysis.js`, `src/export.js`, `src/ui.js`. To już warto robić świadomie i testować funkcję po funkcji, zamiast automatycznie rozcinać zminifikowany bundle.
