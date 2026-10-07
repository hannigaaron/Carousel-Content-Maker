# Übergabe: Beide Posts aus KW 39 mit Aarons Fotos

Auftrag von Aaron (07.10.2026): Beide Carousel-Posts aus KW 39 mit seinen
eigenen Fotos neu bebildern, rendern und ihm schicken. Die Texte bleiben
unverändert.

- Post 1: "Warum keine Zeit fast nie an der Zeit liegt"
- Post 2: "3 Regeln fürs Auswärtsessen, die keine Woche ruinieren"

## Wo alles liegt

- Branch: `claude/automated-carousel-posts-fe7689`
- Posts: `posts/2026-W39/post-1.md` / `post-1.slides.json` und
  `posts/2026-W39/post-2.md` / `post-2.slides.json`
- Rendern: `python3 scripts/render_slides.py posts/2026-W39/post-1.slides.json`
  und dasselbe für `post-2.slides.json`
- Upload-Ordner bauen: `python3 scripts/build_upload_folder.py posts/2026-W39`
- Captions: stehen bereinigt im Abschnitt `## Caption` der Post-Dateien,
  CTA-Codewort PLAN. Nicht neu umbrechen.

## Post 1: Aktuelle Bebilderung

| Slide | Text | Foto jetzt | Was passen würde |
|---|---|---|---|
| 1 Cover | Warum "keine Zeit" fast nie an der *Zeit* liegt | Aaron am Automaten, abends (eigenes Foto) | Aaron im Alltag unter Zeitdruck, nicht im Gym. Kann bleiben. |
| 2 Grund 01 | Es ist eine *Prioritäten*-Frage (zwei Stunden Serie am Abend) | Stock: Fernseher im Wohnzimmer | Sofa, Fernseher oder Handy am Abend |
| 3 Grund 02 | Du rechnest mit der *falschen* Zahl (fünf Einheiten unrealistisch, zwei feste Termine halten) | keins | Gepackte Sporttasche an der Tür, Kalender mit zwei Terminen |
| 4 Grund 03 | Der Umweg über die *Perfektion* (20 Minuten, die stattfinden, schlagen 90 geplante) | keins | Kurze Einheit, Uhr oder Timer sichtbar |
| 5 Grund 04 | Am Ende zählt der *Kalender* (was nicht geblockt ist, verliert) | Stock: Handy und Notizbuch am Schreibtisch | Handy-Kalender oder Planer mit geblockten Terminen |

## Post 2: Aktuelle Bebilderung

| Slide | Text | Foto jetzt | Was passen würde |
|---|---|---|---|
| 1 Cover | 3 Regeln fürs Auswärtsessen, die keine Woche *ruinieren* | Stock: Bistrotisch im Restaurant | Aaron im Restaurant, in der Kantine oder beim Essen mit Freunden |
| 2 Regel 01 | Vorher nicht *hungrig* hinsetzen (vorher ein Joghurt oder eine Hand Nüsse) | Stock: Skyr mit Brombeeren | Joghurt, Skyr oder Nüsse als kleiner Snack |
| 3 Regel 02 | Eine *Entscheidung*, nicht der ganze Abend (Vorspeise oder Nachtisch, nicht beides) | Stock: Torte im Café | Nachtisch oder Vorspeise im Restaurant |
| 4 Regel 03 | Der *nächste* Tag zählt mehr als der Abend (normal weiteressen statt hungern) | Stock: Frühstück mit Toast und Kaffee | Normales Frühstück am nächsten Morgen |

Eigene Fotos von Aaron ersetzen die Stock-Bilder, wo sie passen. Passt kein
eigenes Foto, bleibt das Stock-Bild.

## Regeln, die gelten

- Jedes Foto zeigt die Situation, über die der Slide spricht. Stimmungsbilder
  nur fürs Cover. Test steht in `prompts/weekly-run.md`, Fotos zuordnen, Punkt 6.
- Kein Text im Foto darf die Headline überlappen. Nach dem Rendern jeden Slide
  ansehen.
- `config/gesperrte-fotos.md` und die 8-Wochen-Sperre in `config/foto-historie.md`
  beachten.
- Im Zweifel bleibt ein Slide ohne Foto, statt ein halb passendes zu nehmen.

## Abschluss

1. `config/foto-historie.md` nachtragen, Foto-Begründungen in `post-1.md` und
   `post-2.md` aktualisieren.
2. Upload-Ordner neu bauen, committen, auf `claude/automated-carousel-posts-fe7689`
   pushen.
3. Pro Post einen SendUserFile-Aufruf an Aaron: alle Slides in Reihenfolge
   plus `caption.txt` aus `FERTIG-ZUM-HOCHLADEN/2026-W39/<Post>/`.
