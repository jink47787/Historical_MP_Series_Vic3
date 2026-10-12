# Proposal: actual control in North America, 1 January 1836

Status: draft for discussion. Nothing in the mod folder is changed by this proposal.

## Summary

Vanilla draws the USA, Mexico and the British companies by what they claimed. This proposal redraws the 1836 start by who actually controlled the ground. State regions (`map_data`) are untouched. Only the ownership splits inside them (`create_state ... owned_provinces`) and the starting claims change.

Across the 34 state regions covered (6,465 provinces):

| Owner | Vanilla | Proposed |
|---|---|---|
| USA | 440 | 133 |
| Mexico (MEX) | 355 | 59 |
| Republic of Texas (TEX) | 81 | 41 |
| Oregon (ORG, British colony) | 353 | 18 |
| Hudson's Bay Company (HBC) | 3,526 | 110 |
| Upper Canada (ONT) / Lower Canada (QUE) | 94 / 220 | 30 / 46 |
| Newfoundland (GBR) | 154 | 47 |
| Native nations, existing tags | 1,242 | 3,491 |
| Native nations, six new tags | 0 | 2,489 |

Maps:

- `map_vanilla.png` / `map_proposed.png`: US close-up, vanilla vs proposed.
- `map_vanilla_na.png` / `map_proposed_na.png`: all of North America.
- `map_proposed_na_borders.png`: proposed map with the 1836 colonial boundaries as dashed lines (reference only).

Per-region numbers are in `summary.md`. Draft state-history blocks with every province are in `draft_states_north_america.txt`, which the game does not load.

## Principles

