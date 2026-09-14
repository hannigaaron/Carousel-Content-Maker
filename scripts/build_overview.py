#!/usr/bin/env python3
"""Baut die Uebersichtsseite fuer alle fertigen Carousel-Wochen.

Ergebnis liegt danach in  build/uebersicht/  :
    index.html          die Seite
    slides/*.jpg        alle Slides, auf 540 px verkleinert

Danach wird die Seite mit dem Artifact-Tool auf dieselbe URL
veroeffentlicht — die URL steht in prompts/weekly-run.md.

    python3 scripts/build_overview.py

Braucht nur Chromium (fuers Verkleinern), keine Zusatzpakete.
"""
import base64, datetime, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from render_slides import find_chromium

OUT   = os.path.join(ROOT, "build", "uebersicht")
THUMB = 540          # Breite der Vorschaubilder in der Uebersicht


# ---------------------------------------------------------------- Text

def quotes(s):
    """Gerade Anfuehrungszeichen typografisch setzen: "x" -> „x“."""
    out = []
    for ch in s:
        if ch == '"':
            prev = out[-1] if out else " "
            out.append("“" if (prev.isalnum() or prev in ".,!?)“’")
                       else "„")
        else:
            out.append(ch)
    return "".join(out)


def unwrap(caption):
    """Zeilenumbrueche der Markdown-Quelle entfernen.

    Instagram bricht selbst um; harte Umbrueche mitten im Satz sehen
    ausgefranst aus. Der letzte Absatz ist der CTA — dort sind die
    Umbrueche gewollt und bleiben stehen.
    """
    paras = caption.strip().split("\n\n")
    out = []
    for i, p in enumerate(paras):
        if i == len(paras) - 1:
            out.append(p.strip())
        else:
            out.append(" ".join(l.strip() for l in p.split("\n")))
    return "\n\n".join(out)


# ---------------------------------------------------------------- Lesen

def read_post(week, nr):
    path = os.path.join(ROOT, "posts", week, f"post-{nr}.md")
    t = open(path, encoding="utf-8").read()

    def field(name, default=""):
        m = re.search(r'^%s: "?(.+?)"?$' % name, t, re.M)
        return m.group(1).strip() if m else default

    def section(name):
        m = re.search(r"## %s\n(.*?)(?=\n## |\Z)" % name, t, re.S)
        return m.group(1).strip() if m else ""

    warum = " ".join(l.strip() for l in section("Warum dieses Thema").split("\n"))
    offen = [quotes(" ".join(x.split()).lstrip("- "))
             for x in section("Offene Punkte").split("\n\n") if x.strip()]

    slides = []
    for m in re.finditer(r"^\| (\d+) \| `([^`]+)` \| (.+?) \| (.+?) \|$", t, re.M):
        slides.append({"n": int(m.group(1)), "counter": m.group(2),
                       "headline": quotes(m.group(3).strip())})

    d = os.path.join(ROOT, "posts", week, f"post-{nr}-slides")
    pngs = sorted(f for f in os.listdir(d) if f.endswith(".png")) if os.path.isdir(d) else []
    images, sources = [], []
    for f in pngs:
        idx = f.split("-")[1].split(".")[0]
        name = f"{week[5:]}-p{nr}-{idx}.jpg"
        images.append("slides/" + name)
        sources.append([os.path.join(d, f), name])

    return {
        "nr": nr,
        "title": re.search(r"^# (.+)$", t, re.M).group(1).strip(),
        "kategorie": field("kategorie", "Post"),
        "schmerz": quotes(field("zielgruppen-schmerz")),
        "warnung": quotes(field("warnung")),      # rote Box: nicht hochladen
        "warum": quotes(warum),
        "caption": quotes(unwrap(section("Caption"))),
        "offen": offen,
        "slides": slides,
        "images": images,
    }, sources


def week_range(week):
    """'2026-W37' -> '8.–14. September 2026'"""
    MON = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
           "August", "September", "Oktober", "November", "Dezember"]
    y, w = int(week[:4]), int(week[6:])
    a = datetime.date.fromisocalendar(y, w, 1)
    b = datetime.date.fromisocalendar(y, w, 7)
    if a.month == b.month:
        return f"{a.day}.–{b.day}. {MON[b.month-1]} {y}"
    return f"{a.day}. {MON[a.month-1]} – {b.day}. {MON[b.month-1]} {y}"


