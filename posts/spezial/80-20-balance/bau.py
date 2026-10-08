"""80/20 Balance (Urlaub & Arbeit) — Cover, drei Split-Slides, Abschluss.

Aufruf aus dem Repo-Wurzelverzeichnis:  python3 posts/spezial/80-20-balance/bau.py
Fotos, die nicht im Pool liegen, stehen daneben in quellen/.
Hinweis: das Gruppenbild bleibt bewusst unbearbeitet — Aaron macht die
Gesichter selbst unkenntlich, bevor der Post online geht.
"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, "..", "..", "..", "scripts"))
from split8020 import foto, split, textslide, ROT, WEISS  # noqa: E402

OUT = os.path.join(HIER, "slides")
Q = os.path.join(HIER, "quellen")
q = lambda name: os.path.join(Q, name)

textslide(foto("DSC06172.jpeg"), os.path.join(OUT, "01.jpg"),
          [("It's all about", WEISS), ("the balance.", ROT)],
          mitte=(0.55, 0.42), kopf_gr=86, staerke=215)

split(q("laptop-venedig.jpg"), q("eis-venedig.jpg"),
      os.path.join(OUT, "02.jpg"), (0.5, 0.55), (0.5, 0.74))
split(q("zu-fuss-nachts.jpg"), foto("38500999-71F0-408B-8E96-ED82F336B0A8.JPG"),
      os.path.join(OUT, "03.jpg"), (0.5, 0.55), (0.5, 0.72))
split(q("schreibtisch-nachts.jpg"), q("gruppe-strand.jpg"),
      os.path.join(OUT, "04.jpg"), (0.5, 0.78), (0.62, 0.42))

textslide(q("palmen-valencia.jpg"), os.path.join(OUT, "05.jpg"),
          [("Nicht das Extrem", WEISS), ("hält dich fit.", ROT)],
          "Abnehmen heißt nicht, nur noch in einem Extrem zu leben und dauerhaft "
          "einen strengen Lifestyle zu fahren. Die richtige Balance ist das, was "
          "dich langfristig fit hält.",
          mitte=(0.5, 0.42), kopf_gr=70, staerke=250)
