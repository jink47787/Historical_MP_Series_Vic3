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
    'coast.geojson': 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_coastline.geojson',
}
REGION_FILES = ['05_north_america.txt', '06_central_america.txt']
COL = {'USA':(46,92,170),'MEX':(64,140,60),'TEX':(150,200,110),'ORG':(200,60,60),'NBS':(220,110,110),'NVS':(220,140,140),'ALK':(245,245,252),
       'HBC':(170,40,40),'ONT':(230,140,140),'QUE':(200,160,200),'GBR':(190,50,50),'SEQ':(140,110,190),'SML':(230,160,60),'LKT':(196,154,108),
       'PWN':(214,190,90),'COM':(210,120,70),'ARP':(170,130,80),'ABS':(150,170,120),'BLF':(90,90,90),'IRC':(120,150,170),'SLS':(90,160,150),
       'NZP':(140,180,200),'BNN':(190,170,140),'UTE':(200,150,160),'NVJ':(170,100,120),'APC':(220,190,150),'ATB':(160,160,120),
       'CTF':(110,170,110),'SFX':(180,200,120),'OSG':(160,90,60),'CLF':(230,210,120),'INU':(150,205,215),'INN':(100,85,150),'CHN':(200,120,180),
       'CSC':(40,110,110),'CHY':(120,80,40),'MHA':(230,170,40),'CCM':(170,150,90),'MNM':(60,130,60),'HCK':(140,60,90)}
COL['HBC'] = (176, 120, 70)

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

def feats(lon, lat, deg=4):
    x = (np.asarray(lon, float) + 100) / 40; y = (np.asarray(lat, float) - 45) / 25
    return np.stack([x ** i * y ** j for i in range(deg + 1) for j in range(deg + 1 - i)], -1)

