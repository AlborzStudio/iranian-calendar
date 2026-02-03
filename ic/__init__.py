"""
Iranian Calendar (IC) - Solar calendar with epoch at 3000 BCE

This package provides date representation, conversion, and manipulation
for the Iranian Calendar system.

Epoch: 1 Farvardin 1 IC = 3000 BCE (proleptic Gregorian)
Structure: Identical to Solar Hijri (Persian calendar)
Year conversion: IC = Gregorian + 3000 = Solar Hijri + 3621
"""

__version__ = '1.0.0'
__author__ = 'IC Project'

from .core import ICDate
from .leap import is_leap_year_33cycle, is_leap_year_astronomical
from .conversions import ic_to_gregorian, gregorian_to_ic

__all__ = [
    'ICDate',
    'is_leap_year_33cycle',
    'is_leap_year_astronomical',
    'ic_to_gregorian',
    'gregorian_to_ic',
]
