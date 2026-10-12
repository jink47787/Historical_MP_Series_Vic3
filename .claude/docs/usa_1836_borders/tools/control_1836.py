# Who actually controlled the ground on 1 January 1836, per Vic3 state region.
# Rules are (owner, polygon in lon/lat); first match wins, else the state's default.
# FOOTHOLDS override: the province containing the point goes to that owner.

# Vanilla tags that are defined but unused at the 1836 start; reused here instead of new tags.
REUSED_TAGS = {
    'CTF': 'Council of Three Fires: Ojibwe, with the Odawa, Nipissing, Algonquin, Mississauga, Saulteaux and Oji-Cree; the small Menominee and Ho-Chunk lands folded in',
}
NEW_TAGS = {
    'SFX': 'Sauk and Meskwaki (Ioway and Potawatomi lands folded in)',
    'OSG': 'Osage (Kansa lands folded in)',
    'CLF': 'Californian peoples (Yokuts, Miwok, Maidu, Pomo, Yuman; one aggregate tag)',
    'INU': 'Inuit (Arctic coast and islands, Nunavik, northern Labrador)',
    'INN': 'Innu and Bay Cree (Cree-Innu continuum: Innu, Naskapi, James Bay, Moose and Swampy Cree)',
}

R = {}

R['STATE_MICHIGAN'] = dict(default='USA', rules=[
    # Upper Peninsula: Ojibwe; ceded east of the Chocolay by the Treaty of Washington, 28 Mar 1836
    ('CTF', [(-90.6,45.9),(-90.6,47.7),(-83.8,47.7),(-83.3,46.1),(-84.6,45.95),(-86.0,45.6),(-87.7,45.05),(-88.2,45.9)]),
    # Northern Lower Peninsula: Odawa/Ojibwe, same 1836 treaty; no US settlement north of Saginaw/Grand River
    ('CTF', [(-87.2,43.15),(-85.2,43.25),(-84.15,43.95),(-83.2,44.05),(-82.6,45.6),(-84.6,45.95),(-87.2,45.9)]),
], footholds=[('USA',-84.62,45.85,'Fort Mackinac'),('USA',-84.35,46.50,'Fort Brady, Sault Ste. Marie')])

R['STATE_WISCONSIN'] = dict(default='CTF', rules=[
    # Ceded by 1836: south of the Fox-Wisconsin waterway (1829, 1832, 1833) and east of Fox/Green Bay (Menominee 1831)
    ('USA', [(-91.3,42.4),(-91.2,43.05),(-90.6,43.2),(-90.0,43.25),(-89.6,43.4),(-89.4,43.55),(-89.1,43.8),(-88.7,44.05),
             (-88.45,44.25),(-88.05,44.5),(-87.75,44.95),(-87.2,45.35),(-86.5,45.3),(-86.5,42.4)]),
])

R['STATE_MINNESOTA'] = dict(default='LKT', rules=[
    # 1825 Prairie du Chien Dakota-Ojibwe line: St Croix falls - Watab - Otter Tail Lake - Goose River
    ('CTF', [(-92.65,45.4),(-94.2,45.65),(-95.6,46.4),(-96.85,47.45),(-97.4,47.45),(-97.4,49.5),(-89.0,49.5),(-89.0,45.4)]),
])

R['STATE_IOWA'] = dict(default='SFX', rules=[
    # Black Hawk Purchase (1832, opened 1833), Half-Breed Tract and the 1830 Neutral Ground (federal buffer, Fort Crawford)
    ('USA', [(-91.4,40.38),(-92.2,40.6),(-91.85,41.6),(-92.0,42.5),(-93.3,42.9),(-93.3,43.6),(-91.0,43.6),(-90.0,42.5),(-90.1,41.5),(-91.0,40.5)]),
    # Dakota lands north-west of the 1830 Neutral Ground
    ('LKT', [(-96.8,42.3),(-95.5,42.3),(-94.2,42.9),(-93.0,43.3),(-92.4,43.6),(-96.8,43.6)]),
])

R['STATE_MISSOURI'] = dict(default='USA', rules=[
    # Platte country west of the 1821 line: Ioway and Sauk & Meskwaki of the Missouri until the 1836-37 Platte Purchase
    ('SFX', [(-94.45,39.12),(-94.45,40.62),(-96.0,40.62),(-96.0,39.12)]),
])

R['STATE_FLORIDA'] = dict(default='USA', rules=[
    # Second Seminole War (from Dec 1835): Seminole hold the peninsula south of the Withlacoochee / Fort King line
    ('SML', [(-83.0,28.85),(-82.6,29.15),(-81.7,29.15),(-81.0,28.85),(-79.0,28.85),(-79.0,24.3),(-83.0,24.3)]),
], footholds=[('USA',-82.46,27.94,'Fort Brooke (Tampa)'),('USA',-81.78,24.55,'Key West')])

