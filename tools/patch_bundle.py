#!/usr/bin/env python3
"""Integrate iPBL React bundle by checked substitutions, preserve original bundle."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
original=root/'js/original/app.bundle.original.js'
out=root/'js/app.bundle.js'
s=original.read_text(encoding='utf-8')
def change(old,new,expected=1):
    global s
    count=s.count(old)
    if count!=expected:
        raise RuntimeError(f'Znaleziono {count} fragmentów zamiast {expected}: {old[:120]}')
    s=s.replace(old,new)
change('return GL(await t.async("text"))}',
       'return window.IPBLSearchUtils.indexRecords(GL(await t.async("text")))}')
change('jo(Object.values(N).join(" ")).includes(L)',
       'window.IPBLSearchUtils.matchesRecord(N,L)')
dollar=chr(36)
tick=chr(96)
old='jo('+tick+dollar+'{b.name} '+dollar+'{b.file} '+dollar+'{b.url} '+dollar+'{b.method} '+dollar+'{iPBLAuthorSearchIndex[b.file]||""}'+tick+').includes(C)'
change(old,'window.IPBLSearchUtils.matchesSource(b,C,iPBLAuthorSearchIndex[b.file]||"")')
change('nm=UL.filter(({label:e})=>Number(e)>=2018&&Number(e)<=2025)',
       'nm=UL.filter(({label:e})=>/^\\d{4}$/.test(e)&&Number(e)>=2018&&Number(e)<=new Date().getFullYear())')
change('children:"Dane maj\\u0105 charakter badawczy. Zakres metadanych mo\\u017Ce r\\xF3\\u017Cni\\u0107 si\\u0119 pomi\\u0119dzy \\u017Ar\\xF3d\\u0142ami. \\xB7 Wersja aplikacji 0.2"',
       'children:'+tick+'Dane mają charakter badawczy. Zakres metadanych może różnić się pomiędzy źródłami. · Wersja aplikacji '+dollar+'{window.IPBL_CONFIG.version}'+tick)
change('className:"about-number about-number--version",children:"0.3"',
       'className:"about-number about-number--version",children:window.IPBL_CONFIG.version')
change('children:"Wersja: 0.3"',
       'children:'+tick+'Wersja: '+dollar+'{window.IPBL_CONFIG.version}'+tick)
change('href:C.url,target:"_blank",rel:"noreferrer",className:"catalog-main-link"',
       'href:C.url||void 0,target:"_blank",rel:"noreferrer",className:"catalog-main-link",onClick:C.url?void 0:e=>e.preventDefault(),style:C.url?void 0:{cursor:"default",opacity:.7}')
out.write_text(s,encoding='utf-8')
print('Wygenerowano dostosowany app.bundle.js; oryginał bez zmian.')
