# Denkmäler digital erfassen

One-Page-Website mit Vollbild-Abschnitten: Cover, die drei Geräte und danach alle Projekte aus `projects/`.

## Ordnerstruktur

```
index.html
cover/                  ← erster Bildschirm
  text.de.txt
  text.en.txt
  cloud.ply | model.glb | foto.jpg
projects/               ← jedes Unterverzeichnis wird ein Abschnitt
  01-rundtempel/
    beschreibung.de.txt
    beschreibung.en.txt
    rundtempel.ply | rundtempel.glb | rundtempel.jpg
    config.json         (optional)
  02-obelisk/
    text.txt
    obelisk.ply
tools/build_manifest.py
.github/workflows/pages.yml
```

Pro Ordner wird die erste passende Textdatei und genau ein Hauptmedium verwendet:

- Rotierend: zuerst `.ply`, sonst `.glb`
- Statisch: falls kein 3D-Modell da ist, ein Bild (`.png`, `.jpg`, `.jpeg`, `.webp`, `.avif`, `.gif`)

Der Dateiname ist egal.
Projekte erscheinen alphabetisch nach Ordnernamen. Mit Präfixen wie `01-`, `02-` legst du die Reihenfolge fest.

## Textdatei

Der erste Satz wird zur Überschrift, der Rest zum Text darunter.

```
Kloster Maulbronn. Fassadenscan der Klosterkirche mit 24 Standpunkten.

Eine Leerzeile beginnt einen neuen Absatz.
```

Die Überschrift endet am ersten `.`, `!` oder `?` mit folgendem Leerzeichen oder am ersten Zeilenumbruch.
Enthält die Überschrift selbst einen Punkt (z. B. „St. Michael“), schreib sie allein in die erste Zeile ohne Punkt am Ende.
Speichere die Datei am besten als UTF-8. Ältere Windows-Kodierung wird aber auch erkannt.

### Mehrsprachig (Deutsch/Englisch)

Es gibt zwei Wege:

1. Zwei Dateien pro Ordner: `*.de.txt` und `*.en.txt` (empfohlen)
2. Eine Datei mit Blöcken:

   ```
   [de]
   Deutscher Titel. Deutscher Absatz.

   [en]
   English title. English paragraph.
   ```

Sprachwechsel im Frontend: `?lang=de` oder `?lang=en` (plus DE/EN-Schalter oben links).

## GLB-Modell (.glb)

`.glb`-Dateien werden als rotierendes 3D-Modell eingebunden (Web Component `model-viewer`).
Wenn zusätzlich eine `.ply` im selben Ordner liegt, hat `.ply` Vorrang.

## Statisches Bild

Wenn nur ein Bild vorhanden ist, wird es vollflächig als nicht-rotierendes Hintergrundmedium angezeigt.

## Punktwolke (.ply)

Unterstützt werden ASCII- und Binär-PLY, mit oder ohne Farben (`red/green/blue`). Landeskoordinaten wie UTM sind kein Problem.
Die Wolke wird automatisch zentriert und skaliert.

Große Scans vorher ausdünnen, sonst lädt die Seite lange. In CloudCompare geht das so:

1. Edit → Subsample → Random oder Spatial wählen und auf etwa 100.000–300.000 Punkte reduzieren.
2. Über File → Save als PLY speichern, Format **binary**.

Die Seite zeigt ohnehin höchstens 150.000 Punkte, bei mehr wird gleichmäßig ausgedünnt. GitHub erlaubt maximal 100 MB pro Datei.
Ziel sollten unter 10 MB pro Wolke sein.

## config.json (optional)

```json
{
  "up": "z",
  "yaw": -25,
  "zoom": 1,
  "pointSize": 1.2,
  "colors": "original",
  "maxPoints": 150000
}
```

Die Optionen bedeuten:

- `up`: die Hochachse der Wolke. `"z"` ist Standard und typisch für FARO, CloudCompare und Metashape. Für Meshlab- oder Blender-Exporte `"y"` verwenden.
- `yaw`: der Drehwinkel der Ansicht in Grad.
- `zoom`: die Größe der Wolke auf dem Bildschirm.
- `pointSize`: die Punktgröße.
- `colors`: `"stone"` ignoriert die Punktfarben und zeichnet in Sandsteinfarbe.
- `maxPoints`: die maximale Anzahl dargestellter Punkte.

## Veröffentlichen auf GitHub Pages

1. Alle Dateien in dein Repository hochladen, auch den versteckten Ordner `.github`.
2. Unter **Settings → Pages → Build and deployment → Source** die Option **GitHub Actions** wählen.
3. Pushen. Die Action erzeugt `manifest.json` aus den Ordnern und veröffentlicht die Seite. Den Fortschritt siehst du im Tab **Actions**.

Ein neues Projekt anlegen heißt dann nur: Ordner in `projects/` anlegen, Textdatei und Medium (`.ply`, `.glb` oder Bild) hineinlegen, pushen.

Ohne GitHub Action liest die Seite die Ordner als Rückfall über die GitHub-API. Das klappt nur bei öffentlichen Repositories und ist auf 60 Abfragen pro Stunde und Besucher begrenzt.

## Lokal testen

Browser erlauben das Laden von Dateien nicht, wenn man `index.html` direkt per Doppelklick öffnet. Deshalb im Projektordner:

```
python3 tools/build_manifest.py
python3 -m http.server 8000
```

Dann http://localhost:8000 öffnen.
