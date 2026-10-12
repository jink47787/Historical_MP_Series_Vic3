"""Draw the flags for the 1836 Native North American tags.

Each flag is one full-size textured emblem (768x512, uncompressed A8R8G8B8 DDS, no mips, the same format as
gfx/coat_of_arms/textured_emblems/UFB_emblem.dds) laid over pattern_solid, so the game shows exactly what is drawn here.
None of these peoples flew a flag in 1836; each design is built from a symbol the people themselves used.

    python3 -I flags.py --out <mod_package dir> --preview <png>
"""
import argparse
import math
import os
import struct

from PIL import Image, ImageDraw, ImageFont

W, H, SS = 768, 512, 3          # final size and supersampling factor
CW, CH = W * SS, H * SS


def hexc(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))


def canvas(bg):
    im = Image.new('RGB', (CW, CH), hexc(bg))
    return im, ImageDraw.Draw(im)


def P(x, y):
    """Unit coordinates (x across the width, y down the height) to supersampled pixels."""
    return (x * CW, y * CH)


def poly(d, pts, fill):
    d.polygon([P(x, y) for x, y in pts], fill=hexc(fill))


def rect(d, x0, y0, x1, y1, fill):
    d.rectangle([P(x0, y0), P(x1, y1)], fill=hexc(fill))


def circle(d, cx, cy, r, fill):
    """r is in units of the flag height."""
    x, y = P(cx, cy)
    rr = r * CH
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=hexc(fill))


def flame(d, cx, cy, h, fill, m=1.6):
    """Teardrop flame, point up, centred at (cx, cy), h = height in flag heights."""
    a = h * CH / 2
    x0, y0 = P(cx, cy)
    pts = []
    for i in range(200):
        t = 2 * math.pi * i / 200
        pts.append((x0 + 0.62 * a * math.sin(t) * math.sin(t / 2) ** m, y0 - a * math.cos(t)))
    d.polygon(pts, fill=hexc(fill))


def star(d, cx, cy, R, r, n, fill, rot=-90):
    x0, y0 = P(cx, cy)
    pts = []
    for i in range(2 * n):
        ang = math.radians(rot + 180 * i / n)
        rad = (R if i % 2 == 0 else r) * CH
        pts.append((x0 + rad * math.cos(ang), y0 + rad * math.sin(ang)))
    d.polygon(pts, fill=hexc(fill))


def superellipse(d, cx, cy, a, b, n, fill, flat=1.0):
    """Formline ovoid: a, b in flag heights; flat < 1 flattens the lower half."""
    x0, y0 = P(cx, cy)
    pts = []
    for i in range(240):
        t = 2 * math.pi * i / 240
        c, s = math.cos(t), math.sin(t)
        x = a * CH * math.copysign(abs(c) ** (2 / n), c)
        y = b * CH * math.copysign(abs(s) ** (2 / n), s)
        if y > 0:
            y *= flat
        pts.append((x0 + x, y0 + y))
    d.polygon(pts, fill=hexc(fill))


def line(d, pts, fill, w):
    d.line([P(x, y) for x, y in pts], fill=hexc(fill), width=int(w * CH), joint='curve')


# ---------------------------------------------------------------------------------------------------------------
# Core proposal

def ctf():
    """Council of Three Fires (Niswi-mishkodewin): the Ojibwe, Odawa and Potawatomi as three council fires.
    Green for the Great Lakes forest, the three fires on a white council ground."""
    im, d = canvas('#1f5a3a')
    circle(d, 0.5, 0.5, 0.38, '#f4f1e6')
    for cx, cy in ((0.5, 0.35), (0.4, 0.6), (0.6, 0.6)):
        flame(d, cx, cy, 0.3, '#c93a1b')
        flame(d, cx, cy + 0.035, 0.18, '#f2c230')
    return im


def sfx():
    """Sauk and Meskwaki: the Meskwaki are the Red Earth People (Meshkwahkihaki), the Sauk the Yellow Earth People
    (Asakiwaki). Red over yellow, divided by a white band."""
    im, d = canvas('#b5282a')
    rect(d, 0, 0.5, 1, 1, '#d8a224')
    rect(d, 0, 0.47, 1, 0.53, '#f4f1e6')
    return im


def osg():
    """Osage: the nation is two moieties, the Tsi-zhu (Sky People) and the Honga (Earth People), joined by the morning
    star that leads the Sky People's rites."""
    im, d = canvas('#3f78bd')
    rect(d, 0, 0.5, 1, 1, '#76462a')
    star(d, 0.5, 0.5, 0.3, 0.12, 8, '#f4f1e6', rot=-90)
    circle(d, 0.5, 0.5, 0.07, '#d8a224')
    return im


