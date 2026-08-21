#!/usr/bin/env python3
"""Lädt die Fotos aus dem Drive-Ordner nach assets/fotos/.

Warum dieses Skript existiert: Die Bilder über den Drive-Connector zu holen
schickt sie als Base64 durch den Modell-Kontext — ein einziges 25-KB-Bild
kostet dabei rund 9.000 Tokens, ein 800-KB-Original ein Vielfaches davon.
Für 17 Slides pro Woche ist das nicht tragbar. Über die Drive-API landen die
Dateien dagegen direkt auf der Platte.

Voraussetzungen:
  1. Der Ordner ist für "Jeder mit dem Link" freigegeben (Leserechte genügen).
  2. Ein Google-API-Key mit aktivierter Drive API liegt in DRIVE_API_KEY.

Aufruf:
    DRIVE_API_KEY=... python3 scripts/fetch_drive_photos.py
    DRIVE_API_KEY=... python3 scripts/fetch_drive_photos.py --limit 20
"""
import argparse, json, os, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "fotos")
FOLDER_ID = "1tjgIb9c8dXdXgBLqYhBcS53jTsK_YSLh"   # Claude Carousel Pool Blanko Fotos
API = "https://www.googleapis.com/drive/v3/files"


def call(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")[:300]
        if "API key" in detail or "API_KEY" in detail:
            sys.exit("Kein gültiger API-Key. DRIVE_API_KEY setzen und "
                     "sicherstellen, dass die Drive API dafür aktiviert ist — "
                     "siehe config/photo-sources.md.")
        if err.code == 404:
            sys.exit("Datei oder Ordner nicht erreichbar. Ist der Ordner für "
                     "'Jeder mit dem Link' freigegeben?")
        sys.exit(f"Drive-API antwortete {err.code}: {detail}")


def list_images(key):
    """Alle Bilder im Ordner, über alle Seiten hinweg."""
    files, page_token = [], None
    while True:
        params = {
            "q": f"'{FOLDER_ID}' in parents and mimeType contains 'image/' "
                 f"and trashed = false",
            "fields": "nextPageToken,files(id,name,size,imageMediaMetadata(width,height))",
            "pageSize": "1000",
            "key": key,
        }
        if page_token:
            params["pageToken"] = page_token
        payload = json.loads(call(f"{API}?{urllib.parse.urlencode(params)}"))
        files.extend(payload.get("files", []))
        page_token = payload.get("nextPageToken")
        if not page_token:
            return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, help="nur die ersten N Bilder laden")
    args = parser.parse_args()

    key = os.environ.get("DRIVE_API_KEY")
    if not key:
        sys.exit("DRIVE_API_KEY ist nicht gesetzt — siehe config/photo-sources.md.")

    os.makedirs(OUT_DIR, exist_ok=True)
    images = list_images(key)
    if args.limit:
        images = images[:args.limit]
    print(f"{len(images)} Bilder im Ordner.")

    index, loaded, skipped = [], 0, 0
    for image in images:
        target = os.path.join(OUT_DIR, image["name"])
        meta = image.get("imageMediaMetadata") or {}
        entry = {"datei": image["name"], "id": image["id"],
                 "breite": meta.get("width"), "hoehe": meta.get("height")}
        index.append(entry)

        if os.path.exists(target) and os.path.getsize(target) == int(image.get("size", 0)):
            skipped += 1
            continue
        url = f"{API}/{image['id']}?alt=media&key={urllib.parse.quote(key)}"
        with open(target, "wb") as fh:
            fh.write(call(url))
        loaded += 1
        size = f"  {meta['width']}x{meta['height']}" if meta.get("width") else ""
        print(f"  geladen: {image['name']}{size}")

    with open(os.path.join(OUT_DIR, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)

    print(f"\n{loaded} neu geladen, {skipped} schon vorhanden.")
    print(f"Ablage: {os.path.relpath(OUT_DIR, ROOT)}/")


if __name__ == "__main__":
    main()
