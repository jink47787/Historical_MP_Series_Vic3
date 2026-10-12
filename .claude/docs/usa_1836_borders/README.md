# North America borders at the 1836 start

This describes the borders the mod uses now (state history as of commit 48dc5751a on main). It replaces the earlier proposal; the proposal, its draft files and its build tools are in git history (commit 48dc5751a).

The mod draws the 1836 start by who actually controlled the ground on 1 January 1836, not by what each country claimed. State regions (`map_data`) keep their vanilla provinces; only the ownership splits (`create_state ... owned_provinces`) and the starting claims differ from vanilla. They live in `Historical MP Series/common/history/states/00_states.txt`.

## Files

- `summary.md`: owners per state region, vanilla vs current; totals; claim changes; detached colonial pieces.
- `province_table.csv`: every province in the 35 changed regions, with its vanilla and current owner.
- `map_vanilla.png` / `map_current.png`: US close-up. `map_vanilla_na.png` / `map_current_na.png`: all of North America.
- `tools/maps.py`: regenerates all of the above from the mod's files. Rerun it after any border change:

  ```
  py -3.14 -I tools/maps.py --game ../../../basegame-ver --mod "../../../Historical MP Series" --out .
  ```

  (Run from this folder. Needs numpy and Pillow. Delete `tools/__pycache__` afterwards.)

## Overview

Across the 35 changed regions:

| Owner | Vanilla provinces | Current |
|---|---|---|
| USA | 440 | 137 |
| Mexico (MEX) | 355 | 54 |
| Republic of Texas (TEX) | 81 | 42 |
| Oregon (ORG) | 353 | 17 |
| Hudson's Bay Company (HBC) | 3,526 | 13 |
| Russian America (ALK) | 284 | 51 |
| Upper / Lower Canada (ONT / QUE) | 94 / 220 | 30 / 46 |
| Newfoundland (GBR) | 154 | 47 |
| New Brunswick (NBS) | 0 | 1 |
| Native nations | 1,986 | 7,055 |

## Principles

1. **Control, not claims.** A province belongs to whoever governed or held it on 1 Jan 1836. Treaty cessions, charters and paper counties count only where they came with settlement, garrisons or administration.
2. **Few isolated provinces.** Most splits connect to their owner's land. The deliberate exceptions are forts and posts the owner really held (full list in `summary.md`):
   - USA: Fort Mackinac and Sault Ste. Marie (Michigan), Fort Brooke/Tampa and Key West (Florida).
   - HBC: its Bay posts (Severn House, Fort Albany, Moose Factory, Rupert House, Eastmain, Fort George, Fort Chimo, Churchill, York Factory, Norway House), each a single province apart from the Red River block.
   - Russian America (ALK): Fort Ross in California, and its coastal and island posts in Alaska.
3. **Removal is handled by events, not borders.** The Cherokee, Creek and Chickasaw were inside state jurisdictions by 1836, so they stay as pops in US states and their story stays in the Indian Removal content.
4. **Native tags.** Five new decentralized tags (SFX, OSG, CLF, INU, INN) and the reused vanilla tag CTF hold land that vanilla gave to colonial owners. See "Native tags" below.

## Region by region

### Great Lakes and upper Mississippi
- **Michigan:** US south of the Grand River–Saginaw line, plus Mackinac and Sault Ste. Marie. The rest is Ojibwe and Odawa (CTF) until the Treaty of Washington (28 Mar 1836).
- **Wisconsin:** US south of the Fox–Wisconsin waterway and along the lakeshore. Ojibwe, Menominee and Ho-Chunk land to the north is CTF.
- **Minnesota:** Dakota (LKT) and Ojibwe (CTF) along the 1825 Prairie du Chien line. No US split.
- **Iowa:** US in the Black Hawk Purchase strip, the Half-Breed Tract and the Neutral Ground; Sauk & Meskwaki (SFX) in the interior; Dakota (LKT) in the northwest.
- **Missouri:** US, except the three-province Platte country, which is SFX until the Platte Purchase (1836–37).
- **Arkansas:** fully US, as in vanilla.
- **Florida:** Second Seminole War. The Seminoles (SML) hold the peninsula south of the Withlacoochee/Fort King line (17 of 35 provinces). The US keeps Tampa and Key West.

