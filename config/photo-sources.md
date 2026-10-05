# Bildquelle

## Aktive Quelle: `assets/fotos/` im Repo

**Entscheidung: die Bilder liegen im Repo**, nicht in Drive. Sie werden über die
GitHub-Weboberfläche hochgeladen und beim Wochenlauf automatisch mitgeklont.
Kein API-Key, keine Kosten, keine externe Abhängigkeit.

Anleitung für den Upload: `assets/fotos/README.md`.
Welche Motive für die aktuellen Posts gebraucht werden:
`assets/fotos/BENOETIGTE-MOTIVE.md`.

### Stand 05.10.2026: Drive geht wieder direkt

**Die Netzsperre ist weg.** `drive.google.com` und
`drive.usercontent.google.com` antworten aus der Umgebung, und ein Download
funktioniert **ohne API-Key**, solange der Ordner auf "Jeder mit dem Link"
steht:

```
curl -L -o ziel.jpeg "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download"
```

Getestet mit einem 7,2-MB-Original aus dem Pool-Ordner. Die Datei landet direkt
auf der Platte, nichts davon geht durch den Modell-Kontext.

Was weiterhin einen Key braucht, ist das **Auflisten** des Ordnerinhalts über
die Drive-API. Dafür gibt es zwei Wege: entweder `DRIVE_API_KEY` setzen (Anleitung
unten), oder eine Session mit angebundenem Drive-Connector listet den Ordner und
lädt die fehlenden Dateien per curl nach. Der Wochenlauf-Trigger hat **keine
Connectors**, kann also von sich aus nicht in Drive schauen — bis ein Key
hinterlegt ist, bleibt der Fotobranch die Quelle für den automatischen Lauf.

### HEIC muss gewandelt werden

iPhone-Uploads sind oft `.HEIC`. **Der Renderer öffnet HEIC nicht** — solche
Dateien zählen faktisch nicht zum Pool. Umwandeln:

```
pip install pillow-heif
python3 -c "import pillow_heif, glob, os; from PIL import Image, ImageOps; pillow_heif.register_heif_opener()
[ImageOps.exif_transpose(Image.open(f)).convert('RGB').save(os.path.splitext(f)[0]+'.jpeg', quality=92) for f in glob.glob('assets/fotos/*.HEIC')]"
```

### Historie: warum der Pool wochenlang leer schien

Der Drive-Ordner *Claude Carousel Pool Blanko Fotos*
(`1tjgIb9c8dXdXgBLqYhBcS53jTsK_YSLh`) ist zwar lesbar — auflisten funktioniert.
Aber der Connector übergibt Dateien nur als Base64 durch den Modell-Kontext:
gemessen **rund 9.000 Tokens für ein 25-KB-Bild**, das obendrein nur 359×780
Pixel groß war. Die Originale im Ordner sind 700–900 KB. Für 17 Slides pro
Woche trägt dieser Weg nicht.

Der direkte Download über `drive.google.com` ist durch die Netzwerkrichtlinie
der Umgebung gesperrt. Erreichbar wäre `www.googleapis.com`, also die
Drive-API — dafür liegt `scripts/fetch_drive_photos.py` bereit, es fehlt nur
ein API-Key in `DRIVE_API_KEY`. Der Weg bleibt als Option bestehen, falls das
manuelle Hochladen später lästig wird; die Einrichtung steht unten.

Bilder, die lokal im Repo liegen, kosten dagegen fast nichts: Sie lassen sich
direkt ansehen und rendern, ohne dass ihre Bytes durch den Kontext müssen.

## Lesbarkeit hat Vorrang vor Motiv

Der Text muss auf jedem Slide im Vordergrund stehen. Der Renderer prüft das
selbst: Er misst nach dem Rendern die mittlere Helligkeit im Textbereich
(unteres Drittel) und verstärkt den Verlauf automatisch in bis zu drei Stufen.
Reicht auch die stärkste nicht, gibt er eine Warnung aus — dann braucht dieser
Slide ein anderes Foto oder einen anderen Ausschnitt (`focus`).

Daraus folgt für die Fotoauswahl:

