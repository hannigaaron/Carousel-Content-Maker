# Bildquelle

## Aktive Quelle: `assets/fotos/` im Repo

**Entscheidung: die Bilder liegen im Repo**, nicht in Drive. Sie werden über die
GitHub-Weboberfläche hochgeladen und beim Wochenlauf automatisch mitgeklont.
Kein API-Key, keine Kosten, keine externe Abhängigkeit.

Anleitung für den Upload: `assets/fotos/README.md`.
Welche Motive für die aktuellen Posts gebraucht werden:
`assets/fotos/BENOETIGTE-MOTIVE.md`.

### Warum nicht direkt aus Drive

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