R['STATE_KANSAS'] = dict(default='ARP', rules=[
    # Emigrant reserves under the 1834 Indian Intercourse Act: Shawnee, Delaware, Kickapoo, Wea/Piankashaw/Peoria, Ottawa
    # Cherokee Neutral Lands, Wea/Piankashaw/Peoria, Ottawa, Shawnee (to the Kansas River arm), Delaware, Kickapoo
    # settled belt only: the reserves ran ~120 miles west on paper, but the villages lay within ~40 miles of the Missouri line
    ('SEQ', [(-94.6,37.0),(-95.1,37.0),(-95.0,37.6),(-95.3,38.2),(-95.5,38.6),(-95.7,39.0),(-95.5,39.5),(-95.6,39.8),(-95.4,40.05),(-94.6,40.05)]),
    # Osage reserve (1825) and Kansa reserve up the Kansas River
    ('OSG', [(-95.1,37.0),(-98.3,37.0),(-98.5,38.3),(-98.0,38.75),(-98.0,39.4),(-96.75,39.5),(-95.7,39.6),(-95.5,39.5),(-95.7,39.0),
             (-95.5,38.6),(-95.3,38.2),(-95.0,37.6)]),
    # Pawnee hunting grounds on the Republican and Smoky Hill, south to the Arkansas (Pawnee Rock, Pawnee Fork)
    ('PWN', [(-96.75,39.5),(-95.8,39.5),(-95.8,40.05),(-100.4,40.05),(-100.1,39.5),(-100.4,39.0),(-99.9,38.6),(-100.0,37.75),(-98.8,38.36),(-98.5,38.3),(-98.0,38.75),(-98.0,39.4)]),
    # Kiowa/Comanche south of the Arkansas (Adams-Onis line west of 100W)
    ('COM', [(-98.3,37.0),(-102.1,37.0),(-102.1,38.05),(-100.0,37.75),(-98.8,38.36),(-98.5,38.3)]),
], footholds=[('USA',-94.92,39.35,'Fort Leavenworth')])

R['STATE_NEBRASKA'] = dict(default='ARP', rules=[
    # Pawnee, with Otoe-Missouria and Omaha (all under the Council Bluffs agency)
    ('PWN', [(-95.3,40.0),(-101.6,40.0),(-101.2,40.5),(-100.8,40.9),(-100.77,41.12),(-99.0,41.8),(-97.6,42.4),(-96.4,42.5),(-95.3,41.0)]),
    # Sandhills and the Niobrara: Lakota north of the North Platte, Arapaho and Cheyenne south of it
    ('LKT', [(-104.1,43.1),(-104.1,41.98),(-103.67,41.87),(-103.1,41.67),(-102.15,41.33),(-101.4,41.18),(-100.77,41.12),
             (-99.0,41.8),(-97.6,42.4),(-96.4,42.5),(-96.4,43.1)]),
])

R['STATE_SOUTH_DAKOTA'] = dict(default='LKT', rules=[])

R['STATE_NORTH_DAKOTA'] = dict(default='LKT', rules=[
    ('CTF', [(-100.5,48.4),(-99.6,48.1),(-98.8,47.85),(-98.3,47.75),(-97.6,47.55),(-96.8,47.3),(-96.5,47.4),(-96.5,49.1),(-100.5,49.1)]),   # Pembina and Turtle Mountain, north of the Sheyenne
    ('IRC', [(-104.1,47.6),(-101.5,47.9),(-100.5,48.4),(-100.5,49.1),(-104.1,49.1)]), # Assiniboine
])

R['STATE_MONTANA'] = dict(default='ABS', rules=[
    ('SLS', [(-116.1,49.1),(-114.0,49.1),(-113.3,48.3),(-112.4,47.1),(-112.2,46.6),(-112.5,46.0),(-113.0,45.6),(-113.95,45.69),(-114.6,45.5),(-116.1,46.0)]),
    ('BNN', [(-113.95,45.69),(-113.0,45.6),(-111.6,45.6),(-111.1,44.4),(-114.0,44.4)]),
    ('BLF', [(-114.0,49.1),(-107.6,49.1),(-107.3,48.35),(-107.6,47.65),(-108.3,47.3),(-109.5,47.0),(-110.5,46.6),(-111.6,45.6),(-112.5,46.0),(-112.2,46.6),(-112.4,47.1),(-113.3,48.3)]),
    ('IRC', [(-107.6,49.1),(-104.0,49.1),(-104.0,48.0),(-104.8,48.12),(-105.6,48.09),(-106.5,47.95),(-107.6,47.65),(-107.3,48.35)]),   # Assiniboine east of Frenchman Creek, north of the Missouri
    ('LKT', [(-104.0,48.0),(-105.0,47.0),(-105.9,46.2),(-106.1,45.0),(-105.8,44.4),(-105.3,43.8),(-104.9,43.0),(-103.5,43.0),(-103.5,48.0)]),   # east of the Powder River (Little Missouri, Belle Fourche)
])

R['STATE_WYOMING'] = dict(default='ARP', rules=[
    ('BNN', [(-111.1,41.0),(-111.1,45.0),(-110.0,45.0),(-109.5,44.0),(-108.5,43.3),(-107.2,42.6),(-107.6,42.1),(-107.3,41.6),(-107.5,41.0)]),   # Shoshone, west of the Great Divide basin
    ('LKT', [(-104.0,48.0),(-105.0,47.0),(-105.9,46.2),(-106.1,45.0),(-105.8,44.4),(-105.3,43.8),(-104.9,43.0),(-103.5,43.0),(-103.5,48.0)]),   # Black Hills west slope, Belle Fourche
    ('ABS', [(-110.0,45.0),(-104.05,45.0),(-104.05,44.6),(-105.6,44.2),(-106.3,43.3),(-107.2,42.6),(-108.5,43.3),(-109.5,44.0)]),
])

