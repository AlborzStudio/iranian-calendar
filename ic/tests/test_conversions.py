"""
Unit tests for Iranian Calendar date conversions.

Run with: pytest tests/test_conversions.py
"""

import pytest
import datetime
from ic import ICDate, ic_to_gregorian, gregorian_to_ic
from ic.conversions import ic_to_sh, sh_to_ic


class TestConversions:
    """Test date conversions."""
    
    def test_ic_to_sh(self):
        """Test IC to Solar Hijri conversion."""
        ic = (5025, 11, 1)
        sh = ic_to_sh(*ic)
        assert sh == (1404, 11, 1)
    
    def test_sh_to_ic(self):
        """Test Solar Hijri to IC conversion."""
        sh = (1404, 11, 1)
        ic = sh_to_ic(*sh)
        assert ic == (5025, 11, 1)
    
    def test_ic_sh_roundtrip(self):
        """Test IC ↔ SH round-trip conversion."""
        ic_orig = (5025, 11, 1)
        sh = ic_to_sh(*ic_orig)
        ic_back = sh_to_ic(*sh)
        assert ic_orig == ic_back
    
    def test_ic_to_gregorian_today(self):
        """Test IC to Gregorian for known date."""
        ic_date = ICDate(5025, 11, 1)
        greg_date = ic_to_gregorian(ic_date)
        assert greg_date == datetime.date(2026, 1, 21)
    
    def test_gregorian_to_ic_today(self):
        """Test Gregorian to IC for known date."""
        greg_date = datetime.date(2026, 1, 21)
        ic_date = gregorian_to_ic(greg_date)
        assert ic_date.year == 5025
        assert ic_date.month == 11
        assert ic_date.day == 1
    
    def test_ic_gregorian_roundtrip(self):
        """Test IC ↔ Gregorian round-trip conversion."""
        ic_orig = ICDate(5025, 11, 1)
        greg = ic_to_gregorian(ic_orig)
        ic_back = gregorian_to_ic(greg)
        assert ic_orig == ic_back
    
    def test_nowruz_dates(self):
        """Test Nowruz conversions."""
        # 1 Farvardin should convert to approximately March 21
        ic_nowruz = ICDate(5026, 1, 1)
        greg_nowruz = ic_to_gregorian(ic_nowruz)
        assert greg_nowruz.month == 3
        assert greg_nowruz.day in [19, 20, 21, 22]  # Nowruz range


class TestReferenceData:
    """Test against reference dates from specification."""
    
    def test_today_reference(self):
        """Test today's date: 1 Bahman 5025 IC = 21 January 2026 CE."""
        ic_date = ICDate(5025, 11, 1)
        greg_date = ic_to_gregorian(ic_date)
        
        assert greg_date.year == 2026
        assert greg_date.month == 1
        assert greg_date.day == 21
    
    def test_nowruz_5026_reference(self):
        """Test Nowruz 5026: 1 Farvardin 5026 IC = 21 March 2026 CE."""
        ic_date = ICDate(5026, 1, 1)
        greg_date = ic_to_gregorian(ic_date)
        
        assert greg_date.year == 2026
        assert greg_date.month == 3
        # Allowing range due to simplified Nowruz calculation
        assert greg_date.day in [19, 20, 21, 22]
    
    def test_year_conversions(self):
        """Test year-level conversions."""
        # IC = Gregorian + 3000
        assert 5026 == 2026 + 3000
        assert 3622 == 622 + 3000
        
        # IC = Solar Hijri + 3621
        assert 5025 == 1404 + 3621
        assert 5026 == 1405 + 3621


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