def clf():
    """Californian peoples: the rattlesnake diamond band of Yokuts and Pomo coiled basketry, black and red on
    sedge-root cream."""
    im, d = canvas('#eee0bd')
    rect(d, 0, 0.3, 1, 0.33, '#1d1a17')
    rect(d, 0, 0.67, 1, 0.7, '#1d1a17')
    n = 6
    w = 1 / n
    for i in range(n):
        cx = (i + 0.5) * w
        poly(d, [(cx, 0.36), (cx + w / 2, 0.5), (cx, 0.64), (cx - w / 2, 0.5)], '#1d1a17')
        poly(d, [(cx, 0.43), (cx + w / 4, 0.5), (cx, 0.57), (cx - w / 4, 0.5)], '#b23a24')
    return im


def inu():
    """Inuit: an inuksuk, the stone figure Inuit built across the Arctic to mark routes and caribou drives,
    on sea ice under the sky."""
    im, d = canvas('#7fb0d6')
    rect(d, 0, 0.72, 1, 1, '#f4f6f8')
    s = '#2a2a2c'
    rect(d, 0.43, 0.56, 0.47, 0.75, s)          # legs
    rect(d, 0.53, 0.56, 0.57, 0.75, s)
    rect(d, 0.42, 0.5, 0.58, 0.57, s)           # hips
    rect(d, 0.33, 0.39, 0.67, 0.46, s)          # arms
    rect(d, 0.45, 0.46, 0.55, 0.5, s)           # body
    rect(d, 0.44, 0.27, 0.56, 0.39, s)          # chest
    rect(d, 0.47, 0.18, 0.53, 0.27, s)          # head
    return im


def inn():
    """Innu and Bay Cree: the mitshuap, the conical hunting lodge of the Innu and Cree, in the boreal forest
    above the winter snow."""
    im, d = canvas('#24553a')
    rect(d, 0, 0.68, 1, 1, '#f4f6f8')
    poly(d, [(0.5, 0.24), (0.64, 0.74), (0.36, 0.74)], '#b3262b')
    poly(d, [(0.5, 0.52), (0.54, 0.74), (0.46, 0.74)], '#1d1a17')    # door
    line(d, [(0.5, 0.24), (0.46, 0.12)], '#f4f1e6', 0.012)           # poles
    line(d, [(0.5, 0.24), (0.54, 0.12)], '#f4f1e6', 0.012)
    line(d, [(0.5, 0.24), (0.5, 0.1)], '#f4f1e6', 0.012)
    return im


# ---------------------------------------------------------------------------------------------------------------
# Optional "plus6" tags

def csc():
    """Northwest Coast: a formline ovoid eye, the basic unit of Haida, Tsimshian and Kwakwaka'wakw art, in black and
    red on cedar-bark cream, with Chilkat-blanket teal borders."""
    im, d = canvas('#f1ead8')
    rect(d, 0, 0, 1, 0.1, '#2e7d7a')
    rect(d, 0, 0.9, 1, 1, '#2e7d7a')
    rect(d, 0, 0.1, 1, 0.13, '#1d1a17')
    rect(d, 0, 0.87, 1, 0.9, '#1d1a17')
    superellipse(d, 0.5, 0.5, 0.36, 0.26, 2.6, '#1d1a17', flat=0.75)
    superellipse(d, 0.5, 0.5, 0.27, 0.18, 2.6, '#f1ead8', flat=0.75)
    superellipse(d, 0.5, 0.5, 0.2, 0.12, 2.6, '#b5282a', flat=0.75)
    superellipse(d, 0.5, 0.49, 0.1, 0.07, 2.4, '#1d1a17', flat=0.8)
    return im


def chy():
    """Cheyenne: the Morning Star, the Cheyenne symbol of the sacred arrows' giver Sweet Medicine and the name of
    their chiefs, on a sky field over the red earth of the southern plains."""
    im, d = canvas('#3b6fb6')
    rect(d, 0, 0.84, 1, 1, '#a8322d')
    star(d, 0.5, 0.46, 0.34, 0.08, 4, '#f4f1e6', rot=-90)
    circle(d, 0.5, 0.46, 0.06, '#a8322d')
    return im


