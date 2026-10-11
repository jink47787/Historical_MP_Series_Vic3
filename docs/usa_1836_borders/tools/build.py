"""Rebuild the 1836 North America control proposal.

Georeferences the Vic3 province map from the state hub towns, then assigns every
province in the regions listed in control_1836.py to an owner and writes maps,
summary tables and a draft of the state history blocks.

usage: python -I build.py --game <Victoria 3 game dir> --work <cache dir> --out <output dir>
Needs numpy, pillow, matplotlib (and rdata, shapely for --counties).
"""
import argparse, glob, json, os, pickle, re, sys, unicodedata, urllib.request
from collections import Counter, defaultdict
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from matplotlib.path import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pdx import parse, get
import control_1836 as CC

Image.MAX_IMAGE_PIXELS = None
DOWNLOADS = {
    'cities.json': 'https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json',
    'rivers.geojson': 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_lake_centerlines.geojson',
}
REGION_FILES = ['05_north_america.txt', '06_central_america.txt']
COL = {'USA':(46,92,170),'MEX':(64,140,60),'TEX':(150,200,110),'ORG':(200,60,60),'NBS':(220,110,110),'NVS':(220,140,140),'ALK':(245,245,252),
       'HBC':(170,40,40),'ONT':(230,140,140),'QUE':(200,160,200),'GBR':(190,50,50),'SEQ':(140,110,190),'SML':(230,160,60),'LKT':(196,154,108),
       'PWN':(214,190,90),'COM':(210,120,70),'ARP':(170,130,80),'ABS':(150,170,120),'BLF':(90,90,90),'IRC':(120,150,170),'SLS':(90,160,150),
       'NZP':(140,180,200),'BNN':(190,170,140),'UTE':(200,150,160),'NVJ':(170,100,120),'APC':(220,190,150),'ATB':(160,160,120),
       'OJB':(110,170,110),'SFX':(180,200,120),'OSG':(160,90,60),'CLF':(230,210,120)}

def fetch(work, name):
    path = os.path.join(work, name)
    if not os.path.exists(path):
        print('downloading', name)
        urllib.request.urlretrieve(DOWNLOADS[name], path)
    return path

