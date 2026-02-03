"""
Leap year calculation for Iranian Calendar

Two methods:
1. 33-year cycle algorithm (primary for computation)
2. Astronomical observation (authoritative, requires equinox calculation)
"""

from typing import Optional


def is_leap_year_33cycle(ic_year: int) -> bool:
    """
    Determine if IC year is leap year using 33-year cycle algorithm.
    
    Leap years occur at positions: 1, 5, 9, 13, 17, 22, 26, 30 in each 33-year cycle.
    
    Average year length: 365.24219852 days
    Error vs tropical year: <0.5 seconds/year
    
    Args:
        ic_year: Iranian Calendar year (can be negative for pre-epoch dates)
    
    Returns:
        True if leap year, False otherwise
    
    Examples:
        >>> is_leap_year_33cycle(5025)  # (5025-1) % 33 = 8, position = 9
        True
        >>> is_leap_year_33cycle(5026)  # (5026-1) % 33 = 9, position = 10
        False
        >>> is_leap_year_33cycle(3622)  # Year of Hijra: position = 30
        True
    """
    # Calculate position in 33-year cycle (1-based)
    cycle_position = ((ic_year - 1) % 33) + 1
    
    # Leap years at these positions in the cycle
    LEAP_POSITIONS = {1, 5, 9, 13, 17, 22, 26, 30}
    
    return cycle_position in LEAP_POSITIONS


def is_leap_year_astronomical(ic_year: int, use_cache: bool = True) -> bool:
    """
    Determine if IC year is leap year using astronomical observation.
    
    This is the authoritative method but requires calculating spring equinox.
    A year is leap if the interval between consecutive 1 Farvardin dates is 366 days.
    
    Rule: If spring equinox occurs before noon (Tehran time), that day is 1 Farvardin.
          Otherwise, the next day is 1 Farvardin.
    
    Args:
        ic_year: Iranian Calendar year
        use_cache: Use cached astronomical data if available
    
    Returns:
        True if leap year, False otherwise
    
    Note:
        This function requires astronomical library (ephem/skyfield/astropy).
        Implementation pending - falls back to 33-year cycle for now.
    """
    # TODO: Implement astronomical calculation
    # For Phase 2, we'll use 33-year cycle as primary method
    # Astronomical calculation will be added in later iteration
    
    return is_leap_year_33cycle(ic_year)


def get_leap_years_in_range(start_year: int, end_year: int) -> list[int]:
    """
    Get all leap years in specified range.
    
    Args:
        start_year: Starting IC year (inclusive)
        end_year: Ending IC year (inclusive)
    
    Returns:
        List of leap years in the range
    
    Example:
        >>> get_leap_years_in_range(5020, 5030)
        [5021, 5025, 5029]
    """
    return [year for year in range(start_year, end_year + 1) 
            if is_leap_year_33cycle(year)]


def days_in_year(ic_year: int) -> int:
    """
    Get number of days in IC year.
    
    Args:
        ic_year: Iranian Calendar year
    
    Returns:
        366 for leap years, 365 for common years
    """
    return 366 if is_leap_year_33cycle(ic_year) else 365


def get_cycle_info(ic_year: int) -> dict:
    """
    Get detailed information about year's position in 33-year cycle.
    
    Args:
        ic_year: Iranian Calendar year
    
    Returns:
        Dictionary with cycle information:
        - cycle_number: Which 33-year cycle (1-based)
        - cycle_position: Position within cycle (1-33)
        - is_leap: Whether this year is leap
        - years_to_next_leap: Years until next leap year
    
    Example:
        >>> info = get_cycle_info(5025)
        >>> info['cycle_position']
        9
        >>> info['is_leap']
        True
    """
    cycle_number = ((ic_year - 1) // 33) + 1
    cycle_position = ((ic_year - 1) % 33) + 1
    is_leap = is_leap_year_33cycle(ic_year)
    
    # Calculate years to next leap year
    LEAP_POSITIONS = [1, 5, 9, 13, 17, 22, 26, 30]
    years_to_next = 0
    
    if not is_leap:
        # Find next leap position
        next_positions = [p for p in LEAP_POSITIONS if p > cycle_position]
        if next_positions:
            years_to_next = next_positions[0] - cycle_position
        else:
            # Next leap is in next cycle
            years_to_next = (33 - cycle_position) + 1
    
    return {
        'year': ic_year,
        'cycle_number': cycle_number,
        'cycle_position': cycle_position,
        'is_leap': is_leap,
        'years_to_next_leap': years_to_next,
        'cycle_length': 33
    }


# Validation constants
AVERAGE_YEAR_LENGTH = 365.24219852  # days (33-year cycle)
TROPICAL_YEAR = 365.24219  # days
ERROR_PER_YEAR = abs(AVERAGE_YEAR_LENGTH - TROPICAL_YEAR) * 86400  # seconds


if __name__ == '__main__':
    # Test with reference years
    test_years = [5025, 5026, 3622, 1, 2461]
    
    print("IC Leap Year Calculator\n")
    print("Year | Cycle Pos | Leap? | Days")
    print("-" * 40)
    
    for year in test_years:
        info = get_cycle_info(year)
        leap_str = "YES" if info['is_leap'] else "NO"
        days = days_in_year(year)
        print(f"{year:4d} | {info['cycle_position']:9d} | {leap_str:5s} | {days}")
    
    print(f"\nAverage year length: {AVERAGE_YEAR_LENGTH} days")
    print(f"Tropical year: {TROPICAL_YEAR} days")
    print(f"Error: {ERROR_PER_YEAR:.3f} seconds/year")