def mha():
    """Mandan, Hidatsa and Arikara: the earth lodge of the Missouri River villages above the river itself."""
    im, d = canvas('#dcc79c')
    rect(d, 0, 0.82, 1, 1, '#2f6fa8')
    for k in range(5):                                             # river ripples
        y = 0.88 + 0.05 * (k % 2)
        line(d, [(0.1 + 0.18 * k, y), (0.16 + 0.18 * k, y - 0.02), (0.22 + 0.18 * k, y)], '#cfe3f0', 0.012)
    x0, y0 = P(0.5, 0.82)
    a, b = 0.3 * CH, 0.42 * CH
    d.pieslice([x0 - a * 1.5, y0 - b, x0 + a * 1.5, y0 + b], 180, 360, fill=hexc('#76462a'))
    rect(d, 0.465, 0.66, 0.535, 0.82, '#1d1a17')                  # entrance passage
    rect(d, 0.48, 0.4, 0.52, 0.44, '#1d1a17')                      # smoke hole
    return im


def ccm():
    """O'odham: I'itoi in the maze (the Man in the Maze), the O'odham emblem of life's journey, black on desert tan."""
    im, d = canvas('#e3cfa4')
    k = '#1d1a17'
    cx, cy = P(0.5, 0.55)
    rings = 6
    for i in range(rings):
        r = (0.08 + 0.055 * i) * CH
        gap = 22 - i
        if i % 2 == 0:
            spans = [(-90 + gap, 270 - gap)]                     # opening at the top
        else:
            spans = [(90 + gap, 450 - gap)]                      # opening at the bottom
        for a0, a1 in spans:
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=hexc(k), width=int(0.018 * CH))
    for i in range(rings - 1):                                    # radial walls that force the winding path
        r0 = (0.08 + 0.055 * i) * CH
        r1 = (0.08 + 0.055 * (i + 1)) * CH
        ang = math.radians(90 if i % 2 == 0 else -90) + (0.35 if i % 2 == 0 else -0.35)
        d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))],
               fill=hexc(k), width=int(0.018 * CH))
    # I'itoi standing at the entrance
    top = 0.55 - (0.08 + 0.055 * (rings - 1)) - 0.02
    circle(d, 0.5, top - 0.11, 0.025, k)
    line(d, [(0.5, top - 0.085), (0.5, top - 0.02)], k, 0.016)
    line(d, [(0.475, top - 0.06), (0.525, top - 0.06)], k, 0.014)
    line(d, [(0.5, top - 0.02), (0.485, top + 0.02)], k, 0.014)
    line(d, [(0.5, top - 0.02), (0.515, top + 0.02)], k, 0.014)
    return im


def mnm():
    """Menominee: Mamaceqtaw, the wild-rice people; manoomin standing in the lake, ripe for the harvest."""
    im, d = canvas('#cfe3f0')
    rect(d, 0, 0.66, 1, 1, '#2f6fa8')
    for x, h, lean in ((0.3, 0.42, -0.03), (0.4, 0.5, -0.01), (0.5, 0.56, 0.0), (0.6, 0.5, 0.01), (0.7, 0.42, 0.03)):
        top = (x + lean, 0.88 - h - 0.22)
        line(d, [(x, 0.9), (x + lean * 0.5, 0.6), top], '#3d7a3a', 0.014)
        for j in range(6):                                        # drooping seed head
            t = j / 5
            px = top[0] + 0.03 * t * (1 if lean >= 0 else -1) + 0.012 * math.sin(t * 3)
            py = top[1] + 0.038 * j
            x0, y0 = P(px, py)
            d.ellipse([x0 - 0.021 * CH, y0 - 0.033 * CH, x0 + 0.021 * CH, y0 + 0.033 * CH], fill=hexc('#b8862b'))
    return im


