# iPBL — niezależny proces przygotowania danych

Oryginalne dane wejściowe są zachowane w `processing/raw/`. Skrypt **tylko odczytuje oryginały** i generuje kopie dla aplikacji w `data/`. Nie zmienia identyfikatorów rekordów.

## Jedno polecenie

`python processing/build_all.py` wykonuje kolejno: inicjalizację oryginalnych źródeł (tylko pierwszy raz), normalizację, kontrolowane dostosowanie skompilowanego Reacta, testy, budowę samodzielnego HTML oraz odnowienie manifestu.

## Pliki

- `processing/raw/records.original.zip`, `catalog.original.json`, `sources.original.json` — **niezmieniane źródła prawdy**, inicjalizowane tylko gdy wszystkie są nieobecne;
- `js/original/app.bundle.original.js` — niezmodyfikowany React bundle;
- `data/records.zip`, `data/*.json` — dane aplikacji wygenerowane z kopii;
- `processing/reports/summary.json` — wyniki i sumy kontrolne SHA-256;
- `processing/reports/manual_review.csv` oraz `manual_review.json` — raport przypadków nierozstrzygniętych z trwałym `case_id`;
- `processing/manual_decisions.csv` — miejsce przechowywania zweryfikowanych decyzji; nigdy nie poprawiaj ręcznie raportu wynikowego.

## Zasady

Automatycznie interpretujemy tylko jednoznaczne sekwencje BibTeX, bezpieczne separatory autorów, zapis URL i warianty ortograficzne kategorii. Brakujące adresy, niepewne daty i możliwe duplikaty trafiają do raportu. Wprowadzony rok `0201` **nie jest zgadywany**. Wspólne adresy nie są deduplikowane.

Skrypt nie potwierdza dostępności sieciowej adresów ani ich prawidłowości merytorycznej. Kolumna `status` w raporcie jest wyliczana z obecności decyzji w `processing/manual_decisions.csv`; same decyzje nie są stosowane do danych bez osobnego zatwierdzonego procesu.

GitHub Actions uruchamia testy i przygotowuje raport oraz HTML w artefaktach. Na gałęzi przygotowawczej może również zapisać gotowe pliki wynikowe do repozytorium po poprawnym przejściu testów.
