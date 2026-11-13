# The HFM Enhanced Series (MP) - Changelog


**Credit:**
All mods / mod ideas used linked below:
- Country colour changes: https://steamcommunity.com/sharedfiles/filedetails/?id=2881165239, https://steamcommunity.com/sharedfiles/filedetails/?id=2881470170
- Synth Oil & Rubber: https://steamcommunity.com/sharedfiles/filedetails/?id=2880155469
- Ally recognition: https://steamcommunity.com/sharedfiles/filedetails/?id=2881810342&searchtext=recognition
- Dense Market Details: https://steamcommunity.com/sharedfiles/filedetails/?id=2881762225
- Dense Trade Routes: https://steamcommunity.com/sharedfiles/filedetails/?id=2881996099
- Complete Pop Lists: https://steamcommunity.com/sharedfiles/filedetails/?id=2880832253
- Improved Building Grid: https://steamcommunity.com/sharedfiles/filedetails/?id=2883323135
- Extra Topbar GUI: https://steamcommunity.com/sharedfiles/filedetails/?id=2888391145
- State Traits Building & Production Overview: https://steamcommunity.com/sharedfiles/filedetails/?id=2951560430
- Retain Homelands on Releasing: https://steamcommunity.com/sharedfiles/filedetails/?id=2934872102
- Useful Malaria Icons: https://steamcommunity.com/sharedfiles/filedetails/?id=3005297540
- Cold Water Ports: https://steamcommunity.com/sharedfiles/filedetails/?id=2997299912
- Historically Accurate Randomize Farming Yields: https://steamcommunity.com/sharedfiles/filedetails/?id=3073886807
- Forts & Engineers: https://steamcommunity.com/sharedfiles/filedetails/?id=3005432154
- Authority for Political Interactions: https://steamcommunity.com/sharedfiles/filedetails/?id=3045555636
- Historically Accurate Randomize Farming Yields: https://steamcommunity.com/workshop/filedetails/?id=3073886807
- War Is Politics: https://steamcommunity.com/sharedfiles/filedetails/?id=3124519140&searchtext=
- Ideologies & Traits Expansion: https://steamcommunity.com/sharedfiles/filedetails/?id=3300629321
- Better Civil War Flag: https://steamcommunity.com/sharedfiles/filedetails/?id=2945028897
- GDP Ownership Display: https://steamcommunity.com/sharedfiles/filedetails/?id=3290552216
- GDP Plot Line Plus Minimized: https://steamcommunity.com/sharedfiles/filedetails/?id=3261478691&searchtext=graph
- GDP Growth Rate (Fixed): https://steamcommunity.com/sharedfiles/filedetails/?id=3255320685
- Kate's Liberate Country as Subject: https://steamcommunity.com/sharedfiles/filedetails/?id=3241445760
- Remove all trade routes' line and arrows: https://steamcommunity.com/sharedfiles/filedetails/?id=2897200021
- Join War mod: https://steamcommunity.com/sharedfiles/filedetails/?id=3015811655
- Add Wargoals During Wars: https://steamcommunity.com/sharedfiles/filedetails/?id=3390504397
- Building Preference Rebalance (AI oil and rubber priority ideas): https://steamcommunity.com/sharedfiles/filedetails/?id=3726359241
Thanks to Gelre for his UI, Performance & Flava work.
Thanks to Henry, Orange, and Eilmer as HMPS junior devs. 
Thanks to Yyyman for his Italy company changes.
---
<br/>

**Any problems or changes to suggest can talk to lead devs: [REDACTED], Gracchus or Dr**

<br/>
---
<br/>~~~~~~

# Major Changes Since the Last Workshop Update (7 October 2026)