def load_provinces(game, work):
    cache = os.path.join(work, 'provs.pkl')
    if os.path.exists(cache):
        return pickle.load(open(cache, 'rb'))
    im = np.array(Image.open(os.path.join(game, 'map_data/provinces.png')).convert('RGB'))
    H, W, _ = im.shape
    regions = {}
    for f in REGION_FILES:
        for k, v in parse(open(os.path.join(game, 'map_data/state_regions', f), encoding='utf-8-sig').read()):
            d = {'provinces': [x.strip('"') for _, x in get(v, 'provinces')[0]]}
            for h in ['city', 'port', 'farm', 'mine', 'wood']:
                if get(v, h): d[h] = get(v, h)[0].strip('"')
            regions[k] = d
    want = {int(p[1:], 16): (s, p) for s, d in regions.items() for p in d['provinces']}
    sub = im[:, :W // 2].astype(np.int64)
    code = (sub[:, :, 0] << 16) | (sub[:, :, 1] << 8) | sub[:, :, 2]
    ys, xs = np.nonzero(np.isin(code, np.array(list(want))))
    vals = code[ys, xs]; o = np.argsort(vals); vals, ys, xs = vals[o], ys[o], xs[o]
    u, idx, cnt = np.unique(vals, return_index=True, return_counts=True)
    prov = {}
    for a, i, c in zip(u, idx, cnt):
        s, p = want[int(a)]
        prov[p] = {'state': s, 'x': xs[i:i + c].astype(np.int32), 'y': ys[i:i + c].astype(np.int32), 'n': int(c)}
    out = {'regions': regions, 'prov': prov, 'W': W, 'H': H}
    pickle.dump(out, open(cache, 'wb'))
    return out

def feats(lon, lat):
    lon = np.asarray(lon, float); lat = np.asarray(lat, float)
    return np.stack([np.ones_like(lon), lon, lat, lon * lon, lon * lat, lat * lat, lon ** 3, lon * lon * lat, lon * lat * lat, lat ** 3], -1)

class Georef:
    """Cubic lon/lat -> pixel fit on the state hub towns (city/port/farm/mine/wood)."""
    def __init__(self, game, work, P):
        loc = {}
        for f in glob.glob(os.path.join(game, 'localization/english/**/*.yml'), recursive=True):
            for line in open(f, encoding='utf-8-sig', errors='ignore'):
                m = re.match(r'\s*(HUB_NAME_STATE_\w+?_(city|port|farm|mine|wood)):\d*\s*"(.*)"', line)
                if m: loc[m.group(1)] = m.group(3)
        def norm(s):
            s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
            s = re.sub(r'^(ft\.?|st\.?)\s+', lambda m: {'ft': 'fort ', 'ft.': 'fort ', 'st': 'saint ', 'st.': 'saint '}[m.group(1)], s)
            return re.sub(r'[^a-z ]', '', s).strip()
        byname = defaultdict(list)
        for c in json.load(open(fetch(work, 'cities.json'))):
            if c['country'] in ('US','CA','MX','GT','BZ','HN','SV','NI','CR','PA','CU','BS','JM','HT','DO','PR'):
                byname[norm(c['name'])].append((float(c['lng']), float(c['lat'])))
        pts = []
        for s, d in P['regions'].items():
            for h in ['city', 'port', 'farm', 'mine', 'wood']:
                nm = loc.get(f'HUB_NAME_{s}_{h}')
                if h in d and nm and byname.get(norm(nm)):
                    p = P['prov'][d[h]]
                    pts.append((float(p['x'].mean()), float(p['y'].mean()), byname[norm(nm)]))
        # robust start: affine RANSAC on towns with a unique name match
        U = np.array([(c[0][0], c[0][1], x, y) for x, y, c in pts if len(c) == 1])
        rng = np.random.default_rng(0); best = None
        A1 = np.c_[np.ones(len(U)), U[:, 0], U[:, 1]]
        for _ in range(3000):
            i = rng.choice(len(U), 4, replace=False)
            cx = np.linalg.lstsq(A1[i], U[i, 2], rcond=None)[0]; cy = np.linalg.lstsq(A1[i], U[i, 3], rcond=None)[0]
            n = (np.hypot(A1 @ cx - U[:, 2], A1 @ cy - U[:, 3]) < 40).sum()
            if best is None or n > best[0]: best = (n, cx, cy)
        pred = lambda lo, la: (best[1][0] + best[1][1] * lo + best[1][2] * la, best[2][0] + best[2][1] * lo + best[2][2] * la)
        thr = 60
        for _ in range(6):
            L = []
            for x, y, c in pts:
                c = np.array(c); px, py = pred(c[:, 0], c[:, 1]); e = np.hypot(px - x, py - y); j = int(np.argmin(e))
                if e[j] < thr: L.append((c[j, 0], c[j, 1], x, y))
            L = np.array(L); A = feats(L[:, 0], L[:, 1])
            self.coef = (np.linalg.lstsq(A, L[:, 2], rcond=None)[0], np.linalg.lstsq(A, L[:, 3], rcond=None)[0])
            pred = self.proj
            px, py = pred(L[:, 0], L[:, 1]); err = np.hypot(px - L[:, 2], py - L[:, 3])
            thr = max(15, np.percentile(err, 90) * 1.5)
        self.stats = (len(L), float(np.median(err)), float(np.percentile(err, 90)))
    def proj(self, lon, lat):
        A = feats(lon, lat); return A @ self.coef[0], A @ self.coef[1]
    def inv(self, x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        lon = np.full_like(x, -95.0); lat = np.full_like(x, 38.0)
        for _ in range(30):
            px, py = self.proj(lon, lat); d = 1e-3
            ax, ay = self.proj(lon + d, lat); bx, by = self.proj(lon, lat + d)
            j11, j21, j12, j22 = (ax - px) / d, (ay - py) / d, (bx - px) / d, (by - py) / d
            det = j11 * j22 - j12 * j21; ex, ey = x - px, y - py
            lon = lon + (j22 * ex - j12 * ey) / det; lat = lat + (-j21 * ex + j11 * ey) / det
        return lon, lat

def vanilla_owners(game, regions):
    h = parse(open(os.path.join(game, 'common/history/states/00_states.txt'), encoding='utf-8-sig').read())
    van, blocks = {}, {}
    for k, v in get(h, 'STATES')[0]:
        s = k[2:]
        if s not in regions: continue
        blocks[s] = v
        for cs in get(v, 'create_state'):
            c = get(cs, 'country')[0][2:]; op = get(cs, 'owned_provinces')
            for p in ([x.strip('"') for _, x in op[0]] if op else regions[s]['provinces']): van[p] = c
    return van, blocks

def classify(P, G):
    rng = np.random.default_rng(1); prop, why = {}, {}
    for s, spec in CC.R.items():
        paths = [(o, Path(np.array(poly))) for o, poly in spec['rules']]
        for p in P['regions'][s]['provinces']:
            v = P['prov'][p]; idx = rng.choice(v['n'], min(v['n'], 150), replace=False)
            pts = np.c_[G.inv(v['x'][idx] + 0.5, v['y'][idx] + 0.5)]
            owner = np.full(len(pts), spec['default'], dtype=object); done = np.zeros(len(pts), bool)
            for o, pa in paths:
                m = pa.contains_points(pts) & ~done; owner[m] = o; done |= m
            vals, cnt = np.unique(owner, return_counts=True)
            prop[p] = vals[np.argmax(cnt)]
        for o, lo, la, name in spec.get('footholds', []):
            x, y = (float(a) for a in G.proj(lo, la))
            dist = {q: np.min((P['prov'][q]['x'] - x) ** 2 + (P['prov'][q]['y'] - y) ** 2) for q in P['regions'][s]['provinces']}
            q = min(dist, key=dist.get)
            if dist[q] <= 144: prop[q] = o; why[q] = name
            else: print('foothold not placed (too far from any province):', name)
    return prop, why

def render(P, own, path, title, box=(1180, 800, 2640, 1580), game=None, scale=1.0):
    X0, Y0, X1, Y1 = box
    im = np.array(Image.open(os.path.join(game, 'map_data/provinces.png')).convert('RGB').crop(box)).astype(np.int64)
    code = (im[:, :, 0] << 16) | (im[:, :, 1] << 8) | im[:, :, 2]
    out = np.full(im.shape, (200, 215, 230), np.uint8); land = np.zeros(code.shape, bool); st = np.full(code.shape, -1, np.int32)
    names = list(P['regions']); acc = defaultdict(lambda: [0.0, 0.0, 0])
    for p, v in P['prov'].items():
        m = (v['x'] >= X0) & (v['x'] < X1) & (v['y'] >= Y0) & (v['y'] < Y1)
        if not m.any(): continue
        xs, ys = v['x'][m] - X0, v['y'][m] - Y0; o = own.get(p)
        out[ys, xs] = COL.get(o, (225, 225, 215)); land[ys, xs] = True; st[ys, xs] = names.index(v['state'])
        if o:
            a = acc[(v['state'], o)]; a[0] += xs.sum(); a[1] += ys.sum(); a[2] += len(xs)
    pe = np.zeros(code.shape, bool); pe[1:] |= code[1:] != code[:-1]; pe[:, 1:] |= code[:, 1:] != code[:, :-1]
    se = np.zeros(code.shape, bool); se[1:] |= st[1:] != st[:-1]; se[:, 1:] |= st[:, 1:] != st[:, :-1]
    se[1:] |= se[:-1].copy(); se[:, 1:] |= se[:, :-1].copy()
    out[pe & land] = (out[pe & land] * 0.82).astype(np.uint8); out[se & land] = (30, 30, 30)
    img = Image.fromarray(out); d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype('DejaVuSans-Bold.ttf', 13); ft = ImageFont.truetype('DejaVuSans-Bold.ttf', 22)
    except OSError:
        try:
            f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13); ft = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
        except OSError:
            f = ft = ImageFont.load_default()
    for (s, o), (sx, sy, n) in acc.items():
        if n >= 300:
            d.text((sx / n, sy / n), o, fill=(0, 0, 0), font=f, anchor='mm', stroke_width=2, stroke_fill=(255, 255, 255))
    d.text((12, 10), title, fill=(0, 0, 0), font=ft, stroke_width=3, stroke_fill=(255, 255, 255))
    if scale != 1.0: img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    img.save(path, optimize=True)

def draft_states(P, prop, van, blocks):
    lines = ['# DRAFT, not loaded by the game. Proposed North America splits for common/history/states.',
             '# Generated by docs/usa_1836_borders/tools/build.py. Homelands and vanilla claims are copied unchanged;',
             '# claims marked "# proposed" are new. state_type is kept for owners that already had a split.', '']
    for s in CC.R:
        v = blocks[s]
        types = {get(cs, 'country')[0][2:]: (get(cs, 'state_type') or [None])[0] for cs in get(v, 'create_state')}
        by = defaultdict(list)
        for p in P['regions'][s]['provinces']: by[prop[p]].append(p)
        lines.append(f'\ts:{s} = {{')
        for o in sorted(by, key=lambda o: (-len(by[o]), o)):
            lines += ['\t\tcreate_state = {', f'\t\t\tcountry = c:{o}', '\t\t\towned_provinces = {', '\t\t\t\t' + ' '.join(by[o]), '\t\t\t}']
            if types.get(o): lines.append(f'\t\t\tstate_type = {types[o]}')
            lines.append('\t\t}')
        lines.append('')
        claims = [c[2:] for c in get(v, 'add_claim')]
        for c in claims: lines.append(f'\t\tadd_claim = c:{c}')
        for c in CC.ADD_CLAIMS.get(s, []):
            if c not in claims: lines.append(f'\t\tadd_claim = c:{c} # proposed')
        for hm in get(v, 'add_homeland'): lines.append(f'\t\tadd_homeland = {hm}')
        lines += ['\t}', '']
    return '\n'.join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', required=True); ap.add_argument('--work', required=True); ap.add_argument('--out', required=True)
    a = ap.parse_args(); os.makedirs(a.work, exist_ok=True); os.makedirs(a.out, exist_ok=True)
    P = load_provinces(a.game, a.work)
    G = Georef(a.game, a.work, P)
    print('georeference: %d towns, median error %.1f px, 90th pct %.1f px' % G.stats)
    van, blocks = vanilla_owners(a.game, P['regions'])
    prop, why = classify(P, G)
    full = dict(van); full.update(prop)
    render(P, van, os.path.join(a.out, 'map_vanilla.png'), 'Vanilla 1836 ownership', game=a.game)
    render(P, full, os.path.join(a.out, 'map_proposed.png'), 'Proposed: actual control, 1 Jan 1836', game=a.game)
    open(os.path.join(a.out, 'draft_states_north_america.txt'), 'w', encoding='utf-8-sig').write(draft_states(P, prop, van, blocks))
    rows = []
    for s in CC.R:
        ps = P['regions'][s]['provinces']
        f = lambda c: ', '.join(f'{k} {c[k]}' for k in sorted(c, key=lambda k: (-c[k], k)))
        rows.append(f"| {s[6:]} | {len(ps)} | {f(Counter(van[p] for p in ps))} | {f(Counter(prop[p] for p in ps))} |")
    fh = [f'| {name} | {s[6:]} | {o} | {p} |' for p, name in why.items() for s, o in [(P['prov'][p]['state'], prop[p])]]
    open(os.path.join(a.out, 'summary.md'), 'w').write('| State | Provinces | Vanilla | Proposed |\n|---|---|---|---|\n' + '\n'.join(rows)
        + '\n\n| Foothold | State | Owner | Province |\n|---|---|---|---|\n' + '\n'.join(fh) + '\n')
    pickle.dump({'prop': prop, 'van': van, 'why': why}, open(os.path.join(a.work, 'classified.pkl'), 'wb'))
    print('wrote', a.out)

if __name__ == '__main__':
    main()
