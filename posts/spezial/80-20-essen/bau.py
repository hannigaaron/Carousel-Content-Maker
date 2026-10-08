"""80/20 Essen — Cover, drei Split-Slides, Abschluss.

Aufruf aus dem Repo-Wurzelverzeichnis:  python3 posts/spezial/80-20-essen/bau.py
Alle Fotos kommen unveraendert aus assets/fotos.
"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, "..", "..", "..", "scripts"))
from split8020 import foto, split, textslide, ROT, WEISS  # noqa: E402

OUT = os.path.join(HIER, "slides")

textslide(foto("DSC06680.jpeg"), os.path.join(OUT, "01.jpg"),
          [("Iss zu 80 % gut.", WEISS), ("Genieß die 20 %.", ROT)],
          mitte=(0.42, 0.58), kopf_gr=74, staerke=215)

# gleicher Einkaufswagen zweimal — der staerkste Vergleich des Posts
split(foto("CE727A64-EA84-460C-BB9C-76DE37F5F4A3_1_105_c.jpeg"),
      foto("38AAFEDB-A2C2-4D16-B56F-82B62D81DB8F_1_105_c.jpeg"),
      os.path.join(OUT, "02.jpg"), (0.5, 0.68), (0.5, 0.17))
split(foto("IMG_8344.jpeg"), foto("stock/frei-kuchen-01.jpeg"),
      os.path.join(OUT, "03.jpg"), (0.5, 0.62), (0.55, 0.55))
split(foto("protein-overnight-oats.png"), foto("IMG_0014.JPG"),
      os.path.join(OUT, "04.jpg"), (0.45, 0.50), (0.32, 0.55))

textslide(foto("IMG_7773.jpeg"), os.path.join(OUT, "05.jpg"),
          [("Perfekt essen", WEISS), ("musst du nicht.", ROT)],
          "Wenn 80 % deiner Mahlzeiten sättigend und nährstoffreich sind, "
          "zerstören die anderen 20 % gar nichts. Genau deshalb hältst du es "
          "durch – und genau deshalb funktioniert es langfristig.",
          mitte=(0.5, 0.45), kopf_gr=70, staerke=250)
