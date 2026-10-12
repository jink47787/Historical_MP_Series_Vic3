"""Countries, cultures and populations for the Native North American tags in the 1836 proposal.

Two packages are built from this: 'corridor' (the core proposal) and 'plus6' (the core plus six more peoples).
Populations are period estimates for c. 1836, not vanilla figures; the sources are listed in SOURCES and in PROPOSAL.md.
"""

# ---------------------------------------------------------------------------------------------------------------
# New cultures. Vanilla already has inuit, cree, algonquian, siouan, caddoan, hokan and oodham, which cover the
# other peoples. Name lists use attested names; the Northwest Coast lists are short and are flagged for review.

CULTURES = {
    'anishinaabe': dict(
        why="Ojibwe, Odawa, Potawatomi, Algonquin, Nipissing, Mississauga, Saulteaux and Oji-Cree. Vanilla folds them "
            "into 'algonquian', whose name list is Shawnee (Catecahassa, Tenskwatawa's Lalawethika, Methoataske).",
        color='hsv{ 0.36 0.45 0.55 }', heritage='heritage_eastern_woodlands_indian', language='language_anishinaabemowin',
        male=['Bagonegiizhig', 'Eshkibagikoonzhe', 'Waabojiig', 'Ozaawindib', 'Gichibizhiki', 'Zhingwaakoons',
              'Asiginaak', 'Nagaanigwaneb', 'Maangozid', 'Oshkaabewis', 'Peguis', 'Gaagigegaabaw', 'Okemos',
              'Wabanosay', 'Ningwegon', 'Biiwaabiko'],
        female=['Ozhaawashkodewekwe', 'Obabaamwewegiizhigokwe', 'Aazhawigiizhigokwe', 'Waabanangokwe', 'Ogimaakwe',
                'Migizikwe', 'Giizhigokwe', 'Memengwaakwe', 'Nookomis', 'Equaysayway'],
        last=['Ajijaak', 'Maang', 'Makwa', 'Name', 'Waabizheshi', 'Migizi', 'Maaingan', 'Adik', 'Bineshii', 'Gekek',
              'Mishiikenh', 'Wazhashk']),           # doodem (clan) names
    'cheyenne': dict(
        why="Tsitsistas and Suhtai. Algonquian-speaking plains people; vanilla has no plains Algonquian culture.",
        color='hsv{ 0.07 0.6 0.55 }', heritage='heritage_plains_indian', language='language_cheyenne', plus6=True,
        male=['Motavato', 'Woquini', 'Ohcumgache', 'Vooheheve', 'Honiahaka', 'Awoninahku', 'Vokivokamast',
              'Hotoakhihoois'],
        female=['Mochi', 'Ehyophsta', 'Monahsetah'],
        last=['Hevhaitaneo', 'Masikota', 'Omisis', 'Heviqsnipahis', 'Hisiometanio', 'Oivimana', 'Wotapio',
              'Hotamitaneo', 'Suhtai', 'Totoimana', 'Ohktounna', 'Hofnowa']),   # the ten bands (manaho) and the Dog Soldiers
    'wakashan': dict(
        why="Kwakwaka'wakw, Nuu-chah-nulth, Heiltsuk and Haisla. Vanilla puts the whole coast under 'salish'.",
        color='hsv{ 0.48 0.55 0.45 }', heritage='heritage_northwest_coast_indian', language='language_wakashan',
        plus6=True, review=True,
        male=['Maquinna', 'Wickaninnish', 'Callicum', 'Tatoosh', 'Cleaskinah', 'Tlupananul'],
        female=['Homiskanis'],                    # Kwakwaka'wakw (Lucy Homiskanis); list needs extending by someone with sources
        last=["Kwagul", 'Mamalilikala', 'Namgis', 'Dzawadaenuxw', 'Mowachaht', 'Tlaoquiaht', 'Ahousaht',
              'Hesquiaht', 'Ditidaht', 'Heiltsuk', 'Haisla']),               # tribal groups
    'haida': dict(
        why="Haida Gwaii. Vanilla's 'salish' name list is already Haida; these names move here.",
        color='hsv{ 0.0 0.55 0.5 }', heritage='heritage_northwest_coast_indian', language='language_haida', plus6=True,
        male=['Cumshewa', 'Cuneah', 'Dah-egin', 'Gush_X-een', 'Guujaaw', 'Hluugitgaa', 'Ninstints', 'Skaay',
              'Skidegate', 'Tahaygen', 'Wiisheyksh', 'Xhuuyaa', 'Idansuu', 'Koyah'],
        female=['Ansnaq', 'Jadal_q-eganga', 'Kung_Jaadee', 'Kwiigeliones', 'K-woiyang', 'Qawkuna', 'Skil_Kew_Wat'],
        last=['Gispwudwada', 'Idinsaw', 'Taantakwaan', 'Y-akwa-lanas', 'Kiusta', 'Masset', 'Kaisun', 'Tanu',
              'Skedans']),
    'tsimshian': dict(
        why="Coast Tsimshian, Nisga'a and Gitxsan of the Skeena and Nass. Vanilla puts them under 'salish'.",
        color='hsv{ 0.56 0.4 0.6 }', heritage='heritage_northwest_coast_indian', language='language_tsimshianic',
        plus6=True, review=True,
        male=['Ligeex', 'Sebassa', 'Neeshot', 'Sgagweet'],
        female=['Neshaki', 'Sudaal'],
        last=['Gispaxloots', 'Gitando', 'Ginaxangiik', 'Gitzaxlaal', 'Gitlaan', 'Gitsiis', 'Gitwilgyoots',
              'Gitkxaala', 'Nisgaa', 'Gitxsan']),                           # the tribes of the Skeena and Nass
}

