# den5_d9_navamsha.py
# D1 sidericky (Lahiri) + výpočet Navamše (D9)

import swisseph as swe
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# -----------------------------
# TU ZADÁŠ ÚDAJE
# -----------------------------
ROK = 2001
MESIAC = 1
DEN = 5
HODINA = 17
MINUTA = 35

LAT = 48.1486
LON = 17.1077
CASOVE_PASMO = "Europe/Bratislava"
DOMOVY_SYSTEM = b"P"
# -----------------------------

PLANETY = [
    ("ASC", None),
    ("Slnko", swe.SUN),
    ("Mesiac", swe.MOON),
    ("Merkúr", swe.MERCURY),
    ("Venuša", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("Rahu", swe.TRUE_NODE),
]

RASi = [
    "Baran","Býk","Blíženci","Rak","Lev","Panna",
    "Váhy","Škorpión","Strelec","Kozorožec","Vodnár","Ryby"
]

NAVAMSHA_LEN = 30 / 9  # 3.333333...

def lokalny_na_utc():
    tz = ZoneInfo(CASOVE_PASMO)
    dt_local = datetime(ROK, MESIAC, DEN, HODINA, MINUTA, tzinfo=tz)
    return dt_local.astimezone(timezone.utc)

def julian_day(dt_utc):
    hod = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hod)

def format_rasi(lon):
    lon = lon % 360
    r = int(lon // 30)
    deg = lon - r * 30
    return f"{RASi[r]} {deg:05.2f}°"

def navamsha_sign_index(rasi_index: int, deg_in_sign: float) -> int:
    """
    Najpoužívanejšie pravidlo (Parášari):
    - pohyblivé (Baran, Rak, Váhy, Kozorožec): začína od toho istého znamenia
    - pevné (Býk, Lev, Škorpión, Vodnár): začína od 9. znamenia od neho
    - dvojtelné (Blíženci, Panna, Strelec, Ryby): začína od 5. znamenia od neho
    Potom sa ide po znameniach ďalej podľa navamša poradia (0..8).
    """
    movable = {0, 3, 6, 9}
    fixed = {1, 4, 7, 10}
    dual = {2, 5, 8, 11}

    nav_index = int(deg_in_sign // NAVAMSHA_LEN)  # 0..8

    if rasi_index in movable:
        start = rasi_index
    elif rasi_index in fixed:
        start = (rasi_index + 8) % 12  # 9. od neho
    else:  # dual
        start = (rasi_index + 4) % 12  # 5. od neho

    return (start + nav_index) % 12

def d9_of_longitude(lon: float) -> str:
    lon = lon % 360
    rasi_index = int(lon // 30)
    deg_in_sign = lon - rasi_index * 30
    d9_idx = navamsha_sign_index(rasi_index, deg_in_sign)
    return RASi[d9_idx]

def main():
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    dt_utc = lokalny_na_utc()
    jd = julian_day(dt_utc)

    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    # ASC sidericky
    houses, ascmc = swe.houses(jd, LAT, LON, DOMOVY_SYSTEM)
    asc_trop = ascmc[0]
    aya = swe.get_ayanamsa_ut(jd)
    asc_sid = (asc_trop - aya) % 360

    print("UTC čas:", dt_utc)
    print("Ayanamša (Lahiri):", f"{aya:.6f}°")
    print("\nD1 (sidericky) + D9 (Navamša):")

    for meno, p in PLANETY:
        if meno == "ASC":
            lon = asc_sid
        else:
            lonlat, _ = swe.calc_ut(jd, p, flags)
            lon = lonlat[0]

        d1 = format_rasi(lon)
        d9 = d9_of_longitude(lon)
        print(f"- {meno:7s}: {d1:18s} | D9: {d9}")

if __name__ == "__main__":
    main()

