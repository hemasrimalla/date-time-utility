"""
=============================================================================
DATE AND TIME UTILITY (date_utility.py)
=============================================================================
Level 1 Internship Task 26: Build a Date and Time Utility.

A beginner-friendly, menu-driven command-line utility for practical date
and time manipulation built using ONLY Python's standard `datetime` module.

Core Design Principles:
  1. Separation of Concerns: Core calculation functions are completely decoupled
     from I/O (input/print) logic, making them 100% testable and reusable.
  2. Robust Input Validation: All date inputs use DD-MM-YYYY format, verified
     through datetime.strptime() with try/except blocks to prevent crashes.
  3. Edge Case Handling: Robustly accounts for leap years (including Feb 29
     births), future birth dates, inverted start/end ranges, and weekend holidays.
  4. Clean & Informative UI: Polished menu-driven CLI interface with prompt
     cancellation support and clear error reporting.
=============================================================================
"""

from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple, Dict, Any


# =============================================================================
# 1. CORE VALIDATION & PARSING FUNCTIONS
# =============================================================================

def parse_date(date_str: str) -> date:
    """
    Parse and validate a date string in DD-MM-YYYY format.

    Uses `datetime.strptime()` to strictly enforce both format structure
    and calendar correctness (e.g., rejecting 31-02-2025 or 29-02-2025).

    Args:
        date_str (str): The date string to validate and parse (e.g., '26-10-2026').

    Returns:
        date: A Python datetime.date object representing the validated date.

    Raises:
        ValueError: If the string is empty, improperly formatted, or represents
                    an impossible calendar date.
    """
    clean_str = date_str.strip()
    if not clean_str:
        raise ValueError("Date string cannot be empty.")

    try:
        # datetime.strptime handles parsing and built-in calendar validation
        parsed_dt = datetime.strptime(clean_str, "%d-%m-%Y")
        return parsed_dt.date()
    except ValueError as err:
        err_msg = str(err).lower()
        # Differentiate between format mismatch and impossible calendar days
        if "range" in err_msg or "day" in err_msg and "does not match format" not in err_msg:
            raise ValueError(
                f"Invalid calendar date '{clean_str}': That day does not exist in the specified month/year."
            )
        elif "does not match format" in err_msg or "unconverted data" in err_msg:
            raise ValueError(
                f"Invalid format '{clean_str}': Expected DD-MM-YYYY (e.g., 26-10-2026)."
            )
        else:
            raise ValueError(f"Invalid date '{clean_str}': {err}")


def is_leap_year(year: int) -> bool:
    """
    Determine if a year is a leap year using Python's datetime.date.

    By leveraging `datetime.date(year, 2, 29)`, we let Python's standard
    library verify whether February 29th exists for that year, avoiding
    manual date arithmetic while strictly using the datetime module.

    Args:
        year (int): The 4-digit calendar year (e.g., 2024).

    Returns:
        bool: True if the year is a leap year, False otherwise.
    """
    try:
        date(year, 2, 29)
        return True
    except ValueError:
        return False


def explain_leap_year(year: int) -> Dict[str, Any]:
    """
    Provide a comprehensive leap year analysis including the Gregorian
    calendar rules, number of days in February, and adjacent leap years.

    Gregorian Rules:
      1. Every year divisible by 4 is a leap year...
      2. EXCEPT century years (ending in 00), which are NOT leap years...
      3. UNLESS the century year is also divisible by 400.

    Args:
        year (int): The year to analyze.

    Returns:
        dict: Leap status, days in February, year length, explanation, and neighbors.
    """
    leap = is_leap_year(year)
    div_4 = (year % 4 == 0)
    div_100 = (year % 100 == 0)
    div_400 = (year % 400 == 0)

    if div_400:
        reason = (
            f"{year} is divisible by 400. Century years divisible by 400 ARE leap years "
            f"(Gregorian quadricentennial rule)."
        )
    elif div_100:
        reason = (
            f"{year} is divisible by 100 but not by 400. It is a century year, so it is "
            f"NOT a leap year."
        )
    elif div_4:
        reason = (
            f"{year} is divisible by 4 and not a century year (not divisible by 100), "
            f"so it IS a leap year."
        )
    else:
        reason = f"{year} is not divisible by 4, so it is NOT a leap year."

    # Find previous and next leap years
    prev_leap = year - 1
    while not is_leap_year(prev_leap):
        prev_leap -= 1

    next_leap = year + 1
    while not is_leap_year(next_leap):
        next_leap += 1

    return {
        "year": year,
        "is_leap": leap,
        "days_in_february": 29 if leap else 28,
        "total_days": 366 if leap else 365,
        "reason": reason,
        "previous_leap_year": prev_leap,
        "next_leap_year": next_leap,
    }


