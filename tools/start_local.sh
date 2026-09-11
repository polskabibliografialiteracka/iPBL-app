#!/usr/bin/env sh
cd "$(dirname "$0")/.." || exit 1
echo "iPBL: http://localhost:8000"
python3 -m http.server 8000
