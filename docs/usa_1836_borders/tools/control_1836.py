# Who actually controlled the ground on 1 January 1836, per Vic3 state region.
# Rules are (owner, polygon in lon/lat); first match wins, else the state's default.
# FOOTHOLDS override: the province containing the point goes to that owner.

NEW_TAGS = {
    'OJB': 'Anishinaabe (Ojibwe, Odawa; Menominee and Ho-Chunk lands folded in)',
    'SFX': 'Sauk and Meskwaki (Ioway and Potawatomi lands folded in)',
    'OSG': 'Osage (Kansa lands folded in)',
    'CLF': 'Californian peoples (Yokuts, Miwok, Maidu, Pomo, Yuman; one aggregate tag)',
}

R = {}

R['STATE_MICHIGAN'] = dict(default='USA', rules=[
    # Upper Peninsula: Ojibwe; ceded east of the Chocolay by the Treaty of Washington, 28 Mar 1836
    ('OJB', [(-90.6,45.9),(-90.6,47.7),(-83.8,47.7),(-83.3,46.1),(-84.6,45.95),(-86.0,45.6),(-87.7,45.05),(-88.2,45.9)]),
    # Northern Lower Peninsula: Odawa/Ojibwe, same 1836 treaty; no US settlement north of Saginaw/Grand River
    ('OJB', [(-87.2,43.15),(-85.2,43.25),(-84.15,43.95),(-83.2,44.05),(-82.6,45.6),(-84.6,45.95),(-87.2,45.9)]),
], footholds=[('USA',-84.62,45.85,'Fort Mackinac'),('USA',-84.35,46.50,'Fort Brady, Sault Ste. Marie')])

R['STATE_WISCONSIN'] = dict(default='OJB', rules=[
    # Ceded by 1836: south of the Fox-Wisconsin waterway (1829, 1832, 1833) and east of Fox/Green Bay (Menominee 1831)
    ('USA', [(-91.3,42.4),(-91.2,43.05),(-90.6,43.2),(-90.0,43.25),(-89.6,43.4),(-89.4,43.55),(-89.1,43.8),(-88.7,44.05),
             (-88.45,44.25),(-88.05,44.5),(-87.75,44.95),(-87.2,45.35),(-86.5,45.3),(-86.5,42.4)]),
])

R['STATE_MINNESOTA'] = dict(default='LKT', rules=[
    # 1825 Prairie du Chien Dakota-Ojibwe line: St Croix falls - Watab - Otter Tail Lake - Goose River
    ('OJB', [(-92.65,45.4),(-94.2,45.65),(-95.6,46.4),(-96.85,47.45),(-97.4,47.45),(-97.4,49.5),(-89.0,49.5),(-89.0,45.4)]),
], footholds=[('USA',-93.18,44.89,'Fort Snelling')])

R['STATE_IOWA'] = dict(default='SFX', rules=[
    # Black Hawk Purchase (1832, opened 1833), Half-Breed Tract and the east end of the Neutral Ground
    ('USA', [(-91.4,40.38),(-92.2,40.6),(-91.85,41.6),(-92.0,42.5),(-92.3,43.1),(-92.3,43.6),(-91.0,43.6),(-90.0,42.5),(-90.1,41.5),(-91.0,40.5)]),
    # Dakota lands north-west of the 1830 Neutral Ground
    ('LKT', [(-96.8,42.3),(-95.5,42.3),(-94.2,42.9),(-93.0,43.3),(-92.4,43.6),(-96.8,43.6)]),
])

R['STATE_MISSOURI'] = dict(default='USA', rules=[])  # Platte strip: Ioway/Sauk until the 1836-37 Platte Purchase; kept USA (see notes)

R['STATE_FLORIDA'] = dict(default='USA', rules=[
    # Second Seminole War (from Dec 1835): Seminole hold the peninsula south of the Withlacoochee / Fort King line
    ('SML', [(-83.0,28.85),(-82.6,29.15),(-81.7,29.15),(-81.0,28.85),(-79.0,28.85),(-79.0,24.3),(-83.0,24.3)]),
], footholds=[('USA',-82.46,27.94,'Fort Brooke (Tampa)'),('USA',-81.78,24.55,'Key West')])

