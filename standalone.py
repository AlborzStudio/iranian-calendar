"""
Iranian Calendar (IC) - Standalone Library
Version: 1.0.0
Date: 2 Bahman 5025 (22 January 2026)
License: MIT

Single-file implementation with configurable calendar naming.

Configuration: Modify these constants to rename the calendar system
"""

from datetime import datetime, timedelta, date
from typing import Tuple, Union

# CONFIGURATION - Change these to rename the calendar
CALENDAR_CODE = "IC"
CALENDAR_FULL_NAME = "Iranian Calendar"
EPOCH_BCE = 3000
GREGORIAN_OFFSET = 3000
SOLAR_HIJRI_OFFSET = 3621

# Month names
MONTH_NAMES_PERSIAN = [
    'فروردین', 'اردیبهشت', 'خرداد',
    'تیر', 'مرداد', 'شهریور', 
    'مهر', 'آبان', 'آذر',
    'دی', 'بهمن', 'اسفند'
]

MONTH_NAMES_LATIN = [
    'Farvardin', 'Ordibehesht', 'Khordad',
    'Tir', 'Mordad', 'Shahrivar',
    'Mehr', 'Aban', 'Azar',
    'Dey', 'Bahman', 'Esfand'
]

MONTH_DAYS = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
LEAP_POSITIONS = {1, 5, 9, 13, 17, 22, 26, 30}


def is_leap_year(year: int) -> bool:
    """Check if year is leap year using 33-year cycle."""
    cycle_position = ((year - 1) % 33) + 1
    return cycle_position in LEAP_POSITIONS


def get_nowruz(year: int) -> date:
    """Get Gregorian date of Nowruz (1 Farvardin) for given year."""
    gregorian_year = year - GREGORIAN_OFFSET
    return date(gregorian_year, 3, 21)  # Simplified


def _days_in_month(year: int, month: int) -> int:
    """Get number of days in month."""
    if month == 12:
        return 30 if is_leap_year(year) else 29
    return MONTH_DAYS[month - 1]


def _ordinal_to_month_day(year: int, ordinal: int) -> Tuple[int, int]:
    """Convert ordinal day to month and day."""
    cumulative = 0
    for month in range(1, 13):
        days_in_month = _days_in_month(year, month)
        if ordinal <= cumulative + days_in_month:
            day = ordinal - cumulative
            return (month, day)
        cumulative += days_in_month
    raise ValueError(f"Invalid ordinal day: {ordinal}")


def _month_day_to_ordinal(year: int, month: int, day: int) -> int:
    """Convert month/day to ordinal day in year."""
    ordinal = sum(_days_in_month(year, m) for m in range(1, month))
    return ordinal + day


def to_ic(gregorian_date: Union[date, datetime]) -> Tuple[int, int, int]:
    """Convert Gregorian date to IC date."""
    if isinstance(gregorian_date, datetime):
        gregorian_date = gregorian_date.date()
    
    year_approx = gregorian_date.year + GREGORIAN_OFFSET
    nowruz_approx = get_nowruz(year_approx)
    
    if gregorian_date < nowruz_approx:
        year = year_approx - 1
        nowruz = get_nowruz(year)
    else:
        year = year_approx
        nowruz = nowruz_approx
    
    days_diff = (gregorian_date - nowruz).days
    ordinal = days_diff + 1
    month, day = _ordinal_to_month_day(year, ordinal)
    
    return (year, month, day)


def from_ic(year: int, month: int, day: int) -> date:
    """Convert IC date to Gregorian date."""
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}")
    
    max_day = _days_in_month(year, month)
    if not (1 <= day <= max_day):
        raise ValueError(f"Invalid day: {day}. Month {month} has {max_day} days.")
    
    nowruz = get_nowruz(year)
    ordinal = _month_day_to_ordinal(year, month, day)
    days_offset = ordinal - 1
    gregorian_date = nowruz + timedelta(days=days_offset)
    
    return gregorian_date


def format_date(year: int, month: int, day: int, style: str = 'persian') -> str:
    """Format IC date in specified style."""
    if style == 'persian':
        month_name = MONTH_NAMES_PERSIAN[month - 1]
        return f"{day} {month_name} {year} {CALENDAR_CODE}"
    elif style == 'latin':
        month_name = MONTH_NAMES_LATIN[month - 1]
        return f"{day} {month_name} {year} {CALENDAR_CODE}"
    elif style == 'numeric':
        return f"{year:04d}-{month:02d}-{day:02d}"
    elif style == 'compact':
        return f"{year:04d}/{month:02d}/{day:02d}"
    else:
        raise ValueError(f"Unknown style: {style}")


def ic_to_sh(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """Convert IC to Solar Hijri (trivial: year offset only)."""
    sh_year = year - SOLAR_HIJRI_OFFSET
    return (sh_year, month, day)


def sh_to_ic(sh_year: int, sh_month: int, sh_day: int) -> Tuple[int, int, int]:
    """Convert Solar Hijri to IC."""
    year = sh_year + SOLAR_HIJRI_OFFSET
    return (year, sh_month, sh_day)


def today_ic() -> Tuple[int, int, int]:
    """Get today's date in IC."""
    return to_ic(date.today())


def get_cycle_info(year: int) -> dict:
    """Get 33-year cycle information for year."""
    cycle_number = ((year - 1) // 33) + 1
    cycle_position = ((year - 1) % 33) + 1
    is_leap = cycle_position in LEAP_POSITIONS
    
    return {
        'year': year,
        'cycle_number': cycle_number,
        'cycle_position': cycle_position,
        'is_leap': is_leap,
        'days_in_year': 366 if is_leap else 365,
    }


if __name__ == '__main__':
    print(f"{CALENDAR_FULL_NAME} - Standalone Library v1.0.0")
    print("=" * 60)
    
    print("\n1. Today's Date:")
    today = today_ic()
    print(f"   {format_date(*today, 'latin')}")
    print(f"   {format_date(*today, 'numeric')}")
    
    print("\n2. Conversion Example:")
    test_date = date(2026, 3, 21)
    ic_date = to_ic(test_date)
    print(f"   Gregorian: {test_date}")
    print(f"   {CALENDAR_CODE}: {format_date(*ic_date, 'latin')}")
    
    back = from_ic(*ic_date)
    print(f"   Round-trip: {back} ({'✓' if back == test_date else '✗'})")
    
    print("\n3. Leap Year Info:")
    for year in [5025, 5026]:
        info = get_cycle_info(year)
        print(f"   {year}: Position {info['cycle_position']}, "
              f"{'Leap' if info['is_leap'] else 'Common'}, "
              f"{info['days_in_year']} days")
    
    print("\n" + "=" * 60)
