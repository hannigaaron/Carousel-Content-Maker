# Wo dieses Projekt steht — Übergabe

Diese Datei ist für die Claude-Sitzung gedacht, die als Nächstes hier
weiterarbeitet (z. B. in der Desktop-App auf Aarons Mac). Sie fasst zusammen,
was fertig ist, was ansteht und wo die Fallstricke liegen.

## Worum es geht

Aaron (@coach.aaron.hannig, Personal Trainer) will wöchentlich drei fertige
Instagram-Carousel-Posts, die er nur noch durchsieht und hochlädt. Themenwahl,
Slide-Texte, Caption und Fotoauswahl sollen automatisch entstehen.

## Was fertig ist

- **Sein Format ist ausgelesen** aus einem echten Referenz-Post und in
  `config/carousel-format.md` festgeschrieben: Listen-Post mit Cover plus N
  nummerierten Punkten, Foto formatfüllend, dunkler Verlauf, Zähler oben links,
  Headline mit genau einem hellblauen Kursivwort (`#7CC7EC`), Trennlinie,
  Fließtext. Dazu Textregeln, Tonalität und der vollständige Referenz-Post.
- **Zielgruppe und Stimme** stehen in `config/profile.md`: vielbeschäftigte
  Berufstätige mit hohem Stresslevel und wenig Freizeit, die langfristige
  Ergebnisse bei geringem Zeitaufwand wollen. Daraus vier verbindliche Regeln
  für jeden Post.
- **Caption-Aufbau** mit sieben festen Blöcken und dem CTA-Codewort "PLAN",
  ebenfalls in `config/carousel-format.md`.
- **Renderer** (`scripts/render_slides.py`): macht aus einer JSON-Spezifikation
  fertige 1080×1350-PNGs. Braucht nur Chromium, keine Zusatzpakete. Prüft
  automatisch die Lesbarkeit (siehe unten).
- **Drei fertige Post-Entwürfe** in `posts/2026-W35/` — Texte, Captions und
  gerenderte Slides. **Aber noch ohne Fotos**, alle 17 Slides auf grauem
  Platzhalter.
- **Wochenlauf-Anweisung** in `prompts/weekly-run.md` — die Anleitung, die der
  automatische Montagslauf abarbeitet.

## Was als Nächstes ansteht

**Die Fotos zuordnen und neu rendern.** Konkret:

1. Aarons Foto-Ordner durchsehen — **die Bilder wirklich ansehen**, nicht nach
   Dateinamen raten. Die Dateien heißen alle wie `76CF5AF0-0CCD-…jpeg`.
2. Für jeden der 17 Slides das passende Foto wählen. Was pro Slide gebraucht
   wird und warum, steht in `assets/fotos/BENOETIGTE-MOTIVE.md` — dort ist auch
   vermerkt, welches Klischee jeweils zu vermeiden ist (z. B. **kein Laufband**
   beim Cardio-Slide, weil er dort für Alltagsbewegung argumentiert).
3. Die Pfade in `posts/2026-W35/post-*.slides.json` eintragen (Feld `photo`,
   relativ zur JSON-Datei) und rendern:
   `python3 scripts/render_slides.py posts/2026-W35/post-1.slides.json`
4. Die gerenderten PNGs ansehen und prüfen, ob der Text gut sitzt. Bei Bedarf
   `focus` setzen (z. B. `"focus": "top"`) und neu rendern.
5. Ergebnis an Aaron schicken.

## Fallstricke

- **HEIC wird nicht gerendert.** Der Renderer bricht mit klarer Meldung ab.
  iPhone-Fotos vorher als JPG exportieren.
- **Lesbarkeit prüft der Renderer selbst.** Er misst die Helligkeit im
  Textbereich und verstärkt den Verlauf in bis zu drei Stufen. Meldet er
  `Textbereich bleibt hell`, ist das Foto ungeeignet — dann tauschen, nicht
  durchwinken. Aaron hat ausdrücklich verlangt, dass der Text immer im
  Vordergrund steht und gut lesbar ist.
- **Das untere Drittel ist die Textzone.** Fotos mit Fenster, Spiegelung,
  Schrift oder Gesicht genau dort sind ungeeignet, egal wie gut sie sonst sind.
- **GitHub-Push war in der Web-Umgebung blockiert** (403, die Claude-App war im
  Konto nicht installiert). Zehn Commits lagen nur lokal. Auf dem Mac ist das
  kein Thema mehr — falls das Repo doch wieder angebunden wird, vorher prüfen,
  ob `git push` durchgeht.
- **Google Drive und der API-Weg** (`scripts/fetch_drive_photos.py`) sind
  dokumentiert, aber nicht mehr nötig, wenn die Fotos lokal liegen. Der Grund
  für den Umweg: Der Drive-Connector schickt Bilder als Base64 durch den
  Kontext — rund 9.000 Tokens für ein 25-KB-Bild. Lokale Dateien kosten das
  nicht.

## Offene inhaltliche Fragen an Aaron

Stehen auch in `posts/2026-W35/_REVIEW.md`:

1. Trifft der Ton? Das Format ist nachgebaut, aber mit nur einem Referenz-Post
   ist die Stimme noch nicht sicher getroffen. Weitere Beispiel-Posts von ihm
   wären der größte Hebel.
2. Post 1, Slide 4: Soll eine konkrete Schrittzahl rein? Bewusst offen
   gelassen, weil die Angaben je nach Quelle schwanken.
3. Post 2, Regel 01: "in drei stressigen Wochen verlierst du keine Muskeln" —
   vertretbar, aber ohne Quelle.
4. Post 3, Zeichen 02: setzt voraus, dass tagsüber zu wenig gegessen wird.
   Eventuell zu pauschal.
5. Der Zähler heißt bei Post 2 `REGEL` und bei Post 3 `ZEICHEN`, abgeleitet aus
   seinem `DING`. Er hat das nie so benutzt — bestätigen lassen.

## Wöchentliche Automatik

Eine Routine ist angelegt (montags 7:03 Uhr, Benachrichtigung per Push und
E-Mail), die `prompts/weekly-run.md` abarbeitet. Sie hing an der
Web-Umgebung und am GitHub-Zugriff. Läuft die Arbeit künftig lokal, muss der
wiederkehrende Lauf dort neu eingerichtet werden.