R['STATE_COLORADO'] = dict(default='ARP', rules=[
    ('BNN', [(-109.1,40.45),(-109.1,41.1),(-107.5,41.1),(-107.4,40.8),(-107.6,40.5)]),   # Shoshone in the Little Snake country, north of the Yampa
    ('UTE', [(-109.05,37.0),(-109.05,40.45),(-108.0,40.5),(-107.3,40.45),(-106.85,40.3),(-106.2,40.3),(-105.8,40.25),(-105.3,40.0),
             (-105.2,38.8),(-105.0,38.0),(-105.0,37.0)]),   # south of the Yampa; North Park is Arapaho ground
    ('COM', [(-105.0,37.0),(-102.04,37.0),(-102.04,38.05),(-103.6,38.08),(-104.6,38.25),(-105.0,38.4)]),
])

R['STATE_OKLAHOMA'] = dict(default='COM', rules=[
    # settled Cherokee, Creek and Choctaw country; the Chickasaw district stayed empty until 1837
    ('SEQ', [(-94.4,33.6),(-96.3,33.8),(-96.4,34.4),(-96.2,35.0),(-96.4,35.5),(-96.3,36.0),(-96.1,36.5),(-96.2,37.0),(-94.6,37.0),(-94.4,35.4)]),
    ('OSG', [(-96.2,37.0),(-96.1,36.5),(-96.3,36.0),(-96.4,35.5),(-97.2,35.4),(-98.0,35.6),(-98.6,36.0),(-98.9,36.7),(-99.0,37.0)]),   # Osage hunting grounds north of the Canadian; Clermont's band on the Verdigris
])

R['STATE_TEXAS'] = dict(default='COM', rules=[
    ('MEX', [(-106.7,31.6),(-106.0,31.2),(-105.6,31.0),(-105.9,31.9),(-106.7,32.0)]),                       # El Paso valley
    ('MEX', [(-97.15,25.9),(-99.6,27.0),(-100.3,28.3),(-99.5,28.6),(-98.4,28.4),(-97.6,27.9),(-97.2,27.6)]),  # Nueces strip, Laredo
    ('TEX', [(-93.6,29.7),(-97.2,27.6),(-97.6,27.9),(-98.4,28.4),(-98.9,29.3),(-98.3,29.8),(-97.7,30.5),(-97.3,31.3),
             (-96.4,31.9),(-95.9,32.5),(-96.0,33.1),(-95.6,33.9),(-94.0,33.9),(-93.9,32.0),(-93.5,30.0)]),
    ('APC', [(-106.7,32.1),(-103.95,32.1),(-103.95,32.0),(-103.49,31.42),(-102.4,31.06),(-101.82,30.69),(-101.56,29.8),(-101.36,29.70),
             (-102.5,29.0),(-103.2,28.9),(-104.6,29.4),(-106.7,31.6)]),  # Mescalero/Lipan, west of the Pecos
], footholds=[('MEX',-106.35,31.68,'El Paso valley (Ysleta, Socorro, San Elizario)')])

R['STATE_NEW_MEXICO'] = dict(default='APC', rules=[
    ('UTE', [(-109.1,37.1),(-109.1,36.7),(-108.6,36.62),(-108.0,36.55),(-107.5,36.45),(-107.0,36.45),(-106.7,36.8),(-106.6,37.1)]),   # Capote and Weeminuche Ute: San Juan basin north of the river, upper Chama
    ('MEX', [(-107.3,33.9),(-106.4,33.9),(-106.2,34.6),(-105.9,35.0),(-104.9,35.0),(-104.9,35.6),(-105.3,36.0),(-105.3,36.8),
             (-106.4,36.8),(-106.8,36.2),(-107.4,35.3),(-107.7,34.8),(-107.3,34.4)]),
    ('MEX', [(-107.4,33.95),(-106.5,33.95),(-106.6,33.0),(-106.3,32.0),(-106.75,31.9),(-107.1,32.6),(-107.4,33.3)]),  # Camino Real, Socorro to El Paso
    ('NVJ', [(-109.05,34.8),(-109.05,37.0),(-106.9,37.0),(-106.8,36.2),(-107.4,35.3),(-107.7,34.8)]),
    ('COM', [(-103.95,31.9),(-104.23,32.42),(-104.4,32.84),(-104.45,33.39),(-104.24,34.47),(-104.68,34.94),(-104.9,35.6),(-104.9,37.1),(-102.9,37.1),(-102.9,31.9)]),  # east of the Pecos
])

R['STATE_ARIZONA'] = dict(default='APC', rules=[
    ('MEX', [(-111.4,31.33),(-110.7,31.33),(-110.6,31.8),(-110.6,32.35),(-111.0,32.45),(-111.2,32.4),(-111.25,31.9)]),   # Santa Cruz valley: Tucson, San Xavier, Tubac
    ('MEX', [(-113.1,31.33),(-111.4,31.33),(-111.2,32.4),(-110.9,32.6),(-111.4,33.4),(-112.6,33.4),(-113.3,32.8),(-113.05,32.45),(-113.35,32.1),(-113.1,31.6)]),  # O'odham (CCM option)
    ('NVJ', [(-109.05,34.8),(-109.05,37.0),(-112.0,37.0),(-111.8,36.0),(-111.6,35.3),(-110.0,34.9)]),
    # River Yumans (Mohave, Halchidhoma, Quechan, Maricopa) on the lower Colorado and lower Gila
    ('CLF', [(-115.0,31.0),(-113.1,31.0),(-113.1,31.6),(-113.35,32.1),(-113.05,32.45),(-113.3,32.8),(-113.6,33.4),(-114.0,34.3),(-113.8,35.2),(-114.1,36.1),(-115.0,36.1)]),
    ('UTE', [(-114.1,36.1),(-113.5,36.2),(-112.9,36.35),(-112.3,36.25),(-111.9,36.4),(-112.0,37.05),(-114.1,37.05)]),   # Arizona Strip, north of the Grand Canyon: Kaibab Southern Paiute
    # default APC: Western Apache, with the Yavapai and Pai uplands
])

