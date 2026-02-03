"""
Unit tests for Iranian Calendar core ICDate class.

Run with: pytest tests/test_core.py
"""

import pytest
from ic import ICDate


class TestICDate:
    """Test ICDate class."""
    
    def test_create_valid_date(self):
        """Test creating valid dates."""
        date = ICDate(5025, 11, 1)
        assert date.year == 5025
        assert date.month == 11
        assert date.day == 1
    
    def test_invalid_month(self):
        """Test invalid month raises error."""
        with pytest.raises(ValueError):
            ICDate(5025, 13, 1)
        
        with pytest.raises(ValueError):
            ICDate(5025, 0, 1)
    
    def test_invalid_day(self):
        """Test invalid day raises error."""
        with pytest.raises(ValueError):
            ICDate(5025, 1, 32)  # Farvardin has 31 days
        
        with pytest.raises(ValueError):
            ICDate(5026, 12, 30)  # Esfand has 29 days in common year
    
    def test_esfand_leap_year(self):
        """Test Esfand has correct days in leap/common years."""
        # Leap year: Esfand has 30 days
        date_leap = ICDate(5025, 12, 30)  # Should work
        assert date_leap.day == 30
        
        # Common year: Esfand has 29 days
        date_common = ICDate(5026, 12, 29)  # Should work
        assert date_common.day == 29
    
    def test_string_representation(self):
        """Test string formatting."""
        date = ICDate(5025, 11, 1)
        assert "بهمن" in str(date)
        assert "5025" in str(date)
        assert "IC" in str(date)
    
    def test_date_comparison(self):
        """Test date comparison operators."""
        date1 = ICDate(5025, 11, 1)
        date2 = ICDate(5026, 1, 1)
        date3 = ICDate(5025, 11, 1)
        
        assert date1 < date2
        assert date2 > date1
        assert date1 == date3
        assert date1 <= date3
        assert date1 >= date3
    
    def test_ordinal_calculation(self):
        """Test ordinal day calculation."""
        # 1 Farvardin = day 1
        date1 = ICDate(5025, 1, 1)
        assert date1.ordinal() == 1
        
        # 1 Bahman = day 307 (6*31 + 5*30 + 1)
        date2 = ICDate(5025, 11, 1)
        assert date2.ordinal() == 307


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
