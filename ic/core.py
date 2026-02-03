"""
Core ICDate class for Iranian Calendar date representation.

Provides date storage, validation, arithmetic, and formatting.
"""

from typing import Optional, Union
from .leap import is_leap_year_33cycle, days_in_year


class ICDate:
    """
    Iranian Calendar date representation.
    
    Stores year, month, day and provides validation, arithmetic, and formatting.
    Months and days are 1-indexed (1 Farvardin = month 1, day 1).
    
    Attributes:
        year (int): IC year (can be negative for pre-epoch dates)
        month (int): Month number (1-12)
        day (int): Day of month (1-31)
    """
    
    # Persian month names (standard spelling)
    MONTH_NAMES_PERSIAN = [
        'فروردین',    # 1. Farvardin (Spring)
        'اردیبهشت',   # 2. Ordibehesht (Spring)
        'خرداد',       # 3. Khordad (Spring)
        'تیر',         # 4. Tir (Summer)
        'مرداد',       # 5. Mordad (Summer)
        'شهریور',      # 6. Shahrivar (Summer)
        'مهر',         # 7. Mehr (Autumn)
        'آبان',        # 8. Aban (Autumn)
        'آذر',         # 9. Azar (Autumn)
        'دی',          # 10. Dey (Winter)
        'بهمن',        # 11. Bahman (Winter)
        'اسفند'        # 12. Esfand (Winter)
    ]
    
    # Transliterated month names (for ASCII contexts)
    MONTH_NAMES_LATIN = [
        'Farvardin', 'Ordibehesht', 'Khordad',
        'Tir', 'Mordad', 'Shahrivar',
        'Mehr', 'Aban', 'Azar',
        'Dey', 'Bahman', 'Esfand'
    ]
    
    # Days per month (common year)
    # First 6 months: 31 days
    # Next 5 months: 30 days
    # Last month (Esfand): 29 days (30 in leap year)
    MONTH_DAYS = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    
    # Persian weekday names (week starts Saturday)
    WEEKDAY_NAMES_PERSIAN = [
        'شنبه',        # Saturday
        'یکشنبه',      # Sunday
        'دوشنبه',      # Monday
        'سه‌شنبه',     # Tuesday
        'چهارشنبه',    # Wednesday
        'پنجشنبه',     # Thursday
        'جمعه'         # Friday
    ]
    
    WEEKDAY_NAMES_LATIN = [
        'Shanbe', 'Yekshanbe', 'Doshanbe',
        'Seshanbe', 'Chaharshanbe', 'Panjshanbe', 'Jome'
    ]
    
    def __init__(self, year: int, month: int, day: int):
        """
        Create IC date with validation.
        
        Args:
            year: IC year (can be negative for pre-epoch)
            month: Month (1-12)
            day: Day of month (1-31, depending on month)
        
        Raises:
            ValueError: If date is invalid
        
        Examples:
            >>> date = ICDate(5025, 11, 1)  # 1 Bahman 5025
            >>> date = ICDate(3622, 1, 1)   # 1 Farvardin 3622 (Hijra year)
        """
        if not self.is_valid(year, month, day):
            raise ValueError(
                f"Invalid IC date: {year}/{month}/{day}. "
                f"Month must be 1-12, day must be valid for that month."
            )
        
        self.year = year
        self.month = month
        self.day = day
    
    @staticmethod
    def is_valid(year: int, month: int, day: int) -> bool:
        """
        Check if date components form a valid IC date.
        
        Args:
            year: IC year
            month: Month (1-12)
            day: Day of month
        
        Returns:
            True if valid, False otherwise
        """
        # Check month range
        if not (1 <= month <= 12):
            return False
        
        # Check day range for this month
        max_day = ICDate.days_in_month(year, month)
        return 1 <= day <= max_day
    
    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """
        Get number of days in specified month of given year.
        
        Args:
            year: IC year
            month: Month (1-12)
        
        Returns:
            Number of days in that month
        
        Examples:
            >>> ICDate.days_in_month(5025, 12)  # Esfand in leap year
            30
            >>> ICDate.days_in_month(5026, 12)  # Esfand in common year
            29
        """
        if not (1 <= month <= 12):
            raise ValueError(f"Invalid month: {month}. Must be 1-12.")
        
        # Esfand (month 12) varies: 30 in leap year, 29 in common year
        if month == 12:
            return 30 if is_leap_year_33cycle(year) else 29
        
        return ICDate.MONTH_DAYS[month - 1]
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Check if year is leap year.
        
        Args:
            year: IC year
        
        Returns:
            True if leap year, False otherwise
        """
        return is_leap_year_33cycle(year)
    
    def ordinal(self) -> int:
        """
        Calculate ordinal day number within the year (1-365 or 1-366).
        
        Returns:
            Day number in year (1 Farvardin = 1, 1 Bahman = 306, etc.)
        """
        # Sum days in previous months
        days = sum(self.days_in_month(self.year, m) for m in range(1, self.month))
        # Add day of current month
        return days + self.day
    
    def to_tuple(self) -> tuple[int, int, int]:
        """Return (year, month, day) tuple."""
        return (self.year, self.month, self.day)
    
    def __str__(self) -> str:
        """
        Format date in standard Persian format: "day month_name year IC"
        
        Returns:
            Formatted string, e.g., "1 بهمن 5025 IC"
        """
        month_name = self.MONTH_NAMES_PERSIAN[self.month - 1]
        return f"{self.day} {month_name} {self.year} IC"
    
    def __repr__(self) -> str:
        """Python representation."""
        return f"ICDate({self.year}, {self.month}, {self.day})"
    
    def format(self, fmt: str = 'persian') -> str:
        """
        Format date according to specified format.
        
        Args:
            fmt: Format type:
                - 'persian': "1 بهمن 5025 IC" (default)
                - 'latin': "1 Bahman 5025 IC"
                - 'numeric': "5025-11-01"
                - 'compact': "5025/11/01"
                - 'full': "1 بهمن 5025 IC (1404 SH)"
        
        Returns:
            Formatted date string
        """
        if fmt == 'persian':
            month_name = self.MONTH_NAMES_PERSIAN[self.month - 1]
            return f"{self.day} {month_name} {self.year} IC"
        
        elif fmt == 'latin':
            month_name = self.MONTH_NAMES_LATIN[self.month - 1]
            return f"{self.day} {month_name} {self.year} IC"
        
        elif fmt == 'numeric':
            return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
        
        elif fmt == 'compact':
            return f"{self.year:04d}/{self.month:02d}/{self.day:02d}"
        
        elif fmt == 'full':
            month_name = self.MONTH_NAMES_PERSIAN[self.month - 1]
            sh_year = self.year - 3621
            return f"{self.day} {month_name} {self.year} IC ({sh_year} SH)"
        
        else:
            raise ValueError(f"Unknown format: {fmt}")
    
    def __eq__(self, other) -> bool:
        """Check date equality."""
        if not isinstance(other, ICDate):
            return False
        return (self.year == other.year and 
                self.month == other.month and 
                self.day == other.day)
    
    def __lt__(self, other) -> bool:
        """Compare dates for ordering."""
        if not isinstance(other, ICDate):
            return NotImplemented
        return self.to_tuple() < other.to_tuple()
    
    def __le__(self, other) -> bool:
        """Less than or equal comparison."""
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        """Greater than comparison."""
        if not isinstance(other, ICDate):
            return NotImplemented
        return self.to_tuple() > other.to_tuple()
    
    def __ge__(self, other) -> bool:
        """Greater than or equal comparison."""
        return self == other or self > other
    
    def __hash__(self) -> int:
        """Make ICDate hashable."""
        return hash((self.year, self.month, self.day))


if __name__ == '__main__':
    # Test ICDate class
    print("IC Date Class Tests\n")
    
    # Current date
    today = ICDate(5025, 11, 1)
    print(f"Today: {today}")
    print(f"Numeric: {today.format('numeric')}")
    print(f"Latin: {today.format('latin')}")
    print(f"Full: {today.format('full')}")
    print(f"Ordinal day: {today.ordinal()}")
    print(f"Is leap year: {today.is_leap_year(today.year)}")
    print()
    
    # Next Nowruz
    nowruz = ICDate(5026, 1, 1)
    print(f"Next Nowruz: {nowruz}")
    print(f"Days in Esfand 5025: {ICDate.days_in_month(5025, 12)}")
    print(f"Days in Esfand 5026: {ICDate.days_in_month(5026, 12)}")
    print()
    
    # Historical dates
    hijra = ICDate(3622, 1, 1)
    print(f"Hijra: {hijra}")
    
    cyrus = ICDate(2461, 1, 1)
    print(f"Cyrus enters Babylon: {cyrus}")
    print()
    
    # Comparison
    print(f"Today < Nowruz: {today < nowruz}")
    print(f"Hijra < Cyrus: {hijra < cyrus}")
