from pathlib import Path
import json, base64, re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "release" / "iPBL_app_standalone.html"

def data_uri(path: Path, mime="image/png"):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")

css = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
analytics = (ROOT / "js" / "analytics.js").read_text(encoding="utf-8")
tooltip = (ROOT / "js" / "tooltip.js").read_text(encoding="utf-8")
bundle = (ROOT / "js" / "app.bundle.js").read_text(encoding="utf-8")

ipbl_data = {
    "sources": json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8")),
    "catalog": json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8")),
    "catalogTypes": json.loads((ROOT / "data" / "catalog-types.json").read_text(encoding="utf-8")),
    "catalogFields": json.loads((ROOT / "data" / "catalog-fields.json").read_text(encoding="utf-8")),
}

# app.bundle.js expects the data in window.IPBL_DATA
payload = json.dumps(ipbl_data, ensure_ascii=False, separators=(",", ":"))

# Re-embed the records ZIP so the release remains a single downloadable HTML file.
zip64 = base64.b64encode((ROOT / "data" / "records.zip").read_bytes()).decode("ascii")
bundle = bundle.replace('fetch("data/records.zip")', 'fetch("data:application/zip;base64,' + zip64 + '")')

# Re-embed images used by the compiled bundle.
for name in ["iPBL_logo.png", "ibl_pan_logo.png", "pbl_logo.png", "nprh_logo.png"]:
    bundle = bundle.replace("assets/" + name, data_uri(ROOT / "assets" / name))

favicon = data_uri(ROOT / "assets" / "iPBL_logo.png")
html = f'''<!doctype html>
<html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Analiza danych iPBL</title><meta name="description" content="Samodzielne narzędzie do przeglądania i analizy danych iPBL.">
<link rel="icon" href="{favicon}">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0B8F78RT52"></script>
<script>{analytics}</script>
<style>{css}</style></head><body><div id="root"></div>
<script>window.IPBL_DATA={payload};</script>
<script>{bundle}</script>
<script>{tooltip}</script>
</body></html>'''
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"Gotowe: {OUT}")
