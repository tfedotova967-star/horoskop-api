# den3_asc_domy.py
# Pridá ASC + MC + domy (cusps) k výpočtu.

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

DOMOVY_SYSTEM = b"P"  # P=Placidus (najčastejší v západnej astrológii)
# -----------------------------

ZNAMENIA = [
    "Baran","Býk","Blíženci","Rak","Lev","Panna",
    "Váhy","Škorpión","Strelec","Kozorožec","Vodnár","Ryby"
]

def lokalny_na_utc():
    tz = ZoneInfo(CASOVE_PASMO)
    dt_local = datetime(ROK, MESIAC, DEN, HODINA, MINUTA, tzinfo=tz)
    return dt_local.astimezone(timezone.utc)

def julian_day(dt_utc):
    hod = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hod)

def format_pozicia(ecl_lon):
    ecl_lon = ecl_lon % 360
    idx = int(ecl_lon // 30)
    stupne = ecl_lon - idx * 30
    return f"{ZNAMENIA[idx]} {stupne:05.2f}°"

def main():
    dt_utc = lokalny_na_utc()
    jd = julian_day(dt_utc)

    # Domy + Asc/MC
    houses, ascmc = swe.houses(jd, LAT, LON, DOMOVY_SYSTEM)
    asc = ascmc[0]
    mc = ascmc[1]

    print("UTC čas:", dt_utc)
    print("ASC:", format_pozicia(asc), f"({asc:.2f}°)")
    print("MC :", format_pozicia(mc),  f"({mc:.2f}°)")

    print("\nDomové hroty (1–12):")
    for i, cusp in enumerate(houses, start=1):
        print(f"{i:2d}. dom: {format_pozicia(cusp)}  ({cusp:.2f}°)")

if __name__ == "__main__":
    main()

