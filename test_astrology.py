# ~/Projects/test_astrology.py
# Western (Kerykeion) + Chinese BaZi (lunar_python) demo

from kerykeion import AstrologicalSubject
from lunar_python import Solar


def western_demo():
    # Example birth: Jan 1, 1990, 12:00 in Boston
    person = AstrologicalSubject(
        "Test User",
        1990, 1, 1, 12, 0,
        lng=-71.0589,
        lat=42.3601,
        tz_str="America/New_York",
    )

    sun_sign = person.sun.get("sign", "Unknown")

    return {
        "name": "Test User",
        "sun_sign": sun_sign,
    }


def bazi_demo(gender: int = 1):
    # Example birth: Jan 1, 1990, 12:00
    solar = Solar.fromYmdHms(1990, 1, 1, 12, 0, 0)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()

    bazi_str = ec.toString()

    # Compute Yun (fate cycle) and DaYun (10-year luck cycles)
    yun = ec.getYun(gender)
    start_year = yun.getStartYear()
    start_month = yun.getStartMonth()
    start_day = yun.getStartDay()

    da_yun = yun.getDaYun(3)
    da_yun_pretty = [
        f"{dy.getGanZhi()} (starts age {dy.getStartAge()}, year {dy.getStartYear()})"
        for dy in da_yun
    ]

    return {
        "bazi": bazi_str,
        "yun_start_offset": {
            "years": start_year,
            "months": start_month,
            "days": start_day,
        },
        "first_3_dayun": da_yun_pretty,
    }


def main():
    print("=== Western (Kerykeion) ===")
    w = western_demo()
    print(f"Sun sign: {w['sun_sign']}")

    print("\n=== Chinese / BaZi (lunar_python) ===")
    b = bazi_demo(gender=1)  # 1 = male, 0 = female
    print("BaZi pillars:", b["bazi"])
    ys = b["yun_start_offset"]
    print(
        f"Yun starts after: {ys['years']} years, {ys['months']} months, {ys['days']} days"
    )
    print("First 3 DaYun:", b["first_3_dayun"])


if __name__ == "__main__":
    main()

