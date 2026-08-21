# Bildquelle

## Aktive Quelle

**Google-Drive-Ordner "Claude Carousel Pool Blanko Fotos"**
`1tjgIb9c8dXdXgBLqYhBcS53jTsK_YSLh`
https://drive.google.com/drive/folders/1tjgIb9c8dXdXgBLqYhBcS53jTsK_YSLh

**Status: Inhalt noch nicht lesbar.** Der Ordner gehört
`personalcoach.aaron@gmail.com`; verbunden ist in dieser Umgebung
`hannigaaron@gmail.com`. Über die ID lässt sich der Ordner zwar auflösen (Name,
Besitzer, Änderungsdatum), seine Dateien tauchen aber in keiner Suche auf — ein
nur per Link freigegebener Ordner landet nicht im Datei-Index des anderen
Kontos.

**Was das löst:** den Ordner aus dem Besitzer-Konto heraus **direkt an
`hannigaaron@gmail.com` freigeben** (nicht nur "Link kopieren"). Danach steht er
unter "Für mich freigegeben" und ist auflistbar. Alternativ das zweite
Google-Konto auf claude.ai als eigenen Connector verbinden.

## So kommen die Bilder in den Renderer

Der Drive-Connector kann die Dateien zwar auflisten und herunterladen, schickt
sie dabei aber als Base64 durch den Modell-Kontext. Gemessen: **ein einziges
25-KB-Bild kostet rund 9.000 Tokens** — und ist mit 359×780 Pixeln ohnehin nur
eine verkleinerte Kopie. Die brauchbaren Originale im Ordner sind 700–900 KB.
Für 17 Slides pro Woche ist dieser Weg nicht tragbar.

Der direkte Download über `drive.google.com` ist von hier aus gesperrt
(Netzwerkrichtlinie der Umgebung). **Erreichbar ist aber
`www.googleapis.com`** — die Drive-API. Ihr fehlt nur ein API-Key; für einen
per Link freigegebenen Ordner genügt ein einfacher Key, kein OAuth.

### Einrichtung (einmalig)

1. In der [Google Cloud Console](https://console.cloud.google.com/) ein Projekt
   anlegen (oder ein vorhandenes nehmen).
2. Unter *APIs & Dienste → Bibliothek* die **Google Drive API** aktivieren.
3. Unter *Anmeldedaten* einen **API-Schlüssel** erstellen. Sinnvoll einschränken:
   Anwendung auf die Drive API begrenzen.
4. Der Ordner muss auf **"Jeder mit dem Link — Betrachter"** stehen.
5. Den Key als Umgebungsvariable `DRIVE_API_KEY` in der Umgebung hinterlegen
   (Claude Code on the web → Environment → Umgebungsvariablen). **Nicht ins
   Repo committen.**

Danach:

```
DRIVE_API_KEY=... python3 scripts/fetch_drive_photos.py
```

Das lädt alle Bilder nach `assets/fotos/`, überspringt schon vorhandene und
schreibt eine `index.json` mit Dateiname, ID und Bildmaßen. Von dort holt der
Renderer sie direkt — ohne Kontextkosten.

### Kostenfrage

Der API-Key kostet nichts. Die Drive API hat keine kostenpflichtige Stufe,
sondern nur Nutzungskontingente im Bereich von Tausenden Anfragen pro Tag —
gebraucht werden hier ein paar Dutzend pro Woche. Ein Abrechnungskonto ist
für einen API-Key nicht erforderlich.

## Alternative ohne Google-Projekt: Fotos im Repo

Genauso gut funktioniert es, die Bilder direkt unter `assets/fotos/` ins Repo
zu legen — über die GitHub-Weboberfläche hochladen, ohne Terminal. Dann liegen
sie bei jedem Klon des Wochenlaufs automatisch bereit, ohne API und ohne
Kontextkosten. Der Renderer greift auf denselben Ordner zu, es ändert sich
also nichts am Ablauf.

Zwei Hinweise dazu:

- **Kuratieren statt alles hochladen.** 30–40 gute Bilder reichen für Monate;
  100 Originale à 800 KB blähen das Repo unnötig auf.
- **Nachlegen ist Handarbeit.** Neue Fotos musst du selbst hochladen, während
  der API-Weg den Drive-Ordner bei jedem Lauf automatisch abgleicht.

### Solange weder Key noch Bilder im Repo vorliegen

Der Wochenlauf textet die Posts vollständig und beschreibt pro Slide, welches
Foto gebraucht wird. Die Slides werden auf grauem Platzhalter gerendert. Das
ist der dokumentierte Zwischenstand, kein stiller Fehler.

## Zugriff der Automatik

Der Wochenlauf läuft in einem Container in der Cloud und hat keinen Zugriff auf
die Fotos-App oder die iCloud-Mediathek — nur auf Google Drive. Der Ordner oben
ist deshalb die Brücke: Bilder vom iPhone über die Drive-App hochladen, vom Mac
über Google Drive für Desktop im Finder ablegen.

Wichtig für die Routine selbst: Sie wurde ohne Connector-Rechte angelegt und
kommt damit **nicht** an Drive. Damit sie die Fotos eigenständig aussucht, muss
sie einmal über die Routines-Oberfläche auf claude.ai neu angelegt und Google
Drive dabei freigegeben werden.

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

## Auswahlregeln (gelten, sobald die Quelle steht)

1. **Passung vor Schönheit** — das Foto muss zum Slide-Inhalt gehören, nicht nur
   gut aussehen.
2. **Kein Foto zweimal in 8 Wochen.** Verwendete Dateien werden pro Woche in
   `posts/JJJJ-Wxx/_REVIEW.md` protokolliert.
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