LANGUAGES = {   # language -> group (new groups are created where vanilla has none)
    'language_anishinaabemowin': ('language_group_algic', 'Anishinaabemowin'),
    'language_cheyenne': ('language_group_algic', 'Cheyenne'),
    'language_wakashan': ('language_group_wakashan', 'Wakashan'),
    'language_haida': ('language_group_haida', 'Haida'),
    'language_tsimshianic': ('language_group_tsimshianic', 'Tsimshianic'),
}
NEW_LANGUAGE_GROUPS = {'language_group_wakashan': 'Wakashan', 'language_group_haida': 'Haida (isolate)',
                       'language_group_tsimshianic': 'Tsimshianic'}

# ---------------------------------------------------------------------------------------------------------------
# Countries. 'reuse' tags already exist in vanilla (defined, not used at the 1836 start) and are changed with INJECT.

TAGS = {
    'CTF': dict(color=(110, 170, 110), reuse=True, name='Council of Three Fires', adj='Three Fires', cultures=['anishinaabe'],
                capital='STATE_MICHIGAN', flag='Three council fires: the Ojibwe, Odawa and Potawatomi.'),
    'SFX': dict(color=(180, 200, 120), name='Sauk and Meskwaki', adj='Sauk', cultures=['algonquian'], capital='STATE_IOWA',
                flag='Red over yellow: the Meskwaki are the Red Earth People, the Sauk the Yellow Earth People.'),
    'OSG': dict(color=(160, 90, 60), name='Osage', adj='Osage', cultures=['siouan'], capital='STATE_KANSAS',
                flag='Sky over earth, the two Osage moieties (Tsi-zhu and Honga), joined by the morning star.'),
    'CLF': dict(color=(230, 210, 120), name='Californian Peoples', adj='Californian', cultures=['hokan'], capital='STATE_CALIFORNIA',
                flag='The rattlesnake diamond band of Yokuts and Pomo basketry.'),
    'INU': dict(color=(150, 205, 215), name='Inuit', adj='Inuit', cultures=['inuit'], capital='STATE_NUNAVUT',
                flag='An inuksuk on the sea ice.'),
    'INN': dict(color=(100, 85, 150), name='Innu and Cree', adj='Innu', cultures=['cree'], capital='STATE_QUEBEC',
                flag='The mitshuap, the conical hunting lodge, in the boreal forest above the snow.'),
    # plus6
    'CSC': dict(color=(40, 110, 110), reuse=True, plus6=True, name='Northwest Coast', adj='Northwest Coast',
                cultures=['wakashan', 'haida', 'tsimshian'], capital='STATE_BRITISH_COLUMBIA',
                flag='A formline ovoid in black and red, with Chilkat-blanket borders.'),
    'CHY': dict(color=(120, 80, 40), plus6=True, name='Cheyenne', adj='Cheyenne', cultures=['cheyenne'], capital='STATE_COLORADO',
                flag='The Morning Star over the red earth of the southern plains.'),
    'MHA': dict(color=(230, 170, 40), plus6=True, name='Mandan and Hidatsa', adj='Mandan', cultures=['siouan', 'caddoan'],
                capital='STATE_NORTH_DAKOTA', flag='An earth lodge above the Missouri.'),
    'CCM': dict(color=(170, 150, 90), reuse=True, plus6=True, name="O’odham Country", adj="O’odham", cultures=['oodham'],
                capital='STATE_ARIZONA', flag="I'itoi in the maze (the Man in the Maze)."),
    'MNM': dict(color=(60, 130, 60), plus6=True, name='Menominee', adj='Menominee', cultures=['algonquian'], capital='STATE_WISCONSIN',
                flag='Wild rice (manoomin) standing in the lake: the Menominee are the wild-rice people.'),
    'HCK': dict(color=(140, 60, 90), plus6=True, name='Ho-Chunk', adj='Ho-Chunk', cultures=['siouan'], capital='STATE_WISCONSIN',
                flag='The Thunderbird, the clan of the Ho-Chunk peace chiefs.'),
}

