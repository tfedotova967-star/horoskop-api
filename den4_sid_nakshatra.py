# den4_sid_nakshatra.py
# Siderický zodiak (Lahiri) + nakšatra + pada.

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

DOMOVY_SYSTEM = b"P"  # zatiaľ Placidus
# -----------------------------

PLANETY = [
    ("Slnko", swe.SUN),
    ("Mesiac", swe.MOON),
    ("Merkúr", swe.MERCURY),
    ("Venuša", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("Rahu (True Node)", swe.TRUE_NODE),
]

# Siderické znamenia (Džjotiš)
RASi = [
    "Baran","Býk","Blíženci","Rak","Lev","Panna",
    "Váhy","Škorpión","Strelec","Kozorožec","Vodnár","Ryby"
]

NAKSHATRY_27 = [
    "Ašviní","Bharaní","Krittiká","Rohiní","Mrigáširá","Árdrá","Punarvasu","Pušja","Ášléšá",
    "Maghá","Púrva Phalguní","Uttara Phalguní","Hasta","Čitra","Svátí","Višákhá","Anurádhá","Džjéšthá",
    "Múla","Púrva Ašádhá","Uttara Ašádhá","Šravaná","Dhaništhá","Šatabhišá","Púrva Bhádrapadá","Uttara Bhádrapadá","Révatí"
]

NAK_LEN = 13 + 20/60  # 13°20' = 13.333333...
PADA_LEN = NAK_LEN / 4  # 3°20'


def lokalny_na_utc():
    tz = ZoneInfo(CASOVE_PASMO)
    dt_local = datetime(ROK, MESIAC, DEN, HODINA, MINUTA, tzinfo=tz)
    return dt_local.astimezone(timezone.utc)

def julian_day(dt_utc):
    hod = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hod)

def format_rasi(lon):
    lon = lon % 360
    idx = int(lon // 30)
    deg = lon - idx * 30
    return f"{RASi[idx]} {deg:05.2f}°"

def nakshatra_pada(lon):
    lon = lon % 360
    n = int(lon // NAK_LEN)  # 0..26
    within = lon - n * NAK_LEN
    pada = int(within // PADA_LEN) + 1  # 1..4
    return NAKSHATRY_27[n], pada

def main():
    # 1) nastav siderický režim Lahiri
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    dt_utc = lokalny_na_utc()
    jd = julian_day(dt_utc)

    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    print("UTC čas:", dt_utc)
    print("Ayanamša (Lahiri) :", f"{swe.get_ayanamsa_ut(jd):.6f}°")

    # ASC sidericky: najprv tropický ASC z houses, potom odčítať ayanamšu
    houses, ascmc = swe.houses(jd, LAT, LON, DOMOVY_SYSTEM)
    asc_trop = ascmc[0]
    aya = swe.get_ayanamsa_ut(jd)
    asc_sid = (asc_trop - aya) % 360

    print("\nASC (sidericky):", format_rasi(asc_sid), f"({asc_sid:.2f}°)")

    print("\nPlanéty (sidericky) + nakšatra:")
    for meno, p in PLANETY:
        lonlat, _ = swe.calc_ut(jd, p, flags)
        lon = lonlat[0]
        nak, pada = nakshatra_pada(lon)
        print(f"- {meno:14s}: {format_rasi(lon):16s} | {nak}, pada {pada}")

if __name__ == "__main__":
    main()

