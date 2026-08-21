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