R['STATE_UTAH'] = dict(default='UTE', rules=[
    ('NVJ', [(-110.9,37.0),(-109.05,37.0),(-109.05,37.35),(-109.6,37.3),(-110.2,37.25),(-110.7,37.15)]),   # south of the San Juan
    ('BNN', [(-114.1,38.15),(-114.1,42.0),(-111.05,42.0),(-111.05,41.0),(-112.3,40.5),(-112.9,39.3),(-113.4,39.2),(-113.6,38.7),(-113.85,38.3)]),   # Shoshone and Goshute, with Snake Valley
])

R['STATE_NEVADA'] = dict(default='BNN', rules=[
    ('CLF', [(-115.0,34.9),(-114.0,34.9),(-114.0,35.9),(-114.5,35.6),(-114.8,35.2)]),   # Mohave, along the Colorado at Nevada's southern tip
    ('UTE', [(-116.0,35.0),(-114.0,35.0),(-114.0,38.1),(-115.4,37.8),(-115.9,36.5)]),   # Southern Paiute, Las Vegas and Moapa
])

R['STATE_CALIFORNIA'] = dict(default='CLF', rules=[
    # Mission, presidio, pueblo and rancho belt, San Diego to Sonoma
    ('MEX', [(-116.7,32.53),(-116.5,33.0),(-116.7,33.6),(-117.0,34.1),(-117.6,34.45),(-118.4,34.65),(-119.0,34.75),(-119.6,34.95),
             (-120.1,35.3),(-120.4,35.95),(-121.0,36.6),(-121.3,37.1),(-121.6,37.7),(-121.7,38.1),(-122.3,38.6),
             (-122.9,38.6),(-123.5,38.0),(-122.0,35.5),(-118.5,32.5)]),
    # Great Basin peoples east of the Sierra crest: Modoc and Klamath, Northern Paiute, Washoe, Owens Valley Paiute, Panamint Shoshone
    ('BNN', [(-121.6,42.05),(-121.6,41.6),(-121.3,41.0),(-120.9,40.4),(-120.3,39.6),(-120.2,39.2),(-119.9,38.6),(-119.6,38.2),
             (-119.2,37.6),(-118.7,37.0),(-118.3,36.3),(-118.0,35.7),(-117.3,35.5),(-116.6,35.5),(-115.0,35.9),(-115.0,42.05)]),
])

R['STATE_OREGON'] = dict(default='SLS', rules=[
    ('CLF', [(-124.6,41.9),(-124.6,42.25),(-124.2,42.3),(-123.7,42.15),(-123.2,42.15),(-122.6,42.25),(-122.3,42.1),(-122.3,41.9)]),   # Tolowa-Chetco and Shasta, astride the 42nd parallel
    ('ORG', [(-123.3,46.25),(-121.9,45.75),(-122.2,45.3),(-122.6,44.4),(-123.3,44.4),(-123.5,45.0),(-123.5,46.0)]),
    # Sahaptin and Nez Perce on the Columbia plateau, south to the Blue Mountains and the John Day
    ('NZP', [(-121.9,45.75),(-116.4,46.0),(-116.9,45.0),(-116.9,44.5),(-117.6,44.6),(-118.3,44.3),(-119.3,44.0),
             (-120.5,44.2),(-121.4,44.5),(-121.8,44.9),(-122.0,45.3)]),
    # Northern Paiute and Klamath country east of the Cascade crest
    ('BNN', [(-122.4,41.9),(-116.4,41.9),(-116.4,46.0),(-121.9,45.75),(-122.0,45.3),(-121.9,44.4),(-122.1,43.4),(-122.3,42.6)]),
])

R['STATE_WASHINGTON'] = dict(default='SLS', rules=[
    # HBC Columbia core: Fort Vancouver, Cowlitz, Fort Nisqually and the Puget lowland north to Fort Langley
    ('ORG', [(-123.3,46.25),(-121.9,45.6),(-121.9,46.2),(-122.0,47.3),(-121.75,47.75),(-121.95,48.2),(-121.7,48.6),(-121.9,49.05),(-122.8,49.05),(-122.5,47.9),(-122.9,47.3),(-123.2,46.8)]),
    ('NZP', [(-121.9,45.6),(-116.9,46.0),(-117.0,47.1),(-117.8,47.05),(-118.6,46.9),(-119.6,46.95),(-120.3,47.3),(-121.3,47.2),(-121.9,46.2)]),
])