def collect():
    weeks, sources = [], []
    base = os.path.join(ROOT, "posts")
    for week in sorted(os.listdir(base), reverse=True):      # neueste zuerst
        if not re.fullmatch(r"\d{4}-W\d{2}", week):
            continue
        nrs = sorted(int(m.group(1)) for m in
                     (re.fullmatch(r"post-(\d+)\.md", f)
                      for f in os.listdir(os.path.join(base, week))) if m)
        posts = []
        for nr in nrs:
            p, s = read_post(week, nr)
            if not p["images"]:
                print(f"  übersprungen: {week} Post {nr} — keine gerenderten Slides")
                continue
            posts.append(p)
            sources += s
        if posts:
            weeks.append({"week": week, "range": week_range(week), "posts": posts})
    return weeks, sources


# ---------------------------------------------------------------- Bilder

def shrink(sources, outdir):
    """Slides ueber Chromium auf THUMB px verkleinern und als JPEG sichern."""
    os.makedirs(outdir, exist_ok=True)
    page = """<body><pre id=o></pre><script>
var F=%s, out={}, i=0, W=%d;
function next(){
  if(i>=F.length){document.getElementById('o').textContent=JSON.stringify(out);return;}
  var j=F[i++], img=new Image();
  img.onerror=function(){out[j[1]]="ERR";next();};
  img.onload=function(){
    try{
      var c=document.createElement('canvas');
      c.width=W; c.height=Math.round(W*img.naturalHeight/img.naturalWidth);
      c.getContext('2d').drawImage(img,0,0,c.width,c.height);
      out[j[1]]=c.toDataURL('image/jpeg',0.82).split(',')[1];
    }catch(e){out[j[1]]="EXC";}
    next();
  };
  img.src="file://"+j[0];
}
next();
</script></body>""" % (json.dumps(sources), THUMB)

    tmp = os.path.join(outdir, "_shrink.html")
    open(tmp, "w").write(page)
    r = subprocess.run([find_chromium(), "--headless", "--disable-gpu", "--no-sandbox",
                        "--allow-file-access-from-files", "--virtual-time-budget=300000",
                        "--dump-dom", "file://" + tmp],
                       capture_output=True, text=True)
    os.remove(tmp)
    m = re.search(r'<pre id="o">(.*?)</pre>', r.stdout, re.S)
    if not m or not m.group(1).strip():
        sys.exit("Verkleinern fehlgeschlagen — Chromium hat nichts geliefert.\n"
                 + r.stderr[-600:])
    data = json.loads(m.group(1))
    bad = [n for n, b in data.items() if len(b) < 20]
    for name, b64 in data.items():
        if len(b64) >= 20:
            open(os.path.join(outdir, name), "wb").write(base64.b64decode(b64))
    if bad:
        print("  WARNUNG, nicht verkleinert:", ", ".join(sorted(bad)))
    return len(data) - len(bad)


# ---------------------------------------------------------------- Main

def refresh_captions(weeks):
    """caption.txt im Upload-Ordner auf den Stand der Post-Datei bringen."""
    n = 0
    for wk in weeks:
        base = os.path.join(ROOT, "FERTIG-ZUM-HOCHLADEN", wk["week"])
        if not os.path.isdir(base):
            continue
        for post in wk["posts"]:
            for folder in os.listdir(base):
                if folder.startswith(f"{post['nr']} \u2014 "):
                    open(os.path.join(base, folder, "caption.txt"), "w",
                         encoding="utf-8").write(post["caption"] + "\n")
                    n += 1
    return n


def main():
    os.makedirs(OUT, exist_ok=True)
    weeks, sources = collect()
    if not weeks:
        sys.exit("Keine Wochen mit gerenderten Slides gefunden.")

    n = shrink(sources, os.path.join(OUT, "slides"))
    refresh_captions(weeks)

    tpl = open(os.path.join(HERE, "overview", "template.html"), encoding="utf-8").read()
    data = json.dumps(weeks, ensure_ascii=False, indent=1).replace("</script>", "<\\/script>")
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        tpl.replace("__DATA__", data))

    posts = sum(len(w["posts"]) for w in weeks)
    print(f"Fertig: {len(weeks)} Wochen, {posts} Posts, {n} Slides -> {OUT}")
    for w in weeks:
        print(f"  {w['week']}  {len(w['posts'])} Posts  "
              + " | ".join(p["title"] for p in w["posts"]))


if __name__ == "__main__":
    main()
