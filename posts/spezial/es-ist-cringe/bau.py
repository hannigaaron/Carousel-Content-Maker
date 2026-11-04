"""„Es ist cringe, bis…" — Storytelling-Format mit weisser Konturschrift.

Nachgebaut nach Aarons eigenen Slides (weisse Fettschrift mit schwarzer
Kontur, ein Textblock oben, optional ein zweiter unten rechts).
Aufruf aus dem Repo-Wurzelverzeichnis:
    python3 posts/spezial/es-ist-cringe/bau.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(HIER)))
POOL = os.path.join(WURZEL, "assets", "fotos")
OUT = os.path.join(HIER, "slides")
FONT = os.path.join(WURZEL, "assets", "fonts", "Poppins-ExtraBold.ttf")
W, H = 1080, 1350
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)


def fuellen(pfad, mitte=(0.5, 0.5)):
    im = ImageOps.exif_transpose(Image.open(pfad)).convert("RGB")
    return ImageOps.fit(im, (W, H), method=Image.LANCZOS, centering=mitte)


def umbrechen(d, text, font, max_breite):
    zeilen, zeile = [], ""
    for wort in text.split():
        probe = f"{zeile} {wort}".strip()
        if d.textlength(probe, font=font) <= max_breite or not zeile:
            zeile = probe
        else:
            zeilen.append(zeile)
            zeile = wort
    if zeile:
        zeilen.append(zeile)
    return zeilen


def block(blatt, text, oben, groesse=62, breite=0.86, mitte_x=0.5, kontur=7):
    """Zeichnet einen zentrierten Textblock. `oben` ist der y-Anteil der ersten Zeile."""
    d = ImageDraw.Draw(blatt)
    f = ImageFont.truetype(FONT, groesse)
    max_b = int(W * breite)
    zeilen = []
    for absatz in text.split("\n"):
        zeilen += umbrechen(d, absatz, f, max_b) if absatz.strip() else [""]
    zeilenhoehe = int(groesse * 1.22)
    y = int(H * oben)
    for zeile in zeilen:
        if zeile:
            b = d.textlength(zeile, font=f)
            d.text((W * mitte_x - b / 2, y), zeile, font=f, fill=WEISS,
                   stroke_width=kontur, stroke_fill=SCHWARZ)
        y += zeilenhoehe
    return y


def slide(foto, ziel, oben_text, unten_text="", mitte=(0.5, 0.5),
          gr_oben=62, gr_unten=52, oben_y=0.055, breite_oben=0.86,
          unten_x=0.5, breite_unten=0.70, unten_y=None):
    blatt = fuellen(os.path.join(POOL, foto), mitte)
    block(blatt, oben_text, oben_y, gr_oben, breite_oben)
    if unten_text:
        d = ImageDraw.Draw(blatt)
        f = ImageFont.truetype(FONT, gr_unten)
        zeilen = []
        for absatz in unten_text.split("\n"):
            zeilen += umbrechen(d, absatz, f, int(W * breite_unten)) if absatz.strip() else [""]
        hoehe = len(zeilen) * int(gr_unten * 1.22)
        start = unten_y if unten_y is not None else (H - 80 - hoehe) / H
        block(blatt, unten_text, start, gr_unten, breite_unten, unten_x, 6)
    blatt.save(ziel, quality=95, subsampling=0)
    print("  ", os.path.basename(ziel))


slide("DSC06534.jpeg", os.path.join(OUT, "01.jpg"),
      "Es ist cringe,\nSachen im Internet\nzu posten.",
      "Bis…", mitte=(0.5, 0.45), gr_oben=74, gr_unten=66, oben_y=0.06, unten_y=0.78, unten_x=0.5)

slide("DSC06671.jpeg", os.path.join(OUT, "02.jpg"),
      "…dir Kunden täglich\nsolche Nachrichten\nschicken.",
      mitte=(0.5, 0.45), gr_oben=66, oben_y=0.06)

slide("laptop-handy-sprechen.jpeg", os.path.join(OUT, "03.jpg"),
      "…du immer wieder\nhörst: „Du hast mein\nLeben verändert.“",
      mitte=(0.5, 0.30), gr_oben=64, oben_y=0.06)

slide("DSC06621.jpeg", os.path.join(OUT, "04.jpg"),
      "…die Leute, die dich\nanfangs ausgelacht\nhaben, dich nach\ndeinem Rat fragen.",
      mitte=(0.5, 0.42), gr_oben=62, oben_y=0.055)

slide("alltag-schloss-abendlicht.jpeg", os.path.join(OUT, "05.jpg"),
      "…die Leute sehen,\nwie glücklich dich\ndas Ganze macht.",
      mitte=(0.5, 0.45), gr_oben=66, oben_y=0.06)

slide("DSC06785.jpeg", os.path.join(OUT, "06.jpg"),
      "Den ersten Schritt zu\nmachen wird immer\nunangenehm sein.",
      "Aber wenn aus Anfangen lang genug\nDranbleiben wird, ist der Erfolg so\ngut wie sicher.\n\nAlso: Fang an. Und stick to the plan.",
      mitte=(0.5, 0.42), gr_oben=62, gr_unten=48, oben_y=0.055,
      breite_unten=0.88, unten_y=0.66)
