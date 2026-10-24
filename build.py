#!/usr/bin/env python3
"""Baut aus inhalt/ die Seite docs/index.html.  Aufruf: python3 build.py"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INH = ROOT / "inhalt"


def load(p):
    return json.loads(p.read_text(encoding="utf8"))


meta = load(INH / "meta.json")
data = {
    "meta": {"stand": meta["stand"]},
    "semester": meta["semester"],
    "seminare": meta["seminare"],
    "sitzungen": sorted((load(p) for p in (INH / "sitzungen").glob("*.json")), key=lambda s: (s["seminar"], s["nr"])),
    "glossar": load(INH / "glossar.json"),
    "vokabeln": load(INH / "vokabeln.json"),
    "kommentare": load(INH / "kommentare.json"),
    "quellen": load(INH / "quellen.json"),
}

# Konsistenzprüfung
problems = []
sem_ids = {s["id"] for s in data["seminare"]}
sess_ids = [s["id"] for s in data["sitzungen"]]
gl_ids = [g["id"] for g in data["glossar"]]
if len(set(sess_ids)) != len(sess_ids): problems.append("doppelte Sitzungs-ID")
if len(set(gl_ids)) != len(gl_ids): problems.append("doppelte Glossar-ID")
for s in data["seminare"]:
    if s["semester"] not in {x["id"] for x in data["semester"]}: problems.append("Seminar ohne Semester: " + s["id"])
for s in data["sitzungen"]:
    if s["seminar"] not in sem_ids: problems.append("Sitzung ohne Seminar: " + s["id"])
    for b in s.get("begriffe", []):
        if b not in gl_ids: problems.append("unbekannter Begriff in %s: %s" % (s["id"], b))
for v in data["vokabeln"]:
    if v["sitzung"] not in sess_ids: problems.append("Vokabel ohne Sitzung: " + v["de"])
txt = json.dumps(data, ensure_ascii=False)
for m in re.finditer(r"\[\[([a-z0-9-]+)\|", txt):
    if m.group(1) not in gl_ids: problems.append("kaputter Link [[%s|…]]" % m.group(1))
for g in data["glossar"]:
    for i in g.get("see", []):
        if i not in gl_ids: problems.append("see-Verweis ohne Ziel: %s → %s" % (g["id"], i))
if problems:
    print("FEHLER:"); [print(" -", p) for p in problems]; sys.exit(1)

html = (ROOT / "template.html").read_text(encoding="utf8").replace(
    "__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
out = ROOT / "docs" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf8")
print("OK: %s (%d KB) · %d Seminar(e), %d Sitzung(en), %d Begriffe, %d Vokabeln"
      % (out.relative_to(ROOT), len(html) // 1024, len(data["seminare"]), len(data["sitzungen"]),
         len(data["glossar"]), len(data["vokabeln"])))
