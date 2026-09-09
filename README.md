# Carousel Content Maker

Aus einer JSON-Datei werden fertige Instagram-Carousels: gerenderte Slides,
passende **frei lizenzierte Fotos aus dem Netz**, Caption und Bildnachweise.

```
python3 -m carousel build content/beispiel-fokus.json
```

→ `out/beispiel-fokus/fokus-01.jpg … fokus-06.jpg`, `fokus-caption.txt`, `fokus-CREDITS.md`

## Installation

```bash
pip install -r requirements.txt
```

Schriften (Plus Jakarta Sans, Inter) werden beim ersten Lauf von Google Fonts geladen
und in `fonts/` gecacht. Ohne Netz greift der Renderer auf eine Systemschrift zurück.

## Bilder

Jeder Slide kann ein `image` haben:

| Wert | Bedeutung |
| --- | --- |
| `"search:foggy forest path"` | sucht online ein frei lizenziertes Foto |
|  `"IMG_7773.jpeg"` | nutzt ein Bild aus dem Repo |
| weggelassen | einfarbiger Hintergrund im Theme |

Gesucht wird bei **Wikimedia Commons** (Erstquelle) und **Openverse** (Fallback).
Es werden nur Bilder übernommen, die kommerziell nutzbar und bearbeitbar sind –
Public Domain, CC0, CC BY, CC BY-SA. NC- und ND-Lizenzen fliegen raus.

Namensnennung ist bei CC BY und CC BY-SA Pflicht. Der Build schreibt sie in
`<slug>-CREDITS.md` – der Inhalt gehört in die Caption oder in den ersten Kommentar.

Vor dem Bauen prüfen, was ein Stichwort liefert:

```bash
python3 -m carousel search "foggy forest morning path"
```

Zweimal dasselbe Stichwort im selben Carousel liefert automatisch
unterschiedliche Fotos (Treffer 0, dann Treffer 1, …). Mit
`"search:burger fries plate#2"` wählst du einen Treffer gezielt aus.

## Slide-Typen

| `type` | Felder | Wofür |
| --- | --- | --- |
| `cover` | `kicker`, `title`, `subline` | erster Slide, der den Swipe auslösen muss |
| `text` | `kicker`, `title`, `body` | ein Gedanke pro Slide |
| `list` | `title`, `items[]`, `numbered` | die eigentliche Liste |
| `stat` | `value`, `label` | eine große Zahl |
| `quote` | `quote`, `author` | Zitat |
| `cta` | `kicker`, `title`, `body`, `button` | letzter Slide |
| `photo` | `title` | Foto füllt den Slide, ein Satz in Versalien liegt mittig darauf |
| `summary` | `title`, `lines[]`, `closing[]` | Überschrift, Trennlinie, kurze Zeilen, Blatt, Schlusssatz |

Zusätzlich auf jedem Slide möglich: `image`, `scrim` (0–1, wie stark das Foto
abgedunkelt wird) und `blur` (Weichzeichner in Pixeln).

`photo` kennt zusätzlich `anchor` (0–1, Höhe des Textes im Bild), `size`,
`tracking` (Sperrung), `max_lines` und `color`. `summary` nutzt dieselben
Felder plus `body_size`, `rule` (Breite der Trennlinie) und `leaf` (Größe des
Blattzeichens). Die Schriftfarbe wird sonst
automatisch gewählt: Der Renderer misst die Helligkeit hinter dem Text und
schreibt auf hellen Tellern dunkel statt weiß. Für dieses Format gehört
`"footer": false` auf Deck-Ebene dazu – Instagram zeigt den Slide-Zähler selbst.

Schriftgrößen werden automatisch verkleinert, bis der Text in seine Box passt –
lange Texte brechen das Layout nicht, sie werden nur kleiner.

## Content-Datei

```jsonc
{
  "slug": "fokus",              // Dateiname der Slides
  "title": "…",                 // Überschrift der CREDITS-Datei
  "handle": "@deinhandle",      // Fußzeile links
  "format": "portrait",         // portrait (1080×1350) oder square (1080×1080)
  "theme": "midnight",          // midnight | paper | forest | clean | sunset
  "theme_overrides": { "accent": "#7dd3a0" },   // optional
  "slides": [ … ],
  "caption": "…",
  "hashtags": ["fokus", "deepwork"]
}
```

`python3 -m carousel themes` listet die Themes mit ihren Farben. Das Theme
`clean` gehört zum `photo`-Format.

Gesetzt wird durchgehend in **Plus Jakarta Sans** (Überschriften und Text auf
Fotos) und **Inter** (Fließtext). Beide sind Grotesken – auf einem Foto trägt
eine kräftige Groteske deutlich weiter als eine Serifenschrift, und Versalien
darin brauchen nur wenig Sperrung.

Zwei Beispiele liegen bei:

- `content/beispiel-fokus.json` – gemischte Slide-Typen, dunkles Theme
- `content/ernaehrung-30-tage.json` – neun Slides im `photo`- und `summary`-Format

## Struktur

```
carousel/
  theme.py    Farben, Typo, Maße
  fonts.py    Schriften laden (Google Fonts + Fallback)
  images.py   Bildsuche, Lizenzfilter, Download-Cache
  render.py   Layout der einzelnen Slide-Typen
  build.py    JSON → Slides + Caption + Credits
  cli.py      build / search / themes
content/      Content-Dateien
*.jpeg        deine eigenen Fotos (im Repo-Wurzelverzeichnis)
out/          Ergebnis (nicht eingecheckt)
```