## Economic
#### Stone & Building Materials
- Two new goods: Stone and Building Materials. Building Materials are now the main input of the construction sector, and every urban building uses a small amount as upkeep
- New Quarries produce Stone and follow the mine layout: Steam Automation (Hand Cranked Crane, Steam Donkey) replaces the crushers, and haulage is Road Carts or Rail only, like mines. How many a state can build depends on its geology; 12 famous stone districts (e.g. Carrara Marble, Welsh Slate, Aswan Granite) boost quarries, and Silica Sands states boost glassworks and quarries
- New Builders' Yards turn wood, hardwood, stone, coal and steel into Building Materials, with Timber, Masonry and Automation methods that improve with tech
- Construction sector reworked into three groups: Foundations (Timber Footings, Brick Footings, Concrete Foundations, Piles and Caissons), Fittings (Bare Finish, Fitted Interiors, Electric Lifts) and Site Machinery (Manual Labour, Steam Plant, Motorised Plant). Better foundations add construction points; Windows and Pipes adds +0.5% construction sector throughput per level and Electric Lifts +1% per level; site machinery only saves labour. Reinforced Concrete (was +15%) and Pneumatic Tools (was +10%) no longer add construction throughput. Construction now pays normal industry wages and employs far more workers, so it is a much bigger cost to the government. Foundations now use Building Materials and wood at every era, Fittings no longer use hardwood, and each era costs about 20% more per construction point than vanilla; the newest Foundations and Fittings are always the cheapest per point
- Steel mills, glassworks and railways now use Stone; subsistence farms, orchards, pastures, rice farms and fishing villages produce a little Building Materials
#### Hardwood
- Hardwood is back as its own resource: Hardwood Forestry can be built in 208 states, and hardwood is used by Builders' Yards
#### Trade
- New Balance of Trade mechanic: a market's exports minus imports is measured as a share of its GDP. Past 1% of GDP either way, the side that is ahead loses 5% trade advantage per 1% (up to -100% at 20%) and the other side gains 2.5% per 1% (up to +50%). A surplus lowers export advantage and raises import advantage; a deficit does the reverse. Updated weekly, and every country in the market gets the same effect
#### Reserve Currency
- New Reserve Currency: one market at a time holds it. Only a Great Power whose market runs a Balance of Trade deficit can take it: a rival takes it over once its market has out-imported the holder's for 6 months in a row, and a vacant Reserve Currency goes to the top importer among them the same way. A holder whose market goes 6 months in a row without a deficit loses it, and it stays vacant until someone qualifies. A holder that stops being a Great Power loses it at once. The holder gets +25% trade advantage
#### Guano
- Guano works like gold: deposits are discovered over time and run out, and Guano Harvestries are placed automatically on known deposits instead of being built. In 1836 only Peru's coast is known
#### Infrastructure
- Added minor canals (unlocked by Urbanization) that raise state infrastructure and provide transportation, available in 65 states; 24 historical canals already exist in 1836 and start on Pound Locks, the best canal method of that era
#### Railroad Bubble
- Railroad Bubble reworked: it starts when a major power expands its railways quickly, grows with railway building and expensive transportation, and boosts railway throughput and construction while it lasts. Choices at the start (embrace or regulate), at the peak (let it run, cool the market, prop it up or let the banks carry it) and at the crash (rebuild or relief works). The crash cuts wages and adds radicals. New "The Railway King" event
#### Companies
- 151 territory-bound companies can now also be founded by an overlord when the territory belongs to one of its subjects (or their subjects) and needs buildings of level 3, not only by the owner. 27 of them with resource-only buildings can also own trade centers

## Political
- Multiculturalism reworked and renamed Multinationalism; ideologies that strongly disapproved of it now only disapprove
- The Boost War Support decision is turned off for now: vanilla 1.15 changed war support to run from 0 to 100, so the decision could never be taken. When it returns, it will be usable below 25 war support and give +50
- The Political Question journal entry is paused: it no longer starts at game start and its progress hooks are off, with its definition and laws kept dormant so it can be turned back on. The Springtime of the Peoples is back to the vanilla 1.15 setup: Forest of Bayonets starts it again with the vanilla "Revolutionary Spring" outcome, and European countries with Egalitarianism get its rules after Forest of Bayonets fails. If Forest of Bayonets times out without a Springtime, the 1848 unlock still fires, so Gutter Crown and the major formables still unlock
- Protectorate Political Penalty is back for players: player protectorates get -2 approval on every interest group and +10% radicals and loyalists from standard-of-living changes. It is added monthly while a player country is a protectorate and removed when it stops being one; AI protectorates are exempt

