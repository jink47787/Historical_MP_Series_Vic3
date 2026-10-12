"""Build the drop-in mod package for the 1836 North America proposal.

Writes, under <out>/<variant>/, the files to copy into 'Historical MP Series/':
  common/history/states/00_states.txt         vanilla file with the North American states replaced
  common/history/pops/05_north_america.txt    vanilla file with those states' pops rebuilt
  common/cultures, discrimination_traits, discrimination_trait_groups, country_definitions,
  common/history/countries, common/history/population, coat_of_arms, flag_definitions, static_modifiers,
  gfx/coat_of_arms/textured_emblems (via flags.py), localization/english (+ replace/english for CSC)
and <out>/<variant>/PACKAGE.md with the pop table and the manual follow-ups.

Pops, per state in the province table:
  1. Settler pops (non-indigenous cultures, Metis included) stay with their vanilla owner if it still holds part
     of the state; otherwise SETTLER_MOVES says where they go.
  2. A colonial owner keeps a share of its vanilla indigenous pops equal to the share of its vanilla provinces it
     still holds, unless RESIDENTS says otherwise (absolute sizes or fractions per culture).
  3. New and reused tags get the period populations in natives_1836.PEOPLES.
  4. The rest of the state's vanilla indigenous population is shared among the vanilla native tags that now hold
     land there, in proportion to provinces held (the part matching the new tags' land is replaced by step 3).
     A tag takes pops of its own cultures first; others are converted to its main culture.
  5. Vanilla native tags listed in natives_1836.VANILLA_TARGETS have their indigenous pops in these states scaled to
     the c. 1836 estimate, so they sit on the same scale as the new tags.

    python3 -I package.py --game <basegame> --owners <provinces csv> --draft <draft states> --out <dir> [--variant corridor|plus6]
"""
import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import natives_1836 as N


# Minimal Paradox script reader: a block is a list of (key, value) pairs, with key None for bare values.
def _tokens(text):
    text = re.sub(r'#[^\n]*', '', text)
    return re.findall(r'"[^"]*"|[{}]|[<>!?]?=|[<>]|[^\s{}=<>!?]+', text)


def parse(text):
    toks = _tokens(text)
    i = 0

    def block():
        nonlocal i
        out = []
        while i < len(toks):
            tok = toks[i]
            if tok == '}':
                i += 1
                return out
            if i + 1 < len(toks) and toks[i + 1] in ('=', '?=', '<=', '>=', '!=', '<', '>'):
                i += 2
                if toks[i] == '{':
                    i += 1
                    out.append((tok, block()))
                else:
                    out.append((tok, toks[i]))
                    i += 1
            elif tok == '{':
                i += 1
                out.append((None, block()))
            else:
                out.append((None, tok))
                i += 1
        return out
    return block()


def get(blk, key):
    return [v for k, v in blk if k == key]


