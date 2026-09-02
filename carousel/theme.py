"""Farben, Typo und Maße eines Carousel-Looks."""

from __future__ import annotations

from dataclasses import dataclass, replace

# Instagram-Portrait: bestes Verhältnis von Feed-Fläche zu Textplatz.
SIZE_PORTRAIT = (1080, 1350)
SIZE_SQUARE = (1080, 1080)


@dataclass
class Theme:
    name: str = "midnight"
    width: int = SIZE_PORTRAIT[0]
    height: int = SIZE_PORTRAIT[1]

    bg: str = "#12131a"
    surface: str = "#1c1e29"
    text: str = "#f5f5f7"
    muted: str = "#a3a6b4"
    accent: str = "#f2c14e"
    on_accent: str = "#12131a"

    # Wie stark ein Foto abgedunkelt wird, damit Text darauf lesbar bleibt.
    scrim: float = 0.62
    # Dunkelster Punkt des Verlaufs (unten), 0..1 relativ zu scrim.
    scrim_top: float = 0.15

    font_head: str = "Montserrat:700"
    font_body: str = "Inter:400"
    font_meta: str = "Inter:700"

    margin: int = 84
    radius: int = 36

    def scaled(self, value: int) -> int:
        """Maße sind für 1080px Breite gedacht; andere Formate skalieren mit."""
        return round(value * self.width / 1080)


THEMES: dict[str, Theme] = {
    "midnight": Theme(),
    "paper": Theme(
        name="paper",
        bg="#f4f1ea",
        surface="#ffffff",
        text="#1a1a18",
        muted="#6b6862",
        accent="#c2410c",
        on_accent="#ffffff",
        scrim=0.5,
    ),
    "forest": Theme(
        name="forest",
        bg="#0f1f18",
        surface="#163024",
        text="#f0f5f1",
        muted="#9db3a6",
        accent="#7dd3a0",
        on_accent="#0f1f18",
    ),
    "sunset": Theme(
        name="sunset",
        bg="#1d1120",
        surface="#2b1830",
        text="#fdf2f8",
        muted="#c9a8c4",
        accent="#fb7185",
        on_accent="#1d1120",
    ),
}


def get_theme(name: str | None, overrides: dict | None = None) -> Theme:
    base = THEMES.get(name or "midnight")
    if base is None:
        raise SystemExit(
            f"Unbekanntes Theme {name!r}. Verfügbar: {', '.join(sorted(THEMES))}"
        )
    if overrides:
        unknown = set(overrides) - {f.name for f in base.__dataclass_fields__.values()}
        if unknown:
            raise SystemExit(f"Unbekannte Theme-Felder: {', '.join(sorted(unknown))}")
        base = replace(base, **overrides)
    return base
