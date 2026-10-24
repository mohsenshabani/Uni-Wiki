#!/bin/bash
# Aktualisiert das Wiki: baut docs/index.html neu und schickt alles an GitHub.
# Aufruf im Terminal:  bash update.sh
set -e
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  python3 build.py
else
  echo "Hinweis: python3 nicht gefunden, docs/index.html wird nicht neu gebaut."
fi
git add -A
if git diff --cached --quiet; then
  echo "Nichts zu aktualisieren."
  exit 0
fi
git commit -m "Wiki aktualisiert: $(date '+%d.%m.%Y %H:%M')"
git push
echo "Fertig: Wiki ist auf GitHub aktualisiert."
