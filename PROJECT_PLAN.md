# Iranian Calendar - Project Plan

**Project:** Iranian Calendar (IC)  
**Foundation:** Based on Sherwin Vakili's "On the Determination of the Epoch of History"  
**Document Version:** 1.0  
**Date:** 5 Bahman 5025 (25 January 2026)  
**Status:** Definitive Project Structure

---

## Project Overview

### Purpose
Build a complete implementation of the Iranian Calendar (IC), a solar calendar with epoch at 3000 BCE, maintaining Persian calendar structure with corrected year numbering.

### Core Principle
**Epoch correction, not calendar reform.**
- IC = Gregorian + 3000
- Same months, days, structure as Solar Hijri
- Compatible with existing calendars

### Theoretical Foundation
Based on Sherwin Vakili's paper "On the Determination of the Epoch of History" which argues for establishing a civilizational epoch at ~3000 BCE rather than religious or arbitrary starting points.

---

## Naming Conventions

### File Naming Rules

**Individual Files:**
- Use shortest meaningful names
- Never include version numbers in filenames
- Use underscores for multi-word files: `conversion_table.csv`
- Lowercase for code files, UPPERCASE for documentation: `core.py`, `README.md`
- One of each standard file per directory: one `README.md`, one `CHANGELOG.md`

**Examples:**
```
 Good:
  README.md
  conversion_table.csv
  core.py
  
✗ Bad:
  README_v2.0.md
  IC-Conversion-Table-2026.csv
  iranian_calendar_core.py
```

**Package/Release Naming:**
- Version numbers belong in package releases and tags
- Use semantic versioning: `iranian-calendar-1.0.0.zip`
- Git tags: `v1.0.0`, `v1.0.0`
- PyPI package: `iranian-calendar` (version in metadata)

**Examples:**
```
 Good:
  iranian-calendar-1.0.0.zip  (release package)
  git tag v1.0.0                         (git version)
  pyproject.toml: version = "1.0.0"      (package metadata)
  
✗ Bad:
  README_v2.0.md                         (version in filename)
  core_2024.py                           (date in filename)
```

### Calendar Naming

**Full Name:** Iranian Calendar
**Abbreviation:** IC (2 letters)
**Package Name:** `ic` (short, no redundancy)

**Avoid Redundancy:**
```
 Good:
  ic/core.py           (package name + module)
  IC Converter         (short name + function)
  
✗ Bad:
  ic/         (calendar is redundant)
  IC_calendar.py       (repeating "calendar")
```

### Configurable Naming System

All calendar references go through configuration constants, allowing easy renaming:

**config.py:**
```python
CALENDAR_CODE = "IC"                        # 2-letter code
CALENDAR_FULL_NAME = "Iranian Calendar"
CALENDAR_SHORT_NAME = "Iranian Calendar"

EPOCH_BCE = 3000
GREGORIAN_OFFSET = 3000
SOLAR_HIJRI_OFFSET = 3621
```

**Usage:**
```python
from .config import CALENDAR_CODE, CALENDAR_FULL_NAME

# All references use constants
def format_date(year, month, day):
    return f"{day} {month} {year} {CALENDAR_CODE}"
```

**Result:** Change 2-3 lines in config.py to rename entire system.

---

## Version Control Strategy

### Where Versions Appear

**YES - Version numbers:**
- Release packages: `iranian-calendar-1.0.0.zip`
- Git tags: `v1.0.0`
- Package metadata: `pyproject.toml`, `__init__.py`
- CHANGELOG.md: Version headers
- Documentation references: "As of version 2.0..."

**NO - Version numbers:**
- Individual filenames: `README.md` not `README_v2.md`
- Code files: `core.py` not `core_v2.py`
- Data files: `conversion_table.csv` not `conversion_table_2024.csv`

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

**MAJOR:** Breaking changes (API incompatible)
- Example: Renaming core functions, changing data structures

**MINOR:** New features (backward compatible)
- Example: Adding new functions, new data formats

**PATCH:** Bug fixes, documentation
- Example: Fixing calculation errors, typo corrections

**Current Version:** 1.0.0
- Major version 2 (significant restructure from v1)
- Minor version 0 (base feature set)
- Patch version 0 (initial release of v2)

---

## Project Phases

