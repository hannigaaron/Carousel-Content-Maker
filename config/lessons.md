# Gelernt aus deinem Feedback

Jedes Mal, wenn du einen Post auf `überarbeiten: <Grund>` setzt, wird der Grund
hier als dauerhafte Regel eingetragen. Der nächste Lauf liest diese Datei und
macht denselben Fehler nicht noch mal.

| Datum | Was war falsch | Regel daraus |
|---|---|---|
| 30.09.2026 | Hintergrundfotos passten teils nur als Stimmung, nicht zum Inhalt des Slides | Jedes Foto muss die Situation zeigen, über die der Slide spricht. Test und Beispiele stehen in `prompts/weekly-run.md` unter "Fotos zuordnen", Punkt 6. Im Zweifel kein Foto statt eines halb passenden. |
| 05.10.2026 | Vier Wochen lang meldete der Lauf "Fotopool leer", während 16 Originale ungenutzt in Aarons Drive-Ordner lagen und nie auf dem Fotobranch ankamen. Dazu rendern HEIC-Uploads nicht. | Vor jedem Lauf prüfen, ob der Fotobranch den Stand des Drive-Ordners hat, und HEIC vor der Auswahl nach JPG wandeln. Wenn der Pool leer *wirkt*, ist das zuerst ein Transportproblem, keine Content-Entscheidung. |
| 05.10.2026 | Zwei Wochen Posts existierten nur auf der Übersichtsseite, weil der Lauf nichts committet hat. Aaron konnte sie sehen, aber nicht hochladen. | Der Lauf ist erst fertig, wenn `posts/`, `FERTIG-ZUM-HOCHLADEN/` und die Config-Änderungen committet **und gepusht** sind. Eine aktualisierte Seite ohne Commit zählt nicht als Ergebnis. |
| 19.10.2026 | Der Lauf nannte "20 Minuten" Training als Maß. Das ist nicht Aarons Ansatz. | **Aarons USP ist 30 Minuten pro Einheit, und das ist das absolute Minimum.** Nie "20 Minuten" oder weniger als Trainingsdauer nennen, auch nicht als Notfallversion. Kleinste Version = 30 Minuten. |
| 19.10.2026 | Lauf lieferte nur 2 Posts, weil der eigene Pool leer war, obwohl Internetbilder erlaubt sind. | Aaron: Bildmaterial aus dem Internet aktiv nutzen. Bei leerem oder verbrauchtem Pool zuerst `scripts/fetch_free_photos.py` (CC0/PD, Wikimedia) mit mehreren Suchbegriffen, dann erst Posts kürzen. Bleibt: keine erkennbaren fremden Gesichter, Kennzeichnung `Foto: Stock`, Passungstest aus Punkt 6, 30-Minuten-Regel für Inhalte. |
| 19.10.2026 | Fotos der alten Küche (IMG_7835, IMG_7836, IMG_7838) wirken ungepflegt. | Diese drei nie mehr verwenden. Nur die moderne Küche (IMG_9805) ist okay. Küchen-Slides lieber mit passenden Stock-Fotos bebildern. |
