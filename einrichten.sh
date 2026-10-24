#!/bin/bash
# Einmalige Einrichtung. Vorher auf github.com ein leeres, PRIVATES Repository anlegen
# (z. B. "uni-wiki") und dessen Adresse kopieren.
# Aufruf:  bash einrichten.sh git@github.com:DEIN-NAME/uni-wiki.git
#     oder bash einrichten.sh https://github.com/DEIN-NAME/uni-wiki.git
set -e
cd "$(dirname "$0")"
if [ -z "$1" ]; then
  echo "Bitte die Adresse des GitHub-Repositorys angeben."
  echo "Beispiel: bash einrichten.sh https://github.com/DEIN-NAME/uni-wiki.git"
  exit 1
fi
if [ ! -d .git ]; then git init -q; fi
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "$1"
git add -A
git commit -m "Erste Version des Uni-Wikis" || true
git push -u origin main
echo "Fertig: Das Wiki liegt jetzt auf GitHub."