1. **Control, not claims.** A province belongs to whoever governed or held it on 1 Jan 1836. Treaty cessions, charters and paper counties count only where they came with settlement, garrisons or administration.
2. **No isolated provinces.** Every split must connect to its owner's territory. The exceptions are enclaves inside a split that is itself connected:
   - Fort Mackinac and Sault Ste. Marie (USA, Michigan)
   - Fort Brooke/Tampa and Key West (USA, Florida)
   - Fort Leavenworth (USA, Kansas; it borders Missouri)
   - the El Paso valley (MEX)

   Detached forts and trading posts (Snelling, Pierre, Union, Laramie, Bent's, Ross, Zuni, the interior HBC posts) were removed.
3. **Contiguous colonial cores.** Mexican New Mexico (the Rio Grande down to El Paso) and Oregon (ORG) are each one connected piece. Mexican California is one strip along the Camino Real; it needs no land link to Mexico because it is coastal.
4. **Removal is handled by events, not borders.** The Cherokee, Creek and Chickasaw were inside state jurisdictions by 1836 (Georgia 1830, Alabama 1832, Mississippi 1830). The vanilla Indian Removal journal entry is invalid unless the USA owns all of Georgia. So these nations stay as pops in US states and their story stays in the Indian Removal content.
5. **No tendrils.** A native province that touches at most one province of its own owner but three or more land neighbours is a spur; the build gives it to the neighbouring native owner. Colonial corridors (Camino Real, HBC belt, Fort Langley) and the Indian Territory band are exempt by design.
6. **Detached blocks that remain on purpose:**
   - Apache east (Mescalero) and west (Gila) of the Rio Grande corridor.
   - The Odawa block in northern Michigan (across the Straits of Mackinac from the rest of the Anishinaabe).
   - The coastal Salish west of the Fort Langley corridor (see Pacific Northwest).
   - Islands.

## Region by region

### Great Lakes and upper Mississippi
- **Michigan:** US south of the Grand River–Saginaw line. The northern Lower Peninsula and the Upper Peninsula stay with the Ojibwe and Odawa (CTF) until the Treaty of Washington (28 Mar 1836). The US keeps Mackinac and Sault Ste. Marie.
- **Wisconsin:** US south of the Fox–Wisconsin waterway and along the lakeshore (cessions of 1829, 1831, 1832 and 1833). North of it, Ojibwe land goes to CTF. The Menominee and Ho-Chunk lands are folded into CTF too: both peoples are distinct from the Ojibwe but too small for their own tag, and no existing tag fits them historically.
- **Minnesota:** Dakota (LKT) and Ojibwe (CTF) along the 1825 Prairie du Chien line. Fort Snelling is dropped (isolated).
- **Iowa:**
  - US: the Black Hawk Purchase strip, the Half-Breed Tract and the 1830 Neutral Ground in the northeast (a federal buffer patrolled from Fort Crawford, assigned to the Ho-Chunk in 1832 but not occupied until 1840).
  - Sauk & Meskwaki (SFX): the interior.
  - Dakota (LKT): the northwest.
- **Missouri:** US, except the Platte country west of the 1821 line (a three-province strip joined to Sauk & Meskwaki land in Iowa), which goes to Sauk & Meskwaki (SFX). The Ioway and the Sauk & Meskwaki of the Missouri lived there until the Platte Purchase (signed Sept 1836, annexed 1837).
- **Arkansas:** fully US.
- **Florida:** Second Seminole War. The Seminoles (SML) hold the peninsula south of the Withlacoochee/Fort King line (17 of 35 provinces, up from 5). The US keeps Tampa and Key West.

### Plains
- **US:** in the Louisiana Purchase states the USA keeps only Fort Leavenworth.
- **Kansas:**
  - Indian Territory (SEQ): the emigrant reserves, which in 1836 filled the whole eastern edge of Kansas (Cherokee Neutral Lands, Wea/Piankashaw/Peoria, Ottawa, Kickapoo), with the Shawnee and Delaware reserves running west along the Kansas River.
  - Osage/Kansa (OSG): includes the Kansa reserve further up the Kansas River.
  - Osage/Kansa (OSG): the south and centre.
  - Pawnee (PWN): the north and centre, south to the Arkansas (Pawnee Rock, Pawnee Fork).
  - Cheyenne/Arapaho (ARP): the west.
  - Kiowa/Comanche (COM): south of the Arkansas.
- **Nebraska:** Pawnee with the Otoe and Omaha (all under the Council Bluffs agency) on the Platte and Loup, Lakota in the Sandhills and on the Niobrara, Cheyenne/Arapaho in the southwest corner.
- **Dakotas:** Lakota/Dakota (LKT), Assiniboine (IRC) in the northwest, Pembina/Turtle Mountain Ojibwe (CTF).
- **Montana:**
  - Blackfoot (BLF): the north.
  - Crow (ABS): the Yellowstone.
  - Assiniboine (IRC): the northeast.
  - Salish (SLS): west of the Continental Divide.
  - Shoshone (BNN): the Beaverhead.
- **Wyoming:** Shoshone (BNN), Crow (ABS), Lakota, Cheyenne/Arapaho.
- **Crow/Lakota boundary:** follows the Powder River, not state lines. In 1836 the Crow held the Powder River country and the Lakota held the Black Hills, the Belle Fourche and the Little Missouri; the Lakota push west came in the 1840s and 1850s.
- **Colorado:**
  - Ute: the mountains.
  - Cheyenne/Arapaho: the plains north of the Arkansas.
  - Kiowa/Comanche: south of it.
  - Mexico: none; there was no Mexican settlement in Colorado in 1836.
- **Oklahoma:** Indian Territory (SEQ) east of the Cross Timbers (about 97°W). Osage in the eastern Cherokee Outlet, Comanche/Kiowa/Wichita west.

### Southwest and Texas
- **Texas:**
  - Texian control (TEX): after the Siege of Béxar (Dec 1835), the settled zone from the Sabine to Béxar and Goliad, plus the Red River settlements.
  - Mexico: the Nueces strip and Laredo, and the El Paso valley.
  - The rest is split along the Pecos River: Comanchería (COM) east, Mescalero/Lipan Apache (APC) west in the Trans-Pecos.
- **New Mexico:**
  - Mexico: the Rio Arriba and Rio Abajo (Taos to Socorro) and the Pecos villages, plus the Camino Real down to El Paso.
  - Navajo: the northwest.
  - Comanche: the eastern plains, east of the Pecos River.
  - Apache: the south and southwest (Mescalero west of the Pecos, Gila Apache further west).
- **Arizona:**
  - Mexico: Tucson and Tubac, plus the O'odham land (allied, mission-served). This could instead be its own O'odham tag later.
  - Navajo and Hopi: the northeast.
  - Apache: the east.
  - Yuman peoples (CLF): the west.
- **Utah, Nevada:** Ute, Shoshone-Bannock (BNN) and Western Shoshone/Northern Paiute. The Southern Paiute (folded into UTE) hold southwestern Utah and the Las Vegas/Moapa corner of Nevada; Nevada's southern tip on the Colorado River is Mohave (CLF). No Mexican provinces (vanilla gave Mexico 74 in Nevada).
- **California:** Mexico holds the mission/presidio/rancho strip from San Diego to Sonoma. The interior goes to Californian peoples (CLF). Fort Ross is dropped as isolated; it was Russian until 1841.

### Pacific Northwest (Oregon Country)
- Option A, chosen: ORG holds Fort Vancouver, the Willamette, the Cowlitz, Fort Nisqually and the Puget lowland up to Fort Langley on the Fraser. This keeps an ORG split in British Columbia, so the Oregon journal entry, the BC-settlement button and the border-dispute events keep their targets.
- Plateau peoples (NZP: Nez Perce, Cayuse, Yakama, Klamath), Salish (SLS) and Shoshone-Bannock/Northern Paiute (BNN) hold the rest.
- Rejected alternatives:
  - B: stop ORG at Nisqually.
  - C: B plus a Coast peoples tag.

  Both are rendered in the tool (`--variant nisqually`, `--variant coast_tag`).

### British North America
- **Upper Canada (ONT):** the settled townships, the Huron Tract, Lake Simcoe and the lower Ottawa. North of that is Ojibwe (CTF), including the Oji-Cree of the northwestern upland (they speak Severn Ojibwe). The Hudson Bay Lowland is Swampy and Moose Cree land, so it goes to the Cree-speaking Innu tag (INN) with the James Bay Cree across the bay and the Swampy Cree of northeastern Manitoba.
- **Lower Canada (QUE):**
  - QUE: the St Lawrence seigneuries and townships and the Gaspé coast.
  - Algonquin (CTF, whose language is part of the Ojibwe continuum): the upper Ottawa and Abitibi.
  - Innu and Eastern Cree (INN): the Saguenay, the North Shore, the Labrador plateau and the James Bay Cree.
  - Inuit (INU): Nunavik.
- **Newfoundland (GBR):**
  - GBR: the island and the southern Labrador fishing coast.
  - Inuit: northern Labrador (the Moravian missions).
  - Innu: the interior.
- **New Brunswick / Nova Scotia:** unchanged.
- **Northern Maine (disputed territory):** the upper St John valley (Madawaska) goes to New Brunswick, the Aroostook valley and Houlton stay US, and both keep claims on Maine.
  - New Brunswick administered the Madawaska settlement and arrested Maine officials who tried to act there (1831, 1837).
  - The US Army held Hancock Barracks at Houlton.
  - The forest between was cut by lumbermen from both sides, which led to the Aroostook War (1838–39). The Webster–Ashburton Treaty (1842) split the territory along the St John.
- **Hudson's Bay Company, strict:** the HBC's control was commercial. It governed only the Red River colony (District of Assiniboia) and its Bay posts, so it keeps one connected belt:
  - Red River and the Interlake;
  - the Lake Winnipeg / Norway House / Hayes River boat route to York Factory;
  - the Bay coast from Churchill to Moose Factory;
  - the James Bay east-coast posts.
- **Prairies and north:**
  - Cree country (Plains and Woodland Cree): Iron Confederacy (IRC).
  - Blackfoot Confederacy: BLF.
  - Northeastern Manitoba: the Oji-Cree of Island Lake and God's Lake to CTF; the Swampy Cree lowland north of them (Oxford House, Shamattawa) to INN, with the rest of the Bay Cree.
  - The Cree are split along a real dialect line. The Bay Cree (Swampy, Moose, James Bay) shade into the Innu, so they go to INN. The inland Rock, Woodland and Plains Cree go to the Iron Confederacy (IRC).
  - The Mackenzie basin, northern BC, Yukon and the Northwest Territories: Dene (ATB).
  - The Arctic coast and islands, and the tundra north and east of the treeline (one continuous line from the Mackenzie delta past Great Bear Lake and the Thelon to Hudson Bay near Arviat): Inuit (INU). The Dene (ATB) hold the forest south and west of it.
- **British Columbia:** Dene (ATB) in the north and centre; Salish (SLS) on the south coast, in the southern interior and on the Northwest Coast; ORG only at Fort Langley.
- **Alaska:** unchanged from vanilla.

## Colonial claims

In vanilla, a country cannot colonize a state region where another country has a claim and keeps an interest (`ESTABLISH_COLONY_FOREIGN_CLAIMS`). Colonies also create claims automatically once they hold half a region (`colonial_claims_check`), and the Stake Colonial Claim action lets a country with enough interest claim land held by native nations (decentralized countries). So claims decide who can colonize the land this proposal hands to native nations.

| Claim | Status | Why |
|---|---|---|
| USA on Wyoming, Montana, the Dakotas, Nebraska, Kansas, Minnesota, Florida | vanilla, kept | Louisiana Purchase and Florida |
| USA on Michigan, Wisconsin, Iowa | **new** | US territory; stops Britain colonizing the new Anishinaabe and Sauk land from Ontario |
| USA and NBS on Maine | **new** | the Aroostook/Madawaska dispute, settled 1842; Madawaska was run from New Brunswick |
| MEX on Utah, Texas, Arizona, New Mexico | vanilla, kept | Adams–Onís |
| MEX on California, Nevada | **new** | Alta California; keeps the US out until Manifest Destiny |
| TEX on Texas, New Mexico | vanilla, kept | |
| ORG on Idaho, British Columbia; HBC on Saskatchewan, Alberta | vanilla, kept | |
| ONT on Ontario, QUE on Quebec, GBR on Newfoundland | **new** | colonial boundaries |
| HBC on Manitoba, Nunavut, Northwest Territories, Yukon | **new** | Rupert's Land charter and the 1821 licence for the "Indian Territories" |
| Nobody on Washington and Oregon | deliberate | joint occupation: both sides can colonize, which is what the mod's Oregon journal entry expects |
| Colorado and Oklahoma | no starting claim | the mod's frontier-wars journal entry adds these claims on completion |

## New tags (six)

Rule used: a new tag only for a large people clearly distinct from its neighbours. Smaller peoples go to the closest existing tag where that is historical, and otherwise stay folded into their neighbour's tag (noted above).

All are decentralized, principality tier, and use existing vanilla cultures:

| Tag | Name | Culture | Where |
|---|---|---|---|
| CTF | Ojibwe (one tag for all Ojibwe-speaking peoples: Ojibwe, Odawa, Saulteaux, Mississauga, Nipissing, Algonquin, Oji-Cree; the small Menominee and Ho-Chunk lands folded in) | algonquian | Michigan, Wisconsin, Minnesota, North Dakota, Ontario, Quebec, Manitoba |
| SFX | Sauk and Meskwaki (Ioway and Potawatomi folded in) | algonquian | Iowa |
| OSG | Osage (Kansa folded in) | siouan | Kansas, Oklahoma |
| CLF | Californian peoples (Yokuts, Miwok, Maidu, Pomo, Yuman) | hokan | California, Arizona |
| INU | Inuit | inuit | Arctic, Nunavik, northern Labrador |
| INN | Innu and Bay Cree (the Cree–Innu continuum: Innu, Naskapi, James Bay, Moose and Swampy Cree) | cree | Quebec, Labrador, the Hudson Bay Lowland of Ontario and Manitoba |

Each new tag needs:
- a country definition;
- history (e.g. `effect_starting_technology_tier_6_tech`, `effect_starting_politics_traditional`, native conscription, as vanilla tribes get);
- localisation, a coat of arms and a map colour;
- pops in each new split.

## What this touches (dependencies)

History is regenerated by the maintainer through the history agent (see `docs/modding_notes.md`), so these are notes for that pass, not hand edits.

1. **State history:** copy vanilla `common/history/states/00_states.txt` into the mod and replace the North America blocks with `draft_states_north_america.txt`. A second `create_state` in another file would add to vanilla's splits, not replace them.
2. **Pop history** (vanilla `common/history/pops/05_north_america.txt`, copied and edited):
   - These splits disappear and their pops must move:
     - USA in Minnesota, Nebraska, the Dakotas, Montana, Wyoming and Colorado;
     - MEX in Colorado, Utah and Nevada;
     - SLS in Wyoming;
     - ORG in Idaho;
     - HBC in Saskatchewan, Alberta, British Columbia, Yukon, the Northwest Territories and Nunavut.
   - Native pops go to the native split in the same region.
   - The Métis (16,000 in Saskatchewan, 11,000 in Alberta) go to the Iron Confederacy (IRC) or to Red River.
   - The 800 Mexican pops in Colorado go to New Mexico.
   - The mod's own history files (`HMPS_pops.txt`, `HMPS_generated_buildings.txt`, `HMPS_buildings.txt`) reference none of these splits.
3. **Building history:**
   - The HBC-company logging camp in Alberta must move (to Red River) or go.
   - Shrinking splits keep their buildings while their share of the region's resources falls, so the generator should re-check caps:
     - ORG in British Columbia (3 of 209 provinces), Oregon (7 of 78) and Washington (8 of 60);
     - QUE (46 of 220) and ONT (30 of 94);
     - GBR Newfoundland (47 of 154);
     - HBC in Manitoba (68 of 259);
     - US Michigan (22 of 50), TEX (41 of 81).
4. **Scripts:**
   - The Oregon journal entry and border-dispute events reference `s:STATE_IDAHO.region_state:ORG`, and ORG no longer has an Idaho split. Guard those with `?=` or re-point them.
   - The BC, Oregon and Washington ORG splits still exist under option A.
5. **Journal entries to re-test:**
   - Indian Removal: needs all of Georgia, which is kept.
   - Seminole Wars: completes when the USA owns all of Florida; now a real war.
   - Frontier Wars: needs Montana, Wyoming, the Dakotas, Nebraska and Kansas in full. That is now much harder and probably needs a look at the colonization speed in `hmps_usa_frontier_wars_modifier`.
   - Manifest Destiny and Mexico's `repudiate_manifest_destiny`: both use `owns_entire_state_region` on the Southwest.
   - Texas.

## Gameplay and multiplayer impact

- **USA:** starts with far less land in the West and on the Great Lakes, but most of what it loses held only native pops in vanilla. Expansion now goes through colonization and native wars. Balance colonization speed so the USA still reaches the Pacific on a historical schedule.
- **Mexico:** loses most of its northern frontier on paper (CA, NV, UT, AZ, NM). Its claims keep the US out until Manifest Destiny.
- **Britain (ORG, HBC, ONT, QUE):** the colonies become small settled cores with large native hinterlands to colonize.
- **Possible performance hit:** many more decentralized splits; test late-game speed.

## Test plan

1. Load with the overridden state, pop and building history; check `error.log` for missing `region_state` scopes and over-cap buildings.
2. Start as the USA, Mexico and Britain:
   - Colonization: can each colonize its own claimed native land, and is it blocked from rivals' claimed land?
   - Do overlapping claims (Maine, Ontario HBC vs ONT) behave as intended?
3. Play the Oregon, Indian Removal, Seminole Wars, Texas and Frontier Wars journal entries to completion.
4. Check that the native tags spawn with pops, laws and techs.

## Method and sources

- **Province assignment:** `tools/build.py` matches `provinces.png` to real geography using the trading-hub towns (318 towns, median error about 7 px). It then matches the game coastline to the Natural Earth coastline (median about 1 px), which keeps the Arctic accurate. Each province goes to the owner whose polygon in `tools/control_1836.py` covers most of it. A contiguity pass and a few "connect" rules follow.
- **Rerun:**

  ```
  python -I tools/build.py --game <Victoria 3 game folder> --work <cache folder> --out <output folder>
  ```

- **Treaty lines:** Royce, *Indian Land Cessions in the United States* (1899), via the USDA Forest Service "Tribal Lands Ceded to the United States" geodatabase. Royce numbers run in treaty-date order. That was checked against the dated High Country News *Land-Grab Universities* table (CC0), so cessions up to no. 203 (Treaty of New Echota, 29 Dec 1835) are "ceded by 1836". The proposal matches the Royce lines in the Great Lakes, Iowa and Missouri. Elsewhere it departs from them only where ceded land was still held by the tribe (Florida, the Osage and Pawnee land in Kansas).
- **US administration:** Newberry Library, *Atlas of Historical County Boundaries* (counties in force on 1 Jan 1836), via rOpenSci USAboundariesData.
- **Native territories and posts:** treaty texts and the standard references (Smithsonian *Handbook of North American Indians*), plus known fort and post founding dates.
- **Canada cross-check:** the 1836 population layer of the Victoria 2 mod *The Grand Combination* (The-Grand-Combination/The-Grand-Combo on GitHub). Its per-province native cultures were compared against these polygons, mainly for Canada. No TGC files are copied.
- **Map data:** Natural Earth (public domain); GeoNames town coordinates via lutangar/cities.json (CC BY 4.0).
- **Steam Workshop prior art:** TINO 1836 / Anno 1836 map (tino天成), Hail, Columbia!, and 1835 Rebirth. Found by search only; none of their files or data were used.
