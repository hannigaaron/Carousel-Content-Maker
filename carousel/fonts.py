"""Schriften besorgen: Google Fonts wenn erreichbar, sonst Systemschrift."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import requests
from PIL import ImageFont

CACHE = Path(__file__).resolve().parent.parent / "fonts"
CSS_API = "https://fonts.googleapis.com/css2"
# Der CSS-Endpunkt liefert je nach User-Agent woff2 oder ttf. Pillow will ttf.
UA_TTF = "Mozilla/5.0 (Windows NT 6.1)"

FALLBACKS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def _fallback(weight: int) -> str:
    for path in FALLBACKS:
        if Path(path).exists() and (weight < 600 or "Bold" in path):
            return path
    for path in FALLBACKS:
        if Path(path).exists():
            return path
    raise RuntimeError("Keine nutzbare Systemschrift gefunden")


@lru_cache(maxsize=None)
def font_file(spec: str) -> str:
    """spec ist 'Familie:Gewicht', z.B. 'Inter:700'. Gibt einen Pfad zurück."""
    family, _, weight_raw = spec.partition(":")
    weight = int(weight_raw or 400)
    CACHE.mkdir(exist_ok=True)
    local = CACHE / f"{family.replace(' ', '')}-{weight}.ttf"
    if local.exists() and local.stat().st_size > 10_000:
        return str(local)

    try:
        css = requests.get(
            CSS_API,
            params={"family": f"{family}:wght@{weight}", "display": "swap"},
            headers={"User-Agent": UA_TTF},
            timeout=20,
        )
        css.raise_for_status()
        urls = re.findall(r"src: url\((https://[^)]+\.ttf)\)", css.text)
        if not urls:
            raise RuntimeError(f"keine TTF-Variante für {spec}")
        blob = requests.get(urls[-1], timeout=30)
        blob.raise_for_status()
        local.write_bytes(blob.content)
        return str(local)
    except Exception as exc:  # offline oder Familie unbekannt
        print(f"  ! Schrift {spec} nicht ladbar ({exc}) – nutze Systemschrift")
        return _fallback(weight)


@lru_cache(maxsize=None)
def load(spec: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(font_file(spec), size)
