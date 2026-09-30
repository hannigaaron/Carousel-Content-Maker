#!/usr/bin/env python3
"""Sucht und lädt lizenzfreie Fotos (CC0 / Public Domain) über Openverse.

Kein API-Key nötig. Gesucht wird nur in Wikimedia Commons: andere Openverse-Quellen
(StockSnap, Rawpixel, Flickr) liefern dort nur verkleinerte Vorschauen. Das Skript fragt nur die Lizenzen `cc0` und `pdm` ab: beide
erlauben kommerzielle Nutzung ohne Namensnennung.

Die Treffer landen in assets/fotos/stock/ zusammen mit einer .json-Datei pro
Bild (Quelle, Lizenz, Urheber), damit die Herkunft jederzeit belegbar ist.

    python3 scripts/fetch_free_photos.py "restaurant table dinner" --anzahl 6
    python3 scripts/fetch_free_photos.py "breakfast coffee kitchen" --anzahl 4 --prefix frei-fruehstueck

Die Bilder werden nur geladen. Ob sie zum Slide passen, entscheidet der
Wochenlauf nach dem Ansehen (siehe prompts/weekly-run.md, Fotos zuordnen).
"""
import argparse, json, os, re, struct, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "fotos", "stock")
API = "https://api.openverse.org/v1/images/"
# Wikimedia verlangt einen User-Agent mit Kontaktangabe, sonst 429/400.
UA = {"User-Agent": "CarouselContentMaker/1.0 (https://github.com/hannigaaron/carousel-content-maker)"}

# Nach dem Zuschnitt auf 4:5 soll das Bild noch rund 1080x1350 hergeben.
MIN_BREITE, MIN_HOEHE = 1000, 1250


def hole(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as antwort:
        return antwort.read()


def jpeg_groesse(daten):
    """Liest Breite und Höhe aus einem JPEG, ohne Zusatzpakete."""
    if daten[:2] != b"\xff\xd8":
        return None
    i = 2
    while i < len(daten) - 9:
        if daten[i] != 0xFF:
            i += 1
            continue
        marker = daten[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            hoehe, breite = struct.unpack(">HH", daten[i + 5:i + 9])
            return breite, hoehe
        laenge = struct.unpack(">H", daten[i + 2:i + 4])[0]
        i += 2 + laenge
    return None


def thumb_url(treffer):
    """Wikimedia gibt Originale gedrosselt aus, Standardgrößen aber zuverlässig.
    Hochformat: 1280 px breit. Querformat: 1920 px breit (wird auf 4:5 beschnitten)."""
    url, breite, hoehe = treffer["url"], treffer["width"], treffer["height"]
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w/\w\w)/([^/]+)$", url)
    if not m:
        return url
    ziel = 1280 if hoehe >= breite else 1920
    if breite <= ziel:
        return url
    return f"{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{ziel}px-{m.group(3)}"


def suche(begriff, seite):
    params = {
        "q": begriff,
        "license": "cc0,pdm",
        "mature": "false",
        "source": "wikimedia",
        "page_size": 20,
        "page": seite,
    }
    return json.loads(hole(f"{API}?{urllib.parse.urlencode(params)}"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("begriff")
    ap.add_argument("--anzahl", type=int, default=4)
    ap.add_argument("--prefix", default=None)
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    prefix = args.prefix or "frei-" + re.sub(r"[^a-z0-9]+", "-", args.begriff.lower()).strip("-")
    gespeichert = 0
    for seite in (1, 2, 3):
        for treffer in suche(args.begriff, seite).get("results", []):
            if gespeichert >= args.anzahl:
                break
            if (treffer.get("width") or 0) < MIN_BREITE or (treffer.get("height") or 0) < MIN_HOEHE:
                continue
            try:
                daten = hole(thumb_url(treffer))
            except Exception as fehler:
                print(f"  übersprungen ({fehler}): {treffer['url']}")
                continue
            groesse = jpeg_groesse(daten)
            if not groesse or groesse[0] < MIN_BREITE or groesse[1] < MIN_HOEHE:
                continue
            name = f"{prefix}-{gespeichert + 1:02d}"
            with open(os.path.join(OUT_DIR, name + ".jpeg"), "wb") as f:
                f.write(daten)
            meta = {k: treffer.get(k) for k in ("title", "creator", "license", "license_version",
                                                   "license_url", "foreign_landing_url", "source", "url")}
            meta["groesse"] = groesse
            with open(os.path.join(OUT_DIR, name + ".json"), "w") as f:
                json.dump(meta, f, ensure_ascii=False, indent=1)
            print(f"{name}.jpeg  {groesse[0]}x{groesse[1]}  {meta['license']}  {meta['foreign_landing_url']}")
            gespeichert += 1
        if gespeichert >= args.anzahl:
            break
    if not gespeichert:
        sys.exit("Keine passenden Treffer (Lizenz cc0/pdm, groß genug).")


if __name__ == "__main__":
    main()