## Flava
#### Europe
- French Baby Bust: France can now end it faster by becoming a Confessional State, with two new amendments (Publicly Funded Religious Schools and Publicly Funded Religious Hospitals)
- German unification: Austria can no longer back a German candidate while it is a great power, and the Austria-Hungary dual monarchy now requires Germany to exist
- The Decembrist Sympathizers journal entry for Russia is paused: it no longer starts at game start and can't trigger for now, with its content kept so it can be turned back on
#### East Asia
- New Sakhalin events: Russia can assert its claim against Japanese encroachment, and Japan can answer by settling Karafuto or abandoning it
#### The Americas
- North America map rework: 1836 borders follow who actually controlled the land, with new native nations (Sauk and Meskwaki, Osage, Californian Peoples, Inuit, Innu and Cree), new Canada journal entries, Oregon dispute fixes and a new Oregon Trail event
- Latin America border rework: new native nations (Gê Peoples, Kaingang, Shuar, Tukanoan Peoples), new claims, and new Mosquito Shore and Guiana Boundary Commission events
- New "The Unconquered Interior" journal entry for South American countries with claims on native-held land: colonies grow 90% slower until Railways and Electric Telegraph are researched or the native land is taken. Once any South American country completes it, the slowdown ends for all of them, and they all get the 5-year Open Frontier bonus
- New "The Guano Islands Act" journal entry for the USA: build 5 fully crewed ironclads to get guano fertilizer sell orders that shrink over 30 years
- Manifest Destiny reworked: 40 years to finish, needs 6 US-owned states (California, Nevada, Utah, Arizona, New Mexico, Texas) that no longer have to be incorporated; Colorado moved to the Frontier Wars journal entry and Mexico starts with a claim on it

## UI
- Topbar shows the market's Balance of Trade in place of Prestige, with a graph of the last 52 weeks in its tooltip; the market panel shows the market's exports, imports and balance
- New Reserve Currency alerts in the topbar, next to the vanilla alerts: green when your market is about to take it or it is vacant and yours qualifies, red when you hold it and a rival is about to take it or your surplus is about to lose it. Each shows the days left, and clicking it opens the market panel
- New Specie Famine (red) and Inflationary Period (yellow) alerts in the topbar, shown to every market: they appear while the market's trade balance lets one start, and hide during its cooldown. Clicking either opens the market panel

## Stability/Bug Fixes
- Updated to Victoria 3 version 1.15. Government-built universities no longer need regional investment permission (privately built ones still do), and the India and Kulturkampf progress bars use the new two-colour look (green progress on red, with a marker)

## AI & Performance
- AI builds more construction goods: it wants a high supply of building materials, stone, oil and rubber, prioritises steel mills, glassworks, logging camps, quarries and Builders' Yards, and upgrades construction sector methods soon after unlocking them
- Performance: about 17% faster in early game tests (1836-1839 ran in 1:56 instead of 2:20)

---
<br/>

# Mod Overview

## Political
#### Government Types
- Republic is one government type
- Government names similar to vic2
- Authority is now locked to authoritarianism and is required for more authoritarian policies (higher taxes, more military)
- Legitimacy rebalance
- Movements to change tax laws or army laws are prevented (in the works)
#### Decrees
- Added SoL malus (-0.5) to throughput, renamed them exploit X industry
- Added Suppress Nationalism and Expanded Taxation
- Rebalanced other decrees to make them better or worse
#### Laws
- Separated executive structure from governance principles
- New cameralism & voting system laws
- New tax laws that affect the scaling power of tax buttons
- Professional army gives 10% attack and defence, and no ability to conscript
- Slavery increases landowner political power more
- Command economy gives 75% bureaucrats contribution to the investment pool
- Private & Public schools now allowed on any religion law
- Corporation taxes penalize construction efficiency
- Clerical Voting replaces Landed Voting for theocracies
- Cannot manually change cultural laws until an era 5 tech
- Added in debt, work hour, and pollution laws
- Added migration attraction to liberal laws
- Rebalance of policing laws
- Authority buff to authoritarian laws
#### Institutions
- All education is dependent to varying degrees on SoL
- New institutions for mobilization laws
- Polluition is separated from healthcare
- Colonial Exploitation and Resettlement now give modifier on unincorporated states that scales with the institution rather than the law
- Mass conscription now gives radicals to discourage staying at level 5 unless necessary
- Healthcare institution levels now each require tech, one per era
#### Interest Groups
- More dynamic attraction to various interest groups dependent on laws passed and places of employment, literacy etc.
- Military leaders give less clout
- Penalty from IG losing a civil war doubled to 20 years
#### Ideologies
- Cultural Chauvinism ideology created and applied to armed forces, rural folk, industrialists & landowners
- Liberal disapproves of professional and strongly diapproves of mass conscription
- added unique ideologies to the US
- General rebalance of ideologies
#### Traits
- Reduced the effects of all IG traits, increased thresholds for bonuses. 
#### Bureaucracy
- Slightly reduced base state taxation capacity

