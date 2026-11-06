#!/usr/bin/env python3
"""iPBL processing: source of truth is processing/raw/, never modified.

Outputs data/ and processing/reports/. All manual cases retain stable case_ids.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv
import hashlib
import json
import pathlib
import re
import sys
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'processing'))
from normalization import normalize_bibtex_file,normalize_type,safe_url,author_labels
SRC=ROOT/'processing'/'raw'
DEST=ROOT/'data'
REPORT=ROOT/'processing'/'reports'
MANUAL_COLS=['case_id','source_file','record_id','field','code','original_value','proposed_value','reason','status']

def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def jwrite(path: pathlib.Path,value) -> None:
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    REPORT.mkdir(exist_ok=True)
    DEST.mkdir(exist_ok=True)
    originals=[SRC/'records.original.zip',SRC/'catalog.original.json',SRC/'sources.original.json']
    for path in originals:
        if not path.is_file():
            raise SystemExit(f'BRAK PLIKU ŹRÓDŁOWEGO: {path}')
    before={p.name:digest(p) for p in originals}
    counters=Counter()
    manual=[]
    decision_path=ROOT/'processing'/'manual_decisions.csv'
    previous_decisions={}
    if decision_path.exists():
        with decision_path.open(encoding='utf-8-sig',newline='') as fd:
            previous_decisions={r['case_id']:r for r in csv.DictReader(fd)
                                if r.get('case_id') and r.get('decision')}

    def issue(source_file,record_id,field,code,raw,proposed,reason):
        case=hashlib.sha256((source_file+'\0'+record_id+'\0'+field+'\0'+code+'\0'+raw).encode('utf-8')).hexdigest()[:16]
        manual.append(dict(case_id=case,source_file=source_file,record_id=record_id,field=field,
                           code=code,original_value=raw,proposed_value=proposed,
                           reason=reason,status='rozpatrzono' if case in previous_decisions else 'do_sprawdzenia'))

    catalog=json.loads((SRC/'catalog.original.json').read_text('utf-8'))
    for num,rec in enumerate(catalog,1):
        original=rec.get('url','')
        good,action=safe_url(original,allow_schemeless=True)
        if good:
            rec['url']=good
            if action=='added_https':
                counters['catalog_added_https']+=1
        else:
            rec['url']=''
            counters['catalog_invalid_url']+=1
            issue('catalog.original.json',str(num),'url','invalid_catalog_url',original,'',
                  'Nieprawidłowy adres. Bez zgadywania właściwego URL.')
        old_type=rec.get('type','')
        rec['type']=normalize_type(old_type)
        if rec['type']!=old_type:
            counters['catalog_normalized_type']+=1
    jwrite(DEST/'catalog.json',catalog)
    for col,target in [('type','catalog-types.json'),('field','catalog-fields.json')]:
        counter=Counter(str(row.get(col,'')).strip() for row in catalog)
        jwrite(DEST/target,[{'label':k,'value':v} for k,v in
                            sorted(counter.items(),key=lambda kv:(-kv[1],kv[0].casefold()))])
    by_url=defaultdict(list)
    for index,item in enumerate(catalog,1):
        if item.get('url'):
            by_url[item['url']].append((index,item.get('name','')))
    for u,rows in by_url.items():
        if len(rows)>1:
            for number,title in rows:
                issue('catalog.original.json',str(number),'url','duplicate_catalog_url',u,'',
                      f'Ten sam adres w {len(rows)} pozycjach. Nie usunięto; możliwe poprawne współdzielenie adresu.')
    counters['duplicate_catalog_url_groups']=sum(len(rows)>1 for rows in by_url.values())

    source_rows=json.loads((SRC/'sources.original.json').read_text('utf-8'))
    authors_by_file=defaultdict(Counter)
    rec_count=Counter()
    split_by_file=Counter()
    old_counts={}

    with zipfile.ZipFile(SRC/'records.original.zip') as zin,zipfile.ZipFile(DEST/'records.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
        for info in zin.infolist():
            if info.is_dir():
                zout.writestr(info,b'')
                continue
            if not info.filename.endswith('.bib'):
                issue(info.filename,'','','unexpected_zip_member',info.filename,'','Plik skopiowany bez zmian.')
                zout.writestr(info,zin.read(info))
                continue
            filename=pathlib.PurePosixPath(info.filename).name
            before_text=zin.read(info).decode('utf-8')
            before_ids=re.findall(r'^\s*@\w+\s*\{\s*([^,]+),',before_text,re.M)
            split_before=counters['split_author_fields']
            result,author_fields=normalize_bibtex_file(before_text,filename,issue,counters)
            after_ids=re.findall(r'^\s*@\w+\s*\{\s*([^,]+),',result,re.M)
            if before_ids!=after_ids:
                raise RuntimeError(f'Zmiana identyfikatorów/liczby rekordów: {filename}')
            old_counts[filename]=len(before_ids)
            split_by_file[filename]=counters['split_author_fields']-split_before
            rec_count[filename]=len(after_ids)
            for _id,author in author_fields:
                for label in author_labels(author):
                    authors_by_file[filename][label]+=1
            zout.writestr(info,result.encode('utf8'))

    for row in source_rows:
        fn=row['file']
        if fn not in old_counts:
            raise RuntimeError(f'Brak źródła bibliograficznego w paczce: {fn}')
        if old_counts[fn]!=row['records']:
            raise RuntimeError(f'Rozbieżność rekordów w {fn}: {old_counts[fn]} != {row["records"]}')
        if split_by_file[fn]:
            ac=authors_by_file[fn]
            row['authorsTotal']=len(ac)
            row['authors']=[{'label':label,'value':qty} for label,qty in ac.most_common(10)]
            counters['sources_author_aggregates_updated']+=1
        orig=row.get('url','')
        normalized,action=safe_url(orig,allow_schemeless=True)
        if normalized:
            row['url']=normalized
            if action=='added_https':
                counters['sources_added_https']+=1
        else:
            row['url']=''
            issue(fn,'','source.url','invalid_source_url',orig,'',
                  'Nie można ustalić poprawnego adresu źródła.')
    jwrite(DEST/'sources.json',source_rows)

    manual.sort(key=lambda x:(x['source_file'],x['record_id'],x['field'],x['code'],x['original_value']))
    with (REPORT/'manual_review.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=MANUAL_COLS)
        w.writeheader()
        w.writerows(manual)
    jwrite(REPORT/'manual_review.json',manual)
    comparison=[]
    for row in source_rows:
        f=row['file']
        cnt=authors_by_file[f]
        comparison.append({'file':f,'previous_authorsTotal':row.get('authorsTotal'),
                           'calculated_authorsTotal':len(cnt),
                           'previous_top_authors':row.get('authors',[]),
                           'calculated_top_authors':[{'label':k,'value':v} for k,v in cnt.most_common(10)]})
    jwrite(REPORT/'author_statistics_comparison.json',comparison)
    counters['record_total']=sum(rec_count.values())
    counters['bib_files']=len(rec_count)
    counters['catalog_items']=len(catalog)
    counters['manual_review_items']=len(manual)
    output={'source_sha256':before,
            'output_sha256':{p.name:digest(p) for p in
                             [DEST/'records.zip',DEST/'catalog.json',DEST/'sources.json',
                              DEST/'catalog-types.json',DEST/'catalog-fields.json']},
            'counts':dict(sorted(counters.items())),
            'integrity':{'record_ids_preserved':True,
                         'total_records':sum(rec_count.values()),
                         'original_files_unchanged':all(digest(p)==before[p.name] for p in originals)}}
    if not output['integrity']['original_files_unchanged']:
        raise RuntimeError('Oryginalne dane uległy zmianie!')
    jwrite(REPORT/'summary.json',output)
    print(json.dumps({'counts':output['counts'],'integrity':output['integrity']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
