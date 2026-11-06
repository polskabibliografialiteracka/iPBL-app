"""Conservative, reversible normalizations of copies of iPBL bibliographic data.

No original input is changed. Ambiguous cases go to manual review.
"""
from __future__ import annotations
from collections import Counter
import re
from urllib.parse import urlsplit

_SAFE_ESCAPE = re.compile(r'(?<!\\)\\([_&%#$])')
_FIELD = re.compile(r'^(?P<head>[ \t]*(?P<name>[A-Za-z_]+)[ \t]*=[ \t]*)(?P<quote>["{])(?P<value>.*)(?P<tail>["}][ \t]*,?[ \t]*)$')
_ENTRY = re.compile(r'^\s*@\w+\s*\{\s*([^,]+),', re.M)
_AUTHOR_AND = re.compile(r'\s+and\s+', re.I)
_VIAF_PREFIX = re.compile(r'^\(VIAF:https?://viaf\.org/viaf/\d+/?\),\s*', re.I)
_NAME = re.compile(r"^[A-ZĄĆĘŁŃÓŚŹŻ][\wąćęłńóśźżÁÉÍÓÚà-ÿ’'.-]*(?:\s+[A-ZĄĆĘŁŃÓŚŹŻ][\wąćęłńóśźżÁÉÍÓÚà-ÿ’'.-]*){1,4}$")
_URL_SPLIT = re.compile(r',\s*(?=https?://)', re.I)
_HOST = re.compile(r'^(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63}$')

_TYPE_REPLACEMENTS = {'Youtube':'YouTube', 'youtube':'YouTube', 'w Internecie':'w internecie'}

def strip_safe_escapes(value: str) -> str:
    return _SAFE_ESCAPE.sub(lambda m:m.group(1), value)

def clean_display_person(part: str) -> str:
    part = strip_safe_escapes(part).strip()
    part = _VIAF_PREFIX.sub('', part)
    part = re.sub(r'^ENTITY:\s*', '', part, flags=re.I)
    part = re.sub(r'\s*\((?:VIAF|BN):https?://[^)]+\)\s*$', '', part, flags=re.I)
    return part.strip()

def is_clear_person(part: str) -> bool:
    value = clean_display_person(part)
    if not value or len(value)>110 or ':' in value or ' and ' in value.lower():
        return False
    if ',' in value:
        bits = value.split(',', 1)
        return (1 <= len(bits[0].split()) <= 4
                and 1 <= len(bits[1].split()) <= 5
                and bool(re.search(r'[A-ZĄĆĘŁŃÓŚŹŻ]', bits[0])))
    return bool(_NAME.fullmatch(value))

def split_authors(value: str) -> tuple[str,bool,bool]:
    if not _AUTHOR_AND.search(value):
        return value, False, False
    parts = _AUTHOR_AND.split(value)
    if all(is_clear_person(p) for p in parts):
        return ' | '.join(p.strip() for p in parts), True, False
    return value, False, True

def safe_url(value: str, allow_schemeless: bool=False) -> tuple[str,str]:
    """Only syntactic HTTP(S) validation, not network availability."""
    v = strip_safe_escapes((value or '').strip())
    if not v:
        return '', 'empty'
    if v.startswith('//'):
        v = 'https:'+v
        action = 'added_https'
    elif not re.match(r'^https?://',v,flags=re.I):
        if not allow_schemeless:
            return '', 'invalid'
        v = 'https://'+v
        action = 'added_https'
    else:
        action = 'unchanged'
    try:
        parsed = urlsplit(v)
        if parsed.scheme.lower() not in {'http','https'}:
            return '', 'invalid'
        if parsed.username or parsed.password or not parsed.hostname or any(c.isspace() for c in v):
            return '', 'invalid'
        host = parsed.hostname
        if not _HOST.fullmatch(host) and host != 'localhost':
            return '', 'invalid'
        if not 0 < (parsed.port or 443) < 65536:
            return '', 'invalid'
    except ValueError:
        return '', 'invalid'
    return v,action

def normalize_urls(raw: str) -> tuple[str,list[str]]:
    if not raw.strip():
        return '', []
    output, issues = [], []
    for part in _URL_SPLIT.split(raw):
        url,status = safe_url(part,allow_schemeless=False)
        if url:
            output.append(url)
        else:
            issues.append('url_'+status)
    return ', '.join(output), issues

def normalize_bibtex_file(text: str, source_name: str, add_issue, counts: Counter) -> tuple[str,list[tuple[str,str]]]:
    current_id=''
    collected_authors=[]
    output=[]
    for line in text.splitlines(keepends=True):
        entry = _ENTRY.match(line)
        if entry:
            current_id=entry.group(1).strip()
        ending = '\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
        content=line[:-len(ending)] if ending else line
        m=_FIELD.match(content)
        if not m:
            output.append(line)
            continue
        name,original=m.group('name').lower(),m.group('value')
        changed=strip_safe_escapes(original)
        if changed!=original:
            counts['escaped_'+name]+=1
        if name=='year':
            year_text=original.strip()
            if re.fullmatch(r'\d{4}',year_text) and not(1800<=int(year_text)<=2027):
                add_issue(source_name,current_id,'year','suspicious_year',original,'',
                          'Niewiarygodny rok. Wymagana weryfikacja bibliograficzna.')
                counts['suspicious_years']+=1
        if name=='url':
            cleaned,issues=normalize_urls(changed)
            for reason in issues:
                add_issue(source_name,current_id,'url',reason,original,'',
                          'Nie ustalono poprawnego adresu; brak linku w wersji aplikacyjnej.')
            changed=cleaned
            if cleaned!=strip_safe_escapes(original):
                counts['invalid_url_fields_cleaned']+=1
        elif name=='author':
            changed,split,review=split_authors(changed)
            if split:
                counts['split_author_fields']+=1
            if review:
                add_issue(source_name,current_id,'author','ambiguous_and',original,'',
                          'Niepewna granica między autorami; zachowano pierwotne brzmienie.')
            collected_authors.append((current_id,changed))
        if changed!=original:
            counts['changed_fields']+=1
        output.append(m.group('head')+m.group('quote')+changed+m.group('tail')+ending)
    return ''.join(output),collected_authors

def normalize_type(value: str) -> str:
    for src,dst in _TYPE_REPLACEMENTS.items():
        value=value.replace(src,dst)
    return value

def author_labels(field: str) -> list[str]:
    parts=re.split(r'\s*\|\s*',field or '')
    return [v for p in parts if (v:=clean_display_person(p))]
