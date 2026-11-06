# Historia zmian iPBL

## 0.4.0 — 6 listopada 2026

Ta wersja wdraża bezpieczną, automatyczną poprawę **kopii danych do prezentacji i wyszukiwania**. Surowe metadane bibliograficzne nie są nadpisywane.

**[Uruchom aplikację iPBL](https://polskabibliografialiteracka.github.io/iPBL-app/)** · [README](README.md) · [Workflow i instrukcje](processing/README.md) · [Kolejka ręcznych decyzji](processing/reports/manual_review.csv)

### Automatycznie wprowadzone poprawki

1. **BibTeX i odnośniki:** zinterpretowano jednoznaczne sekwencje specjalne (m.in. `\\_`, `\\&`, `\\#`) w **28 619 polach URL**, pozostawiając nieznane makra LaTeX.
2. **Autorzy:** bezpiecznie rozdzielono **751 pól** z jednoznacznym separatorem BibTeX `and`. Niejednoznaczne zapisy pozostają bez zmian i są raportowane.
3. **Wyszukiwarka:** rozpoznaje zarówno „imię nazwisko”, jak i „nazwisko imię”, niezależnie od polskich znaków i wielkości liter.
4. **Adresy katalogowe:** uzupełniono protokół dla **18** adresów o rozpoznawalnej składni domeny; nieprawidłowe odnośniki nie są przedstawiane jako działające linki.
5. **Kategorie:** ujednolicono **3** pozycje o różnicach ortograficznych (m.in. `YouTube`).
6. **Wykres:** zakres lat nie zatrzymuje się już na 2025; prawidłowe kolejne lata są uwzględniane automatycznie.
7. **Wersja:** numer aplikacji jest odczytywany ze wspólnego pliku `config/app.json`; stopka i ekran informacji o aplikacji pokazują bieżącą wersję.
8. **Pakowanie:** `MANIFEST.json` jest odnawiany automatycznie, dostępny jest także generator jednoplikowego HTML.
9. **Kontrola jakości:** osobny proces Pythona, raport w CSV/JSON, trwałe identyfikatory `case_id`, testy regresji w GitHub Actions.

### Wyniki i integralność

- 203 źródła BibTeX, **150 656 rekordów** — liczba oraz identyfikatory zachowane.
- Wykaz internetowych źródeł literackich: **4003 pozycje** — żadnej nie usunięto.
- **205 spraw** zachowano do późniejszej oceny ręcznej.
- Wejściowe archiwa i JSON znajdują się w `processing/raw/`, a niezmodyfikowany skompilowany kod w `js/original/`.
- [Pełny raport i sumy SHA-256](processing/reports/summary.json).

### Świadomie niepoprawione automatycznie

- podejrzany rok `0201` — nie wolno zgadywać poprawnej daty;
- brakujące lub błędne adresy, gdzie nie można ustalić właściwej strony;
- niejednoznaczne granice między nazwiskami autorów;
- wspólne URL kilku rekordów katalogowych — nie oznaczają automatycznie duplikatu;
- dostępność żywych witryn: sam poprawny składniowo URL nie gwarantuje odpowiedzi HTTP 200.

Sprawy wracają do systemu przez `processing/reports/manual_review.csv`. **Decyzje człowieka zapisujemy osobno** w `processing/manual_decisions.csv`. Nie edytujemy ręcznie wygenerowanych plików, a oryginalne źródła pozostają nietknięte.

### Uruchomienie pełnego procesu

```bash
python processing/build_all.py
```

Weryfikacja przeglądarkowa i testy integralności są także częścią GitHub Actions. Oryginalne dane nigdy nie są aktualizowane na podstawie danych wyjściowych.

## 0.3 — wcześniejsza wersja modułowa

Pierwsze wydzielenie katalogów `data/`, `js/`, `css/`, `assets/`, bez pełnego refaktoringu skompilowanego Reacta.