### PHASE 0: Foundation Documentation

**Objective:** Establish theoretical foundation and source materials

**Tasks:**
1. OCR Sherwin Vakili's original paper (Persian)
2. Translate paper to English
3. Review and enhance English summary
4. Create foundation documentation

**Deliverables:**
```
docs/
├── vakili_paper_persian.pdf      # Original paper (scanned)
├── vakili_paper_persian.txt      # OCR text extraction
├── vakili_paper_english.md       # English translation
└── vakili_summary_english.md     # Enhanced summary
```

**Status:** Pending (awaiting source materials)

**Notes:**
- Original paper is in Persian
- OCR extraction needed for text processing
- Professional translation to English required
- Summary should be accessible to general audience

---

### PHASE 1: Specification & Planning

**Objective:** Define the calendar system completely

**Tasks:**
1. Document epoch definition and rationale
2. Define month structure (Solar Hijri-compatible)
3. Specify leap year algorithm (33-year cycle)
4. Document conversion formulas
5. Create implementation requirements

**Deliverables:**
```
PROJECT_PLAN.md  # This document
```

**Status:** Complete

**Reference Dates:**
- Today: 2 Bahman 5025 IC = 22 January 2026 CE
- Nowruz 5026: 1 Farvardin 5026 IC = 21 March 2026 CE
- Formula: IC = Gregorian + 3000 = Solar Hijri + 3621

---

### PHASE 2: Core Implementation

**Objective:** Build working Python library with configurable naming

**Tasks:**
1. Create package structure
2. Implement configuration system (changeable names)
3. Build core date class
4. Implement leap year algorithm
5. Create conversion functions (IC ↔ Gregorian ↔ Solar Hijri)
6. Develop date formatting (Persian, Latin, numeric)
7. Build command-line interface
8. Write comprehensive tests

**Deliverables:**
```
ic/
├── __init__.py              # Package init, version info
├── config.py                # Name constants (CHANGEABLE)
├── core.py                  # Date class (~300 lines)
├── leap.py                  # Leap year functions (~180 lines)
├── conversions.py           # Conversion functions (~250 lines)
├── cli.py                   # Command-line interface (~250 lines)
└── tests/
    ├── test_core.py         # Core functionality tests
    ├── test_conversions.py  # Conversion tests
    ├── test_leap.py         # Leap year tests
    └── run_tests.py         # Test runner

standalone.py                # Single-file version (all-in-one)

pyproject.toml              # Modern Python packaging (contains version)
setup.py                    # Fallback for older pip
requirements.txt            # Dependencies (minimal/none)
```

**Status:** In Progress

**Completion Criteria:**
- All 39+ tests passing
- Config system working (names changeable via config.py)
- CLI functional (`ic today`, `ic convert`, etc.)
- Standalone file operational
- Code documented with docstrings

---

### PHASE 3: Data Generation

**Objective:** Create reference tables for quick lookup

**Tasks:**
1. Generate 100-year conversion table (2026-2125 CE)
2. Create detailed reference table (5 years with months)
3. Produce multiple formats (CSV, JSON)
4. Validate against known dates

**Deliverables:**
```
data/
├── conversion_table.csv     # 100 years (Excel-friendly)
├── conversion_table.json    # Same data, JSON format
└── reference_table.json     # 5 years with monthly details
```

**Status:** In Progress

**Completion Criteria:**
- All tables validated against reference dates
- CSV opens correctly in Excel/Google Sheets
- JSON is valid and properly formatted
- Data matches calculation outputs exactly

---

### PHASE 4: Documentation

**Objective:** Complete user and developer documentation

**Tasks:**
1. Write comprehensive README with examples
2. Create API reference documentation
3. Add usage guide for different audiences
4. Document theoretical foundation
5. Maintain changelog

**Deliverables:**
```
README.md        # Primary documentation (usage, examples, quick start)
CHANGELOG.md     # Version history and upgrade notes
LICENSE          # MIT license
.gitignore       # Git ignore patterns
```

**Status:** In Progress

**Completion Criteria:**
- README covers all use cases
- Examples are clear and tested
- API fully documented
- Installation instructions verified
- Contributing guidelines added (future)

---

### PHASE 5: Testing & Validation

**Objective:** Ensure correctness and reliability