1. **Ruhiges unteres Drittel.** Dort sitzt der Text. Ein Foto mit Fenster,
   Spiegelung, Beschriftung oder Gesicht genau dort ist ungeeignet, egal wie
   gut es sonst ist.
2. **Motiv verschieben statt Text.** Sitzt das Motiv im Bild unten, hilft
   `"focus": "top"` — das Bild wird anders angeschnitten.
3. **Kein harter Hell-Dunkel-Sprung hinter der Headline.** Das zerreißt die
   Zeile optisch.
4. Ein sehr helles Foto ist nicht verboten, kostet aber Verlaufsstärke — und
   damit Bildwirkung. Bei zwei gleich passenden Motiven gewinnt das dunklere.

## Lizenzfreie Fotos ohne API-Key (Openverse / Wikimedia Commons)

**Aktiver Weg seit 30.09.2026.** Aaron hat ausdrücklich freigegeben, dass für
Motive ohne Person (Küche, Essen, Kalender, Alltagsgegenstände) lizenzfreie
Fotos aus dem Internet genutzt werden.

```
python3 scripts/fetch_free_photos.py "restaurant table" --anzahl 5 --prefix frei-restaurant
```

- Nur Lizenzen **CC0** und **Public Domain Mark**: kommerziell nutzbar, ohne
  Namensnennung. Quelle, Urheber und Lizenz jedes Bildes stehen in der
  gleichnamigen `.json` in `assets/fotos/stock/`.
- Quelle ist nur Wikimedia Commons. Die anderen Openverse-Quellen liefern nur
  Vorschaubilder (960 px). Unsplash und Pixabay blocken Zugriffe ohne Browser
  bzw. ohne API-Key.
- Die Qualität schwankt stark: Museumsstücke, alte Stiche, Amateurfotos,
  fremde Gesichter. **Jeden Treffer ansehen**, am besten als Kontaktbogen, und
  gnadenlos aussortieren. Pro Motiv mehrere Suchbegriffe probieren
  ("skyr", "greek yogurt", "yogurt bowl").
- Nicht verwendete Treffer wieder löschen, damit der Ordner nur genutzte
  Bilder enthält.
- Schrift im Bild (Kalenderblätter, Schilder) darf nicht im Textbereich
  liegen. Überschneidet sie die Headline, Foto tauschen.

Die Grenze "höchstens ein Stock-Foto pro Post" (unten) gilt damit nicht mehr.
Es gilt stattdessen: Passung zum Slide vor Herkunft. Ein passendes Stock-Foto
schlägt ein eigenes Foto, das nur Stimmung liefert. Fremde Gesichter bleiben
tabu.

## Stock-Fotos als Ergänzung (Pixabay)

Zulässig, um Lücken zu füllen — aber sparsam und nur dort, wo keine Person ins
Bild gehört.

**Status:** Netzwerkzugang steht — `pixabay.com` ist in der Umgebung
freigegeben und die API antwortet. Es fehlt nur noch ein kostenloser API-Key
in `PIXABAY_API_KEY`.

**Einrichtung:** Konto auf https://pixabay.com/accounts/register/ anlegen, den
Key auf https://pixabay.com/api/docs/ abholen und als Umgebungsvariable
`PIXABAY_API_KEY` hinterlegen (claude.ai/code → Wolken-Symbol → Zahnrad →
*Environment variables*). Kosten entstehen nicht; das kostenlose Kontingent
liegt bei 100 Anfragen pro Minute.

**Nutzung:**

```
PIXABAY_API_KEY=... python3 scripts/fetch_stock_photos.py "meal prep" --anzahl 3
```

Das Skript sucht nur im **Hochformat ab 1080×1350** und legt die Treffer in
`assets/fotos/stock/` ab. Die Website selbst antwortet auf Kommandozeilen-
Zugriffe mit 403 (Bot-Schutz) — deshalb läuft alles über die API.

**Lizenz:** Die Pixabay Content License erlaubt kostenlose Nutzung auch
kommerziell, ohne Namensnennung. Nicht erlaubt ist der Weiterverkauf der Bilder
selbst — für Instagram-Slides unproblematisch.

**Wann Stock erlaubt ist**

