# den2_planety.py
# Výpočet polôh planét zo zadaného dátumu, času a miesta.
# Výstup: znamenie + stupeň.

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
# -----------------------------

PLANETY = [
    ("Slnko", swe.SUN),
    ("Mesiac", swe.MOON),
    ("Merkúr", swe.MERCURY),
    ("Venuša", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("Urán", swe.URANUS),
    ("Neptún", swe.NEPTUNE),
    ("Pluto", swe.PLUTO),
]

ZNAMENIA = [
    "Baran","Býk","Blíženci","Rak","Lev","Panna",
    "Váhy","Škorpión","Strelec","Kozorožec","Vodnár","Ryby"
]

def lokalny_na_utc():
    tz = ZoneInfo(CASOVE_PASMO)
    dt_local = datetime(ROK, MESIAC, DEN, HODINA, MINUTA, tzinfo=tz)
    return dt_local.astimezone(timezone.utc)

def julian_day(dt_utc):
    hod = dt_utc.hour + dt_utc.minute / 60
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hod)

def format_pozicia(ecl_lon):
    ecl_lon = ecl_lon % 360
    idx = int(ecl_lon // 30)
    stupne = ecl_lon - idx * 30
    return f"{ZNAMENIA[idx]} {stupne:05.2f}°"

def main():
    dt_utc = lokalny_na_utc()
    jd = julian_day(dt_utc)

    print("UTC čas:", dt_utc)
    print("\nPlanéty:")

    for meno, p in PLANETY:
        lonlat, _ = swe.calc_ut(jd, p, swe.FLG_SWIEPH)
        lon = lonlat[0]
        print(f"- {meno:10s}: {format_pozicia(lon)}")

if __name__ == "__main__":
    main()