## Population
#### Migration
- Currently uses vanilla migration, will likely be adjusted for 1.5 in the future
- Trade centre and market capital modifiers removed completely
- Seccession now only occurs if turmoil is above 70%
#### Assimilation
- Minimum no. assimilating increased to 1000 to help performance late-game

## Tech
#### Innovation
- Reduced base innovation generation or usage
- Universities now consume more inputs and have greater outputs as well as giving Education Access
- Renamed literacy to Education Level to more accurately reflect what it is
#### Production
- Percentage multiplier on tax capacity for bureau PM techs

## Economic
- Pops are more likely to consume oil and cars when they are widely available
- Added railroad bubble journal entry and event chain for a lateish game economic crisis
- Agriculture goods now vary in states depending on year, this applies to a small extent on mines as well (Inspired by HARF mod)
- Gold fields don't use infrastructure
- Added era 1 company 
- Added new State Capitalism law
- MAPI readjusted to be harder to get and more spread out around techs
#### Goods
- Hardwood made into its own resource
- Added canals
#### Society
- Quinine shifted to era 4, malaria prevention to era 5
- Devastation takes twice as long to tick down
- Added westernization mod for unrecognized countries to westernize at a certain point
- AI Subjects of players no longer revolt
- Low governmetn and military wages are now much worse
- Increased number of cultural obsessions
- Force recognition tech locked
#### Industries
- Qualifications now matter!
	- Machinists start at 30%
	- Engineers start at 60%
	- Discriminated cultures have a far harder time becoming qualified
	- Aristocrats are easier to get
- Separated artilery from small arms, explosives from fertilizer, military ships from civilian ships (paradox stole this from us!!!)
- Agrarianism now has a small amount of capitalist contribution
- Interventionism and LF switched interest bonus
- Increased max level and effect of economies of scale
- Rebalanced oil and other resources
- Improved various oil PMs
- Changed machinist and engineer requirement for urban PMs
- DC and AC PMs added to power plants
- Colonial oil PMs with lower qualification thresholds
- Added new automobile PMs to more precisely decide how many cars you want to build
- Conveyor belts require rubber

#### Infrastructure
- Halved base state infrastructure
- Ports now provide infrastructure and transportation
- Railroads now provide max transportation from pops to represent benefit of population density

## Diplomacy
- North America Strategic Region Rework
- Puppeting, lowering autonomy, and annexing subjects are now more expensive to encourage direct conquest and partition
- Infamy is more punishing, especially as you get more and more
- Open Market is now much more punishing on the recipient to prevent cheesing
- Removed regime change and ban slavery due to being cheese
- Can now request grants (obligation optional)
#### Actions & Relations
- Added GM actions (Change infamy, change money, add university)
- Added mod to not release homelands on nation release
- Major powers cannot enter customs unions
- Subjects have 0 interests
- Subjects have permanent minor malus
#### CBs
- Cut Down can be done by any non-decentralized power & will remove all conquests from past 15 years rather than 10

