"""Render-Bausteine fuer die 80/20-Split-Carousels (Spezialformat).

Kein Wochen-Standardformat: hier wird direkt mit Pillow gebaut, nicht ueber
scripts/render_slides.py. Ein Post-Ordner unter posts/spezial/ liefert nur
noch die Foto-Auswahl und die Texte (siehe dortige bau.py).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POOL = os.path.join(WURZEL, "assets", "fotos")
F8 = os.path.join(WURZEL, "assets", "fonts", "PlusJakartaSans-ExtraBold.ttf")
F5 = os.path.join(WURZEL, "assets", "fonts", "PlusJakartaSans-Medium.ttf")
W, H = 1080, 1350
HALB = H // 2
ROT = (242, 42, 22)
WEISS = (255, 255, 255)


def fuellen(pfad, groesse, mitte=(0.5, 0.5)):
    im = ImageOps.exif_transpose(Image.open(pfad)).convert("RGB")
    return ImageOps.fit(im, groesse, method=Image.LANCZOS, centering=mitte)


def schatten(blatt, malen, radius=26, deckkraft=155):
    maske = Image.new("L", blatt.size, 0)
    malen(ImageDraw.Draw(maske), 255)
    for r, anteil in ((radius, .8), (max(2, radius // 5), 1.0)):
        ebene = maske.filter(ImageFilter.GaussianBlur(r))
        a = int(deckkraft * anteil)
        blatt.paste(Image.new("RGB", blatt.size, (0, 0, 0)), (0, 0),
                    ebene.point(lambda v: v * a // 255))


def verlauf_unten(blatt, staerke=235, kurve=1.7):
    maske = Image.linear_gradient("L").resize((1, blatt.height)).resize(blatt.size)
    maske = maske.point(lambda v: min(255, int((v / 255) ** kurve * staerke)))
    return Image.composite(Image.new("RGB", blatt.size, (10, 10, 12)), blatt, maske)


def prozent(blatt, text, farbe, y_mitte, groesse=172):
    f = ImageFont.truetype(F8, groesse)
    d = ImageDraw.Draw(blatt)
    k = d.textbbox((0, 0), text, font=f)
    x = (W - (k[2] - k[0])) / 2 - k[0]
    y = y_mitte - (k[3] + k[1]) / 2
    schatten(blatt, lambda t, fill: t.text((x, y), text, font=f, fill=fill))
    ImageDraw.Draw(blatt).text((x, y), text, font=f, fill=farbe)


def split(oben, unten, ziel, mitte_oben=(0.5, 0.5), mitte_unten=(0.5, 0.5)):
    blatt = Image.new("RGB", (W, H))
    blatt.paste(fuellen(oben, (W, HALB), mitte_oben), (0, 0))
    blatt.paste(fuellen(unten, (W, H - HALB), mitte_unten), (0, HALB))
    prozent(blatt, "80%", ROT, HALB * 0.62)
    prozent(blatt, "20%", WEISS, HALB + (H - HALB) * 0.46)
    blatt.save(ziel, quality=94, subsampling=0)
    print("  ", os.path.basename(ziel))


def umbrechen(d, text, font, max_breite):
    zeilen, zeile = [], ""
    for wort in text.split():
        probe = f"{zeile} {wort}".strip()
        if d.textlength(probe, font=font) <= max_breite or not zeile:
            zeile = probe
        else:
            zeilen.append(zeile)
            zeile = wort
    zeilen.append(zeile)
    return zeilen


def textslide(foto, ziel, kopf, koerper="", mitte=(0.5, 0.5), kopf_gr=82, staerke=240):
    blatt = verlauf_unten(fuellen(foto, (W, H), mitte), staerke=staerke)
    fk = ImageFont.truetype(F8, kopf_gr)
    fb = ImageFont.truetype(F5, 39)
    rand = 84
    koerper = umbrechen(ImageDraw.Draw(blatt), koerper, fb, W - 2 * rand) if koerper else []
    hoehe = len(kopf) * int(kopf_gr * 1.17) + (34 + len(koerper) * 54 if koerper else 0)
    y = H - 150 - hoehe
    d = ImageDraw.Draw(blatt)
    for zeile, farbe in kopf:
        d.text((rand, y), zeile, font=fk, fill=farbe)
        y += int(kopf_gr * 1.17)
    y += 34
    for zeile in koerper:
        d.text((rand, y), zeile, font=fb, fill=(238, 238, 240))
        y += 54
    blatt.save(ziel, quality=94, subsampling=0)
    print("  ", os.path.basename(ziel))



def foto(name):
    """Foto aus dem gemeinsamen Pool assets/fotos."""
    return os.path.join(POOL, name)
