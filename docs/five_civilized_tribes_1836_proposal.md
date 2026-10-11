# Proposal: Five Civilized Tribes flavor (1836 start)

Status: proposal for discussion. Nothing here is implemented yet.

## Summary

At the 1836 start the Five Civilized Tribes (Cherokee, Muscogee/Creek, Choctaw, Chickasaw, Seminole) are at the turning point of removal. Vanilla only covers two of the five: the Cherokee (`je_indian_removal` plus the Trail of Tears chain in `events/native_resettlement.txt`) and the Seminole (`je_seminole_wars`). This proposal adds a short chain for each nation and plugs it into the vanilla chain. We do not replace the vanilla journal entry or events. Instead the new events read the variables and modifiers that vanilla already sets. The result is one removal story for the USA, and a "rebuilding in the West" journal entry for the Indian Territory (`SEQ`).

Design goals:
- **Historical timing.** Vanilla removal starts in early 1836, about two years early. New Echota, ratified in May 1836, gave a two-year deadline, and the Cherokee Trail of Tears ran in 1838–39.
- **Cover the gaps.** Vanilla never removes the 22,240 Creeks in Alabama, and it says nothing about the Choctaw, the Chickasaw or life in the Indian Territory after arrival.
- **MP-safe.** Effects stay small. The historical choice is always the default option. No new history or pop changes. Nothing that a player USA can farm, and nothing that cripples it.
- **Vanilla-patch-proof.** No `REPLACE:` of vanilla events or `je_indian_removal`. Only new events, one new JE, and listening to vanilla state.

## Where we stand in 1836 (game and history)