## Military
- Merged rifling, repeaters, and bolt-action rifles into other techs of the same era
- War exhation ticks are longer to give players more time to fight wars without being force peaced out
- Increased relevance on WE based on % land occupied and population occupied
- Using Chemical Weapons reduces infamy decay
- Officers are substantially more difficult to recruit in colonies
#### Battle Sizes
- Predictable sizes (no RnG), scale linearly with tech and consideration for outnumbering enemy (not true in 1.5)
#### General Traits
- Nerfed the larger offense & defence skill traits by around half

## Flava
#### General JEs
- Corn laws market lib landowner leader event gone
- Nerfed arms ban event modifier
#### Europe
- Austria starts with serfdom
- Austrian flavor for Hungarian revolt as well as the ability to form Austria-Hungary after creating a Parliament
- Austria recieves German Confederation modifier until Germany forms 
- French historical pop nerf (there is no mortality multiplier, that is why there are two birth rate modifiers)
- French Language School added
- A crown in the gutter event chain to let Germany form early
- Made forming Gemrany easier
- Prussian-made Germany will not accept South German until it annexes either A-L or the entire Austrian Archduchy
- Added wine blight
- Added potato blight, includes brutal Irish famine event if Ireland is not incorporated
- Added Carlist Revolt at game start
- Russian revolts now begin as wars to prevent griefing
- Sardinia Piedmont buff
- Bosnian tools and arms now swapped for Eastern Thracian clothes
- Early game Netherlands journal entry for Belgium
- Russia has flavor with reformist Czar as well as decisions to annex AI Chinese land
- Scandinavia only requires Nationalism instead of Pan-Nat
- Italy formation adjusted to prevent exploit formation and make it more fun for MP (happens a bit sooner than IRL). San Marco also happens alongside the Hungarian Revolt. 
#### India
- Doctrine of Lapse decision can now annex your future puppets (Sindh, Sikh, Bhutan, etc) as well as your starting puppets
- New India breakup event
- New event to transfer Indian puppets if taken in a war
#### West Asia
- Tanzimat reforms rebalanced for higher difficulty of mod
- Combined Transjordan and Palestine (now properly called Transjordan) as well as Syrian States plus Lebanon so they are good
- Ottomans can now complete journal entry to accept ME cultures
#### East Asia
- Sumatra population increased by tenfold to reflect reality
- Unify China CB has max infamy decay (prevents using other infamy CBs whilst active)
- Complete China rework to increase difficulty and make nation possible for MP without it becoming a superpower
- Redid China collapse event
- Japan buff to make it more viable for MP (basically added ~10 years worth of iron and tools buildings)
- Afghanistan has panhandle in order for it to effectively serve as a buffer state
#### Africa
- Egypt has nominal subject penalty at game start so it can still join a custom union if desired
- Added Equatoria flavor to ensure Egypt can claim entire state within a reasonable time period
- East Africa has severe Malaria to prevent early colonization
- New Congo Event Chain during the Scramble that allows GPs to vote on the recipient of the Congo. This does not now but will spawn the Free State in the future when having colonial subjects is good. 
- Ahistorical journal entry for Africans to get a big boost after researching a certain number of techs
#### The Americas
- Reworked Reconstruction in the US - accepting either Dixie or AA will depend on how loyal they are at end of JE
- The US has an isolationism Journal Entry to limit US expansionism
- Argentina, Chile, and Paraguay get intial boost to colonization so they can take southern cone 
- Made certain Brazil journal entries easier for MP or adjusted them for HMPS
- Combined New England states; MA and CN; DC, MA, and DE; and Northeastern Brazilian states
- Cuba annexed at game start
- Gave all British subjects colonization laws
- Mexico can now accept natives with a decision

## Map
#### Resources
- Oil rebalance
#### State Modifiers
- Added Black Belt to represent Cretaceous soil
- Added areas that can easily do hydro power
- Cold water ports mod integrated
- Added MAPI to more rivers

## UI
- NGF, SGF, GER, KUK country colours more like vic2
- More decimals shown

## Stability/Bug Fixes
- Removed ability to pause/change speed without submod
- Fixed various base game errors
- Made all PMs that use electricity and transport require those goods to exist in the state
- Krakatoa event effect reduced
- Sepoy war does not give infamy
- Reduced rate of both radical and loyalist gain
- Canal companies no longer require occupancy or incorporation
- Added straits to Hokkaido
- Adjusted populating the Americas JE