**Tasks:**
1. Unit tests for all modules
2. Integration tests
3. Validate against reference dates
4. Test CLI commands
5. Cross-check with existing calendars
6. Performance testing

**Deliverables:**
- Comprehensive test suite (in Phase 2 structure)
- Minimum 90% code coverage
- All reference dates validated
- Test report

**Status:** Complete

**Reference Validations:**
- Today: 2 Bahman 5025 IC = 22 Jan 2026 CE
- Nowruz: 1 Farvardin 5026 IC = 21 Mar 2026 CE
- Leap year 5025: Position 9, 366 days
- Round-trip conversions: IC → Gregorian → IC

---

### PHASE 6: Distribution & Publishing

**Objective:** Make the calendar system publicly available

**Tasks:**
1. Publish to PyPI (`pip install iranian-calendar`)
2. Create GitHub repository
3. Set up CI/CD (automated testing)
4. Write contribution guidelines
5. Create project website (optional)

**Deliverables:**
```
PyPI package:     iranian-calendar
GitHub repo:      github.com/username/iranian-calendar
Documentation:    readthedocs or github pages
CI/CD:            GitHub Actions

Additional files:
├── CONTRIBUTING.md    # How to contribute
├── .github/
│   └── workflows/
│       └── tests.yml  # Automated testing
```

**Status:** Not Started

**Prerequisites:**
- All tests passing
- Documentation complete
- Version 1.0.0 released
- License confirmed

---

## Complete Project Structure

```
iranian-calendar/          # Root directory
│
├── docs/                            # Foundation documentation (Phase 0)
│   ├── vakili_paper_persian.pdf
│   ├── vakili_paper_persian.txt
│   ├── vakili_paper_english.md
│   └── vakili_summary_english.md
│
├── ic/                             # Main package (Phase 2)
│   ├── __init__.py
│   ├── config.py                    # Name configuration (changeable)
│   ├── core.py
│   ├── leap.py
│   ├── conversions.py
│   ├── cli.py
│   └── tests/
│       ├── test_core.py
│       ├── test_conversions.py
│       ├── test_leap.py
│       └── run_tests.py
│
├── data/                            # Reference tables (Phase 3)
│   ├── conversion_table.csv
│   ├── conversion_table.json
│   └── reference_table.json
│
├── standalone.py                    # Single-file version (Phase 2)
│
├── pyproject.toml                   # Package config with version
├── setup.py                         # Fallback packaging
├── requirements.txt                 # Dependencies
│
├── README.md                        # Primary documentation (Phase 4)
├── PROJECT_PLAN.md                  # This document (Phase 1)
├── CHANGELOG.md                     # Version history (Phase 4)
├── LICENSE                          # MIT license (Phase 4)
└── .gitignore                       # Git ignores (Phase 4)
```

**Total Files:** ~27 files (may adjust as needed)

**Directory Structure:**
- `docs/` - Foundation papers and translations
- `ic/` - Python package (short name, no redundancy)
- `data/` - Reference tables
- Root level - Documentation and config

---

## Implementation Priorities

### Phase 2 Completion (Current Priority)

**High Priority:**
1. Create `config.py` with changeable name constants
2. Standardize all filenames per naming convention
3. Ensure all imports use config constants
4. Consolidate documentation (single README.md)
5. Organize into clean directory structure

**Medium Priority:**
6. Complete test coverage (target 95%)
7. Add docstrings to all functions
8. Validate standalone.py works identically to package

**Low Priority:**
9. Performance optimization
10. Additional date formats
11. Extended validation tests

### Phase 3 Data Generation

**Priority Tasks:**
1. Rename data files to standard convention
2. Move to `data/` directory
3. Validate all values
4. Add metadata to JSON files

### Phase 0 Foundation (When Materials Available)

**Priority Tasks:**
1. OCR Vakili's paper (Persian)
2. Professional English translation
3. Review and enhance summary
4. Create accessible introduction to theory

---

## Quality Standards

### Code Quality
- Follow PEP 8 style guide
- Type hints for all functions
- Docstrings (Google or NumPy style)
- Minimum 90% test coverage
- No hardcoded strings (use config)

### Documentation Quality
- Clear examples for all features
- Beginner-friendly explanations
- Technical details for developers
- Theory accessible to general audience
- All code examples tested

