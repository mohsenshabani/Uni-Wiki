#!/usr/bin/env python3
# Suche in den Fachlexika (nur lokal, Ordner fachlexika/ liegt nicht in Git). Beispiele:
#   python3 lex.py Fiktionalität
#   python3 lex.py "Code-Switching" -n 4
#   python3 lex.py --lead Handlung        (RDL: Kurzdefinitionen)
#   python3 lex.py --seite sprache 812     (Seite als PNG rendern, für wörtliche Zitate)
# Hinweis: In den Texten fehlen teils ä/ö/ü (Schriftkodierung); Zitate deshalb an der Seitenabbildung prüfen.
import sys, re, subprocess, unicodedata
from pathlib import Path
D = Path(__file__).resolve().parent / "fachlexika"
Q = {"sprache": ("Metzler Lexikon Sprache (5. Aufl.)", "978-3-476-05486-9.pdf", "sprache.txt"),
     "fdid": ("Metzler Lexikon Fremdsprachendidaktik (3. Aufl.)", "978-3-476-06000-6.pdf", "fdid.txt"),
     "rdl": ("Reallexikon der deutschen Literaturwissenschaft", "Reallexikon der deutschen Literaturwissenschaft.pdf", "rdl.txt")}
START = {"sprache": 20, "fdid": 25, "rdl": 70}
_cache = {}
def key(s):
    s = unicodedata.normalize("NFC", s).lower()
    s = re.sub(r"[äöüçß\u00ad]", "", s)  # Umlaute fehlen teils im Text, daher ignorieren
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"[^a-z]", "", s)
def seiten(q):
    if q not in _cache:
        _cache[q] = (D / "_text" / Q[q][2]).read_text(encoding="utf8", errors="replace").split("\f")
    return _cache[q]
def suche(term, n=4, ctx=10):
    k = key(term)
    pat = re.compile(r"^" + re.sub(r"[äöü]", ".?", re.escape(term.lower()).replace(r"\-", "-?")) + r"\s*(\(|f\.|m\.|n\.|Pl\.|Adj\.|Subst\.|$|,|\d\b)", re.I)
    t = re.escape(term.lower()).replace(r"\-", "-?")
    tl = re.sub(r"[äöü]", ".?", t)  # fehlende Umlaute in manchen Texten
    pat2 = re.compile(r"^" + tl + r"\s+(bezeichnet|beschreibt|ist|sind|meint|umfasst|versteht|steht|bedeutet|wird|werden|bzw\.|oder)\b", re.I)
    pat3 = re.compile(r"^" + tl + r"\s*(\(|$)", re.I)
    for q in Q:
        hits = []
        for i, p in enumerate(seiten(q), 1):
            if i < START[q]: continue
            L = p.split("\n")
            for j, z in enumerate(L):
                z2 = z.strip()
                if not z2 or len(z2) > 120: continue
                sc = 3 if pat.match(z2) else (2 if key(z2) == k else 0)
                if q == "fdid":
                    if pat2.match(z2): sc = 4
                    elif pat3.match(z2): sc = 3
                    vor = next((x.strip() for x in reversed(L[:j]) if x.strip()), "")
                    if vor.endswith("]") and re.match(r"^" + tl + r"\b", z2, re.I): sc = 6  # Artikelanfang (vorher Autorenkürzel)
                if not sc: continue
                nxt = " ".join(L[j + 1:j + 9])
                if q == "rdl" and "Expl" in nxt: sc += 3
                if q == "rdl" and sc < 5: continue
                hits.append((sc, i, j, L))
        hits.sort(key=lambda h: (-h[0], h[1]))
        print("=== %s: %d Treffer" % (Q[q][0], len(hits)))
        for sc, i, j, L in hits[:n]:
            print("--- PDF-Seite %d (Wertung %d)" % (i, sc))
            print("\n".join(l[:170] for l in L[j:j + ctx] if l.strip()))

def lead(term, n=6):
    """RDL: Kurzdefinition (Zeilen zwischen Stichwort und 'Expl') aller Treffer."""
    pat = re.compile(r"^" + re.escape(term.lower()).replace(r"\-", "-?") + r"\s*[1-9]?\s*(\([A-Z]\))?$", re.I)
    c = 0
    for i, p in enumerate(seiten("rdl"), 1):
        if i < START["rdl"]: continue
        L = [x.strip() for x in p.split("\n")]
        for j, z in enumerate(L):
            if pat.match(z) and "Expl" in " ".join(L[j + 1:j + 9]):
                k = next((m for m in range(j + 1, min(j + 9, len(L))) if L[m].startswith("Expl")), j + 3)
                print("--- RDL PDF-Seite %d: %s\n%s" % (i, z, " ".join(L[j + 1:k])))
                c += 1
                break
        if c >= n: break
    if not c: print("kein RDL-Treffer")

def seite(q, nr):
    out = D / "_png"; out.mkdir(exist_ok=True)
    pre = str(out / ("%s_%s" % (q, nr)))
    subprocess.run(["pdftoppm", "-f", str(nr), "-l", str(nr), "-r", "110", "-png", str(D / Q[q][1]), pre], check=True)
    print([str(x) for x in out.glob("%s_%s*" % (q, nr))])
if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    if a[0] == "--seite": seite(a[1], a[2])
    elif a[0] == "--lead": lead(a[1])
    else:
        n = int(a[a.index("-n") + 1]) if "-n" in a else 4
        suche(a[0], n)
