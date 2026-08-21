#!/usr/bin/env python3
"""Rendert Carousel-Slides als PNG (1080x1350) im Format aus config/carousel-format.md.

Eingabe: eine JSON-Datei, siehe scripts/beispiel-slides.json.
Aufruf:  python3 scripts/render_slides.py posts/2026-W35/post-1.slides.json

Erzeugt neben der JSON-Datei einen Ordner <name>-slides/ mit slide-01.png ...
Braucht nur Chromium (headless), keine Zusatzpakete.
"""
import base64, html, json, mimetypes, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import png_tools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "templates", "slide.html.tpl")

WIDTH, HEIGHT = 1080, 1350  # Instagram 4:5

# Cover trägt eine größere Headline als die Inhaltsslides.
# Schriftgrößen in vh, bezogen auf das 1350px hohe Referenzlayout
# (1 px entspricht 0.0741vh). Das Cover trägt eine größere Headline.
STYLE = {
    "cover": {"CSIZE": "2.22vh", "CTRACK": "0",     "CCOLOR": "#ffffff",
              "HSIZE": "5.78vh", "BSIZE": "2.30vh", "BWIDTH": "72%"},
    "point": {"CSIZE": "2.00vh", "CTRACK": ".13em", "CCOLOR": "var(--accent)",
              "HSIZE": "4.89vh", "BSIZE": "2.22vh", "BWIDTH": "96%"},
}


def find_chromium():
    for cand in ("/opt/pw-browsers/chromium/chrome-linux/chrome",
                 "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                 shutil.which("chromium"), shutil.which("google-chrome")):
        if cand and os.path.exists(cand):
            return cand
    for base in ("/opt/pw-browsers",):
        for dirpath, _, files in os.walk(base):
            if "chrome" in files:
                return os.path.join(dirpath, "chrome")
    sys.exit("Kein Chromium gefunden — Slides können nicht gerendert werden.")


def shoot(chrome, page_html, out_png, window_height):
    subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--hide-scrollbars", "--force-device-scale-factor=1",
         f"--window-size={WIDTH},{window_height}", f"--screenshot={out_png}",
         "--virtual-time-budget=1500", f"file://{page_html}"],
        check=True, capture_output=True)


def viewport_offset(chrome):
    """Chromium schießt das Fenster, nicht den Viewport — der Viewport ist um
    einen festen Betrag kleiner. Der wird hier einmal gemessen, statt geraten,
    damit das Ergebnis auch in anderen Umgebungen exakt 1080x1350 bleibt."""
    probe = ('<style>html,body{margin:0;height:100%;background:#fff}'
             '.s{position:fixed;inset:0;background:#000}</style><div class="s"></div>')
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "probe.html")
        png = os.path.join(tmp, "probe.png")
        open(page, "w", encoding="utf-8").write(probe)
        shoot(chrome, page, png, HEIGHT)
        rows, width, height, channels = png_tools.decode(png)
        mid = (width // 2) * channels
        filled = max((y for y in range(height) if rows[y][mid] < 128), default=height - 1) + 1
    return HEIGHT - filled


def accent(text):
    """{Wort} wird zum hellblauen Kursivwort. Alles andere wird escaped."""
    out, pos = [], 0
    for m in re.finditer(r"\{([^}]*)\}", text):
        out.append(html.escape(text[pos:m.start()]))
        out.append("<em>" + html.escape(m.group(1)) + "</em>")
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out).replace("\n", "<br>")


def embed_photo(path, base_dir):
    """Foto als data:-URI einbetten, damit die HTML-Datei autark ist."""
    if not path:
        return ('<div class="photo" style="background:'
                'linear-gradient(160deg,#2b2f36,#14161a)"></div>')
    full = path if os.path.isabs(path) else os.path.join(base_dir, path)
    if not os.path.exists(full):
        sys.exit(f"Foto nicht gefunden: {full}")
    mime = mimetypes.guess_type(full)[0] or "image/jpeg"
    if mime == "image/heif" or full.lower().endswith((".heic", ".heif")):
        sys.exit(f"HEIC wird vom Browser nicht gerendert — bitte als JPG "
                 f"exportieren: {full}")
    data = base64.b64encode(open(full, "rb").read()).decode()
    return f'<img class="photo" src="data:{mime};base64,{data}">'


def build_html(slide, base_dir):
    kind = slide.get("type", "point")
    style = dict(STYLE.get(kind, STYLE["point"]))
    body = slide.get("body") or slide.get("subline") or ""
    tpl = open(TEMPLATE, encoding="utf-8").read()
    fields = {
        "PHOTO": embed_photo(slide.get("photo"), base_dir),
        "FOCUS": slide.get("focus", "center"),
        "COUNTER": html.escape(slide.get("counter", "")),
        "HEADLINE": accent(slide.get("headline", "")),
        "BODY": f"<p>{accent(body)}</p>" if body else "",
    }
    for key, val in {**style, **fields}.items():
        tpl = tpl.replace(f"__{key}__", val)
    return tpl


def main():
    if len(sys.argv) != 2:
        sys.exit("Aufruf: render_slides.py <slides.json>")
    spec_path = os.path.abspath(sys.argv[1])
    base_dir = os.path.dirname(spec_path)
    spec = json.load(open(spec_path, encoding="utf-8"))
    slides = spec["slides"]

    out_dir = os.path.join(base_dir, re.sub(r"\.slides\.json$|\.json$", "",
                                            os.path.basename(spec_path)) + "-slides")
    os.makedirs(out_dir, exist_ok=True)
    chrome = find_chromium()
    window_height = HEIGHT + viewport_offset(chrome)

    for i, slide in enumerate(slides, 1):
        png = os.path.join(out_dir, f"slide-{i:02d}.png")
        with tempfile.TemporaryDirectory() as tmp:
            page = os.path.join(tmp, "slide.html")
            open(page, "w", encoding="utf-8").write(build_html(slide, base_dir))
            shoot(chrome, page, png, window_height)
        png_tools.crop_height(png, HEIGHT)
        print(f"  {os.path.relpath(png, ROOT)}")

    print(f"{len(slides)} Slides gerendert nach {os.path.relpath(out_dir, ROOT)}/")


if __name__ == "__main__":
    main()
