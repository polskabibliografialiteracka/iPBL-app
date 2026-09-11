<p align="center">
  <img src="assets/iPBL_logo.png" alt="iPBL" width="260">
</p>

# iPBL – aplikacja do analizy polskiego internetu literackiego

Aplikacja iPBL służy do analizy i wizualizacji danych bibliograficznych zgromadzonych w kolekcji **iPBL – polski internet literacki**.

<p align="center">
  <strong><a href="https://polskabibliografialiteracka.github.io/iPBL-app/">▶ Uruchom aplikację</a></strong>
  &nbsp;·&nbsp;
  <a href="https://github.com/polskabibliografialiteracka/iPBL-app">Repozytorium</a>
  &nbsp;·&nbsp;
  <a href="https://literarybibliography.eu/en/projects/ipbl">Dane iPBL</a>
  &nbsp;·&nbsp;
  <a href="https://pbl.ibl.waw.pl/">Polska Bibliografia Literacka</a>
</p>

## Projekt i finansowanie

Aplikacja iPBL została stworzona z wykorzystaniem danych opracowanych w ramach projektu **„Bibliografia polskiej internetowej kultury cyfrowej wraz z katalogiem źródeł i archiwum – uzupełnienie Polskiej Bibliografii Literackiej”**, finansowanego przez Narodowy Program Rozwoju Humanistyki (NPRH).

