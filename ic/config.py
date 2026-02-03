"""
Configuration constants for Iranian Calendar.

Change these values to rename the entire calendar system globally.
All code references these constants rather than hardcoded strings.
"""

# Version
__version__ = "1.0.0"

# Calendar naming (CHANGEABLE - modify here to rename entire system)
CALENDAR_CODE = "IC"  # 2-letter abbreviation
CALENDAR_FULL_NAME = "Iranian Calendar"
CALENDAR_SHORT_NAME = "Iranian"

# Epoch and offsets (DO NOT CHANGE - these are mathematical constants)
EPOCH_BCE = 3000  # Epoch year in BCE
GREGORIAN_OFFSET = 3000  # IC = Gregorian + 3000
SOLAR_HIJRI_OFFSET = 3621  # IC = Solar Hijri + 3621

# Display format templates
DATE_SUFFIX = CALENDAR_CODE  # Used in formatted dates: "1 Bahman 5025 IC"
YEAR_FORMAT = "{year} {code}"  # Template for year display
