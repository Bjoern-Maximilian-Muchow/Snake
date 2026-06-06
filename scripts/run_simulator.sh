#!/usr/bin/env sh
set -eu

cd simulator/web
python -m http.server 8000
