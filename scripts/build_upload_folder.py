#!/usr/bin/env python3
"""Baut aus einem Wochenordner eine Ablage, in der man nur noch nachsieht.

Aus posts/JJJJ-Wxx/ wird FERTIG-ZUM-HOCHLADEN/JJJJ-Wxx/ mit einem Unterordner
je Post, den Slides in Upload-Reihenfolge und der Caption als Textdatei
daneben. Gedacht zum Ablegen auf dem Schreibtisch.

    python3 scripts/build_upload_folder.py posts/2026-W35
"""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lies(pfad):
    return open(pfad, encoding="utf-8").read() if os.path.exists(pfad) else ""


def abschnitt(text, ueberschrift):
    """Holt einen ##-Abschnitt aus einer Markdown-Datei."""
    treffer = re.search(rf"^## {ueberschrift}\s*\n(.*?)(?=^## |\Z)",
                        text, re.M | re.S)
    return treffer.group(1).strip() if treffer else ""


def titel(text, fallback):
    treffer = re.search(r"^# (.+)$", text, re.M)
    return treffer.group(1).strip() if treffer else fallback


def sicher(name):
    """Dateisystemtauglicher Ordnername."""
    return re.sub(r'[<>:"/\\|?*]', "", name).strip().rstrip(".")


def main():
    if len(sys.argv) != 2:
        sys.exit("Aufruf: build_upload_folder.py posts/JJJJ-Wxx")
    quelle = os.path.abspath(sys.argv[1])
    woche = os.path.basename(quelle)
    ziel = os.path.join(ROOT, "FERTIG-ZUM-HOCHLADEN", woche)
    if os.path.exists(ziel):
        shutil.rmtree(ziel)
    os.makedirs(ziel)

    uebersicht = [f"# Woche {woche}\n",
                  "Drei Posts, fertig zum Hochladen. Je Post ein Ordner mit den",
                  "Slides in Reihenfolge und der Caption als Textdatei.\n"]

    for nummer in sorted(re.findall(r"post-(\d+)\.md", " ".join(os.listdir(quelle)))):
        md = lies(os.path.join(quelle, f"post-{nummer}.md"))
        name = titel(md, f"Post {nummer}")
        ordner = os.path.join(ziel, f"{nummer} — {sicher(name)}")
        os.makedirs(ordner)

        slides = os.path.join(quelle, f"post-{nummer}-slides")
        anzahl = 0
        if os.path.isdir(slides):
            for datei in sorted(os.listdir(slides)):
                if datei.endswith(".png"):
                    shutil.copy2(os.path.join(slides, datei),
                                 os.path.join(ordner, datei.replace("slide-", "")))
                    anzahl += 1

        caption = abschnitt(md, "Caption")
        if caption:
            with open(os.path.join(ordner, "caption.txt"), "w", encoding="utf-8") as fh:
                fh.write(caption + "\n")

        offen = abschnitt(md, "Offene Punkte")
        if offen:
            with open(os.path.join(ordner, "NOCH-ZU-PRUEFEN.txt"), "w",
                      encoding="utf-8") as fh:
                fh.write(offen + "\n")

        uebersicht.append(f"- **{nummer} — {name}** · {anzahl} Slides"
                          + ("  ⚠ siehe NOCH-ZU-PRUEFEN.txt" if offen else ""))

    review = lies(os.path.join(quelle, "_REVIEW.md"))
    if review:
        shutil.copy2(os.path.join(quelle, "_REVIEW.md"),
                     os.path.join(ziel, "REVIEW.md"))
        uebersicht.append("\nWas du prüfen musst, steht in REVIEW.md.")

    with open(os.path.join(ziel, "UEBERSICHT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(uebersicht) + "\n")

    print(f"Fertig: {os.path.relpath(ziel, ROOT)}/")
    for eintrag in sorted(os.listdir(ziel)):
        print(f"  {eintrag}")


if __name__ == "__main__":
    main()