R['STATE_KANSAS'] = dict(default='ARP', rules=[
    # Emigrant reserves under the 1834 Indian Intercourse Act: Shawnee, Delaware, Kickapoo, Wea/Piankashaw/Peoria, Ottawa
    ('SEQ', [(-94.6,38.0),(-95.6,38.0),(-95.6,39.0),(-95.4,40.05),(-94.6,40.05)]),
    # Osage reserve (1825) and Kansa reserve
    ('OSG', [(-94.6,37.0),(-98.3,37.0),(-98.5,38.3),(-98.0,38.75),(-96.8,39.6),(-95.6,39.6),(-95.6,38.0),(-94.6,38.0)]),
    # Pawnee hunting grounds on the Republican and Smoky Hill
    ('PWN', [(-96.8,39.6),(-95.4,40.05),(-100.2,40.05),(-100.2,38.75),(-98.0,38.75)]),
    # Kiowa/Comanche south of the Arkansas (Adams-Onis line west of 100W)
    ('COM', [(-98.3,37.0),(-102.1,37.0),(-102.1,38.05),(-100.0,37.75),(-98.8,38.36),(-98.5,38.3)]),
], footholds=[('USA',-94.92,39.35,'Fort Leavenworth')])

R['STATE_NEBRASKA'] = dict(default='ARP', rules=[
    # Pawnee, with Otoe-Missouria and Omaha (all under the Council Bluffs agency)
    ('PWN', [(-95.3,40.0),(-100.5,40.0),(-100.5,42.3),(-98.0,42.3),(-97.0,42.8),(-96.4,42.5),(-95.3,41.0)]),
    ('LKT', [(-104.1,42.0),(-100.5,42.0),(-100.5,42.3),(-98.0,42.3),(-97.0,42.8),(-96.4,42.5),(-96.4,43.1),(-104.1,43.1)]),
])

R['STATE_SOUTH_DAKOTA'] = dict(default='LKT', rules=[], footholds=[('USA',-100.38,44.37,'Fort Pierre (American Fur Co.)')])

R['STATE_NORTH_DAKOTA'] = dict(default='LKT', rules=[
    ('OJB', [(-100.5,48.4),(-98.8,47.6),(-96.5,47.4),(-96.5,49.1),(-100.5,49.1)]),   # Pembina and Turtle Mountain
    ('IRC', [(-104.1,47.6),(-101.5,47.9),(-100.5,48.4),(-100.5,49.1),(-104.1,49.1)]), # Assiniboine
], footholds=[('USA',-104.04,48.0,'Fort Union (American Fur Co.)')])

R['STATE_MONTANA'] = dict(default='ABS', rules=[
    ('SLS', [(-116.1,49.1),(-114.0,49.1),(-113.3,48.3),(-112.4,47.1),(-112.2,46.6),(-112.5,46.0),(-113.0,45.6),(-113.95,45.69),(-114.6,45.5),(-116.1,46.0)]),
    ('BNN', [(-113.95,45.69),(-113.0,45.6),(-111.6,45.6),(-111.1,44.4),(-114.0,44.4)]),
    ('BLF', [(-114.0,49.1),(-106.5,49.1),(-106.5,47.6),(-108.3,47.3),(-109.5,47.0),(-110.5,46.6),(-111.6,45.6),(-112.5,46.0),(-112.2,46.6),(-112.4,47.1),(-113.3,48.3)]),
    ('IRC', [(-106.5,49.1),(-104.0,49.1),(-104.0,47.8),(-106.5,47.6)]),
    ('LKT', [(-105.3,45.0),(-104.0,45.0),(-104.0,46.4),(-105.0,46.4)]),
])

R['STATE_WYOMING'] = dict(default='ARP', rules=[
    ('BNN', [(-111.1,41.0),(-111.1,45.0),(-110.0,45.0),(-109.5,44.0),(-108.5,43.3),(-107.2,42.6),(-107.0,41.0)]),
    ('ABS', [(-110.0,45.0),(-104.05,45.0),(-104.05,44.6),(-105.6,44.2),(-106.3,43.3),(-107.2,42.6),(-108.5,43.3),(-109.5,44.0)]),
    ('LKT', [(-104.05,44.6),(-105.6,44.2),(-106.3,43.3),(-106.0,43.0),(-104.05,43.0)]),
], footholds=[('USA',-104.56,42.21,'Fort William / Laramie')])

