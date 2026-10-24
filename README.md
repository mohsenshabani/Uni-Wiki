# Uni-Wiki

Persönliches Wiki zu meinen Seminaren. Eine einzige HTML-Seite (`docs/index.html`),
die offline im Browser funktioniert (Doppelklick).

## Wo liegt was?

| Ordner / Datei | Was du damit machst |
|---|---|
| `seminare/<Seminar>/Lektüre/` | Texte und Bücher (PDF) hineinlegen |
| `seminare/<Seminar>/Folien und Aufgaben/` | PowerPoint, Folien, Aufgabenblätter vom Dozenten hineinlegen |
| `seminare/<Seminar>/Notizen/` | eigene Notizen und Hausaufgaben hineinlegen |
| `seminare/<Seminar>/Audio/` | Aufnahmen hineinlegen |
| `docs/index.html` | das fertige Wiki, im Browser öffnen |
| `inhalt/` | die Inhalte des Wikis (macht Claude, du musst nichts anfassen) |
| `update.sh` | schickt das Wiki zu GitHub: `bash update.sh` |
| `einrichten.sh` | einmalige GitHub-Einrichtung |
| `build.py`, `template.html` | Technik, nicht anfassen |

## Arbeitsablauf pro Sitzung

1. Dateien in die passenden Unterordner legen (Dateiname gern mit `S03_` beginnen).
2. In Claude sagen: „Sitzung 3 in <Seminar> hinzufügen“.
3. Im Browser prüfen: `docs/index.html`. Neue Seiten tragen den Vermerk „Entwurf“.
4. Zu GitHub schicken: `bash update.sh`

## Einmalige Einrichtung für GitHub

1. Auf github.com ein neues, **privates** leeres Repository anlegen (z. B. `uni-wiki`).
2. Im Terminal: `cd ~/Documents/Uni-Wiki` und dann
   `bash einrichten.sh https://github.com/DEIN-NAME/uni-wiki.git`
3. Später immer nur `bash update.sh`.

## Hinweise

- Repository privat lassen: Das Wiki enthält Zitate aus Büchern und Folien.
- `seminare/` wird nicht hochgeladen (Urheberrecht, große Dateien).
- Audio wird zuerst in Text umgewandelt (z. B. Whisper). Die Textdatei in `Audio/` oder `Notizen/` ablegen.