---
<br/>

# Minor Changes Since the Last Workshop Update (7 October 2026)

## Political
- Exploit X Industry decrees now cost -0.5 SoL in the affected buildings (was -1)
- The Indirect Rule tooltip lists its effects per level of Colonial Affairs
- Player subjects (puppets, colonies and crown lands) no longer get the +10% bonus to enact laws imposed on them
- Stamp Out Monarchism no longer fires at game start or for countries that were not monarchies
- Stamp Out Theocracy is no longer cancelled by enacting Council Republic
- Removed the old extra acceptance modifier from embracing Ottomanism
- Age of Caudillos: when the armed forces side with the Liberals, the journal entry progress goes down by 100

## Population
- When any pops assimilate or convert, at least 20 do at a time (was 1)

## Tech
- Tech events that give research progress now default to the research option if the player does not choose in time; where an event has several research options, all of them are the default

## Economic
- Builders' Yards employ 5,000 workers per level: every Timber method includes 500 shopkeepers and 2,000 laborers, each production line 1,250 workers (machinists and engineers replace some laborers at higher tiers)
- Timber Yard uses 20 wood for 30 building materials; Laminated Timber uses 5 oil for 75 building materials
- Automation methods cut laborers: Water-tube Boiler (5 tools, 5 coal) cuts 1,500, Rotary Valve Engine (5 tools, 10 coal) cuts 2,000, and Assembly Lines (4 tools, 1 copper, 1 oil, 9 electricity, 2 rubber) cut 2,500 and need electricity. Automation is banned under the Industry Banned law, like vanilla
- Brick Clamps need Shaft Mining and use 10 stone and 5 wood; Hoffmann Kilns use 15 stone and 5 coal for 40 building materials
- Quarry Steam Automation (Hand Cranked Crane, Steam Donkey) uses 4 coal and cuts 1,000 laborers; top-tier quarries produce 215 stone
- Nitroglycerin quarry method produces 25 stone and has vanilla mine mortality (0.3 laborers, 0.2 machinists, 0.1 engineers)
- Steam Cutters employ 3,500 laborers and 1,000 machinists with no engineers, like the mine pump; quarry extraction methods no longer cause laborer mortality
- Construction methods employ 5,000 workers per level, keeping each method's worker mix: Timber Footings 5,000 laborers; Brick Footings 500 bureaucrats, 500 clerks, 750 machinists and 3,250 laborers; Concrete Foundations and Piles and Caissons 500 bureaucrats, 500 clerks, 750 machinists, 750 engineers and 2,500 laborers
- Steam Plant (Steam Donkey, era 3) uses 5 coal and cuts 1,750 laborers; Motorised Plant uses 5 oil and cuts 2,500 laborers
- The market capital sells 10 Building Materials
- New Stone and Brick Consortium company for Builders' Yards and Quarries
- The power bloc construction company can also build Builders' Yards
- Assembly line PMs (furniture, tooling, motor, arms, munition) use 1 more oil and 1 less rubber per worker than before
- Guano Harvestry employs 250 shopkeepers and 750 laborers per level (was 75 and 500), output unchanged; laid-off workers from a depleted deposit no longer become radicals
- Chincha Islands state trait is in Ica, where the guano deposit is, and gives +20% guano mine throughput (was +20% sulfur mine throughput, in Lima)
- Synthetic oil plants can no longer be built by private investors
- Railroad Bubble: Relief Works gives +3% wages for 12 months, "Regulate the exchanges" needs 75 legitimacy, and the Railway King appears in half of all bubbles
- Suez Canal Company only needs a level 5 trade center or port somewhere and no longer gives tax income when prosperous
- Specie Famines and Inflationary Periods can't start before 1 January 1837; a player-led market can roll for a Specie Famine in any month its balance-of-trade deficit is at least 4% of GDP
- Atacama Desert no longer has the -10% construction efficiency malus
- Reserve Currency holder gets +25% trade advantage (the same as Free Trade) at every tier, in place of +10% for imports and -10% for exports
- Inflationary Period: Money Supply Constricted no longer gives -10% wages, and adds +3% loan interest (was +2%)
- The Taj Mahal's second production method was removed
- Artillery Foundry and Basic Port take less input to offset building materials upkeep: Bronze Cannons use 10 hardwood (was 15), Bronze Smoothbores 15 (was 20), and Basic Port clippers 4 (was 6)
- Construction Fittings: Bare Finish gives no construction points; its 0.5 moves into the Foundations methods (Timber 2.0, Brick and Lime 5.0, Concrete 8.0, Piles and Caissons 11.0). Windows and Pipes gives 2.0 points and Electric Lifts 4.0, so each era's best combination keeps the same total. Construction sector throughput shows one decimal place, so the 0.5% Fittings steps are visible

