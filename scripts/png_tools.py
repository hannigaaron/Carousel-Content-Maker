"""Minimale PNG-Hilfen ohne Fremdpakete: dekodieren, zuschneiden, kodieren."""
import struct, zlib

_FILTER_NONE = 0


def decode(path):
    """Gibt (rows, width, height, channels) zurück; rows sind rohe Bytezeilen."""
    data = open(path, "rb").read()
    pos, idat = 8, b""
    width = height = channels = None
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk, payload = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + length]
        if chunk == b"IHDR":
            width, height, depth, color = struct.unpack(">IIBB", payload[:10])
            if depth != 8 or color not in (2, 6):
                raise ValueError(f"PNG-Variante nicht unterstützt: {path}")
            channels = 4 if color == 6 else 3
        elif chunk == b"IDAT":
            idat += payload
        pos += 12 + length

    raw = zlib.decompress(idat)
    stride = width * channels + 1
    prev, rows = bytearray(width * channels), []
    for y in range(height):
        ftype = raw[y * stride]
        line = bytearray(raw[y * stride + 1:(y + 1) * stride])
        if ftype:
            for i in range(len(line)):
                left = line[i - channels] if i >= channels else 0
                up = prev[i]
                upleft = prev[i - channels] if i >= channels else 0
                if ftype == 1:
                    line[i] = (line[i] + left) & 255
                elif ftype == 2:
                    line[i] = (line[i] + up) & 255
                elif ftype == 3:
                    line[i] = (line[i] + (left + up) // 2) & 255
                elif ftype == 4:
                    p = left + up - upleft
                    pa, pb, pc = abs(p - left), abs(p - up), abs(p - upleft)
                    pred = left if (pa <= pb and pa <= pc) else (up if pb <= pc else upleft)
                    line[i] = (line[i] + pred) & 255
                else:
                    raise ValueError(f"Unbekannter PNG-Filter {ftype}")
        rows.append(bytes(line))
        prev = line
    return rows, width, height, channels


def encode(path, rows, width, channels):
    raw = b"".join(bytes([_FILTER_NONE]) + row for row in rows)
    color = 6 if channels == 4 else 2

    def chunk(tag, payload):
        return (struct.pack(">I", len(payload)) + tag + payload
                + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n")
        fh.write(chunk(b"IHDR", struct.pack(">IIBBBBB", width, len(rows), 8, color, 0, 0, 0)))
        fh.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        fh.write(chunk(b"IEND", b""))


def crop_height(path, height):
    """Schneidet ein PNG auf die obersten `height` Zeilen zu (in place)."""
    rows, width, current, channels = decode(path)
    if current <= height:
        return
    encode(path, rows[:height], width, channels)


def mean_luminance(path, top_frac, bottom_frac, left_frac, right_frac):
    """Mittlere Helligkeit (0-255) eines rechteckigen Bildausschnitts.

    Wird benutzt, um zu prüfen, ob der Textbereich hell genug ist, dass weiße
    Schrift darauf untergehen würde.
    """
    rows, width, height, channels = decode(path)
    y0, y1 = int(height * top_frac), int(height * bottom_frac)
    x0, x1 = int(width * left_frac), int(width * right_frac)
    total = count = 0
    for y in range(y0, y1, 2):          # jede zweite Zeile/Spalte reicht
        row = rows[y]
        for x in range(x0, x1, 2):
            off = x * channels
            r, g, b = row[off], row[off + 1], row[off + 2]
            total += (299 * r + 587 * g + 114 * b) // 1000
            count += 1
    return total / count if count else 0.0