R['STATE_IDAHO'] = dict(default='BNN', rules=[
    ('SLS', [(-117.3,46.6),(-117.3,49.1),(-115.9,49.1),(-114.3,47.6),(-114.4,46.6),(-115.0,46.95),(-115.9,47.1),(-116.6,47.0)]),   # Coeur d'Alene, Kalispel, Kootenai
    ('NZP', [(-117.3,44.3),(-116.5,44.9),(-115.8,45.15),(-114.9,45.3),(-114.4,45.6),(-114.6,46.0),(-114.4,46.6),
             (-115.0,46.95),(-115.9,47.1),(-116.6,47.0),(-117.3,46.6)]),   # Clearwater and lower Salmon
])

R['STATE_MAINE'] = dict(default='USA', rules=[
    # Madawaska / upper St John: administered from New Brunswick in 1836 (disputed until 1842)
    ('NBS', [(-69.4,47.6),(-69.3,47.3),(-68.9,47.12),(-68.3,47.05),(-67.75,46.95),(-67.75,47.6)]),   # the St John valley settlements
])

# Existing-tags-only fallback (variant A)
FALLBACK_A = {'CTF':'USA','SFX':'USA','OSG':None,'CLF':'MEX'}
# OSG in variant A: Kansas part -> PWN north / COM south handled by re-running without OSG rules

# ---------------------------------------------------------------- British North America
# HBC control was commercial: it governed only the Red River settlement and its posts. So the HBC holds the
# Red River parishes and its Bay and lake posts as enclaves;
# Cree country goes to the Iron Confederacy (IRC, Cree-Assiniboine), Ontario's Ojibwe and Oji-Cree to CTF,
# the Quebec James Bay Cree to the Innu (INN), the Mackenzie basin to the Dene (ATB), the Arctic to the Inuit.

R['STATE_ONTARIO'] = dict(default='CTF', rules=[
    # Hudson Bay Lowland: Swampy and Moose Cree (Omushkegowuk), with the James Bay Cree across the bay
    ('INN', [(-91.5,57.3),(-91.5,55.0),(-89.0,54.5),(-86.5,53.3),(-84.5,51.8),(-82.5,50.5),(-80.5,49.9),(-79.4,49.9),
             (-79.4,53.5),(-82.0,55.5),(-86.0,57.0)]),
    # Upper Canada: settled townships, Huron Tract, Lake Simcoe, lower Ottawa valley
    ('ONT', [(-83.6,41.5),(-83.0,43.1),(-81.8,43.6),(-81.8,44.1),(-81.0,44.35),(-80.5,44.65),(-79.9,44.95),(-79.2,44.8),
             (-78.3,44.75),(-77.4,45.0),(-76.8,45.35),(-77.3,45.9),(-74.0,45.9),(-74.0,43.0)]),
    # Anishinaabe: Great Lakes basin up to the Hudson Bay height of land, plus Rainy Lake / Lake of the Woods
    ('CTF', [(-95.3,48.3),(-95.3,50.3),(-92.0,50.3),(-90.0,50.0),(-88.5,50.2),(-86.0,49.5),(-84.0,48.9),(-81.5,48.0),
             (-79.6,48.3),(-79.6,45.9),(-77.3,45.9),(-76.8,45.35),(-77.4,45.0),(-78.3,44.75),(-79.2,44.8),(-79.9,44.95),
             (-80.5,44.65),(-81.0,44.35),(-81.8,44.1),(-83.0,45.0),(-84.5,46.0),(-89.0,47.5)]),
    ('CTF', [(-79.7,45.8),(-79.7,48.3),(-74.0,48.3),(-74.0,45.8)]),   # upper Ottawa (Algonquin, Nipissing)
], footholds=[('HBC',-87.63,56.0,'Severn House'),('HBC',-81.67,52.2,'Fort Albany'),('HBC',-80.62,51.26,'Moose Factory')])

R['STATE_QUEBEC'] = dict(default='INN', rules=[
    # Lower Canada: seigneuries and townships of the St Lawrence valley, Gaspe coast
    ('QUE', [(-77.3,45.9),(-76.0,46.3),(-74.5,46.4),(-73.0,46.7),(-72.0,47.0),(-71.2,47.15),(-70.5,47.45),(-69.7,48.2),
             (-69.4,48.1),(-68.0,48.75),(-66.0,49.3),(-64.2,49.1),(-63.5,48.5),(-64.0,47.5),(-67.0,47.0),(-71.0,44.9),(-74.8,44.9)]),
    # Algonquin (Anishinaabe): Temiscamingue, Abitibi south, upper Gatineau
    ('CTF', [(-79.6,45.9),(-79.6,48.5),(-78.5,48.2),(-77.6,48.4),(-77.0,48.2),(-76.0,48.0),(-75.0,48.5),(-73.5,47.6),(-73.0,46.7),(-74.5,46.4),(-76.0,46.3),(-77.3,45.9)]),   # south of the Hudson Bay height of land
    # Nunavik
    ('INU', [(-82.5,55.6),(-82.5,63.0),(-60.0,63.0),(-63.5,58.8),(-66.0,58.3),(-69.5,57.3),(-73.0,55.0),(-76.5,56.0)]),
], footholds=[('HBC',-78.75,51.49,'Rupert House'),('HBC',-78.52,52.25,'Eastmain'),('HBC',-79.0,53.83,'Fort George'),
                ('HBC',-68.4,58.1,'Fort Chimo (1830)')])

