# Übergabe: Post "Warum keine Zeit fast nie an der Zeit liegt" mit Aarons Fotos

Auftrag von Aaron (07.10.2026): Diesen Carousel-Post mit seinen eigenen Fotos
neu bebildern, rendern und ihm schicken. Die Texte bleiben unverändert.

## Wo alles liegt

- Branch: `claude/automated-carousel-posts-fe7689`
- Post: `posts/2026-W39/post-1.md` und `posts/2026-W39/post-1.slides.json`
- Rendern: `python3 scripts/render_slides.py posts/2026-W39/post-1.slides.json`
- Upload-Ordner bauen: `python3 scripts/build_upload_folder.py posts/2026-W39`
- Caption: steht bereinigt im Abschnitt `## Caption` in `post-1.md`, CTA-Codewort
  PLAN. Nicht neu umbrechen.

## Aktuelle Bebilderung

| Slide | Text | Foto jetzt | Was passen würde |
|---|---|---|---|
| 1 Cover | Warum "keine Zeit" fast nie an der *Zeit* liegt | Aaron am Automaten, abends (eigenes Foto) | Aaron im Alltag unter Zeitdruck, nicht im Gym. Kann bleiben. |
| 2 Grund 01 | Es ist eine *Prioritäten*-Frage (zwei Stunden Serie am Abend) | Stock: Fernseher im Wohnzimmer | Sofa, Fernseher oder Handy am Abend |
| 3 Grund 02 | Du rechnest mit der *falschen* Zahl (fünf Einheiten unrealistisch, zwei feste Termine halten) | keins | Gepackte Sporttasche an der Tür, Kalender mit zwei Terminen |
| 4 Grund 03 | Der Umweg über die *Perfektion* (20 Minuten, die stattfinden, schlagen 90 geplante) | keins | Kurze Einheit, Uhr oder Timer sichtbar |
| 5 Grund 04 | Am Ende zählt der *Kalender* (was nicht geblockt ist, verliert) | Stock: Handy und Notizbuch am Schreibtisch | Handy-Kalender oder Planer mit geblockten Terminen |

Eigene Fotos von Aaron ersetzen die Stock-Bilder, wo sie passen.

## Regeln, die gelten

- Jedes Foto zeigt die Situation, über die der Slide spricht. Stimmungsbilder
  nur fürs Cover. Test steht in `prompts/weekly-run.md`, Fotos zuordnen, Punkt 6.
- Kein Text im Foto darf die Headline überlappen. Nach dem Rendern jeden Slide
  ansehen.
- `config/gesperrte-fotos.md` und die 8-Wochen-Sperre in `config/foto-historie.md`
  beachten.
- Im Zweifel bleibt ein Slide ohne Foto, statt ein halb passendes zu nehmen.

## Abschluss

1. `config/foto-historie.md` nachtragen, Foto-Begründungen in `post-1.md`
   aktualisieren.
2. Upload-Ordner neu bauen, committen, auf `claude/automated-carousel-posts-fe7689`
   pushen.
3. Die fünf Slides und `caption.txt` per SendUserFile an Aaron schicken.
