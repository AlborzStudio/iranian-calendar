# Iranian Calendar (IC)

[![Tests](https://github.com/AlborzStudio/iranian-calendar/actions/workflows/tests.yml/badge.svg)](https://github.com/AlborzStudio/iranian-calendar/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/iranian-calendar.svg)](https://badge.fury.io/py/iranian-calendar)
[![Python](https://img.shields.io/pypi/pyversions/iranian-calendar.svg)](https://pypi.org/project/iranian-calendar/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python package for the Iranian Calendar (IC) system...

**Version:** 1.0.0  
**Status:** Production Ready  
**Python:** 3.8+  
**License:** MIT

Solar calendar with epoch at 3000 BCE, based on Sherwin Vakili's "On the Determination of the Epoch of History"

---

## Overview

The **Iranian Calendar (IC)** is an epoch correction to the Persian solar calendar, not a new calendar system. It maintains identical structure, months, and astronomical precision of the Solar Hijri calendar whilst providing a continuous timeline from the beginning of recorded civilisation.

### Key Facts

- **Name:** Iranian Calendar (abbreviated: IC)
- **Epoch:** 1 Farvardin 1 IC = 3000 BCE
- **Structure:** Identical to Solar Hijri (Persian) calendar
- **Conversion:** IC = Gregorian + 3000 = Solar Hijri + 3621
- **Today:** 5 Bahman 5025 IC (25 January 2026 CE)

### What Makes IC Different?

**IC is NOT:**
- A new calendar system
- A replacement for Solar Hijri
- A replacement for Gregorian

**IC IS:**
- An epoch correction (only year number changes)
- Compatible with existing calendars
- A continuous civilisational timeline

---

## Quick Start

### Installation

```bash
# Install from source
pip install -e .

# Or use standalone file (no installation)
python3 standalone.py
```

### Basic Usage

```python
from ic import ICDate, ic_to_gregorian, gregorian_to_ic
import datetime

# Create IC date
today = ICDate(5025, 11, 2)  # 2 Bahman 5025 IC
print(today)  # Output: 2 بهمن 5025 IC

# Format in different styles
print(today.format('persian'))   # 2 بهمن 5025 IC
print(today.format('latin'))     # 2 Bahman 5025 IC
print(today.format('numeric'))   # 5025-11-02
print(today.format('compact'))   # 5025/11/02

# Convert to Gregorian
greg = ic_to_gregorian(today)
print(greg)  # 2026-01-22

# Convert from Gregorian
ic_date = gregorian_to_ic(datetime.date(2026, 3, 21))
print(ic_date)  # ICDate(5026, 1, 1) - Nowruz
```

### Command-Line Interface

```bash
# Show today's date
python3 -m ic.cli today

# Convert dates
python3 -m ic.cli convert 2026-12-25
python3 -m ic.cli convert 5026-10-04

# Check leap year
python3 -m ic.cli leap 5025

# Show Nowruz
python3 -m ic.cli nowruz 5026
```

---

## Calendar Structure

### Months

| No. | Persian | Latin | Days | Season |
|-----|---------|-------|------|--------|
| 1 | فروردین | Farvardin | 31 | Spring |
| 2 | اردیبهشت | Ordibehesht | 31 | Spring |
| 3 | خرداد | Khordad | 31 | Spring |
| 4 | تیر | Tir | 31 | Summer |
| 5 | مرداد | Mordad | 31 | Summer |
| 6 | شهریور | Shahrivar | 31 | Summer |
| 7 | مهر | Mehr | 30 | Autumn |
| 8 | آبان | Aban | 30 | Autumn |
| 9 | آذر | Azar | 30 | Autumn |
| 10 | دی | Dey | 30 | Winter |
| 11 | بهمن | Bahman | 30 | Winter |
| 12 | اسفند | Esfand | 29/30* | Winter |

*30 days in leap years

### Leap Years

**33-year cycle algorithm:**
- Leap years at cycle positions: 1, 5, 9, 13, 17, 22, 26, 30
- Average year: 365.24219852 days
- Error: <0.5 seconds/year (most accurate solar calendar)

**Examples:**
```python
from ic import is_leap_year_33cycle

print(is_leap_year_33cycle(5025))  # True (position 9)
print(is_leap_year_33cycle(5026))  # False (position 10)
```

---

## Examples

### Date Conversions

```python
from ic import ICDate, ic_to_gregorian, gregorian_to_ic
from datetime import date

# Nowruz (New Year)
nowruz = ICDate(5026, 1, 1)
greg = ic_to_gregorian(nowruz)
print(f"{nowruz.format('latin')} = {greg}")
# Output: 1 Farvardin 5026 IC = 2026-03-21

# Historical dates
cyrus = ICDate(2461, 1, 1)  # Cyrus enters Babylon (539 BCE)
hijra = ICDate(3622, 1, 1)  # Islamic calendar epoch (622 CE)

# Your birthday
birthday = date(1990, 5, 15)
ic_bday = gregorian_to_ic(birthday)
print(ic_bday.format('latin'))
```

### Date Arithmetic

```python
from ic import ICDate

date1 = ICDate(5025, 11, 2)
date2 = ICDate(5026, 1, 1)

# Comparison
print(date1 < date2)  # True
print(date1 == ICDate(5025, 11, 2))  # True

# Ordinal day in year
print(date1.ordinal())  # Day number in year (1-366)
```

### Solar Hijri Conversion

```python
from ic.conversions import ic_to_sh, sh_to_ic

# IC to Solar Hijri (trivial: IC - 3621)
sh_date = ic_to_sh(5025, 11, 2)
print(sh_date)  # (1404, 11, 2)

# Solar Hijri to IC
ic_date = sh_to_ic(1404, 11, 2)
print(ic_date)  # (5025, 11, 2)
```

### Configurable Naming

All calendar references use configuration constants:

```python
from ic import config

print(config.CALENDAR_CODE)       "IC"
print(config.CALENDAR_FULL_NAME)  # "Iranian Calendar"

# To rename entire system: edit ic/config.py
# Change CALENDAR_CODE = "IC" to whatever you want
# Everything updates automatically
```

---

## API Reference

### Core Classes

#### `ICDate(year, month, day)`

Main date class.

**Methods:**
- `format(style)` - Format date ('persian', 'latin', 'numeric', 'compact', 'full')
- `ordinal()` - Day number in year (1-366)
- `to_tuple()` - Return (year, month, day)

**Class Methods:**
- `is_valid(year, month, day)` - Validate date
- `days_in_month(year, month)` - Days in month
- `is_leap_year(year)` - Check if leap year

**Operators:**
- Comparison: `<`, `>`, `==`, `<=`, `>=`
- Hash support (can use in sets/dicts)

**Example:**
```python
from ic import ICDate

date = ICDate(5025, 11, 2)
print(date.format('persian'))  # 2 بهمن 5025 IC
print(date.ordinal())          # 307 (day in year)
print(date < ICDate(5026, 1, 1))  # True
```

### Conversion Functions

#### `ic_to_gregorian(ic_date)`

Convert IC date to Gregorian.

```python
from ic import ICDate, ic_to_gregorian

ic = ICDate(5025, 11, 2)
greg = ic_to_gregorian(ic)
print(greg)  # 2026-01-22
```

#### `gregorian_to_ic(gregorian_date)`

Convert Gregorian date to IC.

```python
from ic import gregorian_to_ic
from datetime import date

greg = date(2026, 1, 22)
ic = gregorian_to_ic(greg)
print(ic.format('latin'))  # 2 Bahman 5025 IC
```

### Leap Year Functions

#### `is_leap_year_33cycle(year)`

Check if year is leap using 33-year cycle.

```python
from ic import is_leap_year_33cycle

print(is_leap_year_33cycle(5025))  # True
print(is_leap_year_33cycle(5026))  # False
```

---

## Standalone Version

For simple use without installation:

```python
# Use standalone.py (included)
import standalone as ic

today = ic.today_ic()
print(ic.format_date(*today, 'latin'))
# Output: 2 Bahman 5025 IC

# All functions available
greg = ic.from_ic(5025, 11, 2)
ic_date = ic.to_ic(greg)
```

**Advantages:**
- No installation required
- Single file (copy and use)
- All core functionality
- Configurable (edit constants at top)

---

## Project Structure

```
iranian-calendar-1.0.0/
│
├── ic/                      # Main package
│   ├── __init__.py          # Package exports
│   ├── config.py            # Configuration (CHANGEABLE)
│   ├── core.py              # ICDate class
│   ├── leap.py              # Leap year algorithms
│   ├── conversions.py       # Date conversions
│   ├── cli.py               # Command-line interface
│   └── tests/               # Test suite (39 tests)
│
├── standalone.py            # Single-file version
├── pyproject.toml           # Package configuration
├── setup.py                 # Installation setup
│
├── PROJECT_PLAN.md          # Development roadmap
├── CHANGELOG.md             # Version history
└── LICENSE                  # MIT License
```

## Testing

```bash
# Run test suite
cd ic
python3 tests/run_tests.py

# Expected output: 39/39 tests passed
```

**Test coverage:**
- Leap year calculation
- Date validation
- Date conversions (IC ↔ Gregorian ↔ Solar Hijri)
- Round-trip conversions
- Reference date verification
- Error handling

---

## Theoretical Foundation

Based on Sherwin Vakili's paper "On the Determination of the Epoch of History" which argues for establishing a civilisational epoch at ~3000 BCE rather than religious or arbitrary starting points.

**Key concepts:**
- Epoch correction, not calendar reform
- Historical proportionality
- Continuous civilisational timeline
- Independence from religious/colonial overlays


---

## Technical Specification

**Epoch:** 1 Farvardin 1 IC = 3000 BCE (proleptic Gregorian)

**Year conversion:**
```
IC = Gregorian + 3000
IC = Solar Hijri + 3621
```

**Month structure:** Identical to Solar Hijri (12 months, 365/366 days)

**Leap years:** 33-year cycle (positions 1, 5, 9, 13, 17, 22, 26, 30)

**Nowruz:** 1 Farvardin (spring equinox, ~21 March)


---

## Development

### Requirements

- Python 3.8+
- No external dependencies for core functionality

### Contributing

1. Follow naming conventions (see PROJECT_PLAN.md)
2. Add tests for new features
3. Update documentation
4. Maintain backward compatibility

### Roadmap

**Current (v1.0.0):**
- Core date class
- 33-year cycle leap years
- Date conversions
- Command-line interface
- Configurable naming

**Future:**
- Astronomical Nowruz (precise equinox)
- Date arithmetic (add/subtract)
- Additional language implementations
- Web API
- CalDAV/iCal integration

---

## Frequently Asked Questions

### Q: Is this a replacement for the Persian calendar?

No. IC uses the exact same calendar structure as Solar Hijri. Only the year number is different (IC = SH + 3621).

### Q: How accurate are the leap years?

The 33-year cycle is extremely accurate (<0.5 seconds/year error). It's the same algorithm used by the Persian calendar.

### Q: Can I change the calendar name?

Yes. Edit `ic/config.py` and change `CALENDAR_CODE` to whatever you want. The entire system updates automatically.

### Q: What about dates before 3000 BCE?

The calendar supports negative years for pre-epoch dates. Year 1 IC = 3000 BCE, Year 0 doesn't exist, Year -1 IC = 3001 BCE.

### Q: How do I convert to/from Islamic lunar calendar?

Islamic lunar calendar conversion is not yet implemented (planned for future version).

---

## License

MIT License - See LICENSE file for details.

Free to use, modify, and distribute.

---

## Credits and Attribution

### Theoretical Foundation
This calendar system is based on the theoretical framework developed by **Sherwin Vakili** in his paper "On the Determination of the Epoch of History" (درباره تعیین مبدأ تاریخ). The 3000 BCE epoch is established through extensive historical and archaeological research.

### Implementation
The Python package was developed by **Alborz Teymoorzadeh**, including:
- Algorithm design and implementation
- Data validation and testing framework
- Command-line interface
- Package distribution and documentation

### How to Cite

**Software:**
```
Teymoorzadeh, A. (2026). Iranian Calendar (IC) Python Package (Version 1.0.0) 
[Computer software]. https://github.com/AlborzStudio/iranian-calendar
Based on theoretical framework by Sherwin Vakili.
```

**Academic:**
```
Vakili, S. On the Determination of the Epoch of History (درباره تعیین مبدأ تاریخ).
Implementation: Teymoorzadeh, A. (2026). Iranian Calendar Python Package.
```

See [AUTHORS.md](AUTHORS.md) for complete attribution information.

---

## Support the Project

This calendar system is free and open-source software developed and maintained by **Alborz Teymoorzadeh**, based on the theoretical framework by **Sherwin Vakili**.

### Ways to Support

If your organization or project benefits from this work, please consider:

- ⭐ **Star this repository** - Show your appreciation and help others discover it
- 📢 **Share and credit** - Mention this project when you use it
- 🐛 **Report issues** - Help improve the package
- 💡 **Contribute code** - See [CONTRIBUTING.md](CONTRIBUTING.md)
- 💰 **Sponsor development** - Contact for sponsorship opportunities

### Commercial Support

For organizations requiring:
- Custom implementations or integrations
- Enterprise support and SLA
- Training and consulting
- Feature development

**Contact:** 
- **Commercial inquiries:** [Contact form](https://alborz.studio/contact)
- **Technical questions:** Open a [GitHub issue](https://github.com/AlborzStudio/iranian-calendar/issues)

### Attribution

When using this calendar system in your product, please credit:
- **Sherwin Vakili** (theoretical framework)
- **Alborz Teymoorzadeh** (implementation)

Proper attribution helps others discover and benefit from this work.

---

**Version:** 1.0.0  
**Release Date:** 5 Bahman 5025 IC (25 January 2026 CE)  
**Status:** Production Ready
