# HMPS modding notes

Suggestions for anyone (human or AI assistant) working on the Historical MP Series. They are conventions and design principles the mod follows, not hard rules. When in doubt, ask in the team chat.

## File and syntax conventions
- **UTF-8 with BOM.** Every mod file (.txt, .yml, .gui, .gfx, .asset, .info, ...) starts with the bytes EF BB BF. Keep the BOM when editing. Some editors and tools drop it, so check after saving. (PowerShell 5.1 `Set-Content -Encoding utf8` and Python `encoding='utf-8-sig'` write it.)
- **Extend existing HMPS files.** Put changes into the existing file with `INJECT:` (additive; negatives allowed) or `REPLACE:`. Create a new file only for genuinely new content (new goods or buildings) or when a vanilla file must be copied; follow HMPS naming (`*_HMPS.txt`, `HMPS_NN_*`, `REPLACE_HMPS_*`).
- **No backups or archives inside the mod folder.** No `_archive*` or `*backup*` folders and no `*.bak` / `*.before_*` files; the game can load them and they get committed by accident. Keep backups outside the repo.
- **`basegame-ver/` is a stale vanilla copy.** Check keys and values against the installed game, not against it.
- **Verify syntax online.** Confirm any script key, trigger, effect, modifier or define you are unsure of on the Paradox forums, the Vic3 modding wiki or other mods, plus real usage in vanilla. The bundled script docs are sometimes wrong or outdated.
- **Load order follows file names** (vanilla and mod merged, sorted by name), and the building list shows buildings in that order. That is why `building_quarry` lives at the end of `common/buildings/03_mines_HMPS.txt` and Builders’ Yards in `common/buildings/01_industry_HMPS_yards.txt`.
- **New goods and buildings need hand-declared modifiers.** `goods_input_X_add`, `goods_output_X_add` and `building_X_throughput_add` go in `common/modifier_type_definitions`; vanilla goods already have them. New goods also need a named colour and a texticon in `gui/`.
- **State region files:** the first state in each file has a BOM, so match `^﻿?STATE_` in scripts.

## Names and numbers
- **"Construction" means the construction sector** (`building_construction_sector`: Foundations, Fittings, Site Machinery), not Builders’ Yards (`building_materials_works`).
- **PM display names: 20 characters or fewer.** Longer names overlap the input icons in the PM panel. Keep group names short too.
- **No ASCII apostrophe in localised names.** The game wraps names in single quotes in tooltips, so `'` breaks them. Use the typographic ’ as vanilla does.
- **Worker counts use vanilla steps:** multiples of 250, or 50 / 100 / 150 / 200. Avoid values like 75, 125, 225, 950, 1125, 1875.
- **Goods and pollution values are multiples of 5.** Construction points stay decimal.
- **Every non-default PM has its own unlock tech** within a building. No regional PMs or regional start differences.

## PM design principles
- **Tiers raise value added (VA) per level** and output per worker as techs unlock; inputs grow too, jobs shift from laborers to machinists and engineers, pollution rises. Vanilla steel is the model (VA 750 / 1200 / 1500 / 1700).
- **VA per level = sum(output x price) - sum(input x price).** A level employs about 5000 jobs. Rough targets: tier 1 about 575-600, tier 2 about 850-900, tier 3 about 1300-1350, top tier up to about 2000. Vanilla iron mine: 600 / 900 / 1350 / 2000. Processing buildings keep a lower margin (inputs 50-60% of output value at tier 1); extraction 0-25%.
- **Step sizes follow history.** A transformative innovation (Hoffmann kiln, pneumatic rock drill, dynamite, steam shovel) gets a big jump; a niche or incremental one gets a small or late one. Use the VA targets as a sanity range.
- **Quality shows as more output.** The game has no quality effects (except company prestige goods), so a better method means more output.
- **Construction is balanced by goods cost per construction point**, not VA: at default methods, match vanilla per era (about 1000 / 720 / 540 / 527 per point). Upgrades buy extra points at a somewhat higher cost per point.
- **Building materials have two separate demands:** per construction point in the construction sector, and a flat per-level upkeep on urban buildings. Don't double count.
- **Labour-saving methods never add output or construction points.** Automation, handling, haulage, crushing and site machinery add inputs and cut jobs. Check every combination of methods so no job count goes below zero.
- **Adding an input to an existing PM:** cut other inputs (multiples of 5) so VA stays level; raise an output only if no cut works.
- **Inputs follow the technology:** tools, then coal (steam), then oil or electricity (late), plus explosives or engines only where real. Transportation input only from railways.
- **Mirror vanilla group structure** for resource buildings (equipment tiers, blasting, processing, haulage) and reuse vanilla PMs where they fit. Idle methods have no effects; in two-line buildings only one line has an idle method, listed first.
- **After any PM change, audit VA with vanilla and every mod `INJECT:` / `REPLACE:` merged.** Other files change vanilla PMs too (e.g. upkeep offsets), so a one-file audit misses them. Also check that every PM is defined, has textures and localisation, and that techs exist.
- **Removed content:** sand and the separate bricks/concrete goods were merged into `building_materials`; don't reintroduce them without discussing it.

## Starting history
- **History is generated, not hand-edited.** The maintainer regenerates the starting buildings (mainly `common/history/buildings/HMPS_generated_buildings.txt`) with a script, run through the history agent (`.claude/agents/history-agent.md`, used only on request). Hand edits there can be overwritten by the next pass, so send history changes to the maintainer. Claude Code warns you if you try to edit history.
- **Place starting buildings by the real 1836 distribution of production:** which countries and regions really made the good, and roughly how much, not evenly or by resource availability alone.
- **Never assume imports at the start.** Many markets have no trade access in 1836, so each market (customs unions and subjects that share the overlord's market pooled together) should supply its own inputs. If a market lacks an input, place a domestic producer within state caps rather than relying on imports.
- **Stone prices by 1836 stone class:** stone-rich markets start cheap (about -20%), mixed around 0, stone-poor (brick-building plains and deltas) dearer (+25..+50%). Demand decides how many quarry levels; documented 1836 quarrying districts decide where.
- **Quarry caps follow geology only;** see `Historical MP Series/quarry_cap_proposal.md`.
