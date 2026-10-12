# Handoff: pops, cultures, flags and country files for the 1836 North America proposal

The map/borders session (session_01P6PeS9n3SxnkgNCjjuVqKh, repo jink47787/Historical_MP_Series_Vic3, unpushed branch claude/usa-borders-1836-proposal-onqxdg) has stopped working on this. This note is enough to pick it up in a new session.
Nothing is committed. Nothing in `Historical MP Series/` has been changed: all output is staged in `docs/usa_1836_borders/mod_package/` inside that session's container.
Source files relayed from that session are saved next to this note: `flags.py`, `natives_1836.py`, `package.py` (originally in `docs/usa_1836_borders/tools/`).

**Scope split (Dylan, 2026-10-11):** this thread owns population counts, cultures, flags and running `package.py`. The map session owns only the map. `package.py` no longer imports the map tools: it reads the map session's province table (`--owners`, CSV `province,state,vanilla_owner,proposed_owner`) and draft states file (`--draft`) for each variant. Run: `python3 -I package.py --game <basegame-ver> --owners <csv> --draft <draft_states_north_america.txt> --out <dir> --variant corridor|plus6`. Tag colours now live in `natives_1836.TAGS[*]['color']`.

## Decisions made
- **Reuse vanilla tags instead of new ones.** These are defined in vanilla `00_countries.txt` but unused at the 1836 start. They are changed with `INJECT:` (the mod's convention, see `HMPS_countries.txt`):
  - CTF (Council of Three Fires) replaces OJB.
  - CCM (O'odham Country) replaces ODH; capital moves to `STATE_ARIZONA`.
  - CSC (Cascadia) replaces NWC; English name overridden to "Northwest Coast" in `localization/replace`.
  - The map tools (`control_1836.py`, `build.py`) already use CTF, CSC and CCM.
- **New tags.**
  - Core: SFX, OSG, CLF, INU, INN.
  - plus6 also adds CHY, MHA, MNM and HCK, plus the reused CSC and CCM.
  - All are `country_type = decentralized`, `tier = principality`.
  - History is the vanilla native set: tech tier 6, traditional politics, native conscription 10, low wealth, baseline literacy.
- **New cultures.** Only where vanilla lumps clearly different peoples:
  - `anishinaabe`: vanilla `algonquian` has a Shawnee name list.
  - plus6 only: `cheyenne`, `wakashan`, `haida`, `tsimshian`. Vanilla `salish` has a Haida name list, so those names move to `haida`.
  - Existing vanilla cultures are kept for the rest: inuit, cree (for INN), algonquian (Sauk, Meskwaki, Menominee), siouan (Osage, Kansa, Ioway, Ho-Chunk, Mandan and Hidatsa), caddoan (Arikara), hokan (Californians and Yumans), oodham.
- **New languages:**
  - `language_anishinaabemowin` and `language_cheyenne`, in the existing group `language_group_algic`;
  - `language_wakashan`, `language_haida` and `language_tsimshianic`, each in a new group.
- **Flags.** Each is one full-flag textured emblem over `pattern_solid`:
  - format: 768×512 uncompressed A8R8G8B8 DDS, 1 mip, header identical to `gfx/coat_of_arms/textured_emblems/UFB_emblem.dds`;
  - file names: `te_hmps_<tag>.dds`;
  - each design uses a symbol the people used; the meanings are in the docstrings in `tools/flags.py` and `natives_1836.TAGS[*]['flag']`;
  - the colour round-trip has been verified.
- **Populations.**
  - New and reused tags get period estimates for c. 1836, per state, from `natives_1836.PEOPLES` and `PEOPLES_PLUS6` (sources are in `natives_1836.SOURCES`).
  - Vanilla native tags keep vanilla-scale numbers, which are often 2–4× the historical figures: the area each holds now gets the state's vanilla indigenous pool.
  - Colonial owners keep their settlers. Their native residents are scaled by the share of provinces they keep, unless a `RESIDENTS` override applies.
  - Moves are listed in `SETTLER_MOVES`.
  - The generator stops with an error on any settler pop it has no rule for.

## Files
- `tools/natives_1836.py`: data for cultures (with name lists), languages, tags, per-state populations and sources.
- `tools/package.py`: the generator. It writes `mod_package/<core|plus6>/` with:
  - cultures, languages and language groups;
  - country definitions, country and population history;
  - coat of arms, flag definitions, secondary-culture static modifiers and localisation;
  - full replacements of `common/history/states/00_states.txt` and `common/history/pops/05_north_america.txt`, with homelands added for the new cultures;
  - `PACKAGE.md`: population tables, moves, manual follow-ups and sources.
- `tools/flags.py`: draws the flags (`--out`, `--preview`, `--only TAG,TAG`).
- `flags_preview.png`: all 12 flags (still only in the map session's container).
- Run with `python3 -I package.py --game <basegame-ver> --work <work dir with provs.pkl and classified_<variant>.pkl> --out ../mod_package --variant corridor|plus6`.
  - `classified_<variant>.pkl` comes from `build.py --variant <variant>`, which writes it to the work dir.
  - Delete `tools/__pycache__` afterwards.

## Not finished
1. **Re-run both variants once the map session sends the final province tables** (smoke-tested on synthetic tables 2026-10-11; works). `package.py` already has its last fixes:
   - HBC's BC staff go to ORG in Washington (Fort Vancouver);
   - the Alberta and Saskatchewan Métis go to IRC;
   - the notes print integers.
   The files in `mod_package/` predate those fixes. `package.py` imports `build.py`, `control_1836.py` and `pdx.py` from the map tools, and these are not committed yet. Ask the map session if you need them.
2. **Name lists to review:** `wakashan` has one woman's name (Homiskanis) and `tsimshian` has two. They need sourced names.
3. **Manual patches**, listed in `PACKAGE.md`:
   - two lines per new culture in `common/on_actions/HMPS_secondary_cultures_onactions.txt`;
   - in `HMPS_generated_buildings.txt` (owned by the history agent), buildings for owners that lose a whole state split.
4. **Not loaded in-game yet.** Check the error log for culture, language, CoA or flag definitions and for `region_state` errors.
5. **Open decision for Dylan:** core or plus6.
6. **Decided (Dylan, 2026-10-11): scale vanilla native tags down** to c. 1836 estimates. Done in `natives_1836.VANILLA_TARGETS` and step 5 of `package.build_pops`. SEQ and SML are left at vanilla (removal-era tags; see the five-tribes proposal).

Do not commit or push. Dylan's never-commit-without-permission rule applies.

## Status at hand-off to a local session (2026-10-12)
- `natives_1836.py`: vanilla native tags scale down to c. 1836 targets (`VANILLA_TARGETS`). Comanche was lowered to 25,000 after a source check; Blackfoot, Assiniboine, Navajo and Sioux figures were checked against published estimates (notes beside each target).
- `package.py`: no longer needs the map tools. It was smoke-tested end to end on synthetic province tables for both variants.
- Waiting on: the map session's final province table CSV (`province,state,vanilla_owner,proposed_owner`, every province in all 34 regions) and `draft_states_north_america.txt` for each variant. Then run `package.py` for both variants and report the population table to Dylan.
- Still open for Dylan: core or plus6; the Wakashan and Tsimshian name lists need sourced names.
- Needs Python 3 with Pillow (flags) on the device. `--game` should point at the repo's `basegame-ver`.
- Nothing is committed. Never commit or push without Dylan's explicit permission.