def hck():
    """Ho-Chunk: the Thunderbird, whose clan provided the nation's peace chiefs, in the Great Lakes style, between
    red bands."""
    im, d = canvas('#f4f1e6')
    rect(d, 0, 0, 1, 0.1, '#a8322d')
    rect(d, 0, 0.9, 1, 1, '#a8322d')
    k = '#1d1a17'
    # wings
    poly(d, [(0.5, 0.36), (0.2, 0.26), (0.17, 0.33), (0.25, 0.37), (0.21, 0.42), (0.3, 0.44), (0.5, 0.46)], k)
    poly(d, [(0.5, 0.36), (0.8, 0.26), (0.83, 0.33), (0.75, 0.37), (0.79, 0.42), (0.7, 0.44), (0.5, 0.46)], k)
    # hourglass body and tail fan
    poly(d, [(0.46, 0.33), (0.54, 0.33), (0.515, 0.55), (0.57, 0.74), (0.43, 0.74), (0.485, 0.55)], k)
    poly(d, [(0.43, 0.74), (0.57, 0.74), (0.6, 0.8), (0.4, 0.8)], k)
    # head with horn-like crest and beak
    circle(d, 0.5, 0.27, 0.06, k)
    poly(d, [(0.53, 0.25), (0.6, 0.27), (0.53, 0.29)], k)
    poly(d, [(0.48, 0.22), (0.45, 0.13), (0.5, 0.21)], k)
    # lightning from the wings
    line(d, [(0.22, 0.45), (0.27, 0.55), (0.22, 0.62), (0.27, 0.72)], '#a8322d', 0.016)
    line(d, [(0.78, 0.45), (0.73, 0.55), (0.78, 0.62), (0.73, 0.72)], '#a8322d', 0.016)
    return im


FLAGS = {
    'CTF': ('Council of Three Fires', ctf), 'SFX': ('Sauk and Meskwaki', sfx), 'OSG': ('Osage', osg),
    'CLF': ('Californian peoples', clf), 'INU': ('Inuit', inu), 'INN': ('Innu and Bay Cree', inn),
    'CSC': ('Northwest Coast', csc), 'CHY': ('Cheyenne', chy), 'MHA': ('Mandan, Hidatsa, Arikara', mha),
    'CCM': ("O'odham", ccm), 'MNM': ('Menominee', mnm), 'HCK': ('Ho-Chunk', hck),
}
PLUS6 = ['CSC', 'CHY', 'MHA', 'CCM', 'MNM', 'HCK']


def write_dds(img, path):
    """Uncompressed A8R8G8B8, one mip: header identical in layout to UFB_emblem.dds."""
    img = img.convert('RGBA')
    w, h = img.size
    hdr = struct.pack('<4sIIIIIII', b'DDS ', 124, 0x100F, h, w, w * 4, 0, 1) + b'\0' * 44
    hdr += struct.pack('<IIIIIIII', 32, 0x41, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    hdr += struct.pack('<IIIII', 0x1000, 0, 0, 0, 0)
    r, g, b, a = img.split()
    data = Image.merge('RGBA', (b, g, r, a)).tobytes()
    assert len(hdr) == 128
    with open(path, 'wb') as f:
        f.write(hdr + data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--preview', required=True)
    ap.add_argument('--only', default='', help='comma-separated tags (default: all)')
    a = ap.parse_args()
    only = [x for x in a.only.split(',') if x] or list(FLAGS)
    te = os.path.join(a.out, 'gfx', 'coat_of_arms', 'textured_emblems')
    os.makedirs(te, exist_ok=True)
    imgs = {}
    for tag, (name, fn) in FLAGS.items():
        if tag not in only:
            continue
        im = fn().resize((W, H), Image.LANCZOS)
        write_dds(im, os.path.join(te, f'te_hmps_{tag.lower()}.dds'))
        imgs[tag] = im
    # contact sheet
    tw, th, pad, lab = 256, 171, 24, 34
    cols = 6
    sheet = Image.new('RGB', (cols * (tw + pad) + pad, 2 * (th + lab + pad) + pad + 60), (245, 243, 238))
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 15)
        big = ImageFont.truetype('DejaVuSans-Bold.ttf', 17)
    except OSError:
        font = big = ImageFont.load_default()
    dr.text((pad, 10), 'Core proposal', fill=(30, 30, 30), font=big)
    if any(t in imgs for t in PLUS6): dr.text((pad, th + lab + pad + 40), 'Optional six (plus6 variant)', fill=(30, 30, 30), font=big)
    for row, tags in enumerate((list(FLAGS)[:6], PLUS6)):
        for col, tag in enumerate(t for t in tags if t in imgs):
            x = pad + col * (tw + pad)
            y = 36 + row * (th + lab + pad + 30)
            sheet.paste(imgs[tag].resize((tw, th), Image.LANCZOS), (x, y))
            dr.rectangle([x - 1, y - 1, x + tw, y + th], outline=(90, 90, 90))
            dr.text((x, y + th + 6), f'{tag}  {FLAGS[tag][0]}', fill=(30, 30, 30), font=font)
    sheet.save(a.preview)
    print('wrote', te, a.preview)


if __name__ == '__main__':
    main()
