"""„Ich suche 2-3 Mamas" — reine Textslides in Aarons Farben.

Nachgebaut nach einem Referenz-Post (Screenshots von Aaron): dunkler
Verlauf, weisse Fettschrift, farbige Box um das Schluesselwort, Serifen-
Fliesstext, Kopfzeile, Profil-Fuss und SWIPE-Pfeil. Statt Rot gilt Aarons
Akzentblau #7CC7EC. Kein Foto im Hintergrund, nur das kleine Profilbild.

Aufruf aus dem Repo-Wurzelverzeichnis:
    python3 posts/spezial/mama-suche/bau.py
"""
import base64, io, os, sys, tempfile
from PIL import Image, ImageOps

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(HIER)))
sys.path.insert(0, os.path.join(WURZEL, "scripts"))
import png_tools
from render_slides import find_chromium, shoot, viewport_offset, WIDTH, HEIGHT

OUT = os.path.join(HIER, "slides")
FONT = os.path.join(WURZEL, "assets", "fonts", "Poppins-ExtraBold.ttf")
KOPF = "Fit &amp; stark als Mama &nbsp;|&nbsp; <span>@coach.aaron.hannig</span>"
HANDLE = "@coach.aaron.hannig"
SUB = "Fit &amp; stark als Mama"

# Jeder Slide: Liste von Zeilen (h = Headline, b = Box, t = Text, l = Liste)
SLIDES = [
    ("cover", [("h", "Ich suche"), ("h", "2–3 Mamas,"),
               ("t", "die 10+ kg loswerden wollen.<br>Und das nicht erst ab Januar,<br>"
                     "<mark class='t'>sondern ab sofort!</mark>")]),
    ("p", [("h", "Bis Silvester"), ("h", "sind es"), ("b", "6 Wochen…"),
           ("t", "Du kannst warten, oder bis dahin<br>das Fundament legen und bereits<br>"
                 "die ersten Kilos verlieren!")]),
    ("p", [("h", "Du hast"), ("b", "KEIN BOCK"), ("h", "mehr auf:"),
           ("l", ["Diäten, die nach 3 Wochen scheitern",
                  "Verzicht bei jedem Familienessen",
                  "Pläne, die nur mit viel Freizeit klappen"])]),
    ("p", [("h", "Du"), ("b", "WILLST:"),
           ("l", ["30-Min.-Training, für deinen Mama-Alltag",
                  "Essen, das die ganze Familie mitisst",
                  "Jemand, der sich meldet, wenn du abtauchst"])]),
    ("p", [("h", "Ich coache"), ("b", "jeden Tag."),
           ("t", "Hauptberuflich. Viele berufstätige Mütter<br>haben mit meiner Hilfe ihr Ziel erreicht,<br>"
                 "teils trotz 50 Stunden Arbeit,<br>Haushalt und Kinderbetreuung.")]),
    ("p", [("h", "Dein Kind"), ("h", "braucht ein"), ("b", "Vorbild:"),
           ("t", "Keins, das auf den richtigen Zeitpunkt wartet.<br>Sondern eins, das jetzt anfängt.")]),
    ("last", [("h", "Kommentiere"), ("b", "“MAMA”"),
              ("t", "und ich schicke dir alle Infos per DM!")]),
]

