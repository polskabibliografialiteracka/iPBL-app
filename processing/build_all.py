#!/usr/bin/env python3
"""Reproducible iPBL workflow: preserve raw, normalize, test, build and manifest."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
for args in [
 [sys.executable,'processing/bootstrap_raw.py'],
 [sys.executable,'processing/prepare_data.py'],
 [sys.executable,'tools/patch_bundle.py'],
 [sys.executable,'-m','unittest','discover','-s','processing/tests','-v'],
 [sys.executable,'tools/build_standalone.py'],
 [sys.executable,'processing/update_manifest.py']
]:
 print('\n>>>',' '.join(args),flush=True)
 subprocess.run(args,cwd=root,check=True)
