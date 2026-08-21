# Wochenlauf — 3 Carousel-Posts erstellen

Dies ist die Anweisung, die der wöchentliche Automatik-Lauf ausführt. Sie ist
bewusst so geschrieben, dass sie ohne jeden Vorkontext funktioniert.

---

## Kontext einlesen (immer zuerst, vollständig)

1. `config/profile.md` — Zielgruppe, Tonalität, No-Gos
2. `config/carousel-format.md` — Slide-Aufbau und Referenz-Posts
3. `config/photo-sources.md` — Bildquelle und Auswahlregeln
4. `config/themen-backlog.md` — offene Themen + bereits gepostete
5. `config/lessons.md` — Feedback aus vergangenen Wochen
6. Die letzten **4 Wochenordner** unter `posts/` — für Themen-, Foto- und
   Formulierungs-Wiederholungen

**Abbruchbedingung:** Enthalten `config/profile.md` oder
`config/carousel-format.md` noch `TODO`-Platzhalter an den Stellen Zielgruppe,
Tonalität oder Slide-Aufbau, dann **keine Posts generieren**. Stattdessen eine
kurze Notiz in `posts/JJJJ-Wxx/_REVIEW.md` schreiben, welche Angaben fehlen, und
committen. Erfundene Zielgruppen-Annahmen produzieren nur Arbeit statt sie zu
sparen.

## Feedback der letzten Woche verarbeiten

Jeder Post der Vorwoche mit `status: überarbeiten: <Grund>`:

- Grund als dauerhafte Regel in `config/lessons.md` eintragen
- Den Post überarbeiten und in die neue Woche übernehmen — er zählt als einer
  der drei

## Themen wählen

Drei Themen nach der Reihenfolge in `config/themen-backlog.md`. Prüfen:

- Kein Thema aus den letzten 8 Wochen
- Maximal ein Thema pro Kategorie
- Jedes Thema trifft einen konkreten Schmerz aus `config/profile.md` — wenn du
  den Schmerz nicht benennen kannst, ist es das falsche Thema

## Posts schreiben

Pro Thema eine Datei `posts/JJJJ-Wxx/post-1.md` … `post-3.md` nach
`templates/post-template.md`, streng nach `config/carousel-format.md`.

Regeln, die über allem stehen:

- **Keine erfundenen Fakten.** Zahlen, Studien, Behauptungen entweder belegen
  (Quelle im Post) oder weglassen. Im Zweifel weglassen.
- **Keine Heilversprechen** und nichts, was als medizinischer oder
  Ernährungs-Rat für Einzelfälle gelesen werden kann.
- **Der Stil kommt aus den Referenz-Posts**, nicht aus generischem
  Social-Media-Deutsch.

## Fotos zuordnen

Nach den Auswahlregeln in `config/photo-sources.md`. Für jedes Foto eine
Ein-Satz-Begründung. Kein passendes Foto → `KEIN PASSENDES FOTO` plus
Beschreibung, was aufgenommen werden müsste. Niemals ein unpassendes Foto
danebenlegen, damit die Lücke gefüllt aussieht.

## Review-Datei schreiben

`posts/JJJJ-Wxx/_REVIEW.md`:

- Die drei Themen mit je einem Satz Begründung
- Was **du prüfen musst**: alle offenen Punkte aus den drei Posts gebündelt
- Alle verwendeten Fotos als Liste (für die 8-Wochen-Sperre)
- Ehrlich: was diesmal nicht gut lief oder unsicher ist

## Aufräumen und abschließen

1. `config/themen-backlog.md`: gewählte Themen aus "Offen" nach "Bereits
   gepostet" verschieben
2. Alles committen auf `claude/automated-carousel-posts-fe7689` und pushen
3. **Keinen Pull Request öffnen**, außer es wird ausdrücklich verlangt