class Georef:
    """Polynomial lon/lat -> pixel fit: hub towns (city/port/farm/mine/wood) give the first fit,
    then the Natural Earth coastline is matched to the game coastline (ICP) so the Arctic fits too."""
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
        thr = 60; self.deg = 3
        for _ in range(6):
            L = []
            for x, y, c in pts:
                c = np.array(c); px, py = pred(c[:, 0], c[:, 1]); e = np.hypot(px - x, py - y); j = int(np.argmin(e))
                if e[j] < thr: L.append((c[j, 0], c[j, 1], x, y))
            L = np.array(L); A = feats(L[:, 0], L[:, 1], 3)
            self.coef = (np.linalg.lstsq(A, L[:, 2], rcond=None)[0], np.linalg.lstsq(A, L[:, 3], rcond=None)[0])
            pred = self.proj
            px, py = pred(L[:, 0], L[:, 1]); err = np.hypot(px - L[:, 2], py - L[:, 3])
            thr = max(15, np.percentile(err, 90) * 1.5)
        # coastline ICP, degree 4
        from scipy.spatial import cKDTree
        H, W = P['H'], P['W'] // 2
        land = np.zeros((H, W), bool)
        for v in P['prov'].values(): land[v['y'], v['x']] = True
        edge = np.zeros_like(land)
        edge[1:-1, 1:-1] = land[1:-1, 1:-1] & ~(land[:-2, 1:-1] & land[2:, 1:-1] & land[1:-1, :-2] & land[1:-1, 2:])
        cy, cx = np.nonzero(edge); tree = cKDTree(np.c_[cx, cy])
        ne = []
        for f in json.load(open(fetch(work, 'coast.geojson')))['features']:
            g = f['geometry']
            for part in ([g['coordinates']] if g['type'] == 'LineString' else g['coordinates']):
                a = np.array(part); ne.append(a[(a[:, 0] < -50) & (a[:, 1] > 7)])
        ne = np.concatenate(ne)
        for r in [40, 30, 22, 16, 12, 9, 7, 6, 6]:
            px, py = self.proj(ne[:, 0], ne[:, 1])
            d, i = tree.query(np.c_[px, py], distance_upper_bound=r); m = np.isfinite(d)
            lon = np.r_[ne[m, 0], np.repeat(L[:, 0], 8)]; lat = np.r_[ne[m, 1], np.repeat(L[:, 1], 8)]
            X = np.r_[cx[i[m]], np.repeat(L[:, 2], 8)]; Y = np.r_[cy[i[m]], np.repeat(L[:, 3], 8)]
            A = feats(lon, lat, 4)
            self.coef = (np.linalg.lstsq(A, X, rcond=None)[0], np.linalg.lstsq(A, Y, rcond=None)[0]); self.deg = 4
        px, py = self.proj(L[:, 0], L[:, 1]); err = np.hypot(px - L[:, 2], py - L[:, 3])
        self.stats = (len(L), float(np.median(err)), float(np.percentile(err, 90)), float(np.median(d[m])))
        # coarse grid for the inverse's starting guess
        glon, glat = np.meshgrid(np.arange(-180, -45, 0.5), np.arange(5, 86, 0.5))
        gx, gy = self.proj(glon.ravel(), glat.ravel())
        self.grid = (cKDTree(np.c_[gx, gy]), glon.ravel(), glat.ravel())
    def proj(self, lon, lat):
        A = feats(lon, lat, self.deg); return A @ self.coef[0], A @ self.coef[1]
    def inv(self, x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        _, k = self.grid[0].query(np.c_[x, y]); lon = self.grid[1][k].astype(float); lat = self.grid[2][k].astype(float)
        for _ in range(30):
            px, py = self.proj(lon, lat); d = 1e-3
            ax, ay = self.proj(lon + d, lat); bx, by = self.proj(lon, lat + d)
            j11, j21, j12, j22 = (ax - px) / d, (ay - py) / d, (bx - px) / d, (by - py) / d
            det = j11 * j22 - j12 * j21; ex, ey = x - px, y - py
            lon = lon + (j22 * ex - j12 * ey) / det; lat = lat + (-j21 * ex + j11 * ey) / det
        return lon, lat

def load_adjacency(game, work):
    cache = os.path.join(work, 'adj.pkl')
    if os.path.exists(cache):
        return pickle.load(open(cache, 'rb'))
    im = np.array(Image.open(os.path.join(game, 'map_data/provinces.png')).convert('RGB'))
    im = im[:, :im.shape[1] // 2].astype(np.int64)
    c = (im[:, :, 0] << 16) | (im[:, :, 1] << 8) | im[:, :, 2]
    adj = defaultdict(set)
    for a, b in [(c[1:], c[:-1]), (c[:, 1:], c[:, :-1])]:
        m = a != b
        for u, v in np.unique(np.stack([np.minimum(a[m], b[m]), np.maximum(a[m], b[m])], 1), axis=0).tolist():
            adj['x%06X' % u].add('x%06X' % v); adj['x%06X' % v].add('x%06X' % u)
    import csv
    for row in csv.reader(open(os.path.join(game, 'map_data/adjacencies.csv'), encoding='utf-8-sig'), delimiter=';'):
        if len(row) > 2 and row[0][:1] in 'xX' and row[1][:1] in 'xX':
            a, b = 'x' + row[0][1:].upper(), 'x' + row[1][1:].upper()
            adj[a].add(b); adj[b].add(a)
    adj = dict(adj)
    pickle.dump(adj, open(cache, 'wb'))
    return adj

def components(provs, adj):
    provs = set(provs); seen = set(); out = []
    for p in provs:
        if p in seen: continue
        comp, stack = [], [p]; seen.add(p)
        while stack:
            q = stack.pop(); comp.append(q)
            for r in adj.get(q, ()):
                if r in provs and r not in seen: seen.add(r); stack.append(r)
        out.append(comp)
    return sorted(out, key=len, reverse=True)

def enforce_contiguity(P, adj, van, prop, keep, small=6):
    """Hand detached fragments of fewer than `small` provinces to the neighbouring owner.
    `keep` holds named enclaves that may stay detached. Returns the reassignments and larger detached blocks."""
    changed, flagged = [], []
    for _ in range(10):
        full = dict(van); full.update(prop)
        by = defaultdict(list)
        for p, o in full.items(): by[o].append(p)
        moved = False
        for o in sorted({prop[p] for p in prop}):
            comps = components(by[o], adj)
            for comp in comps[1:]:
                if not any(p in prop for p in comp): continue
                if all(p in keep for p in comp): continue
                if len(comp) >= small:
                    touches = {full[q] for p in comp for q in adj.get(p, ()) if q in full and full[q] != o}
                    if touches: flagged.append((o, len(comp), P['prov'][comp[0]]['state']))
                    continue
                for p in comp:
                    if p not in prop or p in keep: continue
                    nb = Counter(full[q] for q in adj.get(p, ()) if q in full and full[q] != o)
                    if nb:
                        new = nb.most_common(1)[0][0]; changed.append((p, P['prov'][p]['state'], o, new)); prop[p] = new; moved = True
        if not moved: break
    return changed, sorted(set(flagged))

def connect_blocks(P, adj, van, prop, pairs):
    """For each (owner, state) in pairs, join every detached block of the owner's split in that state
    to the owner's largest territory by the shortest path of provinces in the regions being changed."""
    import heapq
    changed = []
    for o, s in pairs:
        full = dict(van); full.update(prop)
        comps = components([p for p, w in full.items() if w == o], adj)
        main = set(comps[0])
        for comp in comps[1:]:
            if not any(P['prov'][p]['state'] == s for p in comp): continue
            dist = {p: 0 for p in comp}; prev = {}; heap = [(0, p) for p in comp]; hit = None
            while heap:
                d, q = heapq.heappop(heap)
                if q in main: hit = q; break
                if d > dist.get(q, 1e9): continue
                for r in adj.get(q, ()):
                    if r not in full or (r not in prop and r not in main): continue
                    nd = d + 1
                    if nd < dist.get(r, 1e9): dist[r] = nd; prev[r] = q; heapq.heappush(heap, (nd, r))
            if hit is None: print('connect: no path for', o, s); continue
            q = prev.get(hit)
            while q is not None and q not in comp:
                changed.append((q, P['prov'][q]['state'], prop[q], o)); prop[q] = o; q = prev.get(q)
    return changed

COLONIAL = {'USA', 'MEX', 'TEX', 'ORG', 'HBC', 'ONT', 'QUE', 'GBR', 'NBS', 'NVS', 'ALK', 'SEQ'}

def smooth_tendrils(P, adj, van, prop, keep, rounds=6):
    """Native-to-native cleanup: a province that touches at most one province of its own owner but three or
    more land neighbours is a tendril tip or a one-province spur; it goes to the native owner holding most of
    its neighbours. Colonial owners and the Indian Territory (deliberate corridors and footholds) are left alone."""
    changed = []
    for _ in range(rounds):
        full = dict(van); full.update(prop); moved = False
        for p in sorted(prop):
            o = prop[p]
            if o in COLONIAL or p in keep: continue
            nb = [full[q] for q in adj.get(p, ()) if q in full]
            if len(nb) < 3 or nb.count(o) > 1: continue
            cand = Counter(x for x in nb if x != o and x not in COLONIAL)
            if not cand: continue
            new = cand.most_common(1)[0][0]
            prop[p] = new; full[p] = new; changed.append((p, P['prov'][p]['state'], o, new)); moved = True
        if not moved: break
    return changed

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

def render(P, own, path, title, box=(1180, 800, 2640, 1580), game=None, scale=1.0, lines=None, G=None):
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
    if lines and G:
        ly = 40
        for label, colour, pts in lines:
            lon = np.array([q[0] for q in pts]); lat = np.array([q[1] for q in pts])
            # densify so the polynomial projection bends long segments correctly
            dl = [np.linspace(0, 1, 12)[:-1] for _ in range(len(pts) - 1)]
            lon = np.concatenate([lon[i] + (lon[i + 1] - lon[i]) * s for i, s in enumerate(dl)] + [lon[-1:]])
            lat = np.concatenate([lat[i] + (lat[i + 1] - lat[i]) * s for i, s in enumerate(dl)] + [lat[-1:]])
            x, y = G.proj(lon, lat); x = x - X0; y = y - Y0
            for i in range(len(x) - 1):
                if i % 2 == 0: d.line([(x[i], y[i]), (x[i + 1], y[i + 1])], fill=colour, width=4)
            d.line([(14, ly + 8), (44, ly + 8)], fill=colour, width=4)
            d.text((52, ly), label, fill=(0, 0, 0), font=f, stroke_width=2, stroke_fill=(255, 255, 255)); ly += 20
    if scale != 1.0: img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    img.save(path, optimize=True)

def draft_states(P, prop, van, blocks):
    lines = ['# DRAFT, not loaded by the game. Proposed North America splits for common/history/states.',
             '# Generated by .claude/docs/usa_1836_borders/tools/build.py. Homelands and vanilla claims are copied unchanged;',
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
    ap.add_argument('--variant', default='corridor', choices=sorted(CC.VARIANTS))
    a = ap.parse_args(); os.makedirs(a.work, exist_ok=True); os.makedirs(a.out, exist_ok=True)
    CC.VARIANTS[a.variant](CC.R)
    P = load_provinces(a.game, a.work)
    G = Georef(a.game, a.work, P)
    print('georeference: %d towns, median error %.1f px, 90th pct %.1f px; coastline median %.1f px' % G.stats)
    van, blocks = vanilla_owners(a.game, P['regions'])
    prop, why = classify(P, G)
    adj = load_adjacency(a.game, a.work)
    for p, s, o, n in connect_blocks(P, adj, van, prop, CC.CONNECT): print(f'connect: {p} in {s[6:]} {o} -> {n}')
    for p, s, o, n in smooth_tendrils(P, adj, van, prop, set(why)): print(f'tendril: {p} in {s[6:]} {o} -> {n}')
    changed, flagged = enforce_contiguity(P, adj, van, prop, set(why))
    for p, s, o, n in changed: print(f'contiguity: {p} in {s[6:]} {o} -> {n}')
    for o, n, s in flagged: print(f'detached block for review: {o}, {n} provinces, {s[6:]}')
    full = dict(van); full.update(prop)
    NA = (150, 0, 2900, 1600)
    render(P, van, os.path.join(a.out, 'map_vanilla.png'), 'Vanilla 1836 ownership', game=a.game)
    render(P, full, os.path.join(a.out, 'map_proposed.png'), 'Proposed: actual control, 1 Jan 1836', game=a.game)
    render(P, van, os.path.join(a.out, 'map_vanilla_na.png'), 'Vanilla 1836 ownership', box=NA, game=a.game, scale=0.6)
    render(P, full, os.path.join(a.out, 'map_proposed_na.png'), 'Proposed: actual control, 1 Jan 1836', box=NA, game=a.game, scale=0.6)
    render(P, full, os.path.join(a.out, 'map_proposed_na_borders.png'), 'Proposed control with 1836 colonial boundaries', box=NA, game=a.game, scale=0.6, lines=CC.HISTORIC_LINES, G=G)
    open(os.path.join(a.out, 'draft_states_north_america.txt'), 'w', encoding='utf-8-sig').write(draft_states(P, prop, van, blocks))
    rows = []
    for s in CC.R:
        ps = P['regions'][s]['provinces']
        f = lambda c: ', '.join(f'{k} {c[k]}' for k in sorted(c, key=lambda k: (-c[k], k)))
        rows.append(f"| {s[6:]} | {len(ps)} | {f(Counter(van[p] for p in ps))} | {f(Counter(prop[p] for p in ps))} |")
    fh = [f'| {name} | {s[6:]} | {o} | {p} |' for p, name in why.items() for s, o in [(P['prov'][p]['state'], prop[p])]]
    open(os.path.join(a.out, 'summary.md'), 'w').write('| State | Provinces | Vanilla | Proposed |\n|---|---|---|---|\n' + '\n'.join(rows)
        + '\n\n| Foothold | State | Owner | Province |\n|---|---|---|---|\n' + '\n'.join(fh) + '\n')
    pickle.dump({'prop': prop, 'van': van, 'why': why}, open(os.path.join(a.work, f'classified_{a.variant}.pkl'), 'wb'))
    print('wrote', a.out)

if __name__ == '__main__':
    main()
