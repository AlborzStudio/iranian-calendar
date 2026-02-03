"""
Date conversion functions between Iranian Calendar and Gregorian calendar.

Handles precise conversions accounting for different New Year dates.
IC = Gregorian + 3000 (with Nowruz adjustment)
IC = Solar Hijri + 3621 (exact, same calendar structure)
"""

import datetime
from typing import Tuple, Optional
from .core import ICDate
from .leap import is_leap_year_33cycle


def ic_to_sh(ic_year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    Convert IC date to Solar Hijri (Persian calendar).
    
    This is trivial: IC = SH + 3621, month and day remain identical.
    
    Args:
        ic_year: IC year
        month: Month (1-12)
        day: Day of month
    
    Returns:
        Tuple of (sh_year, month, day)
    
    Example:
        >>> ic_to_sh(5025, 11, 1)
        (1404, 11, 1)
    """
    sh_year = ic_year - 3621
    return (sh_year, month, day)


def sh_to_ic(sh_year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    Convert Solar Hijri date to IC.
    
    Args:
        sh_year: Solar Hijri year
        month: Month (1-12)
        day: Day of month
    
    Returns:
        Tuple of (ic_year, month, day)
    
    Example:
        >>> sh_to_ic(1404, 11, 1)
        (5025, 11, 1)
    """
    ic_year = sh_year + 3621
    return (ic_year, month, day)


def ic_to_gregorian(ic_date: ICDate) -> datetime.date:
    """
    Convert IC date to Gregorian date.
    
    Process:
    1. Convert IC year to approximate Gregorian year: greg_year ≈ ic_year - 3000
    2. Calculate Nowruz (1 Farvardin) date in that Gregorian year
    3. Count days from Nowruz
    4. Add to Nowruz date to get final Gregorian date
    
    Args:
        ic_date: ICDate object
    
    Returns:
        datetime.date object
    
    Example:
        >>> ic_date = ICDate(5025, 11, 1)
        >>> greg = ic_to_gregorian(ic_date)
        >>> print(greg)  # 2026-01-21
    """
    # Approximate Gregorian year
    greg_year_approx = ic_date.year - 3000
    
    # Get Nowruz date for this IC year
    # Nowruz occurs around March 20-21
    # For now, use simplified approximation: March 21 of corresponding year
    # TODO: Implement precise astronomical calculation
    
    # Calculate which Gregorian year contains this IC year's Nowruz
    # IC year begins at Nowruz (spring), which is in March
    # So IC year 5025 begins March 2025 and ends March 2026
    greg_year_nowruz = greg_year_approx
    
    # Simplified Nowruz: March 21 (this is approximate)
    # Actual date varies between March 19-22 based on equinox timing
    nowruz = datetime.date(greg_year_nowruz, 3, 21)
    
    # Calculate days from Nowruz
    days_from_nowruz = ic_date.ordinal() - 1  # ordinal() returns 1-366, we need 0-365
    
    # Add days to Nowruz
    gregorian_date = nowruz + datetime.timedelta(days=days_from_nowruz)
    
    return gregorian_date


def gregorian_to_ic(greg_date: datetime.date) -> ICDate:
    """
    Convert Gregorian date to IC date.
    
    Process:
    1. Determine which IC year contains this Gregorian date
    2. Find Nowruz for that IC year
    3. Calculate days since Nowruz
    4. Convert to IC month/day
    
    Args:
        greg_date: datetime.date object
    
    Returns:
        ICDate object
    
    Example:
        >>> greg = datetime.date(2026, 1, 21)
        >>> ic_date = gregorian_to_ic(greg)
        >>> print(ic_date)  # 1 بهمن 5025 IC
    """
    # Approximate IC year
    ic_year_approx = greg_date.year + 3000
    
    # Determine which IC year we're in by checking if before or after Nowruz
    # Nowruz for IC year N occurs in Gregorian year (N - 3000)
    # around March 20-21
    
    # Get approximate Nowruz for this IC year
    nowruz_approx = datetime.date(greg_date.year, 3, 21)
    
    # If Gregorian date is before Nowruz, we're still in previous IC year
    if greg_date < nowruz_approx:
        ic_year = ic_year_approx - 1
        # Use previous year's Nowruz
        nowruz = datetime.date(greg_date.year - 1, 3, 21)
    else:
        ic_year = ic_year_approx
        nowruz = nowruz_approx
    
    # Calculate days since Nowruz
    days_diff = (greg_date - nowruz).days
    
    # Convert to IC month and day
    ic_month, ic_day = _ordinal_to_month_day(ic_year, days_diff + 1)
    
    return ICDate(ic_year, ic_month, ic_day)


def _ordinal_to_month_day(ic_year: int, ordinal: int) -> Tuple[int, int]:
    """
    Convert ordinal day number (1-366) to month and day.
    
    Args:
        ic_year: IC year (needed to determine if leap year)
        ordinal: Day number in year (1-366)
    
    Returns:
        Tuple of (month, day)
    
    Example:
        >>> _ordinal_to_month_day(5025, 306)
        (11, 1)  # 1 Bahman
    """
    if ordinal < 1 or ordinal > 366:
        raise ValueError(f"Ordinal day must be 1-366, got {ordinal}")
    
    days_in_months = [ICDate.days_in_month(ic_year, m) for m in range(1, 13)]
    
    cumulative = 0
    for month_idx, days in enumerate(days_in_months):
        if ordinal <= cumulative + days:
            day = ordinal - cumulative
            month = month_idx + 1
            return (month, day)
        cumulative += days
    
    # Should never reach here if ordinal is valid
    raise ValueError(f"Invalid ordinal day: {ordinal}")


def get_nowruz_gregorian(ic_year: int) -> datetime.date:
    """
    Get Gregorian date of Nowruz (1 Farvardin) for given IC year.
    
    Args:
        ic_year: IC year
    
    Returns:
        datetime.date of 1 Farvardin in Gregorian calendar
    
    Note:
        Currently uses simplified approximation (March 21).
        TODO: Implement precise astronomical calculation using equinox.
    
    Example:
        >>> get_nowruz_gregorian(5026)
        datetime.date(2026, 3, 21)
    """
    greg_year = ic_year - 3000
    # Simplified: always March 21
    # Actual varies March 19-22 based on equinox
    return datetime.date(greg_year, 3, 21)


def years_between(date1: ICDate, date2: ICDate) -> int:
    """
    Calculate complete years between two IC dates.
    
    Args:
        date1: First IC date
        date2: Second IC date
    
    Returns:
        Number of complete years (can be negative if date1 > date2)
    """
    years = date2.year - date1.year
    
    # Adjust if we haven't reached the anniversary yet
    if (date2.month, date2.day) < (date1.month, date1.day):
        years -= 1
    
    return years


def days_between(date1: ICDate, date2: ICDate) -> int:
    """
    Calculate days between two IC dates.
    
    Args:
        date1: First IC date
        date2: Second IC date
    
    Returns:
        Number of days (positive if date2 > date1)
    """
    # Convert both to Gregorian and use datetime arithmetic
    greg1 = ic_to_gregorian(date1)
    greg2 = ic_to_gregorian(date2)
    
    return (greg2 - greg1).days


# Reference dates for validation
REFERENCE_DATES = {
    'today': {
        'ic': (5025, 11, 1),
        'gregorian': datetime.date(2026, 1, 21),
        'sh': (1404, 11, 1),
    },
    'nowruz_5026': {
        'ic': (5026, 1, 1),
        'gregorian': datetime.date(2026, 3, 21),
        'sh': (1405, 1, 1),
    },
    'hijra': {
        'ic': (3622, 1, 1),
        'gregorian': datetime.date(622, 3, 21),  # Approximate
        'sh': (1, 1, 1),
    },
}


if __name__ == '__main__':
    print("Iranian Calendar Conversion Tests\n")
    
    # Test IC ↔ SH
    print("IC ↔ Solar Hijri:")
    ic_date = (5025, 11, 1)
    sh_date = ic_to_sh(*ic_date)
    print(f"  IC {ic_date} = SH {sh_date}")
    
    back = sh_to_ic(*sh_date)
    print(f"  SH {sh_date} = IC {back}")
    print(f"  Round-trip: {'✓' if back == ic_date else '✗'}")
    print()
    
    # Test IC → Gregorian
    print("IC → Gregorian:")
    ic = ICDate(5025, 11, 1)
    greg = ic_to_gregorian(ic)
    print(f"  {ic} = {greg}")
    print()
    
    # Test Gregorian → IC
    print("Gregorian → IC:")
    greg_date = datetime.date(2026, 1, 21)
    ic_result = gregorian_to_ic(greg_date)
    print(f"  {greg_date} = {ic_result}")
    print()
    
    # Test round-trip
    print("Round-trip test:")
    ic_orig = ICDate(5025, 11, 1)
    greg = ic_to_gregorian(ic_orig)
    ic_back = gregorian_to_ic(greg)
    print(f"  Original:  {ic_orig}")
    print(f"  Gregorian: {greg}")
    print(f"  Back:      {ic_back}")
    print(f"  Match: {'✓' if ic_orig == ic_back else '✗'}")
    print()
    
    # Test Nowruz dates
    print("Nowruz dates:")
    for year in [5024, 5025, 5026, 5027]:
        nowruz_greg = get_nowruz_gregorian(year)
        print(f"  1 Farvardin {year} IC = {nowruz_greg}")