### Plains
- **Kansas:** the USA holds the eastern border strip (6 provinces, including Fort Leavenworth). Osage/Kansa (OSG) hold the south and centre, Pawnee (PWN) the north, Cheyenne/Arapaho (ARP) the west, Kiowa/Comanche (COM) south of the Arkansas. There is no Indian Territory (SEQ) split in Kansas.
- **Oklahoma:** Indian Territory (SEQ) holds nearly all of it (44 of 48); Comanche (COM) keep 4 provinces in the far west.
- **Nebraska:** Pawnee with the Otoe and Omaha on the Platte and Loup, Lakota in the Sandhills and on the Niobrara, Cheyenne/Arapaho in the southwest.
- **Dakotas:** Lakota/Dakota (LKT); Assiniboine (IRC) and Pembina Ojibwe (CTF) in North Dakota.
- **Montana:** Blackfoot (BLF) north, Crow (ABS) on the Yellowstone, Assiniboine (IRC) northeast, Salish (SLS) west of the Divide, Shoshone (BNN) on the Beaverhead, Lakota in the east.
- **Wyoming:** Shoshone (BNN), Crow (ABS), Lakota, Cheyenne/Arapaho. The Crow/Lakota line follows the Powder River.
- **Colorado:** Ute in the mountains, Cheyenne/Arapaho north of the Arkansas, Comanche south of it. No Mexican or US split.

### Southwest and Texas
- **Texas:** Texian control (TEX) from the Sabine to Béxar and Goliad plus the Red River settlements; Mexico in the Nueces strip, Laredo and the El Paso valley; Comanchería (COM) east of the Pecos and Apache (APC) in the Trans-Pecos.
- **New Mexico:** Mexico on the Rio Grande from Taos to El Paso and the Pecos villages; Navajo northwest; Ute in the far north; Comanche on the eastern plains; Apache south and southwest.
- **Arizona:** Mexico at Tucson, Tubac and the O'odham land; Navajo and Hopi northeast; Ute (Southern Paiute) in the northwest corner; Apache east; Yuman peoples (CLF) west.
- **Utah:** Ute (Southern Paiute folded in) in most of the state, Shoshone-Bannock (BNN) in the north and west, Navajo in the southeast corner. No Mexican split.
- **Nevada:** Shoshone-Bannock/Northern Paiute (BNN), Southern Paiute (UTE) in the south, Mohave (CLF) at the southern tip. No Mexican split.
- **California:** Mexico holds the mission and rancho strip from San Diego to Sonoma; Russian America (ALK) holds Fort Ross; the interior is Californian peoples (CLF) and, in the northeast, BNN.

### Pacific Northwest
- ORG holds Fort Vancouver, the Willamette, the Cowlitz, Fort Nisqually and the Puget lowland, with 2 provinces at Fort Langley in British Columbia.
- Plateau peoples (NZP), Salish (SLS) and Shoshone-Bannock/Northern Paiute (BNN) hold the rest of Oregon, Washington and Idaho. ORG has no Idaho split.

