#!/usr/bin/env python3
"""One-time snapshot of the untouched v0.3 inputs.

Never silently refresh originals from generated data on subsequent runs.
"""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
raw=root/'processing'/'raw'
pairs=[
 (root/'data'/'records.zip',raw/'records.original.zip'),
 (root/'data'/'sources.json',raw/'sources.original.json'),
 (root/'data'/'catalog.json',raw/'catalog.original.json'),
 (root/'js'/'app.bundle.js',root/'js'/'original'/'app.bundle.original.js')
]
exists=[target.exists() for _,target in pairs]
if any(exists) and not all(exists):
    raise SystemExit('BŁĄD: tylko część oryginalnych wejść jest dostępna; nie nadpisuję żadnego oryginału.')
if not any(exists):
    for source,target in pairs:
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
        print('Snapshot oryginału:',target.relative_to(root))
else:
    print('Oryginalne dane już istnieją; nie zostaną nadpisane.')
