"""Regenerate the 1836 North America border docs from the mod's current state history.

Compares the mod's common/history/states/00_states.txt with vanilla for every state region in the North and
Central America region files, keeps the regions whose owners or claims differ, and writes to --out:
  summary.md           owners per region (vanilla vs current), claim changes, detached colonial pieces
  province_table.csv   province,state,vanilla_owner,current_owner for those regions
  map_vanilla.png / map_current.png         US close-up
  map_vanilla_na.png / map_current_na.png   all of North America

py -3.14 -I tools/maps.py --game <repo>/basegame-ver --mod "<repo>/Historical MP Series" --out .
Needs numpy and pillow.
"""
import argparse, csv, os, sys
from collections import Counter, defaultdict
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdx import parse, get

Image.MAX_IMAGE_PIXELS = None
REGION_FILES = ['05_north_america.txt', '06_central_america.txt']
US_BOX, NA_BOX = (1180, 800, 2640, 1580), (150, 0, 2900, 1600)
COLONIAL = {'USA', 'MEX', 'TEX', 'GBR', 'ORG', 'HBC', 'ONT', 'QUE', 'NBS', 'NVS', 'ALK', 'RUS', 'SPA', 'FRA'}
COL = {'USA':(46,92,170),'MEX':(64,140,60),'TEX':(150,200,110),'ORG':(200,60,60),'NBS':(220,110,110),'NVS':(220,140,140),'ALK':(245,245,252),
       'HBC':(176,120,70),'ONT':(230,140,140),'QUE':(200,160,200),'GBR':(190,50,50),'SEQ':(140,110,190),'SML':(230,160,60),'LKT':(196,154,108),
       'PWN':(214,190,90),'COM':(210,120,70),'ARP':(170,130,80),'ABS':(150,170,120),'BLF':(90,90,90),'IRC':(120,150,170),'SLS':(90,160,150),
       'NZP':(140,180,200),'BNN':(190,170,140),'UTE':(200,150,160),'NVJ':(170,100,120),'APC':(220,190,150),'ATB':(160,160,120),
       'CTF':(110,170,110),'SFX':(180,200,120),'OSG':(160,90,60),'CLF':(230,210,120),'INU':(150,205,215),'INN':(100,85,150),'CHN':(200,120,180),
       'CSC':(40,110,110),'CHY':(120,80,40),'MHA':(230,170,40),'CCM':(170,150,90),'MNM':(60,130,60),'HCK':(140,60,90),'RUS':(60,110,60)}
# names for the small detached pieces, by province
PLACES = {'xE76A88': 'Fort Mackinac', 'x8BD355': 'Fort Brady, Sault Ste. Marie', 'xE58A3D': 'Fort Brooke (Tampa)',
          'x4070C0': 'Key West', 'xCF5B71': 'Fort Leavenworth', 'x18F9D5': 'El Paso valley', 'x3F27C8': 'Fort Ross',
          'x8D15CB': 'Severn House', 'x257105': 'Fort Albany', 'x627826': 'Moose Factory', 'x7B6229': 'Rupert House',
          'x33C3E1': 'Eastmain', 'x537B4B': 'Fort George', 'x7020B3': 'Fort Chimo', 'xB5C055': 'Churchill',
          'x9CB866': 'York Factory', 'x6B748E': 'Norway House'}


def norm(p):
    return 'x' + p.strip('"')[1:].upper()


def read(path):
    return parse(open(path, encoding='utf-8-sig').read())


def regions(mod):
    out = {}
    for f in REGION_FILES:
        for k, v in read(os.path.join(mod, 'map_data/state_regions', f)):
            out[k] = [norm(x) for _, x in get(v, 'provinces')[0]]
    return out


def history(path, states):
    """STATE -> (province -> owner, sorted claims)."""
    out = {}
    for _, top in read(path):
        for k, v in top:
            s = k[2:] if k and k.startswith('s:') else None
            if s not in states: continue
            own = {}
            for cs in get(v, 'create_state'):
                o = get(cs, 'country')[0][2:]
                for _, p in get(cs, 'owned_provinces')[0]: own[norm(p)] = o
            out[s] = (own, sorted(c[2:] for c in get(v, 'add_claim')))
    return out


