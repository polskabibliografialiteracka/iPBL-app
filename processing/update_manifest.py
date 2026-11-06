#!/usr/bin/env python3
"""Checksums of the delivered app and reports; excludes raw files and itself."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
paths=[p for p in root.rglob('*') if p.is_file()
       and p.name!='MANIFEST.json'
       and 'processing/raw' not in p.as_posix()
       and '.git' not in p.parts and '__pycache__' not in p.parts]
manifest={'description':'iPBL package manifest; raw snapshots excluded',
          'version':json.loads((root/'config/app.json').read_text())['version'],
          'files':{str(p.relative_to(root)).replace('\\','/'):{
              'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
              for p in sorted(paths)}}
(root/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('MANIFEST.json:',len(manifest['files']),'plików')