CSS = """
@font-face{font-family:P;src:url('file://%(font)s')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%%;height:100%%;overflow:hidden;background:#0b0c0e}
.s{position:fixed;inset:0;font-family:P,'Liberation Sans',sans-serif;
 background:linear-gradient(180deg,#0b0c0e 0%%,#12202c 55%%,#2a4b63 100%%);color:#fff}
.kopf{position:absolute;top:3.6vh;left:0;right:0;text-align:center;font-family:'Liberation Sans',sans-serif;
 font-weight:700;font-size:1.55vh;color:#fff}
.kopf span{font-weight:400;color:rgba(255,255,255,.7)}
.zaehler{position:absolute;top:3.2vh;right:5vw;background:rgba(255,255,255,.12);border-radius:3vh;
 padding:.9vh 2.2vw;font-family:'Liberation Sans',sans-serif;font-weight:700;font-size:2vh}
.mitte{position:absolute;left:4vw;right:4vw;top:0;bottom:0;display:flex;flex-direction:column;
 align-items:center;justify-content:center;text-align:center;padding-bottom:2vh}
.h{font-size:%(hs)s;line-height:1.28;letter-spacing:-.01em}
.c .h{font-size:7.2vh;line-height:1.2}
.b{display:inline-block;background:#7CC7EC;color:#0b0c0e;border-radius:1.5vh;padding:.2vh 2.4vw .6vh;
 font-size:%(hs)s;line-height:1.25;margin:.6vh 0}
.t{font-family:'Liberation Serif','Times New Roman',serif;font-weight:400;font-size:3.1vh;
 line-height:1.28;margin-top:2.2vh;color:rgba(255,255,255,.94)}
mark.t{background:#7CC7EC;color:#0b0c0e;padding:.2vh 1.2vw;border-radius:.8vh;margin:0}
ul{list-style:none;text-align:left;margin-top:3vh;font-family:'Liberation Serif','Times New Roman',serif;
 font-size:3.1vh;line-height:1.35}
li{margin:1.4vh 0;padding-left:2.4vw;position:relative}
li:before{content:'•';position:absolute;left:0;color:#7CC7EC}
.fuss{position:absolute;left:5vw;bottom:3.4vh;display:flex;align-items:center;gap:1.6vw;
 font-family:'Liberation Sans',sans-serif}
.fuss img{width:6.4vh;height:6.4vh;border-radius:50%%;object-fit:cover;border:.25vh solid #7CC7EC}
.fuss b{display:block;font-size:1.7vh}.fuss i{font-style:normal;font-size:1.5vh;color:rgba(255,255,255,.65)}
.swipe{position:absolute;right:5vw;bottom:4.2vh;display:flex;align-items:center;gap:1.2vw;
 font-family:'Liberation Sans',sans-serif;font-weight:700;font-size:2vh;letter-spacing:.08em;color:#fff}
.swipe svg{width:7vh;height:5vh}
"""


def avatar():
    im = ImageOps.exif_transpose(Image.open(os.path.join(WURZEL, "assets/fotos/IMG_0004.jpeg"))).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * .30), int(h * .30), int(w * .70), int(h * .30) + int(w * .40))).resize((240, 240))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def html(art, zeilen, nr, n, av):
    inner = ""
    for k, v in zeilen:
        if k == "h": inner += f"<div class='h'>{v}</div>"
        elif k == "b": inner += f"<div class='b'>{v}</div>"
        elif k == "t": inner += f"<div class='t'>{v}</div>"
        elif k == "l": inner += "<ul>" + "".join(f"<li>{x}</li>" for x in v) + "</ul>"
    hs = "7.2vh" if art == "cover" else "6.4vh"
    css = CSS % {"font": FONT, "hs": hs}
    z = "" if art == "cover" else f"<div class='zaehler'>{nr}/{n}</div>"
    sw = "" if art == "last" else ("<div class='swipe'>SWIPE <svg viewBox='0 0 70 50'><path d='M0 15h40V0l30 25-30 25V35H0z' "
                                    "fill='rgba(255,255,255,.75)'/></svg></div>")
    return (f"<!doctype html><meta charset='utf-8'><style>{css}</style><div class='s{' c' if art=='cover' else ''}'>"
            f"<div class='kopf'>{KOPF}</div>{z}<div class='mitte'>{inner}</div>"
            f"<div class='fuss'><img src='{av}'><div><b>{HANDLE}</b><i>{SUB}</i></div></div>{sw}</div>")


def main():
    os.makedirs(OUT, exist_ok=True)
    chrome = find_chromium()
    wh = HEIGHT + viewport_offset(chrome)
    av = avatar()
    for i, (art, zeilen) in enumerate(SLIDES, 1):
        png = os.path.join(OUT, f"{i:02d}.png")
        with tempfile.TemporaryDirectory() as tmp:
            page = os.path.join(tmp, "s.html")
            open(page, "w", encoding="utf-8").write(html("cover" if i == 1 else art, zeilen, i, len(SLIDES), av))
            shoot(chrome, page, png, wh)
        png_tools.crop_height(png, HEIGHT)
        print(" ", os.path.relpath(png, WURZEL))


if __name__ == "__main__":
    main()