def load_pixels(game, provs):
    im = np.array(Image.open(os.path.join(game, 'map_data/provinces.png')).convert('RGB').crop(NA_BOX)).astype(np.int64)
    code = (im[:, :, 0] << 16) | (im[:, :, 1] << 8) | im[:, :, 2]
    want = {int(p[1:], 16): p for p in provs}
    ys, xs = np.nonzero(np.isin(code, np.array(list(want))))
    vals = code[ys, xs]; o = np.argsort(vals); vals, ys, xs = vals[o], ys[o], xs[o]
    u, idx, cnt = np.unique(vals, return_index=True, return_counts=True)
    pix = {want[int(a)]: (xs[i:i + c] + NA_BOX[0], ys[i:i + c] + NA_BOX[1]) for a, i, c in zip(u, idx, cnt)}
    adj = defaultdict(set)
    for a, b in [(code[1:], code[:-1]), (code[:, 1:], code[:, :-1])]:
        m = a != b
        for x, y in set(zip(a[m].tolist(), b[m].tolist())):
            if x in want and y in want: adj[want[x]].add(want[y]); adj[want[y]].add(want[x])
    with open(os.path.join(game, 'map_data/adjacencies.csv'), encoding='utf-8-sig') as f:
        for r in csv.reader(f, delimiter=';'):
            if len(r) > 2 and r[0].isdigit() and r[1].isdigit():
                x, y = int(r[0]), int(r[1])
                if x in want and y in want: adj[want[x]].add(want[y]); adj[want[y]].add(want[x])
    return pix, adj