### Data Quality
- All reference dates validated
- Cross-checked with multiple sources
- Metadata included in all files
- Multiple formats for accessibility

---

## Maintenance Strategy

### Version Updates

**When to increment:**
- **MAJOR (3.0.0):** Breaking API changes, renamed functions
- **MINOR (1.0.0):** New features, new data formats
- **PATCH (2.0.1):** Bug fixes, typo corrections

**Update checklist:**
1. Update version in `pyproject.toml`
2. Update version in `ic/__init__.py`
3. Add entry to `CHANGELOG.md`
4. Create git tag: `git tag v1.0.0`
5. Build and test package
6. Create release package with version number in filename

### File Management

**Never rename:**
- Standard files: README.md, CHANGELOG.md, LICENSE
- Package files: config.py, core.py, etc.

**Can add:**
- New modules in `ic/`
- New data files in `data/`
- New documentation in `docs/`

**Version control:**
- Use git tags for versions
- Package releases include version in filename
- Individual files never have version numbers

---

## Success Metrics

### Phase 2 Complete When:
- All tests passing (39+)
- Config system working (changeable names)
- CLI functional
- Standalone file works
- Files follow naming convention
- Single README.md with complete guide

### Phase 3 Complete When:
- 100-year table validated
- Reference table detailed and accurate
- Multiple formats (CSV, JSON) available
- Files in `data/` directory

### Phase 0 Complete When:
- Vakili paper OCR'd and translated
- English summary polished
- Foundation documents in `docs/`

### Project Complete When:
- All phases 0-5 done
- Published to PyPI
- Documentation comprehensive
- Community can contribute

---

## Theoretical Foundation

### Source Material

**Primary Source:**
- Title: "On the Determination of the Epoch of History"
- Author: Sherwin Vakili
- Language: Persian (English translation in progress)
- Argument: Proposes 3000 BCE as civilizational epoch

**Key Concepts:**
1. Epoch correction vs calendar reform
2. Historical proportionality
3. Continuous civilizational timeline
4. Independence from religious/colonial overlays

### Documentation Structure

**Foundation Documents (Phase 0):**
1. Original paper (Persian) - authoritative source
2. OCR text - searchable version
3. English translation - accessibility
4. English summary - overview for general audience

**Implementation Documents (Phase 1):**
3. PROJECT_PLAN.md - execution strategy

**User Documents (Phase 4):**
1. README.md - usage guide
2. Examples and tutorials
3. API reference

---

## Risk Management

### Potential Issues

**Technical Risks:**
- Leap year edge cases (mitigated by 33-year cycle validation)
- Date conversion accuracy (mitigated by extensive testing)
- Naming conflicts (mitigated by config.py system)

**Documentation Risks:**
- Translation quality of Vakili paper (mitigated by review process)
- Accessibility of theoretical concepts (mitigated by summary document)

**Maintenance Risks:**
- Package naming collisions (mitigated by unique package name)
- Breaking changes in dependencies (mitigated by minimal dependencies)

### Mitigation Strategies

1. **Comprehensive testing** - Validate against known dates
2. **Configurable naming** - Easy to rename if needed
3. **Minimal dependencies** - Reduce breaking change risk
4. **Clear documentation** - Multiple explanation levels
5. **Version control** - Git tags for all releases

---

## Future Enhancements

### Post-Phase 6

**Potential additions:**
- Web API service
- JavaScript implementation
- Mobile apps (iOS, Android)
- Calendar integration (CalDAV, iCal)
- Historical date database
- Multi-timezone support
- Astronomical precision improvements

**Criteria for new features:**
- Must maintain backward compatibility
- Must not break existing API
- Must be well-documented
- Must include tests

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 21 Jan 2026 | Initial project structure |
| 2.0 | 22 Jan 2026 | Complete phase breakdown |
| 1.0 | 22 Jan 2026 | Refined naming convention, added Phase 0, clarified versioning |

---

## Credits

**Theoretical Foundation:** Sherwin Vakili  
**Implementation:** Alborz Teymoorzadeh  
**Project Structure:** IC Project

---

**Project Plan Version:** 1.0  
**Document Status:** Definitive Reference  
**Last Updated:** 5 Bahman 5025 IC (25 January 2026 CE)