def load_owners(path):
    """The map session's province table: province, state, vanilla owner, proposed owner (CSV with a header row).
    Returns (states in file order -> provinces, proposed owner by province, vanilla owner by province)."""
    states, prop, van = {}, {}, {}
    with open(path, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            p, s = row['province'].strip(), row['state'].strip()
            states.setdefault(s, []).append(p)
            van[p] = row['vanilla_owner'].strip()
            prop[p] = row['proposed_owner'].strip()
    return states, prop, van

INDIGENOUS = {'dakota', 'cherokee', 'muskogean', 'cree', 'siouan', 'comanche', 'caddoan', 'apache',
              'pueblo', 'inuit', 'navajo', 'athabaskan', 'salish', 'nez_perce', 'algonquian', 'iroquoian', 'paiute',
              'hokan', 'oodham'} | set(N.CULTURES)
COLONIAL = {'USA', 'MEX', 'TEX', 'ORG', 'HBC', 'ONT', 'QUE', 'GBR', 'NBS', 'NVS', 'ALK'}
SETTLER = {'USA': 'yankee', 'MEX': 'mexican', 'TEX': 'dixie', 'ORG': 'yankee', 'HBC': 'anglo_canadian',
           'ONT': 'anglo_canadian', 'QUE': 'franco_canadian', 'GBR': 'anglo_canadian', 'NBS': 'franco_canadian'}
# Great Lakes Algonquians held by colonial owners are Anishinaabe (Mississauga, Odawa, Saginaw and Grand River bands)
REMAP = {s: {'algonquian': 'anishinaabe'} for s in
         ('STATE_ONTARIO', 'STATE_QUEBEC', 'STATE_MICHIGAN', 'STATE_MINNESOTA', 'STATE_WISCONSIN', 'STATE_MANITOBA')}

# (state, colonial owner) -> {culture: fraction (<= 1) or absolute size (> 1)}; unlisted cultures use the province share
RESIDENTS = {
    ('STATE_ONTARIO', 'ONT'): {'iroquoian': 1.0, 'algonquian': 1.0, 'cree': 0},   # Six Nations, Mississauga
    ('STATE_ONTARIO', 'HBC'): {'siouan': 0},                                      # home-guard Cree at Moose and Albany
    ('STATE_QUEBEC', 'QUE'): {'cree': 0},
    ('STATE_QUEBEC', 'HBC'): {'inuit': 0},
    ('STATE_NEWFOUNDLAND', 'GBR'): {'inuit': 400},                                # southern Labrador
    ('STATE_MANITOBA', 'HBC'): {'siouan': 0, 'athabaskan': 0, 'cree': 600},       # Peguis's band and Cree at Red River
    ('STATE_MICHIGAN', 'USA'): {'siouan': 0},
    ('STATE_IOWA', 'USA'): {'dakota': 0},
    ('STATE_CALIFORNIA', 'MEX'): {'hokan': 15000},                                # ex-mission and rancho Indians (Cook)
    ('STATE_NEW_MEXICO', 'MEX'): {'pueblo': 1.0},                                 # the Pueblos are in the MEX valley
    ('STATE_ARIZONA', 'MEX'): {'oodham': 8000, 'pueblo': 0},                      # core: the O'odham belt is MEX
    ('STATE_WASHINGTON', 'ORG'): {'nez_perce': 0},
    ('STATE_OREGON', 'ORG'): {'paiute': 0, 'nez_perce': 0},
    ('STATE_BRITISH_COLUMBIA', 'ORG'): {'athabaskan': 0},
}
RESIDENTS_PLUS6 = {('STATE_ARIZONA', 'MEX'): {'oodham': 500, 'pueblo': 0}}       # Tucson, San Xavier, Tubac

# (state, vanilla owner) whose settlers move: {culture or '*': (state, new owner, keep, convert_to)}
SETTLER_MOVES = {
    ('STATE_COLORADO', 'MEX'): {'*': ('STATE_NEW_MEXICO', 'MEX', 0, None)},
    ('STATE_IDAHO', 'ORG'): {'*': ('STATE_OREGON', 'ORG', 0, None)},
    ('STATE_COLORADO', 'USA'): {'*': ('STATE_MISSOURI', 'USA', 0, None)},          # Santa Fe and Bent's Fort traders
    ('STATE_BRITISH_COLUMBIA', 'HBC'): {'*': ('STATE_WASHINGTON', 'ORG', 0, None)},      # Fort Vancouver and Nisqually
    ('STATE_BRITISH_COLUMBIA', 'ORG'): {'anglo_canadian': ('STATE_WASHINGTON', 'ORG', 500, None)},  # Fort Langley keeps 500
    ('STATE_QUEBEC', 'HBC'): {'*': ('STATE_QUEBEC', 'QUE', 300, None)},          # King's Posts and Ottawa valley
    ('STATE_ONTARIO', 'HBC'): {'anglo_canadian': ('STATE_ONTARIO', 'ONT', 300, None),
                               'metis': ('STATE_ONTARIO', 'CTF', 1000, None)},     # Great Lakes Metis
    ('STATE_MAINE', 'USA'): {'anglo_canadian': ('STATE_MAINE', 'NBS', 13500, 'franco_canadian')},  # Madawaska, 2,500
    ('STATE_ALBERTA', 'HBC'): {'metis': ('STATE_ALBERTA', 'IRC', 0, None),       # plains Metis, allied with the Cree
                               'anglo_canadian': (None, None, 0, None)},
    ('STATE_SASKATCHEWAN', 'HBC'): {'metis': ('STATE_SASKATCHEWAN', 'IRC', 0, None),
                                    'anglo_canadian': (None, None, 0, None)},
}
CULTURE_OVERRIDE = {('STATE_KANSAS', 'SEQ'): 'algonquian'}   # emigrant Shawnee, Delaware, Kickapoo and Potawatomi
MIN_COLONIAL = 500


def blocks_of(text, key_re):
    """Yield (name, start, end) for top-level-ish 'key = { ... }' blocks matching key_re."""
    for m in re.finditer(key_re, text):
        i = text.index('{', m.end() - 1) + 1
        d = 1
        j = i
        while d:
            c = text[j]
            d += (c == '{') - (c == '}')
            j += 1
        yield m.group(1), m.start(), j


def vanilla_pops(game):
    t = open(os.path.join(game, 'common/history/pops/05_north_america.txt'), encoding='utf-8-sig').read()
    h = parse(t)
    out = defaultdict(list)          # state -> [(owner, {culture, size, religion?, ...})]
    for k, v in get(h, 'POPS')[0]:
        for rk, rv in v:
            if not (rk or '').startswith('region_state:'):
                continue
            for cp in get(rv, 'create_pop'):
                out[k[2:]].append((rk[13:], {kk: vv for kk, vv in cp}))
    return t, out


def vanilla_tag_cultures(game):
    t = parse(open(os.path.join(game, 'common/country_definitions/00_countries.txt'), encoding='utf-8-sig').read())
    return {k: [x for _, x in get(v, 'cultures')[0]] for k, v in t if get(v, 'cultures')}


def size(p):
    return int(p['size'])


def build_pops(variant, STATES, prop, van, game):
    peoples = N.peoples_for(variant)
    residents = dict(RESIDENTS)
    if variant == 'plus6':
        residents.update(RESIDENTS_PLUS6)
    vt, vp = vanilla_pops(game)
    tagcult = vanilla_tag_cultures(game)
    for s, lst in vp.items():           # a vanilla tag's culture set includes the cultures of its vanilla pops
        for o, p in lst:
            tagcult.setdefault(o, [])
            if p['culture'] not in tagcult[o]:
                tagcult[o].append(p['culture'])
    for t, d in N.tags_for(variant).items():
        tagcult[t] = list(d['cultures'])
    new_tags = set(peoples)
    out = defaultdict(lambda: defaultdict(Counter))   # state -> owner -> (culture, religion) -> size
    notes = []
    newc = defaultdict(Counter)
    vanc = defaultdict(Counter)
    for s in STATES:
        for p in STATES[s]:
            newc[s][prop[p]] += 1
            vanc[s][van[p]] += 1

    def add(s, o, cul, rel, n):
        if n > 0:
            out[s][o][(cul, rel)] += int(round(n))

    for s in STATES:
        pool = Counter()
        for o, p in vp.get(s, []):
            cul, rel, n = p['culture'], p.get('religion'), size(p)
            if cul not in INDIGENOUS:                                   # 1. settlers
                mv = SETTLER_MOVES.get((s, o), {})
                rule = mv.get(cul) or mv.get('*')
                if rule:
                    ds, do, keep, conv = rule
                    if keep and newc[s][o]:
                        add(s, o, cul, rel, min(keep, n))
                    rest = n - (min(keep, n) if newc[s][o] else 0)
                    if ds is None:
                        notes.append(f'dropped {rest} {cul} of {o} in {s[6:]} (no post left)')
                    elif do == '@native':
                        tgt = max((t for t in newc[ds] if t not in COLONIAL), key=lambda t: newc[ds][t])
                        add(ds, tgt, cul, rel, rest)
                        notes.append(f'{rest} {cul} of {o} in {s[6:]} -> {tgt}')
                    else:
                        add(ds, do, conv or cul, rel, rest)
                        notes.append(f'{rest} {cul} of {o} in {s[6:]} -> {do} in {ds[6:]}' + (f' as {conv}' if conv else ''))
                elif newc[s][o]:
                    add(s, o, cul, rel, n)
                else:
                    raise SystemExit(f'no rule for {n} {cul} of {o} in {s}: {o} no longer holds any of it')
                continue
            if o in COLONIAL:                                           # 2. colonial residents
                f = min(1.0, newc[s][o] / vanc[s][o]) if vanc[s][o] else 0
                r = residents.get((s, o), {}).get(cul, f)
                keep = r if r > 1 else n * r
                keep = min(keep, n) if r <= 1 else r
                cul2 = REMAP.get(s, {}).get(cul, cul)
                if newc[s][o]:
                    add(s, o, cul2, rel, keep)
                    pool[cul] += max(0, n - keep)
                else:
                    pool[cul] += n
                continue
            pool[cul] += n
        for (ss, o), d in residents.items():                            # absolute residents not present in vanilla
            if ss == s and newc[s][o]:
                for cul, r in d.items():
                    if r > 1 and not any(k[0] == REMAP.get(s, {}).get(cul, cul) for k in out[s][o]):
                        add(s, o, cul, None, r)
        for t, by_state in peoples.items():                             # 3. new and reused tags
            for cul, n in by_state.get(s, []):
                if not newc[s][t]:
                    raise SystemExit(f'{t} has a population in {s} but no land there')
                add(s, t, cul, None, n)
        natives = {t: c for t, c in newc[s].items() if t not in COLONIAL}
        old = {t: c for t, c in natives.items() if t not in new_tags}
        for t in natives:
            if t in new_tags and t not in {x for x in peoples if s in peoples[x]}:
                raise SystemExit(f'{t} holds {natives[t]} provinces in {s} but has no population there')
        if not old:
            if pool:
                notes.append(f'{s[6:]}: {int(sum(pool.values()))} vanilla indigenous pops replaced by period figures')
            continue
        share = sum(old.values()) / sum(natives.values())             # 4. vanilla native tags
        if share < 1:
            notes.append(f'{s[6:]}: {int(sum(pool.values()) * (1 - share))} of {int(sum(pool.values()))} vanilla '
                         f'indigenous pops replaced by period figures for {", ".join(t for t in natives if t in new_tags)}')
        tot = sum(old.values())
        ov = {t: c for t, c in old.items() if (s, t) in CULTURE_OVERRIDE}
        rest = {t: c for t, c in old.items() if t not in ov}
        for t, c in ov.items():
            add(s, t, CULTURE_OVERRIDE[(s, t)], None, sum(pool.values()) * share * c / tot)
        k_rest = sum(rest.values())
        for cul, n in pool.items():
            if not k_rest:
                break
            n *= share * k_rest / tot
            takers = {t: c for t, c in rest.items() if cul in tagcult.get(t, [])}
            if takers:
                k = sum(takers.values())
                for t, c in takers.items():
                    add(s, t, cul, None, n * c / k)
            else:
                for t, c in rest.items():
                    add(s, t, tagcult[t][0], None, n * c / k_rest)
        for t in old:                                                   # a tag that only got other peoples' pops
            if not out[s][t]:
                add(s, t, CULTURE_OVERRIDE.get((s, t)) or tagcult[t][0], None, 500)
                notes.append(f'{t} in {s[6:]}: no vanilla pops to share, given 500')
    for s in STATES:                                                    # minimum for colonial footholds
        for o, c in newc[s].items():
            if o in COLONIAL and sum(out[s][o].values()) < MIN_COLONIAL:
                add(s, o, SETTLER[o], None, MIN_COLONIAL - sum(out[s][o].values()))
                notes.append(f'{o} in {s[6:]}: topped up to {MIN_COLONIAL} with {SETTLER[o]} (garrison and traders)')
        for o in newc[s]:
            assert out[s][o], (s, o)
    for t, target in N.vanilla_targets_for(variant).items():               # 5. vanilla native tags to period scale
        held = [(s, k) for s in out for k in out[s].get(t, {}) if k[0] in INDIGENOUS]
        total = sum(out[s][t][k] for s, k in held)
        if not total:
            notes.append(f'{t}: no indigenous pops in the proposal states, target {target:,} not applied')
            continue
        f = target / total
        for s, k in held:
            out[s][t][k] = max(1, int(round(out[s][t][k] * f)))
        notes.append(f'{t}: indigenous pops scaled from {total:,} to {target:,} (x{f:.2f}) to match c. 1836 estimates')
    return vt, vp, out, notes


def pops_text(vt, out):
    def state_block(s):
        L = [f'\ts:{s} = {{']
        for o in sorted(out[s], key=lambda o: (-sum(out[s][o].values()), o)):
            L.append(f'\t\tregion_state:{o} = {{')
            for (cul, rel), n in sorted(out[s][o].items(), key=lambda kv: -kv[1]):
                L.append('\t\t\tcreate_pop = {')
                L.append(f'\t\t\t\tculture = {cul}')
                if rel:
                    L.append(f'\t\t\t\treligion = {rel}')
                L.append(f'\t\t\t\tsize = {n}')
                L.append('\t\t\t}')
            L.append('\t\t}')
        L.append('\t}')
        return '\n'.join(L)
    done = set()
    res = []
    last = 0
    for name, a, b in blocks_of(vt, r's:(STATE_\w+)\s*=\s*\{'):
        if a < last:
            continue
        if name in out:
            res.append(vt[last:a])
            res.append(state_block(name).lstrip('\t'))
            last = b
            done.add(name)
    res.append(vt[last:])
    t = ''.join(res)
    missing = [s for s in out if s not in done]
    if missing:   # states with no vanilla pops block: append inside POPS
        k = t.rstrip().rfind('}')
        t = t[:k] + '\n'.join(state_block(s) for s in missing) + '\n' + t[k:]
    return t


def states_text(game, draft, variant):
    peoples = N.peoples_for(variant)
    homes = defaultdict(set)
    for t, by_state in peoples.items():
        for s, lst in by_state.items():
            for cul, _ in lst:
                if cul in N.CULTURES:
                    homes[s].add(cul)
    gen = {}
    for name, a, b in blocks_of(draft, r's:(STATE_\w+)\s*=\s*\{'):
        blk = draft[a:b]
        extra = ''.join(f'\t\tadd_homeland = cu:{c}\n' for c in sorted(homes.get(name, ())) if f'cu:{c}' not in blk)
        if extra:
            k = blk.rfind('}')
            blk = blk[:k].rstrip('\t') + extra + '\t' + blk[k:]
        gen[name] = blk
    vt = open(os.path.join(game, 'common/history/states/00_states.txt'), encoding='utf-8-sig').read()
    res, last = [], 0
    for name, a, b in blocks_of(vt, r's:(STATE_\w+)\s*=\s*\{'):
        if a < last:
            continue
        if name in gen:
            res += [vt[last:a], gen[name].lstrip('\t')]
            last = b
    res.append(vt[last:])
    assert all(f's:{s} = ' in ''.join(res) for s in gen)
    return ''.join(res)


def w(path, text, bom=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='\n') as f:
        f.write(text)


def country_files(root, variant):
    tags = N.tags_for(variant)
    cults = N.cultures_for(variant)
    hdr = '# 1836 North America proposal: generated by docs/usa_1836_borders/tools/package.py\n\n'
    # cultures
    L = [hdr]
    for c, d in cults.items():
        L.append(f'{c} = {{ # {d["why"]}')
        L.append(f'\tcolor = {d["color"]}\n\treligion = animist\n\theritage = {d["heritage"]}\n\tlanguage = {d["language"]}')
        L.append('\ttraditions = { }')
        L.append('\tmale_common_first_names = {\n\t\t' + ' '.join(d['male']) + '\n\t}')
        L.append('\tfemale_common_first_names = {\n\t\t' + ' '.join(d['female']) + '\n\t}')
        L.append('\tcommon_last_names = {\n\t\t' + ' '.join(d['last']) + '\n\t}')
        L.append('\tethnicities = {\n\t\t1 = native_american\n\t}\n\tgraphics = decentralised_americas\n}\n')
    w(f'{root}/common/cultures/HMPS_1836_native_cultures.txt', '\n'.join(L))
    langs = {l: g for l, g in N.LANGUAGES.items() if any(d['language'] == l for d in cults.values())}
    w(f'{root}/common/discrimination_traits/HMPS_1836_native_languages.txt',
      hdr + '\n'.join(f'{l} = {{\n\ttype = language\n\ttrait_group = {g}\n}}\n' for l, (g, _) in langs.items()))
    groups = {g for g, _ in langs.values() if g in N.NEW_LANGUAGE_GROUPS}
    if groups:
        w(f'{root}/common/discrimination_trait_groups/HMPS_1836_native_language_groups.txt',
          hdr + '\n'.join(f'{g} = {{\n\ttype = language\n}}\n' for g in sorted(groups)))
    # country definitions
    L = [hdr]
    for t, d in tags.items():
        col = d['color']
        if d.get('reuse'):
            L.append(f'INJECT:{t} = {{ # vanilla tag, unused at the 1836 start\n\tcolor = {{ {col[0]} {col[1]} {col[2]} }}\n'
                     f'\tcultures = {{ {" ".join(d["cultures"])} }}\n\tcapital = {d["capital"]}\n}}\n')
        else:
            L.append(f'{t} = {{ # {d["name"]}\n\tcolor = {{ {col[0]} {col[1]} {col[2]} }}\n\n\tcountry_type = decentralized\n\n'
                     f'\ttier = principality\n\n\tcultures = {{ {" ".join(d["cultures"])} }}\n\tcapital = {d["capital"]}\n}}\n')
    w(f'{root}/common/country_definitions/HMPS_1836_natives.txt', '\n'.join(L))
    w(f'{root}/common/history/countries/HMPS_1836_natives.txt', '﻿COUNTRIES = {\n' + ''.join(
        f'\tc:{t} ?= {{\n\t\teffect_starting_technology_tier_6_tech = yes\n\t\teffect_starting_politics_traditional = yes\n'
        f'\t\teffect_native_conscription_10 = yes\n\t}}\n' for t in tags) + '}\n', bom=False)
    w(f'{root}/common/history/population/HMPS_1836_natives.txt', '﻿POPULATION = {\n' + ''.join(
        f'\tc:{t} ?= {{\n\t\teffect_starting_pop_wealth_low = yes\n\t\teffect_starting_pop_literacy_baseline = yes\n\t}}\n'
        for t in tags) + '}\n', bom=False)
    # flags
    L = [hdr]
    for t, d in tags.items():
        for suffix in ('', '_subject'):
            L.append(f'{t}{suffix} = {{ # {d["flag"]}\n\tpattern = "pattern_solid.tga"\n\tcolor1 = "white"\n\n'
                     f'\ttextured_emblem = {{\n\t\ttexture = "te_hmps_{t.lower()}.dds"\n'
                     '\t\tinstance = { scale = { 1 1 } position = { 0.5 0.5 } }\n\t}\n}\n')
    w(f'{root}/common/coat_of_arms/coat_of_arms/HMPS_1836_natives.txt', '\n'.join(L))
    w(f'{root}/common/flag_definitions/HMPS_1836_natives.txt', hdr + '\n'.join(
        f'{t} = {{ # {d["name"]}\n\tflag_definition = {{\n\t\tcoa = {t}\n\t\tsubject_canton = {t}_subject\n'
        f'\t\tpriority = 1\n\t}}\n}}\n' for t, d in tags.items()))
    # secondary-culture modifiers (the HMPS system defines one pair per culture)
    w(f'{root}/common/static_modifiers/z_HMPS_1836_native_secondary_culture_modifiers.txt', hdr + ''.join(
        f'  REPLACE_OR_CREATE:secondary_culture_{c} = {{ icon = gfx/interface/population/pop_culture.dds country_{c}_cultural_acceptance_add =  20 }}\n'
        f'REPLACE_OR_CREATE:stigmatised_culture_{c} = {{ icon = gfx/interface/buttons/sort_button_icons/sort_icon_acceptance.dds country_{c}_cultural_acceptance_add = -20 }}\n'
        for c in cults))
    # localisation
    L = ['l_english:']
    for t, d in tags.items():
        if not d.get('reuse'):
            L += [f' {t}:0 "{d["name"]}"', f' {t}_ADJ:0 "{d["adj"]}"']
    for c, d in cults.items():
        L.append(f' {c}:0 "{c.replace("_", " ").title()}"')
        L.append(f'   secondary_culture_{c}:0 "Has {c.title()} as a [concept_secondary_culture]"')
        L.append(f' stigmatised_culture_{c}:0 "Has {c.title()} as a [concept_stigmatised_culture]"')
    for l, (g, name) in langs.items():
        L.append(f' {l}:0 "{name}"')
    for g in sorted(groups):
        L.append(f' {g}:0 "{N.NEW_LANGUAGE_GROUPS[g]}"')
    w(f'{root}/localization/english/HMPS_1836_natives_l_english.yml', '\n'.join(L) + '\n')
    rep = [f' {t}:0 "{d["name"]}"\n {t}_ADJ:0 "{d["adj"]}"' for t, d in tags.items() if d.get('reuse') and t == 'CSC']
    if rep:
        w(f'{root}/localization/replace/english/HMPS_1836_natives_replace_l_english.yml', 'l_english:\n' + '\n'.join(rep) + '\n')
    return tags, cults


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', required=True)
    ap.add_argument('--owners', required=True, help="the map session's province table for this variant (CSV)")
    ap.add_argument('--draft', required=True, help="the map session's draft_states_north_america.txt for this variant")
    ap.add_argument('--out', required=True)
    ap.add_argument('--variant', default='corridor', choices=['corridor', 'plus6'])
    a = ap.parse_args()
    root = os.path.join(a.out, 'core' if a.variant == 'corridor' else 'plus6')
    if os.path.isdir(root):
        shutil.rmtree(root)
    STATES, prop, van = load_owners(a.owners)
    draft = open(a.draft, encoding='utf-8-sig').read()
    tags, cults = country_files(root, a.variant)
    subprocess.run([sys.executable, '-I', os.path.join(HERE, 'flags.py'), '--out', root, '--preview',
                    os.path.join(root, 'flags_preview.png'), '--only', ','.join(tags)], check=True)
    vt, vp, out, notes = build_pops(a.variant, STATES, prop, van, a.game)
    w(f'{root}/common/history/pops/05_north_america.txt', pops_text(vt, out))
    w(f'{root}/common/history/states/00_states.txt', states_text(a.game, draft, a.variant))
    # report
    before = defaultdict(Counter)
    for s in STATES:
        for o, p in vp.get(s, []):
            before[o][p['culture']] += size(p)
    after = defaultdict(Counter)
    for s in out:
        for o in out[s]:
            for (cul, _), n in out[s][o].items():
                after[o][cul] += n
    R = [f'# 1836 North America package ({a.variant})', '',
         'Copy the folders here into `Historical MP Series/`. Generated by `docs/usa_1836_borders/tools/package.py`; '
         'do not edit by hand.', '', '## Population by owner (the states in the proposal only)', '',
         '| Owner | Vanilla | Proposed | Proposed by culture |', '|---|---:|---:|---|']
    for o in sorted(set(before) | set(after), key=lambda o: -sum(after[o].values())):
        R.append(f'| {o} | {sum(before[o].values()):,} | {sum(after[o].values()):,} | '
                 + ', '.join(f'{c} {n:,}' for c, n in after[o].most_common()) + ' |')
    R += ['', '## Population by state and owner', '', '| State | Owner | Pops |', '|---|---|---|']
    for s in STATES:
        for o in sorted(out[s], key=lambda o: -sum(out[s][o].values())):
            R.append(f'| {s[6:]} | {o} | ' + ', '.join(f'{c}{"/" + r if r else ""} {n:,}' for (c, r), n in
                                                   sorted(out[s][o].items(), key=lambda kv: -kv[1])) + ' |')
    R += ['', '## Moves and replacements', ''] + [f'- {n}' for n in notes]
    R += ['', '## Manual follow-ups', '',
          '- `common/on_actions/HMPS_secondary_cultures_onactions.txt`: add these lines to '
          '`HMPS_revolution_inherit_secondary_cultures_modifier` so revolutions inherit the new cultures:', '', '```']
    for c in cults:
        R.append(f'        if = {{ limit = {{ root = {{ has_modifier =   secondary_culture_{c} }} }} scope:target = {{ add_modifier =   secondary_culture_{c} }} }}')
        R.append(f'        if = {{ limit = {{ root = {{ has_modifier = stigmatised_culture_{c} }} }} scope:target = {{ add_modifier = stigmatised_culture_{c} }} }}')
    R += ['```', '',
          '- `common/history/buildings/HMPS_generated_buildings.txt` (owned by the history agent): building entries for '
          'owners that lose a whole state split need moving or removing; see PROPOSAL.md, Dependencies.', '',
          '## Sources for the period populations', ''] + [f'- {x}' for x in N.SOURCES]
    review = [c for c, d in cults.items() if d.get('review')]
    if review:
        R += ['', '## Needs review', '', f'- Name lists for {", ".join(review)} are short; the women\'s names especially.']
    w(f'{root}/PACKAGE.md', '\n'.join(R) + '\n', bom=False)
    print('wrote', root)
    for n in notes:
        print(' ', n)


if __name__ == '__main__':
    main()