R['STATE_COLORADO'] = dict(default='ARP', rules=[
    ('UTE', [(-109.05,37.0),(-109.05,41.0),(-105.6,41.0),(-105.3,40.0),(-105.2,38.8),(-105.0,38.0),(-105.0,37.0)]),
    ('COM', [(-105.0,37.0),(-102.04,37.0),(-102.04,38.05),(-103.6,38.08),(-104.6,38.25),(-105.0,38.4)]),
], footholds=[('USA',-103.43,38.04,"Bent's Fort")])

R['STATE_OKLAHOMA'] = dict(default='COM', rules=[
    ('SEQ', [(-94.4,33.6),(-97.4,33.85),(-97.4,35.5),(-96.6,36.4),(-96.0,37.0),(-94.6,37.0),(-94.4,35.4)]),
    ('OSG', [(-96.6,36.4),(-96.0,37.0),(-98.6,37.0),(-98.6,36.4)]),
])

R['STATE_TEXAS'] = dict(default='COM', rules=[
    ('MEX', [(-106.7,31.6),(-106.0,31.2),(-105.6,31.0),(-105.9,31.9),(-106.7,32.0)]),                       # El Paso valley
    ('MEX', [(-97.15,25.9),(-99.6,27.0),(-100.3,28.3),(-99.5,28.6),(-98.4,28.4),(-97.6,27.9),(-97.2,27.6)]),  # Nueces strip, Laredo
    ('TEX', [(-93.6,29.7),(-97.2,27.6),(-97.6,27.9),(-98.4,28.4),(-98.9,29.3),(-98.3,29.8),(-97.7,30.5),(-97.3,31.3),
             (-96.4,31.9),(-95.6,32.4),(-95.6,33.9),(-94.0,33.9),(-93.9,32.0),(-93.5,30.0)]),
    ('APC', [(-106.7,32.0),(-103.0,32.0),(-102.0,30.5),(-102.0,29.5),(-103.2,28.9),(-104.6,29.4),(-106.7,31.6)]),  # Mescalero/Lipan
], footholds=[('MEX',-106.35,31.68,'El Paso valley (Ysleta, Socorro, San Elizario)')])

R['STATE_NEW_MEXICO'] = dict(default='APC', rules=[
    ('MEX', [(-107.3,33.9),(-106.4,33.9),(-106.2,34.6),(-105.9,35.0),(-104.9,35.0),(-104.9,35.6),(-105.3,36.0),(-105.3,36.8),
             (-106.4,36.8),(-106.8,36.2),(-107.4,35.3),(-107.7,34.8),(-107.3,34.4)]),
    ('NVJ', [(-109.05,34.8),(-109.05,37.0),(-106.9,37.0),(-106.8,36.2),(-107.4,35.3),(-107.7,34.8)]),
    ('COM', [(-104.6,32.0),(-103.0,32.0),(-103.0,37.0),(-104.9,37.0),(-104.9,36.0),(-104.6,35.6)]),
], footholds=[('MEX',-108.85,35.07,'Zuni Pueblo')])

R['STATE_ARIZONA'] = dict(default='CLF', rules=[
    ('MEX', [(-111.4,31.33),(-110.6,31.33),(-110.6,32.4),(-111.2,32.4)]),                                     # Tucson, Tubac
    ('MEX', [(-113.3,31.33),(-111.4,31.33),(-111.2,32.4),(-110.9,32.6),(-111.4,33.4),(-112.6,33.4),(-113.3,32.8)]),  # O'odham (ODH option)
    ('NVJ', [(-109.05,34.8),(-109.05,37.0),(-112.0,37.0),(-111.8,36.0),(-111.6,35.3),(-110.0,34.9)]),
    ('APC', [(-110.6,31.33),(-109.05,31.33),(-109.05,34.8),(-110.0,34.9),(-111.6,35.3),(-112.2,34.5),(-111.4,33.4),(-110.9,32.6),(-110.6,32.4)]),
])

R['STATE_UTAH'] = dict(default='UTE', rules=[
    ('NVJ', [(-110.6,37.0),(-109.05,37.0),(-109.05,37.7),(-110.6,37.7)]),
    ('BNN', [(-114.05,39.3),(-114.05,42.0),(-111.05,42.0),(-111.05,41.0),(-112.3,40.5),(-112.9,39.3)]),
])

