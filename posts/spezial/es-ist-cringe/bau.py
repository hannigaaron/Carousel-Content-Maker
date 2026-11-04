"""„Es ist cringe, bis…" — Storytelling-Format mit weisser Konturschrift.

Nachgebaut nach Aarons eigenen Slides (weisse Fettschrift mit schwarzer
Kontur, ein Textblock oben, optional ein zweiter unten rechts).
Aufruf aus dem Repo-Wurzelverzeichnis:
    python3 posts/spezial/es-ist-cringe/bau.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

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


def block(blatt, text, oben, groesse=62, breite=0.86, mitte_x=0.5, kontur=0):
    """Zentrierter Textblock, weiss ohne Rahmen.

    Statt einer Kontur liegt ein weicher, breit gestreuter Schatten unter der
    Schrift. Er ist als Rand nicht zu sehen, haelt den Text aber auch auf
    hellen Stellen lesbar.
    """
    d = ImageDraw.Draw(blatt)
    f = ImageFont.truetype(FONT, groesse)
    max_b = int(W * breite)
    zeilen = []
    for absatz in text.split("\n"):
        zeilen += umbrechen(d, absatz, f, max_b) if absatz.strip() else [""]
    zeilenhoehe = int(groesse * 1.22)

    maske = Image.new("L", blatt.size, 0)
    md = ImageDraw.Draw(maske)
    y = int(H * oben)
    for zeile in zeilen:
        if zeile:
            b = md.textlength(zeile, font=f)
            md.text((W * mitte_x - b / 2, y), zeile, font=f, fill=255)
        y += zeilenhoehe
    for radius, deckkraft in ((max(8, groesse // 3), 150), (max(3, groesse // 9), 120)):
        ebene = maske.filter(ImageFilter.GaussianBlur(radius))
        blatt.paste(Image.new("RGB", blatt.size, (0, 0, 0)), (0, 0),
                    ebene.point(lambda v: v * deckkraft // 255))

    y = int(H * oben)
    for zeile in zeilen:
        if zeile:
            b = d.textlength(zeile, font=f)
            d.text((W * mitte_x - b / 2, y), zeile, font=f, fill=WEISS)
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
        block(blatt, unten_text, start, gr_unten, breite_unten, unten_x)
    blatt.save(ziel, quality=95, subsampling=0)
    print("  ", os.path.basename(ziel))


# ---------------------------------------------------------------- Nachrichten

INTER = os.path.join(os.path.dirname(FONT), "Inter-Regular.ttf")
INTER_M = os.path.join(os.path.dirname(FONT), "Inter-Medium.ttf")
BLASE = (255, 255, 255)
BLASE_TEXT = (17, 27, 33)
BLASE_ZEIT = (134, 150, 160)


EMOJI = {
    "\U0001F64F\U0001F3FD": "1f64f-1f3fd",
    "\u2764\uFE0F": "2764",
    "\u2764": "2764",
    "\U0001F60C": "1f60c",
}
EMOJI_DIR = os.path.join(os.path.dirname(FONT), "..", "emoji")


def zerlegen(text):
    """Zerlegt einen String in ('t', Text) und ('e', Emoji-Datei)."""
    teile, puffer, i = [], "", 0
    while i < len(text):
        for zeichen in sorted(EMOJI, key=len, reverse=True):
            if text.startswith(zeichen, i):
                if puffer:
                    teile.append(("t", puffer))
                    puffer = ""
                teile.append(("e", EMOJI[zeichen]))
                i += len(zeichen)
                break
        else:
            puffer += text[i]
            i += 1
    if puffer:
        teile.append(("t", puffer))
    return teile


def _breite(d, text, f, groesse):
    b = 0
    for art, wert in zerlegen(text):
        b += d.textlength(wert, font=f) if art == "t" else groesse * 1.18
    return b


def _zeichne(blatt, d, x, y, text, f, groesse, farbe):
    for art, wert in zerlegen(text):
        if art == "t":
            d.text((x, y), wert, font=f, fill=farbe)
            x += d.textlength(wert, font=f)
        else:
            kante = int(groesse * 1.05)
            bild = Image.open(os.path.join(EMOJI_DIR, wert + ".png")).convert("RGBA")
            bild = bild.resize((kante, kante), Image.LANCZOS)
            blatt.paste(bild, (int(x + groesse * 0.06), int(y + groesse * 0.08)), bild)
            x += groesse * 1.18
    return x


def umbrechen_emoji(d, text, f, max_breite, groesse):
    zeilen, zeile = [], ""
    for wort in text.split():
        probe = f"{zeile} {wort}".strip()
        if _breite(d, probe, f, groesse) <= max_breite or not zeile:
            zeile = probe
        else:
            zeilen.append(zeile)
            zeile = wort
    if zeile:
        zeilen.append(zeile)
    return zeilen


def blase(blatt, text, y, zeit="", x=58, groesse=34, max_breite=0.74, radius=30):
    """Zeichnet eine Chat-Blase wie in einem Messenger. Gibt die Unterkante zurueck."""
    d = ImageDraw.Draw(blatt)
    f = ImageFont.truetype(INTER, groesse)
    fz = ImageFont.truetype(INTER, 22)
    innen = 30
    zeilen = []
    for absatz in text.split("\n"):
        zeilen += umbrechen_emoji(d, absatz, f, int(W * max_breite) - 2 * innen, groesse) if absatz.strip() else [""]
    zh = int(groesse * 1.38)
    breite = max(_breite(d, z, f, groesse) for z in zeilen) + 2 * innen
    if zeit:
        breite = max(breite, d.textlength(zeit, font=fz) + 2 * innen + 40)
    breite = int(min(breite, W * max_breite))
    hoehe = len(zeilen) * zh + 2 * innen + (26 if zeit else 0)

    schatten = Image.new("L", blatt.size, 0)
    ImageDraw.Draw(schatten).rounded_rectangle([x, y, x + breite, y + hoehe], radius, fill=140)
    schatten = schatten.filter(ImageFilter.GaussianBlur(14))
    blatt.paste(Image.new("RGB", blatt.size, (0, 0, 0)), (0, 12), schatten)

    d = ImageDraw.Draw(blatt)
    d.rounded_rectangle([x, y, x + breite, y + hoehe], radius, fill=BLASE)
    d.polygon([(x + 6, y + radius - 4), (x - 16, y + 6), (x + 22, y + 8)], fill=BLASE)
    ty = y + innen
    for zeile in zeilen:
        _zeichne(blatt, d, x + innen, ty, zeile, f, groesse, BLASE_TEXT)
        ty += zh
    if zeit:
        zb = d.textlength(zeit, font=fz)
        d.text((x + breite - innen - zb, y + hoehe - innen - 14), zeit, font=fz, fill=BLASE_ZEIT)
    return y + hoehe


def nachrichten(foto, ziel, kopf_text, blasen, mitte=(0.5, 0.5), gr_oben=64,
                oben_y=0.055, start=0.30, abstand=26, abdunkeln=0.42):
    """Kopfzeile oben, darunter echte Nachrichten als Chat-Blasen."""
    blatt = fuellen(os.path.join(POOL, foto), mitte)
    if abdunkeln:
        dunkel = Image.new("RGB", blatt.size, (0, 0, 0))
        blatt = Image.blend(blatt, dunkel, abdunkeln)
    block(blatt, kopf_text, oben_y, gr_oben, 0.86)
    y = int(H * start)
    for text, zeit, gr in blasen:
        y = blase(blatt, text, y, zeit, groesse=gr) + abstand
    blatt.save(ziel, quality=95, subsampling=0)
    print("  ", os.path.basename(ziel))


slide("DSC06534.jpeg", os.path.join(OUT, "01.jpg"),
      "Ja, auf Instagram zu\nposten, als wäre man\nInfluencer, ist cringe…",
      "Aber nur solange, bis…", mitte=(0.5, 0.45), gr_oben=60, gr_unten=52,
      oben_y=0.055, unten_y=0.80, unten_x=0.5)

nachrichten("DSC06671.jpeg", os.path.join(OUT, "02.jpg"),
            "…dir Kunden täglich\nsolche Nachrichten\nschicken.",
            [("Ich hab grad endlich mal wieder richtig gute Laune – danke dafür!", "10:41", 33),
             ("Ich habe die 67 auf der Waage \U0001F60C, was ich schon lange nicht mehr hatte.", "15:15", 33),
             ("War irgendwie cool heute – hatte nach dem Training die ganze Zeit gute Laune!", "20:08", 33),
             ("Danke dir, dass du es tatsächlich schaffst, mich seit 2 Jahren bei der Stange zu halten!", "14:42", 33)],
            mitte=(0.5, 0.45), gr_oben=64, start=0.275, abstand=22)

nachrichten("laptop-handy-sprechen.jpeg", os.path.join(OUT, "03.jpg"),
            "…du immer wieder\nhörst: „Du hast mein\nLeben verändert.“",
            [("Du hast es wirklich geschafft, mein Leben zu verändern! DANKE!\U0001F64F\U0001F3FD\u2764\uFE0F", "09:12", 33),
             ("Ich habe mit dir so viele kg abgenommen, aber viel viel mehr gewonnen. "
              "Ich fühle mich besser, habe mehr Energie, bin nicht müde. Du hast es zu "
              "meinem Lebensstil gemacht.", "20:08", 33),
             ("Dank dir habe ich meinen neuen Weg gefunden.", "15:15", 33)],
            mitte=(0.5, 0.30), gr_oben=64, start=0.285, abstand=22)

slide("DSC06621.jpeg", os.path.join(OUT, "04.jpg"),
      "…die Leute, die dich\nanfangs ausgelacht\nhaben, dich nach\ndeinem Rat fragen.",
      mitte=(0.5, 0.42), gr_oben=62, oben_y=0.055)

slide("laptop-stativ-lachen.jpeg", os.path.join(OUT, "05.jpg"),
      "…die Leute sehen,\nwie glücklich dich\ndas Ganze macht.",
      mitte=(0.5, 0.12), gr_oben=66, oben_y=0.06)

slide("DSC06785.jpeg", os.path.join(OUT, "06.jpg"),
      "Den ersten Schritt zu\nmachen wird immer\nunangenehm sein.",
      "Aber wenn aus Anfangen lang genug\nDranbleiben wird, ist der Erfolg so\ngut wie sicher.\n\nAlso: Fang an. Und stick to the plan.",
      mitte=(0.5, 0.42), gr_oben=62, gr_unten=48, oben_y=0.055,
      breite_unten=0.88, unten_y=0.66)
