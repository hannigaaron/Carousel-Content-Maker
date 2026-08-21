# Bildquelle

## Deine Wahl

**Fotos aus der Bilder-Galerie von iPhone / Mac.**

## Wichtig: die Automatik kommt da nicht direkt ran

Der wöchentliche Lauf läuft in einem Container in der Cloud, nicht auf deinem
Mac. Er hat keinen Zugriff auf die Fotos-App, nicht auf deine iCloud-Mediathek
und nicht auf das Dateisystem deines Rechners. Das ist keine Einstellungssache,
sondern die Grenze der Umgebung.

Damit die Fotos trotzdem automatisch nutzbar sind, braucht es **eine Brücke**:
einen Ordner, in den deine Bilder ohnehin landen und auf den die Automatik
lesend zugreifen darf.

## Empfohlene Brücke: Drive-Ordner, per Sync gefüttert

1. In Google Drive einen Ordner `Content-Fotos/` anlegen, gern mit Unterordnern:

```
Content-Fotos/
  training-gym/
  ernaehrung-essen/
  portraits-mich/
  alltag-behind-the-scenes/
```

2. Auf dem Mac **Google Drive für Desktop** installieren. Der Ordner erscheint
   dann im Finder. Du markierst in der Fotos-App die Bilder, die für Content
   taugen (z. B. mit einem Album "Content"), exportierst sie einmalig in den
   Finder-Ordner — ab da synchronisiert Drive automatisch.
3. Vom iPhone: die Google-Drive-App hat "Hochladen → Fotos". Bilder direkt nach
   `Content-Fotos/` schieben, dauert Sekunden.
4. Ordner-ID hier eintragen: `<TODO>`

Aufwand für dich: einmal einrichten, danach nur noch gute Bilder in den Ordner
schieben, wenn du eh gerade welche gemacht hast.

## Alternative: Fotos ins Repo

Bilder unter `assets/fotos/` ins Repo laden. Funktioniert ohne Drive, ist aber
manueller und für große Mengen unpraktisch.

## Was ich in deinem Drive vorgefunden habe

Viele Bilder, aber verstreut und unsortiert: Kamera-Dumps von 2020–2022
(`P10xxxxx.JPG`), geteilte Urlaubsordner, HEIC-Dateien von anderen Accounts.
Nichts, was als Content-Galerie taugt. Deshalb der eigene Ordner — ohne ihn
rät die Automatik, und das Ergebnis wäre zufällig statt passend.

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