### British North America
- **Upper Canada (ONT):** the settled townships, the Huron Tract, Lake Simcoe and the lower Ottawa. Ojibwe and Oji-Cree (CTF) to the north; the Hudson Bay Lowland Cree go to INN.
- **Lower Canada (QUE):** the St Lawrence seigneuries and townships and the Gaspé. Algonquin (CTF) on the upper Ottawa and Abitibi; Innu and Eastern Cree (INN) on the Saguenay, North Shore, Labrador plateau and James Bay; Inuit (INU) in Nunavik.
- **Newfoundland (GBR):** the island and the southern Labrador coast. Inuit in northern Labrador, Innu inland.
- **Maine:** US, except Madawaska (1 province), which New Brunswick (NBS) administered. Both claim Maine.
- **Hudson's Bay Company:** Red River (Manitoba) and the single-province Bay posts listed above; 13 provinces in all.
- **Prairies and north:** Cree (IRC) and Blackfoot (BLF) on the prairies; Dene (ATB) in the Mackenzie basin, northern Alberta and Saskatchewan, northern BC and the Yukon; Inuit (INU) on the Arctic coast, the islands and the tundra beyond the treeline; Swampy Cree (INN) and Oji-Cree (CTF) in northeastern Manitoba.
- **British Columbia:** Dene (ATB) north and centre, Salish (SLS) on the south coast, in the southern interior and on the Northwest Coast, ORG at Fort Langley.
- **Alaska:** Russian America (ALK) keeps only its coastal and island posts (50 provinces); the rest is Dene (ATB).

## Claims

Claims decide who can colonize native land (`ESTABLISH_COLONY_FOREIGN_CLAIMS`). Current claims differing from vanilla:

| State | Vanilla | Current | Why |
|---|---|---|---|
| Michigan, Wisconsin, Iowa | none | USA | US territory; keeps Britain from colonizing the new native land from Ontario |
| Maine | none | USA, NBS | the Aroostook/Madawaska dispute, settled 1842 |
| California, Nevada | none | MEX | Alta California; keeps the US out until Manifest Destiny |
| Washington, Oregon | none | ORG | |
| British Columbia | ORG | ORG, HBC | |
| Ontario / Quebec | none | ONT, HBC / QUE, HBC | colonial boundaries and Rupert's Land |
| Newfoundland | none | GBR | |
| Manitoba, Northwest Territories, Nunavut | none | HBC | Rupert's Land charter and the 1821 licence |

Vanilla claims are kept everywhere else: USA on the Louisiana Purchase states, Minnesota and Florida; MEX on Texas, New Mexico, Arizona and Utah; TEX on Texas and New Mexico; ORG on Idaho; HBC on Yukon, Alberta and Saskatchewan; ALK on Alaska. Colorado and Oklahoma have no starting claim.

## Native tags

All are `country_type = decentralized`. Definitions are in `common/country_definitions/HMPS_1836_natives.txt`.

| Tag | People | Culture | Where |
|---|---|---|---|
| CTF | Ojibwe-speaking peoples (vanilla tag, reused; Menominee and Ho-Chunk folded in) | anishinaabe (mod culture) | Michigan, Wisconsin, Minnesota, North Dakota, Ontario, Quebec, Manitoba |
| SFX | Sauk and Meskwaki (Ioway and Potawatomi folded in) | algonquian | Iowa, Missouri |
| OSG | Osage (Kansa folded in) | siouan | Kansas |
| CLF | Californian peoples (Yokuts, Miwok, Maidu, Pomo, Yuman) | hokan | California, Arizona, Nevada |
| INU | Inuit | inuit | Arctic, Nunavik, northern Labrador, Yukon coast |
| INN | Innu and Bay Cree | cree | Quebec, Labrador, Hudson Bay Lowland of Ontario and Manitoba |

## Sources

- Treaty lines: Royce, *Indian Land Cessions in the United States* (1899), via the USDA Forest Service "Tribal Lands Ceded to the United States" geodatabase; cessions up to no. 203 (Treaty of New Echota, 29 Dec 1835) count as ceded by 1836.
- US administration: Newberry Library, *Atlas of Historical County Boundaries* (counties in force on 1 Jan 1836).
- Native territories and posts: treaty texts, the Smithsonian *Handbook of North American Indians*, and fort and post founding dates.
- Canada cross-check: the 1836 population layer of the Victoria 2 mod *The Grand Combination*. No files copied.