Projekt był realizowany przez Pracownię Bibliografii Bieżącej Instytutu Badań Literackich PAN w latach **2023–2026**. Więcej informacji na temat projektu można znaleźć w sekcji aktualności strony [Polskiej Bibliografii Literackiej (PBL)](https://pbl.ibl.waw.pl/).

## O aplikacji

Kolekcja iPBL gromadzi dane dotyczące polskiego internetu literackiego, w tym publikacji, autorów, źródeł i innych informacji bibliograficznych.

Celem aplikacji jest udostępnienie wybranych danych w formie interaktywnej i ułatwienie ich eksploracji osobom zainteresowanym polską kulturą literacką i cyfrową.

W aktualnej wersji użytkownik może korzystać z podstawowych analiz danych bibliograficznych, m.in. dotyczących:

- autorów,
- publikacji,
- źródeł internetowych,
- chronologii danych,
- wybranych charakterystyk zgromadzonego materiału.

## Dane

Dane prezentowane w aplikacji są wynikiem prac dokumentacyjnych i bibliograficznych prowadzonych przez zespół Polskiej Bibliografii Literackiej. Aplikacja nie zastępuje procesu opracowania bibliograficznego – stanowi narzędzie służące do dalszej analizy i prezentacji zgromadzonych danych.

Dane zgromadzone w kolekcji iPBL można pobrać ze strony Europejskiej Bibliografii Literackiej:

**[Pobierz / zobacz dane iPBL w ELB](https://literarybibliography.eu/en/projects/ipbl)**

## Wersja 0.3 – zmiana struktury aplikacji

Od wersji **0.3** aplikacja jest rozwijana w strukturze modułowej. Wcześniej kod, style, zasoby graficzne i duża część danych znajdowały się w jednym pliku HTML. Obecnie zostały rozdzielone na osobne katalogi i pliki, dzięki czemu repozytorium jest prostsze w utrzymaniu i łatwiej aktualizować dane bez ingerowania w cały kod aplikacji.

Najważniejsze zmiany:

1. metadane źródeł i katalog internetowych źródeł literackich zostały przeniesione do osobnych plików JSON,
2. rekordy BibTeX znajdują się w osobnej paczce `data/records.zip`,
3. arkusz stylów został wydzielony do `css/style.css`,
4. logotypy i inne zasoby graficzne znajdują się w katalogu `assets/`,
5. dymki informacyjne i Google Analytics są obsługiwane przez osobne skrypty,
6. `index.html` pełni teraz rolę lekkiego punktu wejścia do aplikacji,
7. zachowano możliwość zbudowania samodzielnej, jednoplikowej wersji HTML.

### Struktura repozytorium

```text
iPBL-app/
├── index.html                 # punkt wejścia aplikacji
├── css/
│   └── style.css              # wygląd aplikacji
├── js/
│   ├── loader.js              # ładowanie danych i uruchamianie aplikacji
│   ├── app.bundle.js          # skompilowana logika aplikacji
│   ├── tooltip.js             # dymki informacyjne
│   └── analytics.js           # Google Analytics
├── data/
│   ├── sources.json           # źródła z rekordami bibliograficznymi
│   ├── catalog.json           # Wykaz internetowych źródeł literackich
│   ├── catalog-types.json     # dane do filtrów/statystyk typów
│   ├── catalog-fields.json    # dane do filtrów/statystyk dziedzin
│   └── records.zip            # rekordy BibTeX używane przez aplikację
├── assets/
│   ├── iPBL_logo.png
│   ├── ibl_pan_logo.png
│   ├── pbl_logo.png
│   └── nprh_logo.png
├── tools/
│   ├── start_local.bat        # uruchomienie lokalne w Windows
│   ├── start_local.sh         # uruchomienie lokalne w Linux/macOS
│   └── build_standalone.py    # budowanie wersji jednoplikowej
├── release/                   # katalog dla wersji samodzielnej
└── MANIFEST.json              # informacje techniczne o paczce
```

### Ważne: `app.bundle.js`

Plik `js/app.bundle.js` nadal zawiera skompilowaną logikę obecnej aplikacji React. Nie został automatycznie rozcięty na mniejsze moduły typu `search.js`, `analysis.js`, `records.js` czy `export.js`, ponieważ taki refaktoring powinien być wykonywany świadomie i testowany funkcja po funkcji.

Obecna struktura jest więc pierwszym bezpiecznym etapem porządkowania projektu: **dane, rekordy, style, zasoby i dodatki są już rozdzielone, a działająca logika aplikacji została zachowana**.

## Uruchamianie

### Wersja online

Najprościej korzystać z aplikacji opublikowanej przez GitHub Pages:

**[https://polskabibliografialiteracka.github.io/iPBL-app/](https://polskabibliografialiteracka.github.io/iPBL-app/)**

### Lokalnie w Windows

Uruchom:

```text
tools\start_local.bat
```

Aplikacja powinna być dostępna pod adresem:

```text
http://localhost:8000
```

Nie należy uruchamiać wersji modułowej przez samo dwukrotne kliknięcie `index.html`, ponieważ przeglądarki mogą blokować lokalne zapytania `fetch()` do plików JSON i ZIP.

### Linux / macOS

Uruchom:

```bash
sh tools/start_local.sh
```

## Wersja jednoplikowa

Repozytorium zachowuje możliwość zbudowania samodzielnej wersji HTML, przydatnej np. do przekazywania aplikacji jako pojedynczego pliku.

W katalogu aplikacji uruchom:

```bash
python tools/build_standalone.py
```

Skrypt tworzy plik:

```text
release/iPBL_app_standalone.html
```

Wersja samodzielna ponownie zawiera potrzebne dane i zasoby wewnątrz jednego pliku HTML.

## Technologie

Aplikacja jest statyczną aplikacją internetową wykorzystującą:

- HTML,
- CSS,
- JavaScript,
- React (w postaci skompilowanego bundle),
- JSON,
- Git i GitHub,
- GitHub Pages,
- Google Analytics.

Kod aplikacji znajduje się w tym repozytorium i jest rozwijany z wykorzystaniem systemu kontroli wersji Git.

## Wykorzystanie narzędzi AI

Podczas tworzenia aplikacji wykorzystywano **ChatGPT 5.6** jako narzędzie wspierające pracę programistyczną.

AI było wykorzystywane m.in. do:

- konsultowania rozwiązań programistycznych,
- przygotowywania i modyfikowania fragmentów kodu,
- wyjaśniania błędów i proponowania sposobów ich rozwiązania,
- porządkowania struktury kodu,
- wspierania testowania i debugowania.

Wykorzystanie AI miało charakter wspomagający. Decyzje dotyczące funkcjonalności aplikacji, struktury rozwiązania, sposobu prezentacji danych oraz treści podejmował zespół projektowy.

Kod wygenerowany lub zmodyfikowany z pomocą AI był sprawdzany i testowany przez członków zespołu przed wykorzystaniem go w aplikacji. **Dane bibliograficzne oraz ich opracowanie nie zostały wygenerowane przez AI.**

## Wersja

**Aktualna wersja: 0.3**

Projekt znajduje się na wczesnym etapie rozwoju. Numeracja wersji będzie aktualizowana wraz z wprowadzaniem kolejnych zmian i funkcji.

## Zespół twórców

Aplikacja jest rozwijana przez **Zespół ds. przetwarzania danych Pracowni Bibliografii Bieżącej IBL PAN** ([Barbara Wachek](https://www.linkedin.com/in/barbara-wachek/), [Dariusz Perliński](https://www.linkedin.com/in/dariusz-perli%C5%84ski-a558b9145/)).

Więcej informacji o projekcie i kolekcji iPBL można znaleźć na stronie [Polskiej Bibliografii Literackiej](https://pbl.ibl.waw.pl/).

## Licencja

### Kod aplikacji

Kod aplikacji iPBL jest dostępny na licencji **MIT**.

### Dane

Dane iPBL są dostępne na licencji **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Licencja CC BY 4.0 dotyczy danych iPBL i nie obejmuje treści zewnętrznych stron internetowych ani innych materiałów stron trzecich, do których odwołują się dane.
