"""Write the proposed North America splits into the mod's state history.

Copies vanilla common/history/states/00_states.txt to the mod and replaces each
state block that draft_states_north_america.txt defines. Nothing else changes.

python3 -I apply_map.py --game <basegame-ver> --draft ../draft_states_north_america.txt --mod "../../../../Historical MP Series"
"""
import argparse, os, re


def blocks(text):
    """Map STATE_X -> (start, end) of each top-level 's:STATE_X = { ... }' block."""
    out = {}
    for m in re.finditer(r'^[ \t]*s:(STATE_\w+)\s*=\s*\{', text, re.M):
        depth, i = 0, m.end() - 1
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
                    break
            i += 1
        out[m.group(1)] = (m.start(), i + 1)
    return out


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
        ds, de = db[st]
        out.append(vt[pos:s])
        out.append(dt[ds:de])
        pos = e
    out.append(vt[pos:])

    dst = os.path.join(a.mod, 'common/history/states/00_states.txt')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', encoding='utf-8-sig', newline='\n') as f:
        f.write(''.join(out))
    print(f'replaced {len(db)} states -> {dst}')


if __name__ == '__main__':
    main()