# ---------------------------------------------------------------------------------------------------------------
# Populations c. 1836 for the new and reused tags, per state split: [(culture, size)].

PEOPLES = {
    'CTF': {
        'STATE_ONTARIO': [('anishinaabe', 8000)],       # north shore of Huron and Superior, Nipissing, Rainy Lake, Oji-Cree interior
        'STATE_MINNESOTA': [('anishinaabe', 7000)],     # Leech, Red, Sandy and Mille Lacs bands
        'STATE_WISCONSIN': [('anishinaabe', 4000),      # Lake Superior bands: La Pointe, Lac du Flambeau, Lac Courte Oreilles
                            ('algonquian', 3500),       # Menominee (folded into CTF in the core proposal)
                            ('siouan', 4500)],          # Ho-Chunk (ditto)
        'STATE_MICHIGAN': [('anishinaabe', 6500)],      # Upper Peninsula Ojibwe; Odawa of L'Arbre Croche and Grand Traverse
        'STATE_QUEBEC': [('anishinaabe', 1500)],        # Algonquin of the upper Ottawa and Abitibi
        'STATE_MANITOBA': [('anishinaabe', 2000)],      # Saulteaux of the Winnipeg River; Island Lake Oji-Cree
        'STATE_NORTH_DAKOTA': [('anishinaabe', 500)],   # Pembina and Turtle Mountain
    },
    'SFX': {'STATE_IOWA': [('algonquian', 5900)],                       # Sauk and Meskwaki
            'STATE_MISSOURI': [('siouan', 900), ('algonquian', 500)]},  # Ioway and Missouri Sauk on the Platte
    'OSG': {'STATE_KANSAS': [('siouan', 6500)],         # Osage and Kansa
            'STATE_OKLAHOMA': [('siouan', 600)]},       # Osage bands on the Verdigris
    'CLF': {'STATE_CALIFORNIA': [('hokan', 130000)],    # interior and northern California, after the 1833 malaria epidemic
            'STATE_ARIZONA': [('hokan', 8000)]},        # Yuman peoples of the Colorado: Mohave, Quechan, Halchidhoma, Yavapai
    'INU': {'STATE_NUNAVUT': [('inuit', 5500)], 'STATE_NORTHWEST_TERRITORIES': [('inuit', 2000)],
            'STATE_YUKON_TERRITORY': [('inuit', 500)], 'STATE_QUEBEC': [('inuit', 2500)],
            'STATE_NEWFOUNDLAND': [('inuit', 2000)],    # Labrador: Moravian mission counts plus the northern coast
            'STATE_MANITOBA': [('inuit', 200)]},        # Hudson Bay coast north of Churchill
    'INN': {'STATE_QUEBEC': [('cree', 4500)],           # Innu (Montagnais), Naskapi, inland East James Bay Cree
            'STATE_NEWFOUNDLAND': [('cree', 1500)],     # Labrador Innu and Naskapi
            'STATE_ONTARIO': [('cree', 2000)],          # Omushkego (Swampy and Moose) Cree of the lowland
            'STATE_MANITOBA': [('cree', 1000)]},        # inland Swampy Cree
}

PEOPLES_PLUS6 = {
    'CTF': dict(PEOPLES['CTF'], STATE_WISCONSIN=[('anishinaabe', 4000)]),
    'CSC': {'STATE_BRITISH_COLUMBIA': [('wakashan', 17000), ('tsimshian', 8700), ('haida', 6700)]},
    'CHY': {'STATE_COLORADO': [('cheyenne', 2300)], 'STATE_KANSAS': [('cheyenne', 700)]},
    'MHA': {'STATE_NORTH_DAKOTA': [('siouan', 4100), ('caddoan', 2500)]},  # Mandan 1,600 and Hidatsa 2,500 before the 1837 smallpox; Arikara
    'CCM': {'STATE_ARIZONA': [('oodham', 8000)]},       # Akimel and Tohono O'odham
    'MNM': {'STATE_WISCONSIN': [('algonquian', 3500)]},
    'HCK': {'STATE_WISCONSIN': [('siouan', 4500)]},
}

# ---------------------------------------------------------------------------------------------------------------
# Vanilla native tags scaled down to period figures (Dylan, 2026-10-11: "Scale down"), so every native nation in the
# proposal uses the same yardstick as the tags above. Targets are each tag's indigenous population c. 1836 inside the
# proposal's states only (Alaska stays vanilla). Settler and Metis pops a tag holds are not scaled.
# SEQ and SML are left at vanilla: they are the Indian Removal and Seminole Wars tags, which vanilla journal entries and
# the Five Tribes proposal move pops into, and SML (5,000) is already at the historical figure.
# Values are mid-range estimates from the sources below; review before release.

