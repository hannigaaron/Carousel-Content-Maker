"""Aus Text + Foto wird ein Slide."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from .fonts import load
from .images import Photo
from .theme import Theme


# Slide-Typen, deren Text am oberen Rand beginnt.
TOP_ANCHORED = {"text", "list", "quote"}


# ---------------------------------------------------------------- Hilfsmittel

def _rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def cover(photo_path: Path, size: tuple[int, int], *, blur: float = 0.0) -> Image.Image:
    """Foto formatfüllend zuschneiden (wie CSS object-fit: cover)."""
    img = Image.open(photo_path)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = ImageOps.fit(img, size, method=Image.LANCZOS, centering=(0.5, 0.42))
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    return img


def scrim(
    img: Image.Image,
    theme: Theme,
    *,
    strength: float | None = None,
    top: float | None = None,
) -> Image.Image:
    """Verlauf von oben (hell) nach unten (dunkel), damit Text trägt."""
    strength = theme.scrim if strength is None else strength
    w, h = img.size
    top, bottom = (theme.scrim_top if top is None else top), 1.0
    mask = Image.linear_gradient("L").resize((1, h)).resize((w, h))
    lo, hi = int(255 * top * strength), int(255 * bottom * strength)
    mask = mask.point(lambda v: lo + (hi - lo) * v // 255)
    veil = Image.new("RGB", img.size, _rgb(theme.bg))
    return Image.composite(veil, img, mask)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        line = ""
        for word in paragraph.split():
            probe = f"{line} {word}".strip()
            if draw.textlength(probe, font=font) <= max_w or not line:
                line = probe
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def fit(
    draw: ImageDraw.ImageDraw,
    text: str,
    spec: str,
    max_w: int,
    max_h: int,
    *,
    start: int,
    minimum: int = 28,
    leading: float = 1.18,
) -> tuple[object, list[str], int]:
    """Größte Schriftgröße suchen, bei der der Text in die Box passt."""
    size = start
    while size > minimum:
        font = load(spec, size)
        lines = wrap(draw, text, font, max_w)
        line_h = int(size * leading)
        if len(lines) * line_h <= max_h:
            return font, lines, line_h
        size -= 2
    font = load(spec, minimum)
    return font, wrap(draw, text, font, max_w), int(minimum * leading)


def tracked_width(draw, text: str, font, tracking: int) -> float:
    """Breite inklusive Sperrung – Pillow kennt kein letter-spacing."""
    if not text:
        return 0.0
    return sum(draw.textlength(ch, font=font) for ch in text) + tracking * (len(text) - 1)


def draw_tracked(draw, xy, text: str, font, fill, tracking: int) -> None:
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def wrap_tracked(draw, text: str, font, max_w: int, tracking: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            probe = f"{line} {word}".strip()
            if tracked_width(draw, probe, font, tracking) <= max_w or not line:
                line = probe
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def ink_for(canvas: Image.Image, box: tuple[int, int, int, int], theme: Theme) -> tuple[str, tuple[int, int, int]]:
    """Schriftfarbe nach der Helligkeit hinter dem Text wählen.

    Weiße Schrift auf einem weißen Teller ist auch mit Schatten unlesbar –
    dort wird der Text dunkel und der Schein hell.
    """
    left, top, right, bottom = box
    left, top = max(0, left), max(0, top)
    right, bottom = min(canvas.width, right), min(canvas.height, bottom)
    if right <= left or bottom <= top:
        return theme.on_photo, (0, 0, 0)

    patch = canvas.crop((left, top, right, bottom)).convert("L")
    brightness = sum(patch.getdata()) / max(1, patch.width * patch.height)
    if brightness > 165:
        return theme.text, (255, 255, 255)
    return theme.on_photo, (0, 0, 0)


def soft_shadow(canvas: Image.Image, paint, *, blur: int, opacity: int,
                color: tuple[int, int, int] = (0, 0, 0)) -> Image.Image:
    """Weichen Schatten unter den Text legen, bevor er scharf gezeichnet wird.

    Ohne ihn verschwindet weiße Schrift in hellen Bildstellen wie Reis oder
    einem weißen Teller. Ein Verlauf über das ganze Foto würde das Essen
    dagegen stumpf machen, deshalb dunkelt nur die Schrift selbst ab.
    Zwei Durchgänge: ein breiter Hof und ein enger, harter Rand darunter.
    """
    stencil = Image.new("L", canvas.size, 0)
    paint(ImageDraw.Draw(stencil), 255)
    veil = Image.new("RGB", canvas.size, color)

    for radius, share in ((blur, 0.75), (max(2, blur // 5), 1.0)):
        layer = stencil.filter(ImageFilter.GaussianBlur(radius))
        alpha = int(opacity * share)
        canvas.paste(veil, (0, 0), layer.point(lambda v: v * alpha // 255))
    return canvas


def draw_lines(draw, lines, font, x, y, line_h, fill) -> int:
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return y


def pill(draw, xy, text, font, *, bg, fg, pad=(28, 14), radius=999) -> tuple[int, int]:
    x, y = xy
    tw = draw.textlength(text, font=font)
    th = font.size
    box = (x, y, x + tw + pad[0] * 2, y + th + pad[1] * 2)
    draw.rounded_rectangle(box, radius=radius, fill=bg)
    draw.text((x + pad[0], y + pad[1] - font.size * 0.08), text, font=font, fill=fg)
    return int(box[2] - box[0]), int(box[3] - box[1])


# ------------------------------------------------------------------- Slides

def render_slide(
    slide: dict,
    theme: Theme,
    photo: Photo | None,
    *,
    number: int,
    total: int,
    handle: str = "",
    footer: bool = True,
) -> Image.Image:
    W, H = theme.width, theme.height
    M = theme.scaled(theme.margin)
    kind = slide.get("type", "text")

    if photo is not None:
        canvas = cover(photo.path, (W, H), blur=slide.get("blur", 0))
        # Bei Layouts, deren Text oben sitzt, muss auch oben abgedunkelt werden.
        top = slide.get("scrim_top", 0.9 if kind in TOP_ANCHORED else theme.scrim_top)
        canvas = scrim(canvas, theme, strength=slide.get("scrim"), top=top)
    else:
        canvas = Image.new("RGB", (W, H), _rgb(theme.bg))

    draw = ImageDraw.Draw(canvas)
    text_c, muted_c, accent_c = _rgb(theme.text), _rgb(theme.muted), _rgb(theme.accent)
    inner = W - 2 * M

    if kind == "photo":
        _photo_slide(canvas, slide, theme, inner, M, W, H)
        if slide.get("footer", False):
            _footer(ImageDraw.Draw(canvas), theme, M, W, H, number, total, handle,
                    muted_c, accent_c, kind)
        return canvas

    if kind == "cover":
        _cover_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c)
    elif kind == "quote":
        _quote_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c)
    elif kind == "list":
        _list_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c)
    elif kind == "stat":
        _stat_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c)
    elif kind == "cta":
        _cta_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c)
    else:
        _text_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c)

    if slide.get("footer", footer):
        _footer(draw, theme, M, W, H, number, total, handle, muted_c, accent_c, kind)
    return canvas


def _photo_slide(canvas, slide, theme, inner, M, W, H) -> None:
    """Foto füllt den Slide, ein kurzer Satz in Versalien liegt mittig darauf."""
    text = (slide.get("title") or slide.get("body") or "").upper()
    if not text:
        return

    draw = ImageDraw.Draw(canvas)
    tracking = theme.scaled(slide.get("tracking", theme.tracking))
    box = inner - theme.scaled(40)

    size = theme.scaled(slide.get("size", 82))
    while size > theme.scaled(40):
        font = load(theme.font_display, size)
        lines = wrap_tracked(draw, text, font, box, tracking)
        if len(lines) <= slide.get("max_lines", 3):
            break
        size -= 3
    line_h = int(size * 1.24)

    # Standardmäßig knapp unter die Mitte – dort liegt bei Tellerfotos der Rand.
    anchor = slide.get("anchor", 0.5)
    y0 = H * anchor - len(lines) * line_h / 2

    def paint(target, fill):
        y = y0
        for line in lines:
            x = (W - tracked_width(draw, line, font, tracking)) / 2
            draw_tracked(target, (x, y), line, font, fill, tracking)
            y += line_h

    band = (int((W - box) / 2), int(y0), int((W + box) / 2), int(y0 + len(lines) * line_h))
    ink, glow = ink_for(canvas, band, theme)
    ink = slide.get("color", ink)

    soft_shadow(canvas, paint, blur=theme.scaled(slide.get("shadow_blur", 30)),
                opacity=slide.get("shadow", 205), color=glow)
    paint(ImageDraw.Draw(canvas), _rgb(ink))


def _kicker(draw, slide, theme, M, y, accent_c) -> int:
    text = slide.get("kicker")
    if not text:
        return y
    font = load(theme.font_meta, theme.scaled(30))
    draw.text((M, y), text.upper(), font=font, fill=accent_c)
    return y + theme.scaled(58)


def _cover_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c):
    bottom = H - theme.scaled(150)
    sub = slide.get("subline", "")

    sub_h = 0
    if sub:
        sub_font, sub_lines, sub_lh = fit(draw, sub, theme.font_body, inner,
                                          theme.scaled(220), start=theme.scaled(44), leading=1.35)
        sub_h = len(sub_lines) * sub_lh + theme.scaled(34)

    head_font, head_lines, head_lh = fit(
        draw, slide.get("title", ""), theme.font_head, inner,
        bottom - theme.scaled(300) - sub_h, start=theme.scaled(112), leading=1.08,
    )
    head_h = len(head_lines) * head_lh
    y = bottom - sub_h - head_h

    if slide.get("kicker"):
        kf = load(theme.font_meta, theme.scaled(30))
        pill(draw, (M, y - theme.scaled(86)), slide["kicker"].upper(), kf,
             bg=accent_c, fg=_rgb(theme.on_accent), pad=(theme.scaled(26), theme.scaled(13)))

    y = draw_lines(draw, head_lines, head_font, M, y, head_lh, text_c)
    if sub:
        draw_lines(draw, sub_lines, sub_font, M, y + theme.scaled(34), sub_lh, muted_c)


def _text_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c):
    y = theme.scaled(180)
    y = _kicker(draw, slide, theme, M, y, accent_c)

    if slide.get("title"):
        font, lines, lh = fit(draw, slide["title"], theme.font_head, inner,
                              theme.scaled(360), start=theme.scaled(78), leading=1.12)
        y = draw_lines(draw, lines, font, M, y, lh, text_c) + theme.scaled(40)
        draw.rounded_rectangle((M, y, M + theme.scaled(96), y + theme.scaled(8)),
                               radius=999, fill=accent_c)
        y += theme.scaled(56)

    body = slide.get("body", "")
    if body:
        font, lines, lh = fit(draw, body, theme.font_body, inner,
                              H - y - theme.scaled(190), start=theme.scaled(48), leading=1.45)
        draw_lines(draw, lines, font, M, y, lh, text_c)


def _list_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c):
    y = theme.scaled(180)
    y = _kicker(draw, slide, theme, M, y, accent_c)

    if slide.get("title"):
        font, lines, lh = fit(draw, slide["title"], theme.font_head, inner,
                              theme.scaled(260), start=theme.scaled(72), leading=1.12)
        y = draw_lines(draw, lines, font, M, y, lh, text_c) + theme.scaled(56)

    items = slide.get("items", [])
    if not items:
        return
    room = H - y - theme.scaled(190)
    gap = theme.scaled(30)
    per_item = max(theme.scaled(60), (room - gap * (len(items) - 1)) // max(len(items), 1))
    bullet_font = load(theme.font_meta, theme.scaled(34))
    indent = theme.scaled(86)
    dot = theme.scaled(54)

    # Erst messen, dann mittig setzen – sonst klafft unten eine Lücke.
    measured = []
    for item in items:
        font, lines, lh = fit(draw, item, theme.font_body, inner - indent,
                              per_item, start=theme.scaled(44), leading=1.3)
        measured.append((font, lines, lh, max(len(lines) * lh, dot)))
    block = sum(m[3] for m in measured) + gap * (len(items) - 1)
    y += max(0, (room - block) // 2)

    for i, (item, (font, lines, lh, height)) in enumerate(zip(items, measured), 1):
        marker = str(i) if slide.get("numbered", True) else "•"
        draw.ellipse((M, y + theme.scaled(4), M + dot, y + dot + theme.scaled(4)), fill=accent_c)
        mw = draw.textlength(marker, font=bullet_font)
        draw.text((M + dot / 2 - mw / 2, y + theme.scaled(12)), marker,
                  font=bullet_font, fill=_rgb(theme.on_accent))
        draw_lines(draw, lines, font, M + indent, y, lh, text_c)
        y += height + gap


def _quote_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c):
    mark = load(theme.font_head, theme.scaled(180))
    draw.text((M - theme.scaled(8), theme.scaled(150)), "“", font=mark, fill=accent_c)

    y = theme.scaled(330)
    font, lines, lh = fit(draw, slide.get("quote", slide.get("body", "")), theme.font_head,
                          inner, H - y - theme.scaled(260), start=theme.scaled(76), leading=1.22)
    y = draw_lines(draw, lines, font, M, y, lh, text_c)

    who = slide.get("author") or slide.get("source")
    if who:
        f = load(theme.font_meta, theme.scaled(34))
        draw.text((M, y + theme.scaled(46)), f"— {who}", font=f, fill=muted_c)


def _stat_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c):
    value = str(slide.get("value", ""))
    font, lines, lh = fit(draw, value, theme.font_head, inner, theme.scaled(420),
                          start=theme.scaled(260), leading=1.0)
    y = theme.scaled(400)
    y = draw_lines(draw, lines, font, M, y, lh, accent_c) + theme.scaled(30)

    label = slide.get("label", slide.get("body", ""))
    if label:
        lf, llines, llh = fit(draw, label, theme.font_body, inner,
                              H - y - theme.scaled(200), start=theme.scaled(52), leading=1.35)
        draw_lines(draw, llines, lf, M, y, llh, text_c)


def _cta_slide(draw, slide, theme, inner, M, W, H, text_c, muted_c, accent_c):
    y = theme.scaled(260)
    y = _kicker(draw, slide, theme, M, y, accent_c)

    font, lines, lh = fit(draw, slide.get("title", ""), theme.font_head, inner,
                          theme.scaled(420), start=theme.scaled(88), leading=1.1)
    y = draw_lines(draw, lines, font, M, y, lh, text_c) + theme.scaled(40)

    body = slide.get("body", "")
    if body:
        bf, blines, blh = fit(draw, body, theme.font_body, inner, theme.scaled(300),
                              start=theme.scaled(46), leading=1.4)
        y = draw_lines(draw, blines, bf, M, y, blh, muted_c) + theme.scaled(60)

    if slide.get("button"):
        bf = load(theme.font_meta, theme.scaled(40))
        pill(draw, (M, y), slide["button"], bf, bg=accent_c, fg=_rgb(theme.on_accent),
             pad=(theme.scaled(44), theme.scaled(24)), radius=theme.scaled(theme.radius))


def _footer(draw, theme, M, W, H, number, total, handle, muted_c, accent_c, kind):
    f = load(theme.font_meta, theme.scaled(28))
    y = H - theme.scaled(84)
    if handle:
        draw.text((M, y), handle, font=f, fill=muted_c)

    counter = f"{number}/{total}"
    cw = draw.textlength(counter, font=f)
    draw.text((W - M - cw, y), counter, font=f, fill=muted_c)

    if number < total:
        hint = "weiterwischen  ›"
        hw = draw.textlength(hint, font=f)
        draw.text((W / 2 - hw / 2, y), hint, font=f, fill=accent_c)
