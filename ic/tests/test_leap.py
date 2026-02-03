"""
Unit tests for Iranian Calendar leap year functionality.

Run with: pytest tests/test_leap.py
"""

import pytest
from ic import is_leap_year_33cycle
from ic.leap import get_cycle_info, days_in_year


class TestLeapYear:
    """Test leap year calculation."""
    
    def test_known_leap_years(self):
        """Test against known leap years."""
        assert is_leap_year_33cycle(5025) == True   # Position 9
        assert is_leap_year_33cycle(5021) == True   # Position 5
        assert is_leap_year_33cycle(5029) == True   # Position 13
    
    def test_known_common_years(self):
        """Test against known common years."""
        assert is_leap_year_33cycle(5026) == False  # Position 10
        assert is_leap_year_33cycle(5024) == False  # Position 8
        assert is_leap_year_33cycle(5027) == False  # Position 11
    
    def test_cycle_positions(self):
        """Test 33-year cycle positions."""
        leap_positions = [1, 5, 9, 13, 17, 22, 26, 30]
        
        for pos in leap_positions:
            # Year that has this position
            year = pos  # Year 1 has position 1, year 5 has position 5, etc.
            info = get_cycle_info(year)
            assert info['cycle_position'] == pos
            assert info['is_leap'] == True
    
    def test_days_in_year(self):
        """Test days in year calculation."""
        assert days_in_year(5025) == 366  # Leap
        assert days_in_year(5026) == 365  # Common


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
