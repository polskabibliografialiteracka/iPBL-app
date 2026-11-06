"""Browser regression test for the modular iPBL app; no manual clicks needed.

Starts a local HTTP server so fetch('data/*.json') and records.zip work normally.
This test intentionally checks browser-rendered links and search, not just Python transforms.
"""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import sys

ROOT=Path(__file__).resolve().parents[2]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit('Brak Playwright: pip install playwright && playwright install chromium') from exc
    handler=partial(QuietHandler,directory=str(ROOT))
    server=ThreadingHTTPServer(('127.0.0.1',0),handler)
    Thread(target=server.serve_forever,daemon=True).start()
    address='http://127.0.0.1:'+str(server.server_port)+'/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1280,'height':900})
            errors=[]
            page.on('pageerror',lambda err:errors.append(str(err)))
            page.route('**/googletagmanager.com/**',lambda route:route.abort())
            page.route('**/google-analytics.com/**',lambda route:route.abort())
            page.goto(address,wait_until='domcontentloaded',timeout=60000)
            page.locator('tr').filter(has_text='Afisz Teatralny').first.wait_for(timeout=30000)
            assert '150' in page.locator('body').inner_text()
            assert '2026' in page.locator('body').inner_text()
            assert not errors,errors
            page.locator('tr').filter(has_text='Afisz Teatralny').first.get_by_role(
                'button',name='Analizuj').click(timeout=20000)
            query=page.get_by_placeholder('Szukaj w rekordach…')
            query.wait_for(timeout=30000)
            query.fill('poczucie tego przej')
            match=page.locator('tr').filter(has_text='Poczucie tego przejścia').last
            match.wait_for(timeout=30000)
            link=match.locator('a[href]').first.get_attribute('href')
            assert link and link.endswith('daje-flow_15.html') and '\\' not in link,link
            for author in ['Agnieszka Kobroń','Kobroń Agnieszka']:
                query.fill(author)
                page.locator('tr').filter(has_text='Poczucie tego przejścia').last.wait_for(timeout=30000)
            query.fill('Sex, drugs & rock')
            page.locator('tr').filter(has_text="Sex, drugs & rock’n’roll").last.wait_for(timeout=30000)
            assert not errors,errors
            print('OK: modular UI, years, record loading, cleaned URL, both author orders, BibTeX text')
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

if __name__=='__main__':
    main()