R['STATE_NEWFOUNDLAND'] = dict(default='INN', rules=[
    # Newfoundland island
    ('GBR', [(-59.6,47.4),(-52.3,46.4),(-52.3,50.0),(-55.4,51.75),(-56.2,51.65),(-57.6,50.6),(-59.6,48.5)]),
    # Southern Labrador fishing coast, Strait of Belle Isle to Hamilton Inlet
    ('GBR', [(-57.3,51.35),(-55.4,52.2),(-55.4,53.6),(-57.2,54.35),(-58.4,54.0),(-57.9,53.0),(-57.7,51.4)]),
    # Northern Labrador coast (Moravian missions among the Inuit)
    ('INU', [(-61.3,54.3),(-57.2,54.35),(-57.0,61.0),(-65.0,61.0),(-64.6,58.5),(-62.8,56.5),(-61.8,55.2)]),
])

# Cree / Chipewyan and Beaver line: Lesser Slave Lake, the lower Athabasca, the Churchill River, the Nejanilini country
CREE_CHIPEWYAN = [(-120.1,53.2),(-118.0,53.3),(-116.8,54.3),(-115.8,55.6),(-114.5,56.2),(-113.0,56.6),(-111.5,57.0),(-110.0,57.3),
                  (-108.5,57.0),(-107.0,56.6),(-105.0,56.3),(-103.0,56.6),(-102.0,57.0),(-100.5,57.6),(-98.5,58.2),(-96.5,58.5),
                  (-95.6,58.9),(-95.6,61.0),(-120.1,61.0)]

R['STATE_MANITOBA'] = dict(default='IRC', rules=[
    # Red River settlement: the river-lot parishes on the Red and Assiniboine (the 50-mile District of Assiniboia of 1835 was a claim)
    ('HBC', [(-97.25,49.55),(-97.0,49.55),(-96.95,49.85),(-96.8,50.15),(-96.75,50.42),(-96.95,50.42),(-97.05,50.15),(-97.1,50.0),
             (-97.6,50.0),(-97.65,49.88),(-97.2,49.85)]),
    ('ATB', CREE_CHIPEWYAN),   # Chipewyan
    ('IRC', [(-102.1,48.9),(-98.6,48.9),(-98.6,50.4),(-99.6,51.2),(-100.6,52.6),(-102.1,53.1)]),   # Plains Cree, Assiniboine, Saulteaux
    ('CTF', [(-97.2,48.9),(-95.0,48.9),(-95.0,50.7),(-96.9,50.7),(-96.8,50.4),(-97.15,49.7)]),       # Ojibwe east of the Red River, Winnipeg River
    ('CTF', [(-96.9,50.7),(-96.6,53.6),(-95.6,54.5),(-94.5,54.75),(-93.3,54.55),(-92.2,54.9),(-91.0,54.7),(-89.0,55.0),(-89.0,50.7)]),        # Oji-Cree east of the York boat route (Island Lake, God's Lake)
    ('INN', [(-95.6,54.5),(-95.5,55.5),(-96.0,56.5),(-95.6,57.5),(-95.0,58.6),(-93.5,59.2),(-89.0,59.0),(-89.0,55.0),(-91.0,54.7),(-92.2,54.9),(-93.3,54.55),(-94.5,54.75)]),   # Swampy Cree of the lowland and the Bay coast        # Swampy Cree of the Hudson Bay Lowland (Oxford House, Shamattawa)
], footholds=[('HBC',-94.17,58.77,'Churchill'),('HBC',-92.4,57.0,'York Factory'),('HBC',-97.83,53.98,'Norway House'),
               ('HBC',-97.13,49.89,'Upper Fort Garry, St Boniface'),('HBC',-96.93,50.25,'Lower Fort Garry, St Andrews'),
               ('HBC',-97.53,49.92,'White Horse Plain (St Francois Xavier)'),('HBC',-97.12,49.65,'St Norbert, St Agathe')])

R['STATE_SASKATCHEWAN'] = dict(default='IRC', rules=[
    ('BLF', [(-110.1,48.9),(-107.6,48.9),(-107.9,49.5),(-108.7,49.9),(-109.6,50.7),(-110.1,50.9)]),   # Gros Ventre and Blackfoot: Cypress Hills, west of the Frenchman
    ('ATB', CREE_CHIPEWYAN),   # Chipewyan north of the Churchill River
])

R['STATE_ALBERTA'] = dict(default='IRC', rules=[
    ('BLF', [(-120.1,48.9),(-110.0,48.9),(-110.0,52.7),(-111.0,52.5),(-112.2,52.2),(-113.3,52.25),(-114.4,52.0),(-115.5,51.8),(-120.1,52.3)]),   # north to the Battle and Red Deer
    ('ATB', CREE_CHIPEWYAN),   # Beaver (Dane-zaa) and Chipewyan; Cree south to Fort Edmonton and Lesser Slave Lake
])

R['STATE_BRITISH_COLUMBIA'] = dict(default='ATB', rules=[
    ('ORG', [(-123.3,49.0),(-122.0,49.0),(-121.4,49.2),(-121.5,49.4),(-122.3,49.3),(-123.0,49.35),(-123.3,49.2)]),   # Fort Langley, lower Fraser
    # Interior Salish (Secwepemc, St'at'imc, Nlaka'pamux, Okanagan) and Ktunaxa; Tsilhqot'in and Dakelh to the north are Dene
    ('SLS', [(-129.5,48.2),(-114.0,48.2),(-114.0,50.4),(-116.2,51.2),(-117.6,51.9),(-118.7,52.6),(-119.6,52.9),(-120.4,52.6),
             (-121.6,52.6),(-122.4,52.3),(-122.6,51.6),(-123.6,51.15),(-125.0,51.1),(-126.2,51.7),(-127.3,52.4),(-128.5,51.6),(-129.5,50.5)]),
    ('SLS', [(-134.0,51.0),(-127.5,51.0),(-126.9,51.9),(-127.4,52.6),(-127.0,53.2),(-128.0,54.0),(-128.6,54.6),(-129.0,55.0),(-130.0,56.2),(-134.0,56.2)]),  # Northwest Coast (Haida, Tsimshian, Heiltsuk), aggregate
])

