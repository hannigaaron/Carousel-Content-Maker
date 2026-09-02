"""Ein Carousel aus einer JSON-Beschreibung bauen."""

from __future__ import annotations

import json
from pathlib import Path

from . import images
from .render import render_slide
from .theme import SIZE_PORTRAIT, SIZE_SQUARE, get_theme

ROOT = Path(__file__).resolve().parent.parent
FORMATS = {"portrait": SIZE_PORTRAIT, "square": SIZE_SQUARE}


def load_content(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("slides"):
        raise SystemExit(f"{path}: kein 'slides'-Array gefunden")
    return data


def build(content_path: Path, out_dir: Path, *, quality: int = 92) -> list[Path]:
    data = load_content(content_path)
    slides = data["slides"]
    total = len(slides)

    width, height = FORMATS.get(data.get("format", "portrait"), SIZE_PORTRAIT)
    theme = get_theme(data.get("theme"), data.get("theme_overrides"))
    theme.width, theme.height = width, height
    handle = data.get("handle", "")

    out_dir.mkdir(parents=True, exist_ok=True)
    slug = data.get("slug") or content_path.stem
    written: list[Path] = []
    credits: list[images.Photo] = []
    # Damit dasselbe Stichwort auf zwei Slides nicht dasselbe Foto liefert.
    seen_queries: dict[str, int] = {}

    for i, slide in enumerate(slides, 1):
        spec = slide.get("image")
        photo = None
        if spec:
            offset = seen_queries.get(spec, 0)
            photo = images.resolve(spec, index=offset)
            seen_queries[spec] = offset + 1
        if photo and photo.license != "eigenes Material":
            credits.append(photo)

        canvas = render_slide(slide, theme, photo, number=i, total=total, handle=handle)
        target = out_dir / f"{slug}-{i:02d}.jpg"
        canvas.save(target, quality=quality, subsampling=0, optimize=True)
        written.append(target)
        print(f"  ✓ {target.name}  [{slide.get('type', 'text')}]"
              + (f"  ← {photo.title[:44]}" if photo else ""))

    _write_caption(data, out_dir / f"{slug}-caption.txt")
    if credits:
        _write_credits(credits, out_dir / f"{slug}-CREDITS.md", data.get("title", slug))
    return written


def _write_caption(data: dict, path: Path) -> None:
    parts = [data.get("caption", "").strip()]
    hashtags = data.get("hashtags") or []
    if hashtags:
        parts += ["", " ".join(h if h.startswith("#") else f"#{h}" for h in hashtags)]
    path.write_text("\n".join(p for p in parts if p is not None).strip() + "\n", encoding="utf-8")


def _write_credits(photos: list[images.Photo], path: Path, title: str) -> None:
    lines = [
        f"# Bildnachweise – {title}",
        "",
        "Alle Fotos stehen unter freien Lizenzen (Public Domain / CC0 / CC BY / CC BY-SA).",
        "CC-BY und CC-BY-SA verlangen die Namensnennung – diese Liste gehört in die",
        "Caption oder in den ersten Kommentar des Posts.",
        "",
    ]
    for photo in photos:
        lines.append(f"- **{photo.title}** – {photo.author or 'unbekannt'}, {photo.license}")
        if photo.source:
            lines.append(f"  {photo.source}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
