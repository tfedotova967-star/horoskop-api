import swisseph as swe
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

RASi = ["Baran","Býk","Blíženci","Rak","Lev","Panna","Váhy","Škorpión","Strelec","Kozorožec","Vodnár","Ryby"]

NAKSHATRY_27 = [
    "Ašviní","Bharaní","Krittiká","Rohiní","Mrigáširá","Árdrá","Punarvasu","Pušja","Ášléšá",
    "Maghá","Púrva Phalguní","Uttara Phalguní","Hasta","Čitra","Svátí","Višákhá","Anurádhá","Džjéšthá",
    "Múla","Púrva Ašádhá","Uttara Ašádhá","Šravaná","Dhaništhá","Šatabhišá",
    "Púrva Bhádrapadá","Uttara Bhádrapadá","Révatí"
]


DASHA_ORDER = ["Ketu","Venuša","Slnko","Mesiac","Mars","Rahu","Jupiter","Saturn","Merkúr"]
DASHA_YEARS = {
    "Ketu": 7,
    "Venuša": 20,
    "Slnko": 6,
    "Mesiac": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Merkúr": 17,
}
NAK_LORDS = [DASHA_ORDER[i % 9] for i in range(27)]

def vimshottari_antardasha(md_lord, md_start_dt, md_years, count=9):
    """
    Antardaša (Bhukti) v rámci jednej Mahádaše.
    Dĺžka AD = md_years * (roky_lorda / 120)
    """
    def years_to_timedelta(y):
        return timedelta(days=y * 365.2425)

    out = []
    start_idx = DASHA_ORDER.index(md_lord)
    cur = md_start_dt

    for i in range(count):
        ad_lord = DASHA_ORDER[(start_idx + i) % 9]
        ad_years = md_years * (DASHA_YEARS[ad_lord] / 120.0)
        nxt = cur + years_to_timedelta(ad_years)
        out.append({
            "lord": ad_lord,
            "start": cur.date().isoformat(),
            "end": nxt.date().isoformat(),
            "years": round(ad_years, 3),
        })
        cur = nxt

    return out