R['STATE_NEVADA'] = dict(default='BNN', rules=[
    ('UTE', [(-120.0,35.0),(-114.0,35.0),(-114.0,37.0),(-120.0,37.0)]),
])

R['STATE_CALIFORNIA'] = dict(default='CLF', rules=[
    # Mission, presidio, pueblo and rancho belt, San Diego to Sonoma
    ('MEX', [(-117.0,32.53),(-116.8,33.0),(-116.95,33.6),(-117.2,34.0),(-117.7,34.3),(-118.4,34.45),(-119.0,34.55),(-119.7,34.75),
             (-120.3,35.1),(-120.55,35.85),(-121.15,36.5),(-121.45,37.0),(-121.75,37.6),(-121.85,38.0),(-122.3,38.45),
             (-122.8,38.45),(-123.5,38.0),(-122.0,35.5),(-118.5,32.5)]),
], footholds=[('ALK',-123.24,38.51,'Fort Ross (Russian-American Co.)')])

R['STATE_OREGON'] = dict(default='SLS', rules=[
    ('ORG', [(-124.2,46.3),(-121.9,45.75),(-122.2,45.3),(-122.6,44.4),(-123.3,44.4),(-123.6,45.0),(-124.2,45.9)]),
    ('BNN', [(-121.0,42.0),(-116.4,42.0),(-116.4,44.2),(-118.3,44.2),(-120.0,43.6),(-121.0,43.0)]),
    ('NZP', [(-121.9,45.75),(-116.4,46.0),(-116.4,44.2),(-118.3,44.2),(-120.0,43.6),(-121.0,43.0),(-121.0,42.0),(-122.2,42.0),(-122.0,44.4),(-122.2,45.3)]),
])

R['STATE_WASHINGTON'] = dict(default='SLS', rules=[
    ('ORG', [(-124.1,46.2),(-121.9,45.6),(-121.9,46.2),(-122.2,47.3),(-122.9,47.3),(-123.4,46.8),(-124.1,46.7)]),
    ('NZP', [(-121.9,45.6),(-116.9,46.0),(-117.0,47.2),(-119.5,47.4),(-121.2,47.4),(-121.9,46.2)]),
], footholds=[('ORG',-118.92,46.06,'Fort Walla Walla (HBC)'),('ORG',-118.05,48.63,'Fort Colvile (HBC)'),('ORG',-119.68,48.1,'Fort Okanogan (HBC)')])

R['STATE_IDAHO'] = dict(default='BNN', rules=[
    ('SLS', [(-117.3,46.9),(-117.3,49.1),(-115.9,49.1),(-114.3,47.6),(-114.3,46.9)]),
    ('NZP', [(-117.3,44.9),(-117.3,46.9),(-114.3,46.9),(-114.3,44.9)]),
], footholds=[('ORG',-116.9,43.8,'Fort Boise (HBC)')])

R['STATE_MAINE'] = dict(default='USA', rules=[
    # Madawaska / upper St John: administered from New Brunswick in 1836 (disputed until 1842)
    ('NBS', [(-69.3,47.0),(-67.8,47.0),(-67.8,47.5),(-69.3,47.5)]),
])

# Existing-tags-only fallback (variant A)
FALLBACK_A = {'OJB':'USA','SFX':'USA','OSG':None,'CLF':'MEX'}
# OSG in variant A: Kansas part -> PWN north / COM south handled by re-running without OSG rules

# Starting claims added on top of vanilla (vanilla claims are kept as they are).
# A claim plus an interest in the strategic region stops other countries colonizing the region,
# so these keep each power's 1836 colonial claim to itself; see the proposal for the reasoning.
ADD_CLAIMS = {
    'STATE_MICHIGAN':   ['USA'],          # US sovereign territory; keeps Ontario/GBR from colonizing OJB land
    'STATE_WISCONSIN':  ['USA'],
    'STATE_IOWA':       ['USA'],
    'STATE_MAINE':      ['USA', 'NBS'],   # Aroostook / Madawaska dispute (settled 1842)
    'STATE_CALIFORNIA': ['MEX'],          # Alta California
    'STATE_NEVADA':     ['MEX'],
}