VANILLA_TARGETS = {
    'LKT': 28000,   # Lakota, Dakota and Nakota Sioux; the 1825 Teton count of c. 7,500 is "probably much too low" (encyclopedia.com, Teton)
    'COM': 25000,   # Comanche c. 20,000 before the late-1840s epidemics (Hamalainen 2008, p. 2), plus the allied Kiowa and Plains Apache
    'IRC': 20000,   # Assiniboine c. 10,000 before the 1837 smallpox (NPS, Fort Union), plus the Plains Cree and plains Saulteaux
    'BLF': 18000,   # Blackfoot Confederacy: Catlin 16,500 (1832), Maximilian 18-20,000 (1833); before the 1837 smallpox
    'ATB': 18000,   # Dene and northern Athapaskans of Canada: Chipewyan, Beaver, Slavey, Dogrib, Dakelh, Tsilhqot'in... (HNAI 6)
    'BNN': 15000,   # Northern and Western Shoshone, Bannock and Northern Paiute (HNAI 11)
    'PWN': 14000,   # Pawnee c. 10-12k, with the Otoe-Missouria, Omaha and Ponca folded in (HNAI 13)
    'NZP': 12000,   # Nez Perce, Cayuse, Walla Walla, Umatilla, Yakama and other Plateau Sahaptins (HNAI 12)
    'NVJ': 12000,   # Navajo, about 10-12k (HNAI 10)
    'UTE': 10000,   # Ute and Southern Paiute (HNAI 11)
    'APC': 10000,   # Western, Chiricahua, Mescalero, Jicarilla and Lipan Apache (HNAI 10)
    'ABS': 6000,    # Crow, 4-8k (HNAI 13)
    'ARP': 6500,    # core: Arapaho c. 3,500 with the Cheyenne folded in (HNAI 13)
    'SLS': 44000,   # core: Coast and Interior Salish plus the Northwest Coast peoples the core folds into SLS (Duff; HNAI 7)
}
VANILLA_TARGETS_PLUS6 = {
    'ARP': 3500,    # Arapaho alone; CHY takes the Cheyenne
    'SLS': 12000,   # Salish alone; CSC takes the Northwest Coast
}


def vanilla_targets_for(variant):
    t = dict(VANILLA_TARGETS)
    if variant == 'plus6':
        t.update(VANILLA_TARGETS_PLUS6)
    return t


SOURCES = [
    'Tanner, H. H. (ed.), Atlas of Great Lakes Indian History (1987): Great Lakes peoples, 1830s.',
    'Schoolcraft, H. R., Historical and Statistical Information respecting the Indian Tribes (1851-57), incl. '
    "the Indian Office counts of the 1830s and John Work's HBC census of the Northwest Coast (1836-41).",
    'Annual Reports of the Commissioner of Indian Affairs, 1836-38: Sauk and Meskwaki, Osage, Kansa, Ioway, '
    'Menominee, Ho-Chunk.',
    'Cook, S. F., The Population of the California Indians, 1769-1970 (1976): c. 150,000 by 1845 after the 1833 '
    'malaria epidemic.',
    'Duff, W., The Indian History of British Columbia (1964): Kwakwaka\'wakw, Nuu-chah-nulth, Heiltsuk.',
    'Handbook of North American Indians, vols. 5 (Arctic, 1984), 6 (Subarctic, 1981), 10 (Southwest, 1983), '
    '13 (Plains, 2001): Inuit, Innu and Cree, O\'odham, Cheyenne, Mandan, Hidatsa and Arikara.',
    'Handbook of North American Indians, vols. 7 (Northwest Coast, 1990), 11 (Great Basin, 1986), 12 (Plateau, 1998): '
    'Salish, Shoshone, Bannock, Paiute, Ute and the Plateau peoples (scaled vanilla tags).',
    'Hamalainen, P., The Comanche Empire (2008): Comanche population in the 1830s.',
    'Ewers, J. C., The Blackfeet: Raiders on the Northwestern Plains (1958): Blackfoot before the 1837 smallpox.',
]


def tags_for(variant):
    return {t: d for t, d in TAGS.items() if variant == 'plus6' or not d.get('plus6')}


def cultures_for(variant):
    return {c: d for c, d in CULTURES.items() if variant == 'plus6' or not d.get('plus6')}


def peoples_for(variant):
    if variant == 'plus6':
        p = dict(PEOPLES)
        p.update(PEOPLES_PLUS6)
        return p
    return PEOPLES
