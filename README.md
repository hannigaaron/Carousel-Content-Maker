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