def vimshottari_mahadasha(dt_utc, moon_lon_sid, count=12):
    lon = moon_lon_sid % 360
    nak_index = int(lon // NAK_LEN)  # 0..26
    lord = NAK_LORDS[nak_index]

    within = lon - nak_index * NAK_LEN
    frac_elapsed = within / NAK_LEN
    frac_left = 1 - frac_elapsed

    def years_to_timedelta(y):
        return timedelta(days=y * 365.2425)

    first_years_left = DASHA_YEARS[lord] * frac_left

    out = []
    cur_start = dt_utc

    # 1) prvá (rozbehnutá) mahadaša – len zvyšok
    l = lord
    y = first_years_left
    cur_end = cur_start + years_to_timedelta(y)

    out.append({
        "lord": l,
        "start": cur_start.date().isoformat(),
        "end": cur_end.date().isoformat(),
        "years": y,
        "antardasha": vimshottari_antardasha(l, cur_start, y, count=9),
    })

    # 2) ďalšie mahadaše – celé obdobia
    idx = DASHA_ORDER.index(l)
    for _ in range(count - 1):
        idx = (idx + 1) % 9
        l = DASHA_ORDER[idx]
        y = DASHA_YEARS[l]
        nxt_end = cur_end + years_to_timedelta(y)

        out.append({
            "lord": l,
            "start": cur_end.date().isoformat(),
            "end": nxt_end.date().isoformat(),
            "years": y,
            "antardasha": vimshottari_antardasha(l, cur_end, y, count=9),
     
        })

        cur_end = nxt_end


    return out

DASHA_ORDER = ["Ketu","Venuša","Slnko","Mesiac","Mars","Rahu","Jupiter","Saturn","Merkúr"]

DASHA_YEARS = {
    "Ketu": 7,
    "Venuša": 20,
    "Slnko": 6,
    "Mesiac": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Merkúr": 17,
}

NAK_LORDS = [DASHA_ORDER[i % 9] for i in range(27)]


NAKSHATRY_27 = [
    "Ašviní","Bharaní","Krittiká","Rohiní","Mrigáširá","Árdrá","Punarvasu","Pušja","Ášléšá",
    "Maghá","Púrva Phalguní","Uttara Phalguní","Hasta","Čitra","Svátí","Višákhá","Anurádhá","Džjéšthá",
    "Múla","Púrva Ašádhá","Uttara Ašádhá","Šravaná","Dhaništhá","Šatabhišá","Púrva Bhádrapadá","Uttara Bhádrapadá","Révatí"
]
NAK_LEN = 13 + 20/60
PADA_LEN = NAK_LEN / 4
NAVAMSHA_LEN = 30 / 9

PLANETS = [
    ("Slnko", swe.SUN),
    ("Mesiac", swe.MOON),
    ("Merkúr", swe.MERCURY),
    ("Venuša", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("Rahu", swe.TRUE_NODE),
    ("Uran", swe.URANUS),
    ("Neptún", swe.NEPTUNE),
    ("Pluto", swe.PLUTO),
]

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def _to_utc(y, m, d, hh, mm, tz_name):
    tz = ZoneInfo(tz_name)

    # lokálny čas (fold=0 = prvý výskyt, OK pre 99 % prípadov)
    dt_local = datetime(
        y, m, d, hh, mm, 0,
        tzinfo=tz,
        fold=0
    )

    return dt_local.astimezone(timezone.utc)

def _julday(dt_utc):
    h = dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, h)

def _format_rasi(lon):
    lon = lon % 360
    r = int(lon // 30)
    deg = lon - r*30
    return RASi[r], round(deg, 2), round(lon, 2)

def _nakshatra_pada(lon):
    lon = lon % 360
    n = int(lon // NAK_LEN)
    within = lon - n*NAK_LEN
    pada = int(within // PADA_LEN) + 1
    return NAKSHATRY_27[n], pada

NAVAMSHA_LEN = 30.0 / 9.0  # 3°20' = 3.333...

# Uisti sa, že tento zoznam existuje a názvy sedia s frontend mapou
RASI = ["Baran","Byk","Blíženci","Rak","Lev","Panna","Váhy","Škorpión","Strelec","Kozorožec","Vodnár","Ryby"]

def _navamsha_sign_index(rasi_index, deg_in_sign: float) -> int:
    movable = {0, 3, 6, 9}
    fixed   = {1, 4, 7, 10}
    nav_index = int(deg_in_sign // NAVAMSHA_LEN)  # 0..8

    if rasi_index in movable:
        start = rasi_index
    elif rasi_index in fixed:
        start = (rasi_index + 8) % 12
    else:
        start = (rasi_index + 4) % 12

    return (start + nav_index) % 12

def _d9_sign(lon: float) -> str:
    lon = lon % 360.0
    r = int(lon // 30.0)          # 0..11
    deg_in_sign = lon - r * 30.0
    d9_index = _navamsha_sign_index(r, deg_in_sign)
    return RASI[d9_index]

def calc_d1_nak_d9(
    year, month, day, hour, minute,
    lat, lon,
    tz_name="Europe/Bratislava",
    house_sys=b"P"
):
   
    # result vytvor LEN RAZ, hneď tu (predtým si ho vytvárala až neskôr a prepisovala)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    dt_utc = _to_utc(year, month, day, hour, minute, tz_name)
    jd_ut = _julday(dt_utc)

    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    # ASC sidericky
    houses, ascmc = swe.houses_ex(jd_ut, lat, lon, house_sys, flags)
    asc_sid = ascmc[0] % 360.0

    aya = swe.get_ayanamsa_ut(jd_ut)

    # result vytvor LEN RAZ, až tu
    result = {
        "utc": dt_utc.isoformat(),
        "ayanamsa_lahiri": round(aya, 6),
        "asc": {},
        "planets": []
    }

    # jednotný formát ASC v D1 + doplnené D9
    asc_rasi, asc_deg, asc_lon = _format_rasi(asc_sid)

    # ✅ dopočítaj nakšatru a padu z ekliptickej dĺžky ASC
    nak, pada = _nakshatra_pada(asc_lon)

    result["asc"] = {
        "lon": asc_lon,
        "rasi": asc_rasi,
        "deg_in_rasi": asc_deg,
        "d9": _d9_sign(asc_lon),   # alebo asc_sid, ale asc_lon je čistejšie
        "nakshatra": nak,
        "pada": pada,
    }

    # ak to ešte používaš na fronte, nechaj; inak môžeš neskôr zmazať
    result["asc_rasi"] = asc_rasi
    
    moon_lon = None
    rahu_lon = None

    for name, p in PLANETS:
        if name == "Ketu":
            continue

        try:
            lonlat, _ = swe.calc_ut(jd_ut, p, flags)
        except Exception:
            lonlat, _ = swe.calc_ut(jd_ut, p, (flags | swe.FLG_MOSEPH))

        plon = lonlat[0]

        if name == "Rahu":
            rahu_lon = plon

        speed_lon = lonlat[3]          # toto je kľúčové
        retro = speed_lon < 0

        if name == "Rahu":
            retro = True  # uzly v džjotiši retro
   
        if name == "Mesiac":
            moon_lon = plon

        rasi, deg, lon360 = _format_rasi(plon)
        nak, pada = _nakshatra_pada(plon)

        result["planets"].append({
            "name": name,
            "lon": lon360,
            "rasi": rasi,
            "deg_in_rasi": deg,
            "nakshatra": nak,
            "pada": pada,
            "d9": _d9_sign(plon),
            "retro": retro, 
            "speed": round(speed_lon, 6),            # ✅
            "speed_lon": speed_lon,      # voliteľné, na debug
        })
        
    # Ketu = Rahu + 180°
    if rahu_lon is not None:
        ketu_lon = (rahu_lon + 180.0) % 360.0
        rasi, deg, lon360 = _format_rasi(ketu_lon)
        nak, pada = _nakshatra_pada(ketu_lon)

        result["planets"].append({
            "name": "Ketu",
            "lon": lon360,
            "rasi": rasi,
            "deg_in_rasi": deg,
            "nakshatra": nak,
            "pada": pada,
            "d9": _d9_sign(ketu_lon),
            "retro": True,   # Ketu je vždy retro
        })


    if moon_lon is not None:
        result["vimshottari"] = vimshottari_mahadasha(dt_utc, moon_lon, count=12)

    # 👉 pridáme pratjántardaše
        result["vimshottari"] = add_pratyantara_to_vimshottari(result["vimshottari"])

    print("PLANETS COUNT:", len(result["planets"]))
    print("ASC_RASI:", result.get("asc_rasi"))
    print("PLANETS COUNT:", len(result.get("planets", [])))
    if result.get("planets"):
        print("SAMPLE:", [(p["name"], p["rasi"], p["deg_in_rasi"]) for p in result["planets"][:3]])


    return result
 

def add_pratyantara_to_vimshottari(vim_list):
    """
    Očakáva zoznam mahadaší, kde každá má antardasha list.
    Podporí kľúče: antardasha alebo antardasha_list (ak by si to mala inak).
    Antardaša položka musí mať aspoň: lord + (from,to) alebo (start,end).
    """
    if not isinstance(vim_list, list):
        return vim_list

    for md in vim_list:
        ad_list = md.get("antardasha") or md.get("antardashas") or md.get("antardasha_list")
        if not isinstance(ad_list, list):
            continue

        for ad in ad_list:
            lord = ad.get("lord") or ad.get("planet") or ad.get("name")
            a_from = ad.get("from") or ad.get("start")
            a_to = ad.get("to") or ad.get("end")
            if not (lord and a_from and a_to):
                continue

            ad["pratyantardasha"] = build_pratyantardasha(a_from, a_to, str(lord))

    return vim_list 

# Vimshottari poradie a "roky"
_VIM_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
_VIM_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
_TOTAL = 120

def _parse_dt(x):
    # podporí "YYYY-MM-DD" aj "YYYY-MM-DDTHH:MM:SS"
    if isinstance(x, datetime):
        return x
    s = str(x).strip()
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return datetime.strptime(s[:10], "%Y-%m-%d")

def _fmt_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def _cycle_from(lord: str):
    if lord not in _VIM_ORDER:
        # fallback: ak máš názvy v slovenčine alebo iné, nech to aspoň nepadne
        return _VIM_ORDER[:]
    i = _VIM_ORDER.index(lord)
    return _VIM_ORDER[i:] + _VIM_ORDER[:i]

def build_pratyantardasha(ad_start, ad_end, ad_lord: str):
    """Vracia list PD úsekov v rámci 1 antardaše."""
    s = _parse_dt(ad_start)
    e = _parse_dt(ad_end)
    total_days = (e - s).total_seconds() / 86400.0
    if total_days <= 0:
        return []

    seq = _cycle_from(ad_lord)
    out = []
    cur = s

    for idx, p in enumerate(seq):
        # podiel podľa rokov/120
        frac = _VIM_YEARS[p] / _TOTAL
        days = total_days * frac
        nxt = cur + timedelta(days=days)

        # posledný úsek dorovnaj presne na koniec (kvôli zaokrúhleniu)
        if idx == len(seq) - 1 or nxt > e:
            nxt = e

        out.append({
            "lord": p,
            "from": _fmt_dt(cur),
            "to": _fmt_dt(nxt),
            "days": round((nxt - cur).total_seconds() / 86400.0, 3),
        })

        cur = nxt
        if cur >= e:
            break

    return out

def add_pratyantara_to_vimshottari(vim_list):
    """
    Očakáva zoznam mahadaší, kde každá má antardasha list.
    Podporí kľúče: antardasha alebo antardasha_list (ak by si to mala inak).
    Antardaša položka musí mať aspoň: lord + (from,to) alebo (start,end).
    """
    if not isinstance(vim_list, list):
        return vim_list

    for md in vim_list:
        ad_list = md.get("antardasha") or md.get("antardashas") or md.get("antardasha_list")
        if not isinstance(ad_list, list):
            continue

        for ad in ad_list:
            lord = ad.get("lord") or ad.get("planet") or ad.get("name")import swisseph as swe
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

RASi = ["Baran","Býk","Blíženci","Rak","Lev","Panna","Váhy","Škorpión","Strelec","Kozorožec","Vodnár","Ryby"]

NAKSHATRY_27 = [
    "Ašviní","Bharaní","Krittiká","Rohiní","Mrigáširá","Árdrá","Punarvasu","Pušja","Ášléšá",
    "Maghá","Púrva Phalguní","Uttara Phalguní","Hasta","Čitra","Svátí","Višákhá","Anurádhá","Džjéšthá",
    "Múla","Púrva Ašádhá","Uttara Ašádhá","Šravaná","Dhaništhá","Šatabhišá",
    "Púrva Bhádrapadá","Uttara Bhádrapadá","Révatí"
]


DASHA_ORDER = ["Ketu","Venuša","Slnko","Mesiac","Mars","Rahu","Jupiter","Saturn","Merkúr"]
DASHA_YEARS = {
    "Ketu": 7,
    "Venuša": 20,
    "Slnko": 6,
    "Mesiac": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Merkúr": 17,
}
NAK_LORDS = [DASHA_ORDER[i % 9] for i in range(27)]

def vimshottari_antardasha(md_lord, md_start_dt, md_years, count=9):
    """
    Antardaša (Bhukti) v rámci jednej Mahádaše.
    Dĺžka AD = md_years * (roky_lorda / 120)
    """
    def years_to_timedelta(y):
        return timedelta(days=y * 365.2425)

    out = []
    start_idx = DASHA_ORDER.index(md_lord)
    cur = md_start_dt

    for i in range(count):
        ad_lord = DASHA_ORDER[(start_idx + i) % 9]
        ad_years = md_years * (DASHA_YEARS[ad_lord] / 120.0)
        nxt = cur + years_to_timedelta(ad_years)
        out.append({
            "lord": ad_lord,
            "start": cur.date().isoformat(),
            "end": nxt.date().isoformat(),
            "years": round(ad_years, 3),
        })
        cur = nxt

    return out

def vimshottari_mahadasha(dt_utc, moon_lon_sid, count=12):
    lon = moon_lon_sid % 360
    nak_index = int(lon // NAK_LEN)  # 0..26
    lord = NAK_LORDS[nak_index]

    within = lon - nak_index * NAK_LEN
    frac_elapsed = within / NAK_LEN
    frac_left = 1 - frac_elapsed

    def years_to_timedelta(y):
        return timedelta(days=y * 365.2425)

    first_years_left = DASHA_YEARS[lord] * frac_left

    out = []
    cur_start = dt_utc

    # 1) prvá (rozbehnutá) mahadaša – len zvyšok
    l = lord
    y = first_years_left
    cur_end = cur_start + years_to_timedelta(y)

    out.append({
        "lord": l,
        "start": cur_start.date().isoformat(),
        "end": cur_end.date().isoformat(),
        "years": y,
        "antardasha": vimshottari_antardasha(l, cur_start, y, count=9),
    })

    # 2) ďalšie mahadaše – celé obdobia
    idx = DASHA_ORDER.index(l)
    for _ in range(count - 1):
        idx = (idx + 1) % 9
        l = DASHA_ORDER[idx]
        y = DASHA_YEARS[l]
        nxt_end = cur_end + years_to_timedelta(y)

        out.append({
            "lord": l,
            "start": cur_end.date().isoformat(),
            "end": nxt_end.date().isoformat(),
            "years": y,
            "antardasha": vimshottari_antardasha(l, cur_end, y, count=9),
     
        })

        cur_end = nxt_end


    return out

DASHA_ORDER = ["Ketu","Venuša","Slnko","Mesiac","Mars","Rahu","Jupiter","Saturn","Merkúr"]

DASHA_YEARS = {
    "Ketu": 7,
    "Venuša": 20,
    "Slnko": 6,
    "Mesiac": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Merkúr": 17,
}

NAK_LORDS = [DASHA_ORDER[i % 9] for i in range(27)]


NAKSHATRY_27 = [
    "Ašviní","Bharaní","Krittiká","Rohiní","Mrigáširá","Árdrá","Punarvasu","Pušja","Ášléšá",
    "Maghá","Púrva Phalguní","Uttara Phalguní","Hasta","Čitra","Svátí","Višákhá","Anurádhá","Džjéšthá",
    "Múla","Púrva Ašádhá","Uttara Ašádhá","Šravaná","Dhaništhá","Šatabhišá","Púrva Bhádrapadá","Uttara Bhádrapadá","Révatí"
]
NAK_LEN = 13 + 20/60
PADA_LEN = NAK_LEN / 4
NAVAMSHA_LEN = 30 / 9

PLANETS = [
    ("Slnko", swe.SUN),
    ("Mesiac", swe.MOON),
    ("Merkúr", swe.MERCURY),
    ("Venuša", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("Rahu", swe.TRUE_NODE),
    ("Uran", swe.URANUS),
    ("Neptún", swe.NEPTUNE),
    ("Pluto", swe.PLUTO),
]

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def _to_utc(y, m, d, hh, mm, tz_name):
    tz = ZoneInfo(tz_name)

    # lokálny čas (fold=0 = prvý výskyt, OK pre 99 % prípadov)
    dt_local = datetime(
        y, m, d, hh, mm, 0,
        tzinfo=tz,
        fold=0
    )

    return dt_local.astimezone(timezone.utc)

def _julday(dt_utc):
    h = dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, h)

def _format_rasi(lon):
    lon = lon % 360
    r = int(lon // 30)
    deg = lon - r*30
    return RASI[r], round(deg, 2), round(lon, 2)

def _nakshatra_pada(lon):
    lon = lon % 360
    n = int(lon // NAK_LEN)
    within = lon - n*NAK_LEN
    pada = int(within // PADA_LEN) + 1
    return NAKSHATRY_27[n], pada

NAVAMSHA_LEN = 30.0 / 9.0  # 3°20' = 3.333...

# Uisti sa, že tento zoznam existuje a názvy sedia s frontend mapou
RASI = ["Baran","Byk","Blíženci","Rak","Lev","Panna","Váhy","Škorpión","Strelec","Kozorožec","Vodnár","Ryby"]

def _navamsha_sign_index(rasi_index, deg_in_sign: float) -> int:
    movable = {0, 3, 6, 9}
    fixed   = {1, 4, 7, 10}
    nav_index = int(deg_in_sign // NAVAMSHA_LEN)  # 0..8

    if rasi_index in movable:
        start = rasi_index
    elif rasi_index in fixed:
        start = (rasi_index + 8) % 12
    else:
        start = (rasi_index + 4) % 12

    return (start + nav_index) % 12

def _d9_sign(lon: float) -> str:
    lon = lon % 360.0
    r = int(lon // 30.0)          # 0..11
    deg_in_sign = lon - r * 30.0
    d9_index = _navamsha_sign_index(r, deg_in_sign)
    return RASI[d9_index]

 # =========================
# ===== STRENGTH RATING ===
# =========================

EXALTATION_SIGNS = {
    "Slnko": "Baran",
    "Mesiac": "Byk",
    "Mars": "Kozorožec",
    "Merkúr": "Panna",
    "Jupiter": "Rak",
    "Venuša": "Ryby",
    "Saturn": "Váhy",
}

DEBILITATION_SIGNS = {
    "Slnko": "Váhy",
    "Mesiac": "Škorpión",
    "Mars": "Rak",
    "Merkúr": "Ryby",
    "Jupiter": "Kozorožec",
    "Venuša": "Panna",
    "Saturn": "Baran",
}

OWN_SIGNS = {
    "Slnko": ["Lev"],
    "Mesiac": ["Rak"],
    "Mars": ["Baran", "Škorpión"],
    "Merkúr": ["Blíženci", "Panna"],
    "Jupiter": ["Strelec", "Ryby"],
    "Venuša": ["Byk", "Váhy"],
    "Saturn": ["Kozorožec", "Vodnár"],
}

def clamp_strength(score):
    return max(1, min(5, score))

def stars_from_score(score):
    score = clamp_strength(score)
    return "★" * score + "☆" * (5 - score)

def get_house_from_sign(planet_rasi, asc_rasi, signs12):
    try:
        planet_idx = signs12.index(planet_rasi)
        asc_idx = signs12.index(asc_rasi)
        return ((planet_idx - asc_idx) % 12) + 1
    except ValueError:
        return None

def calculate_planet_strength(planet_name, planet_rasi, asc_rasi, signs12):
    score = 3
    reasons = []

    # znamenie
    if planet_name in EXALTATION_SIGNS and planet_rasi == EXALTATION_SIGNS[planet_name]:
        score += 2
        reasons.append("exaltácia +2")
    elif planet_name in DEBILITATION_SIGNS and planet_rasi == DEBILITATION_SIGNS[planet_name]:
        score -= 2
        reasons.append("debilitácia -2")
    elif planet_name in OWN_SIGNS and planet_rasi in OWN_SIGNS[planet_name]:
        score += 1
        reasons.append("vlastné znamenie +1")

    # dom od ASC
    house = get_house_from_sign(planet_rasi, asc_rasi, signs12)
    if house in [1, 4, 5, 7, 9, 10]:
        score += 1
        reasons.append(f"dobrý dom {house} +1")
    elif house in [6, 8, 12]:
        score -= 1
        reasons.append(f"náročný dom {house} -1")

    score = clamp_strength(score)

    if score == 5:
        label = "veľmi silná"
    elif score == 4:
        label = "silná"
    elif score == 3:
        label = "stredná"
    elif score == 2:
        label = "slabšia"
    else:
        label = "slabá"

    return {
        "strength_score": score,
        "strength_stars": stars_from_score(score),
        "strength_label": label,
        "strength_reasons": reasons,
        "house_from_asc": house,
    }   

def calc_d1_nak_d9(
    year, month, day, hour, minute,
    lat, lon,
    tz_name="Europe/Bratislava",
    house_sys=b"P"
):
   
    # result vytvor LEN RAZ, hneď tu (predtým si ho vytvárala až neskôr a prepisovala)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    dt_utc = _to_utc(year, month, day, hour, minute, tz_name)
    jd_ut = _julday(dt_utc)

    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    # ASC sidericky
    houses, ascmc = swe.houses_ex(jd_ut, lat, lon, house_sys, flags)
    asc_sid = ascmc[0] % 360.0

    aya = swe.get_ayanamsa_ut(jd_ut)

    # result vytvor LEN RAZ, až tu
    result = {
        "utc": dt_utc.isoformat(),
        "ayanamsa_lahiri": round(aya, 6),
        "asc": {},
        "planets": []
    }

    # jednotný formát ASC v D1 + doplnené D9
    asc_rasi, asc_deg, asc_lon = _format_rasi(asc_sid)

    # ✅ dopočítaj nakšatru a padu z ekliptickej dĺžky ASC
    nak, pada = _nakshatra_pada(asc_lon)

    result["asc"] = {
        "lon": asc_lon,
        "rasi": asc_rasi,
        "deg_in_rasi": asc_deg,
        "d9": _d9_sign(asc_lon),   # alebo asc_sid, ale asc_lon je čistejšie
        "nakshatra": nak,
        "pada": pada,
    }

    # ak to ešte používaš na fronte, nechaj; inak môžeš neskôr zmazať
    result["asc_rasi"] = asc_rasi
    
    moon_lon = None
    rahu_lon = None

    for name, p in PLANETS:
        if name == "Ketu":
            continue

        try:
            lonlat, _ = swe.calc_ut(jd_ut, p, flags)
        except Exception:
            lonlat, _ = swe.calc_ut(jd_ut, p, (flags | swe.FLG_MOSEPH))

        plon = lonlat[0]

        if name == "Rahu":
            rahu_lon = plon

        speed_lon = lonlat[3]          # toto je kľúčové
        retro = speed_lon < 0

        if name == "Rahu":
            retro = True  # uzly v džjotiši retro
   
        if name == "Mesiac":
            moon_lon = plon

        rasi, deg, lon360 = _format_rasi(plon)
        nak, pada = _nakshatra_pada(plon)

        strength = calculate_planet_strength(
    planet_name=name,
    planet_rasi=rasi,
    asc_rasi=result["asc"]["rasi"],
    signs12=RASI
)

        result["planets"].append({
            "name": name,
            "lon": lon360,
            "rasi": rasi,
            "deg_in_rasi": deg,
            "nakshatra": nak,
            "pada": pada,
            "d9": _d9_sign(plon),
            "retro": retro, 
            "speed": round(speed_lon, 6),            # ✅
            "speed_lon": speed_lon,      # voliteľné, na debug

            "strength_score": strength["strength_score"],
            "strength_stars": strength["strength_stars"],
            "strength_label": strength["strength_label"],
            "strength_reasons": strength["strength_reasons"],
        })
        
    # Ketu = Rahu + 180°
    if rahu_lon is not None:
        ketu_lon = (rahu_lon + 180.0) % 360.0
        rasi, deg, lon360 = _format_rasi(ketu_lon)
        nak, pada = _nakshatra_pada(ketu_lon)

        strength = calculate_planet_strength(
            planet_name="Ketu",
            planet_rasi=rasi,
            asc_rasi=result["asc"]["rasi"],
            signs12=RASI
        )

        result["planets"].append({
            "name": "Ketu",
            "lon": lon360,
            "rasi": rasi,
            "deg_in_rasi": deg,
            "nakshatra": nak,
            "pada": pada,
            "d9": _d9_sign(ketu_lon),
            "retro": True,   # Ketu je vždy retro

            "strength_score": strength["strength_score"],
            "strength_stars": strength["strength_stars"],
            "strength_label": strength["strength_label"],
            "strength_reasons": strength["strength_reasons"],
        })


    if moon_lon is not None:
        result["vimshottari"] = vimshottari_mahadasha(dt_utc, moon_lon, count=12)

    # 👉 pridáme pratjántardaše
        result["vimshottari"] = add_pratyantara_to_vimshottari(result["vimshottari"])

    print("PLANETS COUNT:", len(result["planets"]))
    print("ASC_RASI:", result.get("asc_rasi"))
    print("PLANETS COUNT:", len(result.get("planets", [])))
    if result.get("planets"):
        print("SAMPLE:", [(p["name"], p["rasi"], p["deg_in_rasi"]) for p in result["planets"][:3]])


    return result
 

def add_pratyantara_to_vimshottari(vim_list):
    """
    Očakáva zoznam mahadaší, kde každá má antardasha list.
    Podporí kľúče: antardasha alebo antardasha_list (ak by si to mala inak).
    Antardaša položka musí mať aspoň: lord + (from,to) alebo (start,end).
    """
    if not isinstance(vim_list, list):
        return vim_list

    for md in vim_list:
        ad_list = md.get("antardasha") or md.get("antardashas") or md.get("antardasha_list")
        if not isinstance(ad_list, list):
            continue

        for ad in ad_list:
            lord = ad.get("lord") or ad.get("planet") or ad.get("name")
            a_from = ad.get("from") or ad.get("start")
            a_to = ad.get("to") or ad.get("end")
            if not (lord and a_from and a_to):
                continue

            ad["pratyantardasha"] = build_pratyantardasha(a_from, a_to, str(lord))

    return vim_list 

# Vimshottari poradie a "roky"
_VIM_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
_VIM_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
_TOTAL = 120

def _parse_dt(x):
    # podporí "YYYY-MM-DD" aj "YYYY-MM-DDTHH:MM:SS"
    if isinstance(x, datetime):
        return x
    s = str(x).strip()
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return datetime.strptime(s[:10], "%Y-%m-%d")

def _fmt_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def _cycle_from(lord: str):
    if lord not in _VIM_ORDER:
        # fallback: ak máš názvy v slovenčine alebo iné, nech to aspoň nepadne
        return _VIM_ORDER[:]
    i = _VIM_ORDER.index(lord)
    return _VIM_ORDER[i:] + _VIM_ORDER[:i]

def build_pratyantardasha(ad_start, ad_end, ad_lord: str):
    """Vracia list PD úsekov v rámci 1 antardaše."""
    s = _parse_dt(ad_start)
    e = _parse_dt(ad_end)
    total_days = (e - s).total_seconds() / 86400.0
    if total_days <= 0:
        return []

    seq = _cycle_from(ad_lord)
    out = []
    cur = s

    for idx, p in enumerate(seq):
        # podiel podľa rokov/120
        frac = _VIM_YEARS[p] / _TOTAL
        days = total_days * frac
        nxt = cur + timedelta(days=days)

        # posledný úsek dorovnaj presne na koniec (kvôli zaokrúhleniu)
        if idx == len(seq) - 1 or nxt > e:
            nxt = e

        out.append({
            "lord": p,
            "from": _fmt_dt(cur),
            "to": _fmt_dt(nxt),
            "days": round((nxt - cur).total_seconds() / 86400.0, 3),
        })

        cur = nxt
        if cur >= e:
            break

    return out

def add_pratyantara_to_vimshottari(vim_list):
    """
    Očakáva zoznam mahadaší, kde každá má antardasha list.
    Podporí kľúče: antardasha alebo antardasha_list (ak by si to mala inak).
    Antardaša položka musí mať aspoň: lord + (from,to) alebo (start,end).
    """
    if not isinstance(vim_list, list):
        return vim_list

    for md in vim_list:
        ad_list = md.get("antardasha") or md.get("antardashas") or md.get("antardasha_list")
        if not isinstance(ad_list, list):
            continue

        for ad in ad_list:
            lord = ad.get("lord") or ad.get("planet") or ad.get("name")
            a_from = ad.get("from") or ad.get("start")
            a_to = ad.get("to") or ad.get("end")
            if not (lord and a_from and a_to):
                continue

            ad["pratyantardasha"] = build_pratyantardasha(a_from, a_to, str(lord))

    return vim_list
  

            a_from = ad.get("from") or ad.get("start")
            a_to = ad.get("to") or ad.get("end")
            if not (lord and a_from and a_to):
                continue

            ad["pratyantardasha"] = build_pratyantardasha(a_from, a_to, str(lord))

    return vim_list
  
