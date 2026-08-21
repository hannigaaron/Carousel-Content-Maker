# Carousel Content Maker

Automatisiertes System, das **jede Woche 3 fertige Carousel-Posts** vorbereitet:
Thema, Slide-für-Slide-Text, Caption, Hashtags und die passenden Fotos aus deiner
Galerie. Du machst nur noch Review — Haken dran oder Kommentar dazu.

## Wie es läuft

1. **Wöchentlicher Lauf** (Routine, standardmäßig Montag früh): startet automatisch
   eine Claude-Session, die `prompts/weekly-run.md` abarbeitet.
2. Die Session liest deine Regeln aus `config/` (Zielgruppe, Stil, Slide-Aufbau,
   Themen-Backlog, was schon gepostet wurde).
3. Sie sucht passende Fotos aus deiner Bildquelle (`config/photo-sources.md`).
4. Sie schreibt 3 Posts nach `templates/post-template.md` in einen neuen Ordner
   `posts/JJJJ-Wxx/` und legt dort eine `_REVIEW.md` mit Checkliste an.
5. Du liest drüber, änderst was du willst, setzt den Status auf `freigegeben`
   und lädst hoch.

## Review-Workflow

Jeder Post hat oben einen Status:

- `entwurf` — frisch generiert, wartet auf dich
- `freigegeben` — passt, kann hoch
- `überarbeiten: <dein Kommentar>` — beim nächsten Lauf wird der Post neu gebaut,
  und der Grund wandert als Lernregel nach `config/lessons.md`

Der nächste Lauf liest die letzten 4 Wochen mit, damit sich Themen und Fotos
nicht wiederholen und dein Feedback tatsächlich ankommt.

## Struktur

| Pfad | Zweck |
|---|---|
| `config/profile.md` | Wer du bist, Zielgruppe, Tonalität, No-Gos |
| `config/carousel-format.md` | Slide-Aufbau, abgeleitet aus deinen Beispiel-Posts |
| `config/photo-sources.md` | Wo die Fotos herkommen und wie ausgewählt wird |
| `config/themen-backlog.md` | Themenpool + was schon gelaufen ist |
| `config/lessons.md` | Gelerntes aus deinem Review-Feedback |
| `prompts/weekly-run.md` | Die Anweisung, die der wöchentliche Lauf ausführt |
| `templates/post-template.md` | Format eines einzelnen Posts |
| `posts/JJJJ-Wxx/` | Die generierten Posts der jeweiligen Woche |

## Manuell auslösen

Einfach in einer Session sagen: *"Führ den Wochenlauf aus"* — dann wird
`prompts/weekly-run.md` sofort abgearbeitet, unabhängig vom Zeitplan.

## Slides als Bild rendern

Der Text allein reicht nicht zum Hochladen — deshalb erzeugt das System die
Slides gleich als fertige PNGs im Format aus `config/carousel-format.md`
(Foto formatfüllend, dunkler Verlauf, Zähler oben links, Headline mit
hellblauem Kursivwort, Trennlinie, Fließtext).

```
python3 scripts/render_slides.py posts/2026-W35/post-1.slides.json
```

Ergebnis: `posts/2026-W35/post-1-slides/slide-01.png` … in 1080×1350.

Aufbau der JSON-Datei: siehe `scripts/beispiel-slides.json`. Kurz:

- `type`: `"cover"` (größere Headline) oder `"point"`
- `counter`: `"1/6"` bzw. `"DING 02 / 05"`
- `headline`: `\n` für Zeilenumbrüche, `{Wort}` für das hellblaue Kursivwort
- `body` (bzw. `subline` auf dem Cover): der Fließtext
- `photo`: Pfad relativ zur JSON-Datei; fehlt er, kommt ein grauer Verlauf
- `focus`: Bildausschnitt, z. B. `"top"` oder `"30% 20%"`, falls der Text über
  einem unruhigen Bildbereich steht

Gebraucht wird nur Chromium — keine Zusatzpakete. HEIC-Dateien vom iPhone
müssen vorher als JPG exportiert werden; das Skript sagt es dir, statt still
etwas Kaputtes zu erzeugen.