# =============================================================================
# 2. OPERATION 1: AGE CALCULATOR & NEXT BIRTHDAY COUNTDOWN
# =============================================================================

def _get_days_in_month(year: int, month: int) -> int:
    """
    Helper to calculate number of days in a given month using datetime and timedelta.
    Finds the 1st of the next month and subtracts 1 day to inspect the day value.
    """
    next_month_year = year + (month // 12)
    next_month = (month % 12) + 1
    last_day_of_month = date(next_month_year, next_month, 1) - timedelta(days=1)
    return last_day_of_month.day


def _add_months_clamped(base_date: date, months_to_add: int) -> date:
    """
    Helper to add months to a date, clamping the day to the last valid day
    of the target month (e.g., 31-Aug + 6 months -> 28-Feb in non-leap year).
    """
    total_months = base_date.year * 12 + (base_date.month - 1) + months_to_add
    target_year = total_months // 12
    target_month = (total_months % 12) + 1
    max_days = _get_days_in_month(target_year, target_month)
    clamped_day = min(base_date.day, max_days)
    return date(target_year, target_month, clamped_day)


def calculate_age(birth_date: date, reference_date: Optional[date] = None) -> Dict[str, Any]:
    """
    Calculate an individual's exact age in years, months, and days.

    Handles edge cases such as leap years (Feb 29 births), variable month
    lengths (e.g. 28, 30, 31 days), and future birth dates.

    Args:
        birth_date (date): The individual's birth date.
        reference_date (date, optional): Reference date for calculation.
                                         Defaults to date.today().

    Returns:
        dict: Contains 'years', 'months', 'days', 'total_days', and 'birth_date'.

    Raises:
        ValueError: If birth_date is in the future relative to reference_date.
    """
    if reference_date is None:
        reference_date = date.today()

    if birth_date > reference_date:
        raise ValueError(
            f"Birth date ({birth_date.strftime('%d-%m-%Y')}) cannot be in the future "
            f"relative to reference date ({reference_date.strftime('%d-%m-%Y')})."
        )

    # Calculate total full months between the two dates
    total_months = (reference_date.year - birth_date.year) * 12 + (reference_date.month - birth_date.month)

    # If the day in reference_date is earlier than birth_date's day in that month,
    # the last full month has not been completed yet.
    candidate_date = _add_months_clamped(birth_date, total_months)
    if candidate_date > reference_date:
        total_months -= 1
        candidate_date = _add_months_clamped(birth_date, total_months)

    years = total_months // 12
    months = total_months % 12
    days = (reference_date - candidate_date).days
    total_days = (reference_date - birth_date).days

    return {
        "birth_date": birth_date,
        "reference_date": reference_date,
        "years": years,
        "months": months,
        "days": days,
        "total_days": total_days,
    }


def get_next_birthday(birth_date: date, reference_date: Optional[date] = None) -> Dict[str, Any]:
    """
    Calculate the next upcoming birthday and countdown in days.

    Handles leap-year babies (Feb 29):
      - In non-leap years, calculates countdown to Feb 28 (common observation).
      - Also calculates the countdown to their next official quadrennial Feb 29.

    Args:
        birth_date (date): The birth date.
        reference_date (date, optional): The reference date. Defaults to date.today().

    Returns:
        dict: Details including next birthday date, days until, leap adjustments,
              and next official leap-day birthday if applicable.
    """
    if reference_date is None:
        reference_date = date.today()

    target_year = reference_date.year

    def _resolve_bday(yr: int) -> Tuple[date, bool]:
        if birth_date.month == 2 and birth_date.day == 29:
            if is_leap_year(yr):
                return date(yr, 2, 29), False
            else:
                # Celebrated on Feb 28 in non-leap years
                return date(yr, 2, 28), True
        return date(yr, birth_date.month, birth_date.day), False

    next_bday, is_leap_adjusted = _resolve_bday(target_year)

    # If the birthday has already passed this year, roll over to next year
    if next_bday < reference_date:
        target_year += 1
        next_bday, is_leap_adjusted = _resolve_bday(target_year)

    days_until = (next_bday - reference_date).days
    is_today = (days_until == 0)

    # For Feb 29 births, also find next actual Feb 29
    next_leap_bday = None
    days_until_leap_bday = None
    if birth_date.month == 2 and birth_date.day == 29:
        leap_yr = reference_date.year
        while True:
            if is_leap_year(leap_yr):
                candidate = date(leap_yr, 2, 29)
                if candidate >= reference_date:
                    next_leap_bday = candidate
                    days_until_leap_bday = (candidate - reference_date).days
                    break
            leap_yr += 1

    return {
        "next_birthday": next_bday,
        "days_until": days_until,
        "is_today": is_today,
        "is_leap_adjusted": is_leap_adjusted,
        "next_leap_birthday": next_leap_bday,
        "days_until_leap_birthday": days_until_leap_bday,
    }


# =============================================================================
# 3. OPERATION 2: DAYS BETWEEN TWO DATES
# =============================================================================

def days_between(date1: date, date2: date) -> Dict[str, Any]:
    """
    Calculate the absolute difference in days and weeks between two dates.

    Handles same-day inputs and inverted date order (end date earlier than start date).

    Args:
        date1 (date): First date.
        date2 (date): Second date.

    Returns:
        dict: Total days, weeks, remaining days, earlier date, later date,
              and whether the input was in chronological order.
    """
    chronological = date1 <= date2
    earlier = min(date1, date2)
    later = max(date1, date2)

    total_days = (later - earlier).days
    weeks = total_days // 7
    remaining_days = total_days % 7

    return {
        "date1": date1,
        "date2": date2,
        "earlier_date": earlier,
        "later_date": later,
        "is_same_day": (date1 == date2),
        "is_chronological": chronological,
        "total_days": total_days,
        "weeks": weeks,
        "remaining_days": remaining_days,
    }


# =============================================================================
# 4. OPERATION 3: WORKING DAYS (BUSINESS DAYS) CALCULATOR
# =============================================================================

def working_days_between(
    start_date: date,
    end_date: date,
    holidays: Optional[List[date]] = None
) -> Dict[str, Any]:
    """
    Count business days (Monday through Friday) between two dates, inclusive,
    excluding weekends and any provided public holidays.

    Real-world payroll/HR nuances handled:
      - Automatically normalizes inverted start and end dates.
      - Deducts holidays falling on Monday–Friday.
      - Detects holidays that fall on weekends so they are not double-deducted.

    Args:
        start_date (date): Start date of the period.
        end_date (date): End date of the period.
        holidays (list of date, optional): List of holiday dates to exclude.

    Returns:
        dict: Calendar days, working days, weekend days, weekday holidays,
              and weekend holidays.
    """
    holidays_set = set(holidays) if holidays else set()

    is_inverted = start_date > end_date
    start = min(start_date, end_date)
    end = max(start_date, end_date)

    total_calendar_days = (end - start).days + 1
    working_days = 0
    weekend_days = 0
    holidays_on_weekdays: List[date] = []
    holidays_on_weekends: List[date] = []

    # Iterate through each day in the span using timedelta
    current = start
    one_day = timedelta(days=1)

    while current <= end:
        weekday = current.weekday()  # 0 = Monday, 4 = Friday, 5 = Saturday, 6 = Sunday
        if weekday < 5:
            # Weekday (Mon-Fri)
            if current in holidays_set:
                holidays_on_weekdays.append(current)
            else:
                working_days += 1
        else:
            # Weekend (Sat-Sun)
            weekend_days += 1
            if current in holidays_set:
                holidays_on_weekends.append(current)

        current += one_day

    return {
        "start_date": start,
        "end_date": end,
        "original_start": start_date,
        "original_end": end_date,
        "is_inverted": is_inverted,
        "total_calendar_days": total_calendar_days,
        "working_days": working_days,
        "weekend_days": weekend_days,
        "holidays_on_weekdays": sorted(holidays_on_weekdays),
        "holidays_on_weekends": sorted(holidays_on_weekends),
    }


# =============================================================================
# 5. OPERATION 4: DATE AND TIME FORMATTER
# =============================================================================

def format_date_time(target_dt: Optional[datetime] = None) -> List[Tuple[str, str, str]]:
    """
    Format a datetime object into a rich variety of human-readable and standard formats.

    Uses `datetime.strftime()` with standard format directives.

    Args:
        target_dt (datetime, optional): The datetime object to format.
                                        Defaults to datetime.now().

    Returns:
        list of tuples: (Format Name, Directive Pattern, Formatted Output)
    """
    if target_dt is None:
        target_dt = datetime.now()

    formats = [
        ("Standard Date (Indian/British)", "%d-%m-%Y", target_dt.strftime("%d-%m-%Y")),
        ("ISO 8601 (International)", "%Y-%m-%d", target_dt.strftime("%Y-%m-%d")),
        ("US Format", "%m/%d/%Y", target_dt.strftime("%m/%d/%Y")),
        ("Full Written Date", "%d %B %Y", target_dt.strftime("%d %B %Y")),
        ("Day and Abbreviated Date", "%A, %d %b %Y", target_dt.strftime("%A, %d %b %Y")),
        ("Complete Long Date", "%A, %B %d, %Y", target_dt.strftime("%A, %B %d, %Y")),
        ("24-Hour Military Time", "%H:%M:%S", target_dt.strftime("%H:%M:%S")),
        ("12-Hour Time with AM/PM", "%I:%M:%S %p", target_dt.strftime("%I:%M:%S %p")),
        ("Full Date & Time (12-Hour)", "%d %B %Y, %I:%M:%S %p", target_dt.strftime("%d %B %Y, %I:%M:%S %p")),
        ("Day of Year & Week", "Day %j, Week %U", target_dt.strftime("Day %j of year, Week %U")),
    ]

    return formats


# =============================================================================
# 6. OPERATION 5 (BONUS): ADD / SUBTRACT DAYS
# =============================================================================

def add_subtract_days(base_date: date, days: int) -> Dict[str, Any]:
    """
    Add or subtract a specified number of days from a given date using timedelta.

    Args:
        base_date (date): The starting date.
        days (int): Number of days to add (positive) or subtract (negative).

    Returns:
        dict: Base date, days delta, resulting date, resulting weekday name.
    """
    delta = timedelta(days=days)
    result_date = base_date + delta

    return {
        "base_date": base_date,
        "days": days,
        "result_date": result_date,
        "weekday": result_date.strftime("%A"),
        "operation": "add" if days >= 0 else "subtract",
    }


# =============================================================================
# 7. INTERACTIVE CLI HELPERS & INPUT PROMPTS
# =============================================================================

def prompt_for_date(prompt_message: str, allow_cancel: bool = True) -> Optional[date]:
    """
    Prompt the user to enter a date string in DD-MM-YYYY format with continuous
    validation and friendly re-prompting on errors.

    Args:
        prompt_message (str): Text prompt displayed to the user.
        allow_cancel (bool): If True, typing 'cancel' or 'c' returns None.

    Returns:
        date or None: Validated date object, or None if user canceled.
    """
    while True:
        try:
            user_input = input(prompt_message).strip()
            if allow_cancel and user_input.lower() in ("c", "cancel", "q", "back"):
                print("  -> Operation cancelled. Returning to main menu.\n")
                return None
            return parse_date(user_input)
        except ValueError as err:
            print(f"  [!] Error: {err}")
            cancel_tip = " (or type 'cancel' to return to menu)" if allow_cancel else ""
            print(f"      Please try again{cancel_tip}.\n")


def prompt_for_int(
    prompt_message: str,
    allow_cancel: bool = True,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None
) -> Optional[int]:
    """
    Prompt for an integer with optional range bounds and cancellation.
    """
    while True:
        user_input = input(prompt_message).strip()
        if allow_cancel and user_input.lower() in ("c", "cancel", "q", "back"):
            print("  -> Operation cancelled. Returning to main menu.\n")
            return None
        try:
            val = int(user_input)
            if min_val is not None and val < min_val:
                print(f"  [!] Error: Value must be at least {min_val}.\n")
                continue
            if max_val is not None and val > max_val:
                print(f"  [!] Error: Value cannot exceed {max_val}.\n")
                continue
            return val
        except ValueError:
            print(f"  [!] Error: '{user_input}' is not a valid integer. Please enter a whole number.\n")


def prompt_for_holidays() -> Optional[List[date]]:
    """
    Prompt user for a comma-separated list of holiday dates in DD-MM-YYYY format.
    Allows empty input (meaning no holidays).
    """
    while True:
        raw = input("Enter public holidays (DD-MM-YYYY separated by commas, or press Enter for none): ").strip()
        if not raw:
            return []
        if raw.lower() in ("c", "cancel", "back"):
            return None

        parts = [p.strip() for p in raw.split(",") if p.strip()]
        valid_holidays: List[date] = []
        has_error = False

        for part in parts:
            try:
                valid_holidays.append(parse_date(part))
            except ValueError as err:
                print(f"  [!] Invalid holiday: {err}")
                print("      Please re-enter the entire holiday list (or press Enter for none).\n")
                has_error = True
                break

        if not has_error:
            return valid_holidays


# =============================================================================
# 8. MENU ACTION HANDLERS
# =============================================================================

def handle_age_calculator() -> None:
    """Handle Operation 1: Age Calculator and Birthday Countdown."""
    print("\n" + "-" * 55)
    print("          OPERATION 1: AGE & BIRTHDAY CALCULATOR")
    print("-" * 55)
    print("Find your exact age in years, months, and days, plus your next birthday!")
    print("(Type 'cancel' at any prompt to return to the main menu)\n")

    birth_date = prompt_for_date("Enter your birth date (DD-MM-YYYY): ")
    if birth_date is None:
        return

    today = date.today()
    try:
        age_info = calculate_age(birth_date, today)
        bday_info = get_next_birthday(birth_date, today)
    except ValueError as err:
        print(f"\n  [!] Calculation Error: {err}\n")
        return

    print("\n" + "=" * 55)
    print(f"  Birth Date      : {birth_date.strftime('%d-%m-%Y')} ({birth_date.strftime('%A')})")
    print(f"  Reference Date  : {today.strftime('%d-%m-%Y')} (Today)")
    print("-" * 55)
    print(f"  Current Age     : {age_info['years']} Years, {age_info['months']} Months, {age_info['days']} Days")
    print(f"  Total Days Lived: {age_info['total_days']:,} days")
    print("-" * 55)

    if bday_info["is_today"]:
        print("  🎉 HAPPY BIRTHDAY! Your birthday is TODAY! Have a wonderful day!")
    else:
        next_bday = bday_info["next_birthday"]
        days_left = bday_info["days_until"]
        note = " (celebrated on 28-Feb in non-leap year)" if bday_info["is_leap_adjusted"] else ""
        print(f"  Next Birthday   : {next_bday.strftime('%d-%m-%Y')} ({next_bday.strftime('%A')}){note}")
        print(f"  Countdown       : {days_left} day(s) remaining until your next birthday!")

        if bday_info["next_leap_birthday"] is not None and bday_info["is_leap_adjusted"]:
            leap_bday = bday_info["next_leap_birthday"]
            days_leap = bday_info["days_until_leap_birthday"]
            print(f"  Next Leap-Day   : {leap_bday.strftime('%d-%m-%Y')} (in {days_leap} days - official 4-year leap day!)")
    print("=" * 55 + "\n")


def handle_days_between() -> None:
    """Handle Operation 2: Days Between Two Dates."""
    print("\n" + "-" * 55)
    print("          OPERATION 2: DAYS BETWEEN TWO DATES")
    print("-" * 55)
    print("Calculate the absolute difference between any two calendar dates.")
    print("(Type 'cancel' at any prompt to return to the main menu)\n")

    date1 = prompt_for_date("Enter first date (DD-MM-YYYY): ")
    if date1 is None:
        return

    date2 = prompt_for_date("Enter second date (DD-MM-YYYY): ")
    if date2 is None:
        return

    diff = days_between(date1, date2)

    print("\n" + "=" * 55)
    print(f"  First Date   : {date1.strftime('%d-%m-%Y')} ({date1.strftime('%A')})")
    print(f"  Second Date  : {date2.strftime('%d-%m-%Y')} ({date2.strftime('%A')})")
    print("-" * 55)

    if diff["is_same_day"]:
        print("  Result       : Both dates are identical (Same Day).")
        print("  Difference   : 0 days (0 weeks and 0 days)")
    else:
        if not diff["is_chronological"]:
            print(f"  Note         : Second date is earlier than first date. Calculating absolute span.")
        print(f"  Span Between : {diff['earlier_date'].strftime('%d-%m-%Y')} and {diff['later_date'].strftime('%d-%m-%Y')}")
        print(f"  Total Days   : {diff['total_days']:,} day(s)")
        print(f"  Breakdown    : {diff['weeks']} week(s) and {diff['remaining_days']} day(s)")
    print("=" * 55 + "\n")


def handle_working_days() -> None:
    """Handle Operation 3: Working Days (Business Days) Calculator."""
    print("\n" + "-" * 55)
    print("        OPERATION 3: WORKING (BUSINESS) DAYS CALCULATOR")
    print("-" * 55)
    print("Count business days (Mon-Fri) excluding weekends and public holidays.")
    print("(Type 'cancel' at any prompt to return to the main menu)\n")

    start = prompt_for_date("Enter start date (DD-MM-YYYY): ")
    if start is None:
        return

    end = prompt_for_date("Enter end date (DD-MM-YYYY): ")
    if end is None:
        return

    holidays = prompt_for_holidays()
    if holidays is None:
        return

    res = working_days_between(start, end, holidays)

    print("\n" + "=" * 55)
    print(f"  Date Range        : {res['start_date'].strftime('%d-%m-%Y')} to {res['end_date'].strftime('%d-%m-%Y')} (Inclusive)")
    if res["is_inverted"]:
        print("  Notice            : End date was earlier than start date; span was automatically ordered.")
    print("-" * 55)
    print(f"  Total Calendar Days: {res['total_calendar_days']}")
    print(f"  Weekend Days (Sat/Sun): {res['weekend_days']}")
    print(f"  Public Holidays on Weekdays: {len(res['holidays_on_weekdays'])}")
    if res["holidays_on_weekdays"]:
        hol_str = ", ".join(d.strftime("%d-%m-%Y (%a)") for d in res["holidays_on_weekdays"])
        print(f"    -> Deducted: {hol_str}")
    if res["holidays_on_weekends"]:
        wknd_hol_str = ", ".join(d.strftime("%d-%m-%Y (%a)") for d in res["holidays_on_weekends"])
        print(f"  Public Holidays on Weekends: {len(res['holidays_on_weekends'])} (Already excluded as weekends)")
        print(f"    -> Non-deducted: {wknd_hol_str}")
    print("-" * 55)
    print(f"  TOTAL WORKING DAYS: {res['working_days']} business day(s)")
    print("=" * 55 + "\n")


def handle_date_formatter() -> None:
    """Handle Operation 4: Date and Time Formatter."""
    print("\n" + "-" * 55)
    print("           OPERATION 4: DATE & TIME FORMATTER")
    print("-" * 55)
    print("Format current timestamp or a custom date into standard global formats.")
    print("  1. Use Current System Date and Time")
    print("  2. Enter a Custom Date (DD-MM-YYYY)")
    print("  3. Cancel and Return to Menu\n")

    choice = input("Enter choice (1-3): ").strip()
    if choice == "1":
        target_dt = datetime.now()
        source_label = "Current System Date and Time"
    elif choice == "2":
        user_date = prompt_for_date("Enter custom date (DD-MM-YYYY): ")
        if user_date is None:
            return
        # Combine date with current system time for a complete timestamp representation
        now_time = datetime.now().time()
        target_dt = datetime.combine(user_date, now_time)
        source_label = f"Custom Date: {user_date.strftime('%d-%m-%Y')} (with current time)"
    elif choice in ("3", "c", "cancel", "q"):
        print("  -> Operation cancelled.\n")
        return
    else:
        print("  [!] Invalid choice. Returning to menu.\n")
        return

    formats = format_date_time(target_dt)

    print("\n" + "=" * 65)
    print(f"  Source: {source_label}")
    print("=" * 65)
    print(f"  {'FORMAT DESCRIPTION':<32} | {'RESULT'}")
    print("-" * 65)
    for desc, _, val in formats:
        print(f"  {desc:<32} | {val}")
    print("=" * 65 + "\n")


def handle_add_subtract_days() -> None:
    """Handle Operation 5A (Bonus): Add or Subtract Days from a Date."""
    print("\n" + "-" * 55)
    print("       OPERATION 5A: ADD / SUBTRACT DAYS FROM DATE")
    print("-" * 55)
    print("Add or subtract N calendar days to find a target future or past date.")
    print("(Type 'cancel' at any prompt to return to the main menu)\n")

    base = prompt_for_date("Enter base date (DD-MM-YYYY): ")
    if base is None:
        return

    days = prompt_for_int("Enter number of days (positive to add, negative to subtract, e.g. +30 or -15): ")
    if days is None:
        return

    res = add_subtract_days(base, days)

    print("\n" + "=" * 55)
    print(f"  Base Date     : {res['base_date'].strftime('%d-%m-%Y')} ({res['base_date'].strftime('%A')})")
    print(f"  Adjustment    : {'+' if days >= 0 else ''}{days} day(s)")
    print("-" * 55)
    print(f"  Result Date   : {res['result_date'].strftime('%d-%m-%Y')} ({res['weekday']})")
    print(f"  Written Date  : {res['result_date'].strftime('%A, %d %B %Y')}")
    print("=" * 55 + "\n")


def handle_leap_year_checker() -> None:
    """Handle Operation 5B (Bonus): Leap Year Checker."""
    print("\n" + "-" * 55)
    print("          OPERATION 5B: LEAP YEAR CHECKER")
    print("-" * 55)
    print("Verify if any year is a leap year and review the calendar rule breakdown.")
    print("(Type 'cancel' at any prompt to return to the main menu)\n")

    year = prompt_for_int("Enter a 4-digit calendar year (e.g., 2024): ", min_val=1, max_val=9999)
    if year is None:
        return

    info = explain_leap_year(year)

    print("\n" + "=" * 60)
    print(f"  Year Under Check : {info['year']}")
    print(f"  Is Leap Year?    : {'YES (Leap Year)' if info['is_leap'] else 'NO (Common Year)'}")
    print(f"  Days in February : {info['days_in_february']} days")
    print(f"  Total Days in Yr : {info['total_days']} days")
    print("-" * 60)
    print(f"  Rule Explanation :\n  {info['reason']}")
    print("-" * 60)
    print(f"  Adjacent Leap Years: Previous = {info['previous_leap_year']} | Next = {info['next_leap_year']}")
    print("=" * 60 + "\n")


# =============================================================================
# 9. MAIN MENU LOOP
# =============================================================================

def print_banner() -> None:
    """Print the program header banner."""
    print("""
======================================================================
               DATE AND TIME UTILITY (v1.0)
        Level 1 Internship Project - Task 26
======================================================================
  Built with Python standard 'datetime' module | Clean, Safe, Robust
======================================================================
  1. Calculate Age & Birthday Countdown
  2. Calculate Days Between Two Dates
  3. Calculate Working (Business) Days (Mon-Fri)
  4. Date and Time Formatter (Multi-format)
  5. Add or Subtract Days from a Date (Bonus)
  6. Leap Year Checker & Rule Breakdown (Bonus)
  7. Exit Application
======================================================================""")


def main_menu() -> None:
    """Main execution loop for the menu-driven command-line interface."""
    while True:
        print_banner()
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            handle_age_calculator()
        elif choice == "2":
            handle_days_between()
        elif choice == "3":
            handle_working_days()
        elif choice == "4":
            handle_date_formatter()
        elif choice == "5":
            handle_add_subtract_days()
        elif choice == "6":
            handle_leap_year_checker()
        elif choice in ("7", "exit", "quit", "q"):
            print("\nThank you for using the Date and Time Utility. Goodbye!\n")
            break
        else:
            print("\n  [!] Invalid selection. Please enter a number between 1 and 7.\n")


if __name__ == "__main__":
    main_menu()
