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
6. `config/foto-historie.md` — welche Bilder schon gelaufen sind
7. Die letzten **4 Wochenordner** unter `posts/` — für Themen-, Foto- und
   Formulierungs-Wiederholungen

Zielgruppe, Tonalität und Slide-Aufbau sind ausgefüllt — der Lauf startet also.
Ist `assets/fotos/` leer, werden die Posts trotzdem vollständig getextet; die
Fotos bleiben dann als beschriebene Leerstellen offen und die Slides rendern
auf grauem Platzhalter. Nichts erfinden, nichts beschönigen.

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

Quelle und Regeln: `config/photo-sources.md`.

1. **Bildpool.** Die Fotos liegen bereits in `assets/fotos/` im Arbeitsbranch.
   Nur falls der Ordner leer ist, vom separaten Branch nachladen:

   ```
   git fetch origin assets/fotos
   git archive origin/assets/fotos | tar -x -C assets/fotos/
   ```

2. **Nur brauchbare Auflösungen verwenden.** Ein großer Teil des Pools sind
   verkleinerte Kopien (359×780). Für 1080×1350 muss ein Bild mindestens
   700 px breit sein — darunter wird es auf Instagram matschig. Vorher filtern.

3. **Jedes in Frage kommende Foto tatsächlich ansehen**, nicht nach Dateinamen
   raten — `IMG_9231.jpeg` sagt nichts über das Motiv. Lokale Dateien
   anzusehen ist billig; das ist der Grund, warum die Bilder im Repo liegen
   und nicht in Drive.

4. **`config/foto-historie.md` beachten:** kein Bild, das in den letzten
   8 Wochen schon lief. Nach der Auswahl die neuen Einträge dort nachtragen.
5. Pro Slide das Foto wählen, das **die Situation zeigt, über die der Slide
   spricht** — nicht das schönste Bild.
6. Vorher prüfen: Ist das untere Drittel ruhig genug für den Text? Wenn nicht,
   `focus` setzen oder ein anderes Foto nehmen.
7. Für jedes Foto eine Ein-Satz-Begründung in den Post schreiben.
8. Kein passendes Foto → `KEIN PASSENDES FOTO` plus Beschreibung, was
   aufgenommen werden müsste. Niemals ein unpassendes Foto danebenlegen, damit
   die Lücke gefüllt aussieht.
9. Meldet der Renderer, dass der Textbereich hell bleibt, wird das Foto
   getauscht — nicht durchgewunken.

## Slides rendern

Für jeden Post zusätzlich eine Datei `post-N.slides.json` nach dem Muster in
`scripts/beispiel-slides.json` schreiben und rendern:

```
python3 scripts/render_slides.py posts/JJJJ-Wxx/post-N.slides.json
```

Damit liegen die fertigen 1080×1350-PNGs in
`posts/JJJJ-Wxx/post-N-slides/` — Aaron kann sie direkt hochladen.

Regeln dafür:

- `{geschweifte Klammern}` markieren das hellblaue Kursivwort. Genau eines pro
  Slide, und zwar das Wort, auf das es ankommt.
- Zeilenumbrüche in der Headline (`\n`) bewusst setzen: 2 Zeilen, der Umbruch
  darf keine Sinneinheit zerreißen.
- Ohne Foto rendert der Slide auf grauem Verlauf. Das ist als Platzhalter
  gedacht und im Post als offener Punkt zu vermerken, nicht als fertig zu
  verkaufen.
- Nach dem Rendern die PNGs ansehen und prüfen: Steht Text über einem unruhigen
  Bildbereich? Dann `focus` anpassen (z. B. `"focus": "top"`) und neu rendern.

## Ablage für Aaron bauen

Zum Schluss die Woche in eine Form bringen, in der er nur noch nachsieht:

```
python3 scripts/build_upload_folder.py posts/JJJJ-Wxx
```

Das erzeugt `FERTIG-ZUM-HOCHLADEN/JJJJ-Wxx/` mit einem Ordner je Post, den
Slides in Upload-Reihenfolge (`01.png`, `02.png`, …), der Caption als
`caption.txt` zum Kopieren und `NOCH-ZU-PRUEFEN.txt`, wo etwas offen ist.

## Review-Datei schreiben

`posts/JJJJ-Wxx/_REVIEW.md`:

- Die drei Themen mit je einem Satz Begründung
- Was **du prüfen musst**: alle offenen Punkte aus den drei Posts gebündelt
- Alle verwendeten Fotos als Liste (für die 8-Wochen-Sperre)
- Ehrlich: was diesmal nicht gut lief oder unsicher ist

## Aufräumen und abschließen

1. `config/themen-backlog.md`: gewählte Themen aus "Offen" nach "Bereits
   gepostet" verschieben
2. `config/foto-historie.md`: verwendete Bilder mit Woche und Slide eintragen
3. Alles committen auf `claude/automated-carousel-posts-fe7689` und pushen
4. **Keinen Pull Request öffnen**, außer es wird ausdrücklich verlangt