| Nation | History, 1836 | In the game today |
|---|---|---|
| Cherokee | Treaty of New Echota signed 29 Dec 1835 by the Ridge "Treaty Party"; Senate ratifies 23 May 1836 by one vote; removal deadline 23 May 1838. John Ross's National Council rejects it (petition of ~15,000 names). Trail of Tears 1838–39, roughly 4,000 dead. Ridges and Boudinot killed June 1839; Act of Union July 1839; internal strife until the 1846 treaty. | `cherokee` pops in GA (8,946), NC (3,644), AL (1,424), TN and AR (30,136), and 50,800 in SEQ's Oklahoma. Vanilla JE + `native_resettlement.1–6`. |
| Muscogee (Creek) | Treaty of Cusseta (1832), then land fraud. The Second Creek War (May 1836) leads to forced removal of ~14,600 in 1836–37, some in chains. The *Monmouth* steamboat disaster (Oct 1837) kills ~300. Creek men drafted against the Seminoles were promised that their families could stay; the families were removed anyway. | 22,240 `muskogean` in Alabama (USA), 3,000 in Florida (USA). **Never removed** by any vanilla content. Alabama keeps the `muskogean` homeland. |
| Choctaw | Dancing Rabbit Creek (1830), removal 1831–33, the first "trail of tears and death". Constitution 1834. Gave $170 for Irish famine relief in 1847. | No `choctaw` culture. In practice part of the SEQ Cherokee block. No flavor. |
| Chickasaw | Treaty of Doaksville (Jan 1837): settle inside the Choctaw Nation. Removal 1837–38, paid for out of their own land-sale fund. Smallpox on arrival. | No culture, no flavor. |
| Seminole | Second Seminole War 1835–42 (Dade's battle 28 Dec 1835). Osceola seized under a flag of truce Oct 1837, dies Jan 1838. Those removed are forced to settle among the Creeks. | `SML` tag in Florida, `je_seminole_wars`, `native_resettlement.7` moves `muskogean` to SEQ. |

## How the vanilla chain works (the hooks we use)

```
on_monthly_pulse_country ─► native_resettlement.1  (USA, bigoted ruler → Jackson qualifies in Jan 1836)
                              └─ adds je_indian_removal
je_indian_removal monthly random_events (20 none / 2 / 2 / 1):
  .2 John Ross petition      sets  john_ross_petition; option b sets trail_of_tears_stall (36 m)
  .3 Preparing for Removal   needs NOT trail_of_tears_stall; moves all Cherokee of one state to SEQ capital,
                             kills 5–10 %, sets trail_of_tears_stall (12 m) and indian_removal_force (1 or 2, 36 m)
  .4 Trail of Tears          needs indian_removal_force; adds trail_of_tears_modifier to SEQ capital (x2 if force)
complete → .5 Clearing of the East (removes Cherokee homelands) or .6 native rights
je_seminole_wars complete → .7 moves Florida muskogean to SEQ
```

The state we can read without touching vanilla files:
- `has_journal_entry = je_indian_removal` on USA: removal is under way.
- `trail_of_tears_stall` on USA: vanilla pauses `.2` and `.3` while it is set. **Setting it ourselves is how we delay removal to 1838.**
- `indian_removal_force` on USA, value 1 or 2: how brutal the removal was.
- `john_ross_petition` on USA: Ross's petition has fired.
- `trail_of_tears_modifier` on `c:SEQ.capital`: the Trail has happened.
- `muskogean` pops in SEQ's capital after `.7`: the Seminoles have arrived.

## Proposed content

New namespace `hmps_five_tribes`, new file `events/HMPS_five_tribes.txt`, one new JE in `common/journal_entries/HMPS_Five_Tribes.txt`, and modifiers in a matching `static_modifiers` file plus localisation. Event numbers below are placeholders.

### A. USA side, in the vanilla removal chain

**1. The Treaty of New Echota** (`hmps_five_tribes.1`, USA). Fires once, on the first monthly pulse with `je_indian_removal` active (so Jan–Feb 1836). It is the hinge that makes vanilla run on the historical timeline.
- *a. Ratify with the two-year grace period* (default, historical). Sets `trail_of_tears_stall` for 27 months (about May 1838) and `hmps_new_echota_ratified`. Gives a small, short approval boost to the IG led by `is_andrew_jackson` or a bigoted leader, mirroring vanilla `USA_rejected_ross_petition`. Effect: vanilla `.3` and `.4` cannot fire until 1838, as in history.
- *b. Demand immediate removal* (Georgia's position). No stall, so vanilla runs as it does today. Sets `indian_removal_force = 2` for 36 months, so a later vanilla `.4` uses its harsher "their blood is on our hands" branch. Small radicals among `cherokee` pops in USA states.
- *c. Refuse the Treaty Party's signatures and treat with Ross.* Only available if the ruler is not bigoted (so not Jackson). Sets `trail_of_tears_stall` for 36 months and gives the John Ross enactment bonus (vanilla `john_ross_enactment`) toward `law_multicultural`/`law_no_colonial_affairs`. This keeps the vanilla "native rights" ending (`.6`) open as a real path.

Note: during the grace period vanilla `.2` (Ross petition) is blocked by the stall. Option (a) should therefore set `john_ross_petition` itself and fold Ross's petition into this event's text, so the petition is not lost but cannot reset the stall later.

**2. The Second Creek War** (`hmps_five_tribes.2`, USA). Fires once between 1836.5.1 and 1837.12.31 if USA owns Alabama and Alabama has `muskogean` pops. This fills the biggest gap: Creek removal is missing from vanilla.
- *a. Send Jesup and remove the Creek Nation* (default). Moves all `muskogean` pops in USA-owned Alabama and Georgia to the SEQ capital, using the same `kill_population_percent_in_state` + `move_pop` pattern as vanilla `.3` (5 %). Sets `hmps_creek_removed`. Adds a short `hmps_creek_war_unrest` modifier to the Alabama state.
- *b. Enlist Creek warriors against the Seminoles; their families may stay.* Only while `je_seminole_wars` is active. The pops stay in Alabama for now. Gives a short USA modifier helping the Florida war (for example a small army morale or offense bonus, kept small for MP). Queues **2b** after about 12 months.
  - **2b. The promise is broken** (`hmps_five_tribes.3`). The families are removed anyway, with the same effects as option a. Lowers `muskogean` acceptance with a short modifier on USA and gives SEQ a short loyalty or relations penalty toward USA. This is the historical outcome and the default.

**3. The *Monmouth* disaster** (`hmps_five_tribes.4`, USA, about 6–18 months after `hmps_creek_removed`). One-off: kills 2 % of `muskogean` in the SEQ capital and adds a short SoL modifier there. Options are text only (accept the contractor's report / order an inquiry with a small cost and small gain in USA legitimacy). It parallels vanilla `.4` for the Creeks without reusing the Cherokee-specific `trail_of_tears_modifier`.

**4. Osceola under the white flag** (`hmps_five_tribes.5`, USA). Fires once from 1837.9.1 while `je_seminole_wars` is active and `SML` exists.
- *a. Seize him at the parley* (default, historical). SML gets a short morale or offense penalty, and USA gets a small amount of infamy. The infamy should be tiny, because HMPS treats infamy as a real cost in MP.
- *b. Honour the truce.* No military effect. A small USA legitimacy or prestige boost.

When `je_seminole_wars` completes, vanilla `.7` already moves the Seminoles west. Event 9 below covers their arrival.

**5. Closing the vanilla JE.** No change to vanilla's ending. If `hmps_creek_removed` is set when `.5` "Clearing of the East" fires, a follow-up `hmps_five_tribes.6` also removes the `muskogean` homeland from Alabama and Georgia. Vanilla removes only Cherokee homelands. This makes the "clearing" consistent for both nations.

### B. Indian Territory side: "The Nations in the West" JE

New JE `je_hmps_nations_in_the_west` for `c:SEQ`. Added at game start (or by event 1 for SEQ). It gives the Indian Territory, usually an AI puppet, a visible story that reacts to what the USA does. The MP default assumes SEQ is AI, so all options have AI weights and historical defaults.

- **Complete:** all of these hold:
  - `trail_of_tears_modifier` was applied and has expired;
  - event 8a (Act of Union) has fired;
  - year ≥ 1846.
- **On complete:** a light "Five Nations" modifier on SEQ (literacy and a little bureaucracy, the Cherokee and Choctaw school systems).
- **Invalid:** SEQ is annexed, or it is no longer a subject of USA. (If it is released or rises up, the flavor no longer fits.)

Events inside the JE (all `country_event` for SEQ unless noted):

**6. The Chickasaw buy their way west** (`hmps_five_tribes.10`). From 1837.1.1. The Treaty of Doaksville. Gives a small one-time `add_treasury` (the Chickasaw land-sale fund) plus a short negative SoL modifier on the SEQ capital (smallpox). No new pops: there is no Chickasaw culture, and pops come only from history files, which the maintainer owns.

**7. The Trail ends at Fort Gibson** (`hmps_five_tribes.11`). Fires when `c:SEQ.capital` gains `trail_of_tears_modifier`, which is set by vanilla `.4`. It is the receiving end of vanilla's Trail of Tears.
- If USA's `indian_removal_force >= 2`: harsher text, and Cherokee radicals in SEQ.
- If removal was the "pay their way" branch: a milder text where Ross manages the detachments.
- Options are small: spend money on relief (shortens the SoL hit with a counter-modifier) or "the nation must endure" (nothing).

**8. Blood Law: the Treaty Party pays** (`hmps_five_tribes.12`, about 6–12 months after event 7). The killings of Major Ridge, John Ridge and Elias Boudinot (June 1839).
- *a. Ross condemns the killings, but the Union comes first* (default). Starts `hmps_cherokee_strife`, a mild political-instability modifier, until event 8b.
- *b. Hunt down the killers.* A shorter strife modifier, but radicals among `cherokee`.

  **8a. The Act of Union** (`hmps_five_tribes.13`, July 1839 or 1 month after event 8). The Eastern Cherokee and the Old Settlers unite under one constitution. This removes nothing but sets `hmps_act_of_union` for the JE.

  **8b. The Treaty of 1846** (`hmps_five_tribes.14`, from 1846.1.1). Ends `hmps_cherokee_strife`.

**9. The Seminoles among the Creeks** (`hmps_five_tribes.15`). Fires when `SML` no longer exists and the SEQ capital has `muskogean` pops (after vanilla `.7`). The Seminoles are forced to settle within the Creek Nation. Their friction ends only with the separate Seminole Nation of 1856. Gives a short, small negative modifier. One option offers the Seminoles their own council (small bureaucracy cost, ends it early).

**10. Kindred spirits: the Choctaw gift to Ireland** (`hmps_five_tribes.16`). Fires once when a state that is an Irish homeland has `has_famine = yes` (the vanilla famine system, see `famine_events.4`).
- *a. Send what we can* (default): small `add_treasury` cost, better relations (`change_relations`) with the owner of that state (normally GBR), a small prestige gain.
- *b. We have nothing to spare*: no effect.

  It is a famous moment, and it costs almost nothing in MP.

**11. Sequoyah's syllabary** (`hmps_five_tribes.17`, early in the JE). Mentions the *Cherokee Phoenix* (1828–34) and announces the *Cherokee Advocate* (1844). Gives a small literacy modifier on SEQ for a long time. This is the "civilized" in the name: the reason these nations were called that, and the reason removal was so bitterly contested.

*Optional / later:* **The Webbers Falls slave revolt** (Nov 1842). SEQ starts with `law_legacy_slavery`, and the pop history already comments on this revolt. Enslaved people of the Vann plantation flee toward Mexico. This could be linked to `HMPS_abolish_slavery`, but it is scope creep, so it is left for a second pass.

## Implementation notes

- **Files** (new, HMPS naming):
  - `events/HMPS_five_tribes.txt`
  - `common/journal_entries/HMPS_Five_Tribes.txt`
  - `common/static_modifiers/HMPS_five_tribes_modifiers.txt`
  - `localization/english/HMPS_five_tribes_l_english.yml`
  - Triggering: one line in the existing HMPS `on_monthly_pulse_country` list in `common/on_actions/00_code_on_actions.txt` (vanilla `native_resettlement.1` is already listed there), and `on_game_started` for the SEQ JE.
- **No vanilla replacements.** Vanilla `native_resettlement.*`, `je_indian_removal` and `je_seminole_wars` stay as they are. Every link goes through the variables and modifiers listed above. If a future patch renames one of them, only our triggers break, and the vanilla chain keeps working.
- **No history edits.** No new cultures (Choctaw/Chickasaw stay folded into SEQ's existing pops) and no pop changes. History is owned by the maintainer's generator.
- **Effects already used in vanilla** for the same purpose: `move_pop`, `kill_population_percent_in_state`, `remove_homeland`, `set_variable` with `months`, `add_treasury`, `change_relations`, `add_radicals`. Check each against the installed game, not `basegame-ver/`.
- **Localisation:** typographic ’ only, no ASCII apostrophe in names. Keep the tone of vanilla `native_resettlement` (sober, no glorification).
- **Interaction with `usa_politics.1`** (Jackson retires): vanilla `.1` needs a bigoted ruler. Jackson is bigoted and stays ruler until the Dec 1836 election, so the JE still starts in Jan 1836. Event 1's option (c) depends on the ruler not being bigoted, so it is effectively locked in 1836. That is intended.

## MP balance

- The USA loses nothing it has today. Delaying `.3` to 1838 only shifts when the pops move. The Creek removal adds ~22k pops moving from Alabama to SEQ: the same market (SEQ is a USA puppet), with a tiny loss of Alabama workforce.
- All modifiers are short or small. There is no war, no tag release and no free claims.
- The SEQ JE is mainly flavor for an AI puppet. If a player ever takes SEQ, the modifiers are mild buffs and debuffs, with nothing to exploit.

## Open questions for the team

1. Should the New Echota delay be on by default (historical 1838), or should it be option (a) vs (b) as proposed, so a player USA can choose an early removal?
2. Should option 2b (Creek warriors in Florida) give a real military bonus, or text only?
3. Should Choctaw and Chickasaw get their own cultures later? That would need a history pass through the maintainer, plus portraits and names.
4. Should the Webbers Falls revolt be included now or later?
