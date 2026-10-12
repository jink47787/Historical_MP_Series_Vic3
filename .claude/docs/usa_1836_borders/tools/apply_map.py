"""Write the proposed North America splits into the mod's state history.

Copies vanilla common/history/states/00_states.txt to the mod and, for each state
in draft_states_north_america.txt, changes only what the proposal changes:
- a vanilla split whose provinces are unchanged keeps its vanilla text;
- a changed split keeps its place, its state_type and vanilla's province order;
- splits for new owners go after the vanilla ones;
- homelands and claims keep their vanilla text, new claims are added at the end.

python3 -I apply_map.py --game <basegame-ver> --draft ../draft_states_north_america.txt --mod "../../../../Historical MP Series"
"""
import argparse, os, re

PROV = re.compile(r'x[0-9A-Fa-f]{6}')
PER_LINE = 16


def close(text, i):
    """Index just past the brace that closes the '{' at text[i]."""
    depth = 0
    while True:
        c = text[i]
        if c == '#':
            i = text.index('\n', i)
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1


def blocks(text):
    """Map STATE_X -> (start, end) of each 's:STATE_X = { ... }' block."""
    out = {}
    for m in re.finditer(r'^[ \t]*s:(STATE_\w+)\s*=\s*\{', text, re.M):
        out[m.group(1)] = (m.start(), close(text, m.end() - 1))
    return out


def splits(block):
    """[(start, end, country, [provinces], body)] for each create_state in a state block."""
    out = []
    for m in re.finditer(r'create_state\s*=\s*\{', block):
        e = close(block, m.end() - 1)
        body = block[m.start():e]
        country = re.search(r'country\s*=\s*c:(\w+)', body).group(1)
        po = re.search(r'owned_provinces\s*=\s*\{([^}]*)\}', body)
        out.append((m.start(), e, country, [p.upper().replace('X', 'x', 1) for p in PROV.findall(po.group(1))], body))
    return out


def split_text(country, provs, extra):
    lines = [' '.join(provs[i:i + PER_LINE]) for i in range(0, len(provs), PER_LINE)]
    t = f'create_state = {{\n\t\t\tcountry = c:{country}\n\t\t\towned_provinces = {{\n'
    t += ''.join(f'\t\t\t\t{l}\n' for l in lines)
    t += '\t\t\t}\n' + ''.join(f'\t\t\t{x}\n' for x in extra) + '\t\t}'
    return t


def rebuild(vblock, dblock):
    vs, ds = splits(vblock), splits(dblock)
    owner = {p: c for _, _, c, ps, _ in ds for p in ps}
    order = {}
    for _, _, _, ps, _ in vs:
        for p in ps:
            order.setdefault(p, len(order))
    if set(order) != set(owner):
        raise SystemExit('province sets differ')
    want = {}
    for p in sorted(owner, key=order.get):
        want.setdefault(owner[p], []).append(p)

    parts, seen = [], set()
    for _, _, c, ps, body in vs:
        if c in seen or c not in want:
            continue
        seen.add(c)
        if ps == want[c]:
            parts.append(body)
        else:
            extra = [l.strip() for l in body.splitlines() if re.match(r'\s*state_type\s*=', l)]
            parts.append(split_text(c, want[c], extra))
    for _, _, c, _, body in ds:
        if c not in seen:
            seen.add(c)
            extra = [l.strip() for l in body.splitlines() if re.match(r'\s*state_type\s*=', l)]
            parts.append(split_text(c, want[c], extra))

    head = vblock[:vs[0][0]]
    tail = vblock[vs[-1][1]:]
    old = set(re.findall(r'add_claim\s*=\s*c:(\w+)', tail))
    new = [c for c in re.findall(r'add_claim\s*=\s*c:(\w+)', dblock) if c not in old]
    if new:
        k = tail.rindex('}')
        tail = tail[:k].rstrip('\t ') + ''.join(f'\t\tadd_claim = c:{c}\n' for c in new) + '\t' + tail[k:]
    if sorted(re.findall(r'add_homeland\s*=\s*cu:(\w+)', vblock)) != sorted(re.findall(r'add_homeland\s*=\s*cu:(\w+)', dblock)):
        raise SystemExit('homelands differ')
    return head + '\n\t\t'.join(parts) + tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', required=True)
    ap.add_argument('--draft', required=True)
    ap.add_argument('--mod', required=True)
    a = ap.parse_args()

    vt = open(os.path.join(a.game, 'common/history/states/00_states.txt'), encoding='utf-8-sig').read()
    dt = open(a.draft, encoding='utf-8-sig').read()
    vb, db = blocks(vt), blocks(dt)
    missing = sorted(set(db) - set(vb))
    if missing:
        raise SystemExit(f'not in vanilla: {missing}')

    out, pos = [], 0
    for st, (s, e) in sorted(vb.items(), key=lambda kv: kv[1][0]):
        if st not in db:
            continue
        out.append(vt[pos:s])
        out.append(rebuild(vt[s:e], dt[slice(*db[st])]))
        pos = e
    out.append(vt[pos:])

    dst = os.path.join(a.mod, 'common/history/states/00_states.txt')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', encoding='utf-8-sig', newline='\n') as f:
        f.write(''.join(out))
    print(f'replaced {len(db)} states -> {dst}')


if __name__ == '__main__':
    main()
