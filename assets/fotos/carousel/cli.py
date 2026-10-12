"""Kommandozeile: bauen, Bilder vorher ansehen, Themes auflisten."""

from __future__ import annotations

import argparse
from pathlib import Path

from . import images
from .build import ROOT, build
from .theme import THEMES


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="carousel", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="Slides aus einem Content-JSON rendern")
    p_build.add_argument("content", type=Path)
    p_build.add_argument("-o", "--out", type=Path, default=ROOT / "out")
    p_build.add_argument("-q", "--quality", type=int, default=92)

    p_search = sub.add_parser("search", help="frei lizenzierte Bilder zu einem Stichwort zeigen")
    p_search.add_argument("query")
    p_search.add_argument("-n", "--limit", type=int, default=6)

    sub.add_parser("themes", help="verfügbare Themes auflisten")

    args = parser.parse_args(argv)

    if args.cmd == "build":
        out = args.out / args.content.stem
        print(f"Baue {args.content} → {out}")
        files = build(args.content, out, quality=args.quality)
        print(f"\n{len(files)} Slides fertig in {out}")
        return 0

    if args.cmd == "search":
        hits = images.search(args.query, limit=args.limit)
        if not hits:
            print("Keine frei lizenzierten Treffer.")
            return 1
        for i, hit in enumerate(hits):
            print(f"[{i}] {hit['title'][:70]}\n    {hit['license']} · {hit['author'] or 'unbekannt'}\n    {hit['source']}")
        return 0

    for name, theme in THEMES.items():
        print(f"{name:10} bg {theme.bg}  text {theme.text}  accent {theme.accent}")
    return 0
