#!/usr/bin/env python3
"""Sucht und lädt Stock-Fotos von Pixabay nach assets/fotos/stock/.

Gedacht für die Slides, auf denen keine Person zu sehen sein muss — Essen,
Küche, Schreibtisch, Details. Die Grenzen dafür stehen in
`config/photo-sources.md`; dieses Skript setzt sie technisch nicht durch.

Voraussetzung: ein kostenloser API-Key in PIXABAY_API_KEY.
Anlegen unter https://pixabay.com/accounts/register/ , der Key steht danach
auf https://pixabay.com/api/docs/ .

    PIXABAY_API_KEY=... python3 scripts/fetch_stock_photos.py "meal prep"
    PIXABAY_API_KEY=... python3 scripts/fetch_stock_photos.py "kitchen evening" --anzahl 5
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "fotos", "stock")
API = "https://pixabay.com/api/"

# Hochformat und gross genug fuer 1080x1350, sonst taugt es fuer die Slides nicht.
MIN_BREITE, MIN_HOEHE = 1080, 1350


def hole(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as antwort:
            return antwort.read()
    except urllib.error.HTTPError as fehler:
        text = fehler.read().decode("utf-8", "replace")[:200]
        if "API key" in text:
            sys.exit("Kein gültiger API-Key. PIXABAY_API_KEY setzen — kostenlos "
                     "unter https://pixabay.com/api/docs/")
        sys.exit(f"Pixabay antwortete {fehler.code}: {text}")


def suche(key, begriff, anzahl):
    params = {
        "key": key,
        "q": begriff,
        "image_type": "photo",
        "orientation": "vertical",
        "min_width": MIN_BREITE,
        "min_height": MIN_HOEHE,
        "safesearch": "true",
        "per_page": max(anzahl * 3, 20),   # Reserve, weil wir noch filtern
    }
    daten = json.loads(hole(f"{API}?{urllib.parse.urlencode(params)}"))
    return daten.get("hits", [])


def dateiname(begriff, treffer):
    stamm = re.sub(r"[^a-z0-9]+", "-", begriff.lower()).strip("-")
    return f"{stamm}-{treffer['id']}.jpg"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("begriff", help="Suchbegriff, z. B. 'meal prep'")
    parser.add_argument("--anzahl", type=int, default=3, help="wie viele laden (Standard 3)")
    args = parser.parse_args()

    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        sys.exit("PIXABAY_API_KEY ist nicht gesetzt — siehe config/photo-sources.md.")

    treffer = suche(key, args.begriff, args.anzahl)
    if not treffer:
        sys.exit(f"Keine Treffer für '{args.begriff}' im Hochformat ab "
                 f"{MIN_BREITE}x{MIN_HOEHE}. Anderen Begriff versuchen.")

    os.makedirs(OUT_DIR, exist_ok=True)
    geladen = 0
    for eintrag in treffer:
        if geladen >= args.anzahl:
            break
        url = eintrag.get("largeImageURL")
        if not url:
            continue
        ziel = os.path.join(OUT_DIR, dateiname(args.begriff, eintrag))
        if not os.path.exists(ziel):
            with open(ziel, "wb") as datei:
                datei.write(hole(url))
        geladen += 1
        print(f"  {os.path.basename(ziel)}  "
              f"{eintrag.get('imageWidth')}x{eintrag.get('imageHeight')}  "
              f"({eintrag.get('pageURL')})")

    print(f"\n{geladen} Bilder in {os.path.relpath(OUT_DIR, ROOT)}/")
    print("Vor dem Einsetzen prüfen: unteres Drittel ruhig genug für den Text? "
          "Keine fremden Gesichter? Höchstens eines pro Post.")


if __name__ == "__main__":
    main()