R['STATE_YUKON_TERRITORY'] = dict(default='ATB', rules=[
    ('INU', [(-141.5,69.4),(-139.5,69.2),(-138.0,68.95),(-136.6,68.6),(-135.5,68.2),(-134.5,68.0),(-133.0,68.0),(-130.0,68.3),(-130.0,71.5),(-141.5,71.5)]),   # Inuvialuit, incl. the Mackenzie delta
])

R['STATE_NORTHWEST_TERRITORIES'] = dict(default='ATB', rules=[
    # Inuvialuit and Copper Inuit: the coast and the tundra north of the treeline (TREELINE_INU, defined below)
])

# Treeline (approx.): Inuit on the tundra to the north and east, Dene in the forest to the south and west
TREELINE_INU = [(-141.0,68.3),(-137.0,68.3),(-133.0,68.3),(-128.0,67.6),(-122.0,66.9),(-116.0,65.6),(-111.0,64.4),(-106.0,63.2),(-102.0,61.8),(-98.0,60.6),(-95.0,59.9),(-60.0,59.9),(-60.0,84.0),(-141.0,84.0)]

R['STATE_NUNAVUT'] = dict(default='ATB', rules=[('INU', TREELINE_INU)])   # Chipewyan south-west of the treeline
R['STATE_NORTHWEST_TERRITORIES']['rules'].append(('INU', TREELINE_INU))

# Blocks joined to the owner's main territory by the shortest province path (contiguity)
CONNECT = [('MEX', 'STATE_NEW_MEXICO')]   # California needs no land link: it is coastal; HBC holds its posts as enclaves

# Starting claims added on top of vanilla (vanilla claims are kept as they are).
# A claim plus an interest in the strategic region stops other countries colonizing the region,
# so these keep each power's 1836 colonial claim to itself; see the proposal for the reasoning.
ADD_CLAIMS = {
    'STATE_MICHIGAN':   ['USA'],          # US sovereign territory; keeps Ontario/GBR from colonizing CTF land
    'STATE_WISCONSIN':  ['USA'],
    'STATE_IOWA':       ['USA'],
    'STATE_MAINE':      ['USA', 'NBS'],   # Aroostook / Madawaska dispute (settled 1842)
    'STATE_CALIFORNIA': ['MEX'],          # Alta California
    'STATE_NEVADA':     ['MEX'],
    # British North America: the colonies and the HBC keep their charter and licence areas to themselves
    'STATE_ONTARIO':    ['ONT'],
    'STATE_QUEBEC':     ['QUE'],
    'STATE_NEWFOUNDLAND': ['GBR'],
    'STATE_MANITOBA':   ['HBC'],          # Rupert's Land
    'STATE_SASKATCHEWAN': ['HBC'],
    'STATE_NUNAVUT':    ['HBC'],
    'STATE_NORTHWEST_TERRITORIES': ['HBC'],   # HBC exclusive licence to the 'Indian Territories' (1821)
    'STATE_YUKON_TERRITORY': ['HBC'],
}

# Historic 1836 boundaries drawn as dashed lines over the map (reference only; they change nothing in game).
# (label, colour, [(lon, lat), ...]); approximate where the source line follows a watershed.
HISTORIC_LINES = [
    ('Adams-Onis line (1819)', (120, 0, 0), [(-93.84,29.69),(-94.04,32.0),(-94.04,33.55),(-94.48,33.64),(-95.3,33.88),(-96.4,33.78),
        (-97.15,33.72),(-98.0,34.1),(-99.2,34.2),(-100.0,34.56),(-100.0,37.75),(-101.0,37.95),(-102.04,38.05),(-103.6,38.08),
        (-104.6,38.25),(-105.2,38.45),(-105.9,38.55),(-106.3,39.25),(-106.3,42.0),(-124.2,42.0)]),
    ('49th parallel (1818)', (120, 0, 0), [(-95.15,49.38),(-95.15,49.0),(-114.06,49.0)]),
    ('Oregon Country (joint occupation)', (150, 30, 120), [(-109.0,42.0),(-109.9,43.4),(-110.6,44.2),(-111.1,44.5),(-112.3,44.55),
        (-113.0,45.0),(-113.95,45.69),(-112.5,46.0),(-112.4,47.1),(-113.3,48.3),(-114.06,49.0),(-115.8,50.3),(-116.3,51.45),
        (-118.0,52.4),(-118.8,53.1),(-120.0,54.0),(-120.7,54.67),(-130.6,54.67)]),
    ("Rupert's Land (Hudson Bay watershed, approx.)", (90, 50, 10), [(-64.43,60.38),(-63.6,58.9),(-64.6,57.6),(-66.0,56.3),
        (-67.2,55.2),(-66.9,54.4),(-68.0,53.8),(-69.8,53.0),(-71.0,52.3),(-71.8,51.5),(-72.0,50.6),(-73.5,49.8),(-75.0,48.5),
        (-77.0,48.3),(-79.6,48.0),(-81.5,48.0),(-84.0,48.9),(-86.0,49.5),(-88.5,50.2),(-90.0,50.0),(-90.8,48.1),(-92.5,48.4),
        (-95.15,49.0),(-114.06,49.0),(-115.8,50.3),(-116.3,51.45),(-118.0,52.4),(-118.3,53.0),(-116.0,53.8),(-113.0,54.5),
        (-110.0,55.5),(-109.9,56.4),(-107.5,57.5),(-105.5,59.0),(-105.0,60.5),(-107.0,62.0),(-107.8,63.2),(-105.5,64.3),
        (-102.0,64.8),(-99.0,65.3),(-95.5,66.0),(-91.5,66.8),(-87.5,66.6),(-86.2,66.5)]),
    ('Maine: US claim', (0, 60, 140), [(-67.78,45.95),(-67.78,47.9),(-68.6,48.0),(-69.5,47.45),(-70.3,46.7),(-70.6,46.0)]),
    ('Maine: British claim', (140, 0, 0), [(-67.78,45.95),(-67.85,46.5),(-68.8,46.2),(-69.8,45.9),(-70.3,45.7)]),
    ('Nueces (limit of Mexican Texas)', (0, 90, 0), [(-97.4,27.85),(-97.9,28.05),(-98.6,28.3),(-99.4,28.45),(-99.9,28.75),(-100.3,29.6)]),
]

