"""Bilder beschaffen: lokale Dateien oder frei lizenzierte Fotos aus dem Netz.

Zwei Quellen, in dieser Reihenfolge:
  1. Wikimedia Commons  – riesig, saubere Lizenz-Metadaten, aber gedrosselt
  2. Openverse          – aggregiert Flickr & Co., gute Treffer bei Alltagsmotiven

Beide liefern nur Bilder, die kommerziell nutzbar und bearbeitbar sind
(CC0 / Public Domain / CC-BY / CC-BY-SA). Namensnennung landet in CREDITS.md.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "images"
SEARCH_CACHE = ROOT / ".cache" / "searches"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
OPENVERSE_API = "https://api.openverse.engineering/v1/images/"
UA = "CarouselContentMaker/1.0 (hannigaaron@gmail.com)"

ALLOWED = ("cc0", "cc-zero", "public domain", "pdm", "pd-", "cc by", "cc-by", "by-sa")
BLOCKED = ("nc", "nd", "fair use", "non-free", "sampling+")


@dataclass
class Photo:
    path: Path
    title: str
    license: str
    author: str
    source: str
    query: str = ""

    def credit(self) -> str:
        who = self.author or "unbekannt"
        return f"{self.title} — {who} ({self.license}) {self.source}".strip()


def _strip(markup: str | None) -> str:
    if not markup:
        return ""
    text = re.sub(r"<[^>]+>", " ", str(markup))
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _license_ok(*parts: str) -> bool:
    blob = " ".join(p.lower() for p in parts if p)
    if any(bad in re.split(r"[\s\-_,/]+", blob) for bad in ("nc", "nd")):
        return False
    if any(bad in blob for bad in BLOCKED[2:]):
        return False
    return any(good in blob for good in ALLOWED)


def _get(url: str, params: dict, *, tries: int = 4) -> requests.Response | None:
    """GET mit Backoff – Commons drosselt geteilte IPs gern mit 429."""
    delay = 2.0
    for attempt in range(tries):
        try:
            resp = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=30)
            if resp.status_code == 200:
                return resp
            if resp.status_code not in (429, 500, 502, 503):
                return None
        except requests.RequestException:
            pass
        if attempt < tries - 1:
            time.sleep(delay)
            delay *= 2
    return None


def _download(url: str, *, tries: int = 5) -> bytes | None:
    delay = 2.0
    for attempt in range(tries):
        try:
            resp = requests.get(url, headers={"User-Agent": UA}, timeout=60)
            if resp.status_code == 200:
                return resp.content
            if resp.status_code not in (429, 500, 502, 503):
                return None
        except requests.RequestException:
            pass
        if attempt < tries - 1:
            time.sleep(delay)
            delay *= 2
    return None


def _search_commons(query: str, limit: int, width: int) -> list[dict]:
    resp = _get(
        COMMONS_API,
        {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {query}",
            "gsrnamespace": 6,
            "gsrlimit": limit,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|size",
            "iiurlwidth": width,
        },
    )
    if resp is None:
        return []
    pages = resp.json().get("query", {}).get("pages", {})

    hits = []
    for page in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        short = _strip(meta.get("LicenseShortName", {}).get("value")) or "?"
        terms = _strip(meta.get("UsageTerms", {}).get("value"))
        if not _license_ok(short, terms) or info.get("thumbwidth", 0) < 900:
            continue
        hits.append(
            {
                "title": page["title"].removeprefix("File:").rsplit(".", 1)[0],
                "url": info.get("thumburl") or info.get("url"),
                "license": short,
                "author": _strip(meta.get("Artist", {}).get("value")),
                "source": info.get("descriptionurl", ""),
            }
        )
    return hits


def _search_openverse(query: str, limit: int, width: int) -> list[dict]:
    resp = _get(
        OPENVERSE_API,
        {
            "q": query,
            "page_size": limit,
            "license_type": "commercial,modification",
            "size": "large",
            "mature": "false",
        },
    )
    if resp is None:
        return []

    hits = []
    for item in resp.json().get("results", []):
        lic = f"{item.get('license', '')} {item.get('license_version', '')}".strip().upper()
        if not _license_ok(item.get("license", "")):
            continue
        url = item.get("url")
        if not url:
            continue
        hits.append(
            {
                "title": _strip(item.get("title")) or query,
                "url": url,
                "license": lic,
                "author": _strip(item.get("creator")),
                "source": item.get("foreign_landing_url", ""),
            }
        )
    return hits


def search(query: str, *, limit: int = 8, width: int = 1600) -> list[dict]:
    """Treffer werden gecacht – Commons drosselt sonst beim zweiten Build."""
    SEARCH_CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"{query}|{limit}|{width}".encode()).hexdigest()[:16]
    cached = SEARCH_CACHE / f"{key}.json"
    if cached.exists():
        return json.loads(cached.read_text(encoding="utf-8"))

    hits = _search_commons(query, limit, width)
    if len(hits) < 2:
        hits += _search_openverse(query, limit, width)

    # Lange Stichwortketten treffen oft nichts – schrittweise entschärfen.
    words = query.split()
    while not hits and len(words) > 2:
        words = words[:-1]
        short = " ".join(words)
        hits = _search_commons(short, limit, width) or _search_openverse(short, limit, width)

    if hits:
        cached.write_text(json.dumps(hits, ensure_ascii=False), encoding="utf-8")
    return hits


def fetch(query: str, *, index: int = 0, width: int = 1600) -> Photo | None:
    hits = search(query, limit=max(8, index + 4), width=width)
    if index >= len(hits):
        print(f"  ! kein frei lizenziertes Bild für {query!r}")
        return None

    CACHE.mkdir(parents=True, exist_ok=True)
    # Einzelne Dateien liefern trotz Backoff dauerhaft 429 – dann lieber den
    # nächsten Treffer nehmen als den Slide ohne Foto zu lassen.
    for hit in hits[index:]:
        path = CACHE / f"{hashlib.sha1(hit['url'].encode()).hexdigest()[:16]}.img"
        if not path.exists():
            blob = _download(hit["url"])
            if blob is None:
                continue
            path.write_bytes(blob)
        return Photo(path=path, query=query,
                     **{k: hit[k] for k in ("title", "license", "author", "source")})

    print(f"  ! kein Foto ladbar für {query!r}")
    return None


def resolve(spec: str | None, *, index: int = 0) -> Photo | None:
    """'search:bergsee' sucht online, alles andere ist ein Pfad im Repo.

    'search:bergsee#2' nimmt gezielt den dritten Treffer – praktisch, wenn
    'carousel search' zeigt, dass das passende Foto nicht ganz oben steht.
    """
    if not spec:
        return None
    if spec.startswith("search:"):
        query = spec.removeprefix("search:").strip()
        if "#" in query:
            query, _, pick = query.rpartition("#")
            if pick.isdigit():
                return fetch(query.strip(), index=int(pick))
            query = f"{query}#{pick}"
        return fetch(query, index=index)
    path = Path(spec) if Path(spec).is_absolute() else ROOT / spec
    if not path.exists():
        print(f"  ! Bild nicht gefunden: {spec}")
        return None
    return Photo(path=path, title=path.name, license="eigenes Material", author="", source=spec)