| Erlaubt | Nicht erlaubt |
|---|---|
| Essen, Zutaten, Küche | Jeder Slide, auf dem Aaron zu sehen sein sollte |
| Schreibtisch, Kalender, Alltagsgegenstände | Cover — die tragen sein Gesicht |
| Details ohne Gesicht (Hantel, Schuhe, Gürtel) | Trainingsszenen |
| | Bilder mit fremden Personen |

**Harte Grenzen**

1. **Höchstens ein Stock-Foto pro Post.** Aarons Format lebt davon, dass er
   selbst drauf ist. Mischt sich Katalogoptik unter Handyfotos, merkt man den
   Bruch sofort — das war bei der Overnight-Oats-Bowl schon grenzwertig.
2. **Keine fremden Gesichter**, auch nicht angeschnitten. Model Releases sind
   bei Pixabay nicht garantiert.
3. **Im Post als Stock kennzeichnen**, damit Aaron es beim Review sofort sieht:
   Zeile `Foto: Stock (Pixabay)` in der Slide-Tabelle.
4. **Eigenes Foto schlägt Stock immer.** Stock nur, wenn im Pool nichts
   Passendes liegt.

## Gesperrte Fotos

**Vor jeder Auswahl `config/gesperrte-fotos.md` lesen.** Dort stehen Dateien,
die dauerhaft nicht verwendet werden dürfen, und die Regel dahinter: keine
Unterwäsche, kein nackter Oberkörper, keine Umkleide- oder Badsituationen.
Diese Regel steht über jeder anderen Erwägung — ein Slide bleibt lieber ohne
Bild.

Für Cover ohne Person eignen sich Gegenstände: Gymtasche, Trinkflasche,
Schuhe, Hantel, Trainingsplan auf dem Handy.

## Auswahlregeln

1. **Passung vor Schönheit** — das Foto muss zum Slide-Inhalt gehören, nicht nur
   gut aussehen.
2. **Kein Foto zweimal in 8 Wochen.** Verwendete Dateien werden pro Woche in
   `posts/JJJJ-Wxx/_REVIEW.md` protokolliert; dort steht auch, was schon lief.
3. **Hochformat 4:5 bevorzugt**, quadratisch okay, Querformat nur wenn nichts
   anderes passt (Zuschnitt-Hinweis dann im Post vermerken).
4. **Keine fremden Gesichter** ohne dokumentiertes Einverständnis.
5. Bei jedem Vorschlag wird **begründet**, warum genau dieses Foto zu diesem
   Slide passt — damit du die Auswahl in 5 Sekunden prüfen kannst.
6. Findet sich für einen Slide kein passendes Foto: ehrlich `KEIN PASSENDES FOTO`
   schreiben plus Beschreibung, was du fotografieren müsstest. Nichts erfinden.

## Format-Hinweis HEIC

iPhone-Fotos sind oft `.HEIC`. Instagram kommt damit klar, aber für die
Vorschau ist JPG einfacher. Falls du magst, in der Fotos-App beim Export
"Automatisch" statt "Original" wählen — dann kommt JPG raus.

## Option für später: automatischer Abgleich mit Drive

Falls das manuelle Hochladen lästig wird, holt `scripts/fetch_drive_photos.py`
die Bilder bei jedem Lauf selbst aus dem Drive-Ordner nach `assets/fotos/`.

1. In der [Google Cloud Console](https://console.cloud.google.com/) ein Projekt
   anlegen.
2. Unter *APIs & Dienste → Bibliothek* die **Google Drive API** aktivieren.
3. Unter *Anmeldedaten* einen **API-Schlüssel** erstellen, sinnvollerweise auf
   die Drive API eingeschränkt.
4. Der Ordner muss auf **"Jeder mit dem Link — Betrachter"** stehen.
5. Den Key als `DRIVE_API_KEY` in der Umgebung hinterlegen (Claude Code on the
   web → Environment → Umgebungsvariablen). **Nicht ins Repo committen.**

Kosten entstehen dabei nicht: Die Drive API hat keine kostenpflichtige Stufe,
nur Nutzungskontingente im Bereich von Tausenden Anfragen pro Tag, und ein
Abrechnungskonto ist für einen API-Key nicht erforderlich.