# Pacific Northwest options (see proposal). 'corridor' is the rule set above.
def _nisqually(R):
    wa = R['STATE_WASHINGTON']['rules']
    R['STATE_WASHINGTON']['rules'] = [('ORG', [(-123.3,46.25),(-121.9,45.6),(-121.9,46.2),(-122.2,47.3),(-122.9,47.3),(-123.2,46.8)])] + [r for r in wa if r[0] != 'ORG']
    R['STATE_BRITISH_COLUMBIA']['rules'] = [r for r in R['STATE_BRITISH_COLUMBIA']['rules'] if r[0] != 'ORG']
def _coast_tag(R):
    _nisqually(R)
    R['STATE_OREGON']['default'] = 'CHN'
    R['STATE_WASHINGTON']['rules'].insert(1, ('CHN', [(-125.0,46.0),(-123.3,46.25),(-123.2,46.8),(-122.95,47.3),(-123.0,48.2),(-125.0,48.6)]))
VARIANTS = {'corridor': lambda R: None, 'nisqually': _nisqually, 'coast_tag': _coast_tag}

# Optional variant: six more peoples that are folded into aggregates in the main proposal.
PLUS6_TAGS = {
    'CSC': 'Northwest Coast peoples, reusing the vanilla CSC tag (Haida, Tsimshian, Heiltsuk, Kwakwaka\'wakw, Nuu-chah-nulth)',
    'CHY': 'Cheyenne (split from the Arapaho)',
    'MHA': 'Mandan, Hidatsa and Arikara (Missouri River villages)',
    'CCM': 'O\'odham, reusing the vanilla CCM tag (Tohono and Akimel O\'odham)',
    'MNM': 'Menominee',
    'HCK': 'Ho-Chunk',
}
def _plus6(R):
    bc = R['STATE_BRITISH_COLUMBIA']['rules']
    bc[:] = [r for r in bc if not (r[0] == 'SLS' and r[1][0] == (-134.0, 51.0))]
    bc.insert(0, ('CSC', [(-134,56.2),(-130,56.2),(-129,55),(-127,53),(-126.5,51.8),(-124.8,50.6),(-125.0,49.9),(-124.8,48.7),(-126.5,48.3),(-134,48.3)]))
    for s in ('STATE_COLORADO', 'STATE_KANSAS', 'STATE_NEBRASKA'):
        R[s]['rules'].append(('CHY', [(-106.0,36.5),(-99.3,36.5),(-99.3,38.6),(-100.0,39.0),(-101.0,39.3),(-102.0,39.5),(-103.0,39.6),
                                      (-104.0,39.4),(-105.0,39.0),(-106.0,39.0)]))   # Bent's Fort country, Arkansas to the Smoky Hill
    R['STATE_NORTH_DAKOTA']['rules'].insert(0, ('MHA', [(-100.6,46.75),(-100.9,47.2),(-101.6,47.65),(-102.6,47.9),(-102.8,47.55),(-101.9,47.15),(-101.2,46.8)]))  # Missouri villages: Knife River, Fort Clark
    az = R['STATE_ARIZONA']['rules']
    i = [k for k, r in enumerate(az) if r[0] == 'MEX'][1]
    az[i] = ('CCM', az[i][1])
    wi = R['STATE_WISCONSIN']['rules']
    wi.append(('MNM', [(-89.6,44.2),(-88.5,44.25),(-88.0,44.6),(-87.6,45.1),(-88.1,45.8),(-89.6,45.4)]))
    wi.append(('HCK', [(-91.4,43.1),(-90.6,43.2),(-90.0,43.25),(-89.6,43.4),(-89.4,43.55),(-89.6,44.2),(-89.6,45.0),(-91.6,44.9),(-91.6,43.6)]))
VARIANTS['plus6'] = _plus6