def render(pix, state_of, own, path, title, box, scale=1.0):
    X0, Y0, X1, Y1 = box
    W, H = X1 - X0, Y1 - Y0
    out = np.full((H, W, 3), (200, 215, 230), np.uint8); prov = np.full((H, W), -1, np.int32); st = np.full((H, W), -1, np.int32)
    names = sorted(set(state_of.values())); ids = {p: i for i, p in enumerate(pix)}; acc = defaultdict(lambda: [0.0, 0.0, 0])
    for p, (x, y) in pix.items():
        m = (x >= X0) & (x < X1) & (y >= Y0) & (y < Y1)
        if not m.any(): continue
        xs, ys = x[m] - X0, y[m] - Y0; o = own.get(p)
        out[ys, xs] = COL.get(o, (225, 225, 215)); prov[ys, xs] = ids[p]; st[ys, xs] = names.index(state_of[p])
        if o:
            a = acc[(state_of[p], o)]; a[0] += xs.sum(); a[1] += ys.sum(); a[2] += len(xs)
    land = prov >= 0
    pe = np.zeros(land.shape, bool); pe[1:] |= prov[1:] != prov[:-1]; pe[:, 1:] |= prov[:, 1:] != prov[:, :-1]
    se = np.zeros(land.shape, bool); se[1:] |= st[1:] != st[:-1]; se[:, 1:] |= st[:, 1:] != st[:, :-1]
    se[1:] |= se[:-1].copy(); se[:, 1:] |= se[:, :-1].copy()
    out[pe & land] = (out[pe & land] * 0.82).astype(np.uint8); out[se & land] = (30, 30, 30)
    img = Image.fromarray(out); d = ImageDraw.Draw(img)
    try:
        f, ft = ImageFont.truetype('arialbd.ttf', 13), ImageFont.truetype('arialbd.ttf', 22)
    except OSError:
        f = ft = ImageFont.load_default()
    for (s, o), (sx, sy, n) in acc.items():
        if n >= 300:
            d.text((sx / n, sy / n), o, fill=(0, 0, 0), font=f, anchor='mm', stroke_width=2, stroke_fill=(255, 255, 255))
    d.text((12, 10), title, fill=(0, 0, 0), font=ft, stroke_width=3, stroke_fill=(255, 255, 255))
    if scale != 1.0: img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    img.save(path, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', required=True); ap.add_argument('--mod', required=True); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    R = regions(a.mod)
    van = history(os.path.join(a.game, 'common/history/states/00_states.txt'), R)
    cur = history(os.path.join(a.mod, 'common/history/states/00_states.txt'), R)
    for s in R:  # a state the mod does not override keeps vanilla
        cur.setdefault(s, van.get(s, ({}, [])))
    changed = [s for s in R if s in van and (van[s][0] != cur[s][0] or van[s][1] != cur[s][1])]
    state_of = {p: s for s, ps in R.items() for p in ps}
    V = {p: o for s in R for p, o in van.get(s, ({}, []))[0].items()}
    C = {p: o for s in R for p, o in cur[s][0].items()}
    pix, adj = load_pixels(a.game, list(state_of))

    with open(os.path.join(a.out, 'province_table.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['province', 'state', 'vanilla_owner', 'current_owner'])
        for s in changed:
            for p in R[s]: w.writerow([p, s, V.get(p, ''), C.get(p, '')])

    fmt = lambda c: ', '.join(f'{k} {c[k]}' for k in sorted(c, key=lambda k: (-c[k], k)))
    lines = ['# 1836 North America: owners per state region', '',
             'Generated by `tools/maps.py` from the mod\'s state history. Only regions that differ from vanilla are listed.', '',
             '| State | Provinces | Vanilla | Current |', '|---|---|---|---|']
    for s in changed:
        lines.append(f'| {s[6:]} | {len(R[s])} | {fmt(Counter(V.get(p, "none") for p in R[s]))} | {fmt(Counter(C.get(p, "none") for p in R[s]))} |')
    tot_v = Counter(V.get(p, 'none') for s in changed for p in R[s]); tot_c = Counter(C.get(p, 'none') for s in changed for p in R[s])
    lines += ['', '## Totals over these regions', '', '| Owner | Vanilla | Current |', '|---|---|---|']
    for o in sorted(set(tot_v) | set(tot_c), key=lambda o: (-tot_c[o], -tot_v[o], o)):
        lines.append(f'| {o} | {tot_v[o]} | {tot_c[o]} |')
    lines += ['', '## Claims that differ from vanilla', '', '| State | Vanilla | Current |', '|---|---|---|']
    for s in changed:
        if van[s][1] != cur[s][1]:
            lines.append(f'| {s[6:]} | {", ".join(van[s][1]) or "none"} | {", ".join(cur[s][1]) or "none"} |')
    lines += ['', '## Detached colonial pieces', '',
              'Pieces of a colonial owner\'s land in North America not connected (by land or a strait) to its largest block.', '',
              '| Owner | State | Provinces | Place |', '|---|---|---|---|']
    for o in sorted({C[p] for s in changed for p in R[s] if C.get(p) in COLONIAL}):
        mine = {p for p, x in C.items() if x == o}; seen = set(); comps = []
        for p in mine:
            if p in seen: continue
            comp, stack = [], [p]; seen.add(p)
            while stack:
                q = stack.pop(); comp.append(q)
                for r in adj[q]:
                    if r in mine and r not in seen: seen.add(r); stack.append(r)
            comps.append(comp)
        comps.sort(key=len, reverse=True)
        for comp in comps[1:]:
            if not any(state_of[p] in changed for p in comp): continue
            sts = ', '.join(sorted({state_of[p][6:] for p in comp}))
            place = ', '.join(PLACES[p] for p in comp if p in PLACES)
            lines.append(f'| {o} | {sts} | {" ".join(sorted(comp))} | {place} |')
    open(os.path.join(a.out, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    render(pix, state_of, V, os.path.join(a.out, 'map_vanilla.png'), 'Vanilla 1836 ownership', US_BOX)
    render(pix, state_of, C, os.path.join(a.out, 'map_current.png'), 'HMPS 1836 ownership', US_BOX)
    render(pix, state_of, V, os.path.join(a.out, 'map_vanilla_na.png'), 'Vanilla 1836 ownership', NA_BOX, 0.6)
    render(pix, state_of, C, os.path.join(a.out, 'map_current_na.png'), 'HMPS 1836 ownership', NA_BOX, 0.6)
    print(len(changed), 'regions differ from vanilla:', ' '.join(s[6:] for s in changed))


if __name__ == '__main__':
    main()
