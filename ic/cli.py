"""
Command-line interface for Iranian Calendar operations.

Usage:
    ic today                    # Show today's date in IC
    ic convert 5025-11-01       # Convert IC to Gregorian
    ic convert 2026-01-21       # Convert Gregorian to IC
    ic leap 5025                # Check if year is leap
    ic cal 5026                 # Show calendar for year (future)
"""

import sys
import datetime
import argparse
from .core import ICDate
from .leap import is_leap_year_33cycle, get_cycle_info, days_in_year
from .conversions import ic_to_gregorian, gregorian_to_ic, get_nowruz_gregorian


def cmd_today():
    """Display today's date in IC format."""
    greg_today = datetime.date.today()
    ic_today = gregorian_to_ic(greg_today)
    
    print(f"\nToday's Date:")
    print(f"  IC:        {ic_today}")
    print(f"  Latin:     {ic_today.format('latin')}")
    print(f"  Numeric:   {ic_today.format('numeric')}")
    print(f"  Gregorian: {greg_today.strftime('%d %B %Y')}")
    print(f"  Full:      {ic_today.format('full')}")
    print()


def cmd_convert(date_str):
    """
    Convert date between IC and Gregorian.
    
    Accepts:
        - IC format: 5025-11-01
        - Gregorian format: 2026-01-21
    """
    try:
        parts = date_str.split('-')
        if len(parts) != 3:
            print(f"Error: Invalid date format '{date_str}'")
            print("Expected: YYYY-MM-DD")
            return
        
        year, month, day = map(int, parts)
        
        # Determine if IC or Gregorian based on year magnitude
        # IC years are > 3000, Gregorian years are < 3000
        if year >= 3000:
            # IC → Gregorian
            ic_date = ICDate(year, month, day)
            greg_date = ic_to_gregorian(ic_date)
            
            print(f"\nIC → Gregorian Conversion:")
            print(f"  IC:        {ic_date}")
            print(f"  Gregorian: {greg_date.strftime('%d %B %Y')}")
            print(f"  Numeric:   {greg_date.isoformat()}")
            
        else:
            # Gregorian → IC
            greg_date = datetime.date(year, month, day)
            ic_date = gregorian_to_ic(greg_date)
            
            print(f"\nGregorian → IC Conversion:")
            print(f"  Gregorian: {greg_date.strftime('%d %B %Y')}")
            print(f"  IC:        {ic_date}")
            print(f"  Numeric:   {ic_date.format('numeric')}")
        
        print()
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error converting date: {e}")


def cmd_leap(year_str):
    """Check if IC year is leap year and show cycle information."""
    try:
        year = int(year_str)
        info = get_cycle_info(year)
        
        print(f"\nLeap Year Information for {year} IC:")
        print(f"  Is leap year:       {'Yes' if info['is_leap'] else 'No'}")
        print(f"  Days in year:       {days_in_year(year)}")
        print(f"  33-year cycle:      #{info['cycle_number']}")
        print(f"  Position in cycle:  {info['cycle_position']}/33")
        
        if not info['is_leap']:
            print(f"  Next leap year in:  {info['years_to_next_leap']} years")
        
        print()
        
    except ValueError:
        print(f"Error: Invalid year '{year_str}'")


def cmd_nowruz(year_str):
    """Show Nowruz (1 Farvardin) date for given IC year."""
    try:
        year = int(year_str)
        
        # IC Nowruz
        nowruz_ic = ICDate(year, 1, 1)
        
        # Gregorian equivalent
        nowruz_greg = get_nowruz_gregorian(year)
        
        print(f"\nNowruz {year} IC:")
        print(f"  IC:        {nowruz_ic}")
        print(f"  Gregorian: {nowruz_greg.strftime('%d %B %Y')}")
        print(f"  Day of week: {nowruz_greg.strftime('%A')}")
        print()
        
    except ValueError as e:
        print(f"Error: {e}")


def cmd_info():
    """Display information about IC calendar system."""
    print("""
Iranian Calendar (IC) Information
================================

Epoch:     1 Farvardin 1 IC = 3000 BCE (proleptic Gregorian)
Structure: Identical to Solar Hijri (Persian) calendar
Months:    12 months (6×31, 5×30, 1×29/30 days)
Year:      365 days (common), 366 days (leap)
Leap rule: 33-year cycle (8 leap years per cycle)

Conversions:
  IC = Gregorian + 3000
  IC = Solar Hijri + 3621

Current Implementation:
  ✓ Date representation and validation
  ✓ IC ↔ Gregorian conversion
  ✓ Leap year calculation (33-year cycle)
  ✓ Multiple date formats

Example dates:
  Today:        1 Bahman 5025 IC = 21 January 2026 CE
  Nowruz 5026:  1 Farvardin 5026 IC = 21 March 2026 CE
  Hijra:        1 Farvardin 3622 IC = 622 CE (approx)
  Cyrus:        1 Farvardin 2461 IC = 539 BCE (approx)

For more information, see README.md
""")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Iranian Calendar (IC) command-line tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ic today                    Show today's date in IC
  ic convert 5025-11-01       Convert IC date to Gregorian
  ic convert 2026-01-21       Convert Gregorian date to IC
  ic leap 5025                Check if year is leap year
  ic nowruz 5026              Show Nowruz date for year
  ic info                     Display IC calendar information
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['today', 'convert', 'leap', 'nowruz', 'info'],
        default='today',
        help='Command to execute'
    )
    
    parser.add_argument(
        'args',
        nargs='*',
        help='Arguments for the command'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Iranian Calendar v1.0.0'
    )
    
    # Parse arguments
    if len(sys.argv) == 1:
        # No arguments, show today by default
        cmd_today()
        return
    
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'today':
        cmd_today()
    
    elif args.command == 'convert':
        if not args.args:
            print("Error: 'convert' requires a date argument (YYYY-MM-DD)")
            print("Example: ic convert 5025-11-01")
            sys.exit(1)
        cmd_convert(args.args[0])
    
    elif args.command == 'leap':
        if not args.args:
            print("Error: 'leap' requires a year argument")
            print("Example: ic leap 5025")
            sys.exit(1)
        cmd_leap(args.args[0])
    
    elif args.command == 'nowruz':
        if not args.args:
            print("Error: 'nowruz' requires a year argument")
            print("Example: ic nowruz 5026")
            sys.exit(1)
        cmd_nowruz(args.args[0])
    
    elif args.command == 'info':
        cmd_info()


if __name__ == '__main__':
    main()