## Diplomacy
- Regional investment rights tooltip clarified: the investor can build only in the chosen state but can buy privatized buildings anywhere in the country
- Revanchism fixes, including state transfers
- Subjects no longer pass infamy to their overlord while in a diplomatic play or war against it (e.g. independence), and infamy gained during a rebellion is never passed on later

## Military
- Forts that are not naval forts no longer add blockade resistance
- Military Airships (event now fires on Military Aviation, era 5, instead of Zeppelins, era 4), the War Hero fighter general and Montenegro's "Rifles" option give +10% army offense instead of flat offense (was +30, +30 and +10); Rifles also gives +10% defense (was +10 flat)

## Flava
- Initiate Manifest Destiny also claims Colorado, so the USA can still take it if Mexico colonizes it first; Repudiate Manifest Destiny removes that claim. Texas no longer starts with a claim on New Mexico
- Paraguay starts with the Frontier Colonization law, and Paraguay and Bolivia start with claims on Alto Paraguay (the Gran Chaco)
- Colombia starts with a claim on Antioquia, so it can colonize the one province there held by the Wayuu
- Peru and Bolivia start with level 2 trade centers in Lima, Cajamarca, Ica and La Paz; Bolivia also starts with them in Potosí and Antofagasta, and South Peru in Arequipa and Tarapacá
- Russian Alaska can no longer colonize California from Fort Ross: the Fort Ross state starts with a "Fort Ross Trading Post" modifier (-100% colony growth speed) that ends when the Fort Ross sale event transfers the post
- Russian-American Company starts with a one-line infantry battalion in Alaska, in an army called "Sitka Garrison"
- Russia's Great Reformer "Army Modernization" requirement now also accepts Partial Conscription, alongside Volunteer Only and Mass Conscription
- Peru-Bolivian Confederation: Bolivia no longer annexes North and South Peru on day 1; they start as its puppets, as in vanilla. Bolivia must keep legitimacy over 50 and hold its subjects for 5 years to complete it (was 10 years)
- The Fall of Salaverry event is now sent only to AI South American countries; players no longer get it (was sent to players too)
- The Spanish Lake (Spain's Our American Empire journal entry reward) gives +20% income from subjects and -5% subject liberty desire, on top of vanilla's +20% prestige and +20% authority

## Map
- Guano deposits: in 1836 only Peru's coast is known (Ica 30 known + 20 hidden, Cajamarca 10 + 10, Lima 10, Tarapacá 10 + 10). Everything else starts hidden: Antofagasta, Baja California, Namaqualand, Haiti, Santo Domingo, Bahamas, West Indies, Puerto Rico, West Micronesia and Nauru 10 each; East Micronesia 15; Oman 5; Hawaiian Islands 10; Tahiti 10; Western Australia 10; Jamaica 5; Honduras 5; Queensland 5; Cape Colony 5; Patagonia 5. Total 275 levels. Worked deposits run out at 75% of the vanilla gold-field rate
- Added Malaria to eight Amazon states: Guayana, Guaviare, Pastaza, Santa Cruz, Pará, Amazonas, Acre and Mato Grosso
- Pacific islands have severe malaria again: Micronesia, Solomon Islands, Nauru, Fiji, Vanuatu, New Caledonia, Bougainville, Tahiti and Tonga
- York Factory now starts owned by the Hudson's Bay Company instead of the Innu and Cree; in exchange, a neighbouring province goes from the Hudson's Bay Company to the Innu and Cree
- Spain's mineral resources redistributed between its states
- Ingria no longer has a cold water port
- Cuba has hardwood
- Removed Pará's four isolated Brazilian fort enclaves in Amazonas. Each province now belongs to the native nation around it: Rio Branco to ORN, two Rio Negro and central provinces to TKN, and the Tabatinga area to AMZ. Pará keeps its river block toward Barra (Manaus)
- Starting quarries are spread across each market's quarrying districts instead of piling onto the first-listed states (each market's total unchanged except the Netherlands); Wales starts with 2 levels as Britain's slate district, and Madras and Saxony each gain a starting quarry; the Netherlands has exactly 1 quarry level in Gelre (was 2), so Dutch stone starts at +15% instead of -50%; Greece (Attica, Pentelic marble) and the Papal States (Lazio, Tivoli travertine) each start with 1 quarry, so their builders' yards fire clamp brick instead of standing idle

