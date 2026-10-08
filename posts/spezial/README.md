# Spezial-Posts

Posts, die **nicht** dem Wochen-Standardformat folgen (kein `*.slides.json`, kein
`scripts/render_slides.py`). Sie werden direkt mit Pillow gebaut, ueber die
gemeinsamen Bausteine in `scripts/split8020.py`.

Format: 1080 × 1350, zwei Fotos uebereinander, rotes **80 %** oben, weisses
**20 %** unten; davor ein Cover und dahinter ein Abschluss-Slide mit Text ueber
einem abgedunkelten Foto. Vorbild war ein Referenz-Post, den Aaron geschickt hat.

| Ordner | Thema |
|---|---|
| `80-20-balance/` | 80 % unterwegs & arbeiten, 20 % chillen (Urlaub/Alltag) |
| `80-20-essen/` | 80 % gesund essen, 20 % Genuss |

Neu bauen (aus dem Repo-Wurzelverzeichnis):

```
python3 posts/spezial/80-20-essen/bau.py
```

Die fertigen Slides liegen in `slides/01.jpg` … `05.jpg`, die Caption in `post.md`.