- Oil Rush and Limited Oil Rush state modifiers now use vanilla values: migration pull +100% / +50%, oil rig throughput +20% / +10%, oil rig jobs +50% / +25%; Oil Rush also gives -1 standard of living and +20% mortality in oil rigs
## UI
- Technology Research Speed tooltip shows one decimal place (e.g. +2.5% instead of +2%)
- Trade partner lists show the value of trade instead of the quantity
- The GM no longer gets leverage alerts about AI countries
- The market panel's "Inflationary Period Possible" warning is yellow
- The topbar Balance of Trade number is green when the balance is within 1% of GDP either way (no modifier applies); it is red at -4% or lower, yellow at +4% or higher, and white in between. The market panel's "Trade is balanced: no effect" line is green to match
- Ledger Markets list: Imports column comes before Exports, number columns are centered, and "Net exports" is renamed "Balance" so the header is no longer cut off
- Ledger Markets list: clicking the Imports, Exports or Balance header sorts by that column (first click largest first, second click smallest first); the sorted order refreshes weekly
- The market panel's "Specie Famine Possible!" warning no longer shows for the Reserve Currency holder once it has researched Mutual Funds, as it is immune to Specie Famines
- Reserve Currency tooltips (market panel and alert) list the top 5 importing markets that could hold it, ranked monthly, with the holder's and challengers' months marked, plus your market's weekly imports. The market panel says "(you)" when you hold it

## Stability/Bug Fixes
- Fixed the Oregon journal entry re-adding the US claim on Idaho, Oregon and Washington every month
- Fixes to the Congo vote and the Scramble for Africa events
- Fixed script errors in the Russian tsar events and the ACW segregation events; removed an unreachable Spanish event
- Vanilla 1.15 follow-ups: failing the Sick Man of Europe journal entry now gives the Dead Man of Europe modifier and starts the Great Eastern Crisis journal entry (a main failure also removes the Rumelian tradition from Albanian, Bosniak and Sephardic cultures); the West America journal entry no longer blocks the Oregon Trail event; Pot Stills give +10 groceries (was +15), because vanilla added glass and copper inputs; Electric Lifts no longer use electricity and now take 10 glass, 5 hardwood, 5 lead, 5 steel, 5 copper and 5 engines, at the same cost
- Vanilla 1.15 drift sync: about 70 small differences from vanilla in laws, amendments, interest groups, journal entries, events, decrees, formable nations, characters, scripted effects and modifiers were brought up to date where vanilla changed them after HMPS last did; anything HMPS may have kept on purpose stays as it was
- The De Facto Capitulation event works again on 1.15: war support now runs from 0 to 100, so its check is at 0 (was -100) and its war support option adds 25 (was 50)
- Updated to vanilla 1.15.1: vanilla's 1.15.1 changes merged into HMPS (defines, armed forces, on actions, political movements, scripted triggers, static modifiers, two tooltip and right-click menu files, state region resource caps such as copper mines, and the Caucasian War journal entry text). HMPS's AI oil stance still starts at pumpjacks; the AI now also values radios and telephones, as in vanilla
