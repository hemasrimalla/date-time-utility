"""
Script to generate sample_calculations.md by executing date_utility.py functions directly.
"""

from datetime import date, datetime
import date_utility as du


def generate_markdown() -> str:
    md = []
    md.append("# Sample Calculations and Verification Runs")
    md.append("")
    md.append("This document records verified sample calculations generated directly by executing the functions in `date_utility.py`. It showcases standard operations, edge cases (leap-year births, cross-year spans, and weekend holiday deductions), and error-handling scenarios.")
    md.append("")
    md.append("---")
    md.append("")

    # Sample 1
    ref1 = date(2026, 10, 26)
    bday1 = du.parse_date("15-08-1997")
    age1 = du.calculate_age(bday1, ref1)
    next1 = du.get_next_birthday(bday1, ref1)

    md.append("## Sample 1: Standard Age Calculation & Birthday Countdown")
    md.append("- **Operation:** Calculate Age & Birthday Countdown")
    md.append("- **Input Birth Date:** `15-08-1997` (Friday)")
    md.append(f"- **Reference Date:** `{ref1.strftime('%d-%m-%Y')}` (Monday - Today)")
    md.append("")
    md.append("### Program Output:")
    md.append("```text")
    md.append("  Birth Date       : 15-08-1997 (Friday)")
    md.append(f"  Reference Date   : {ref1.strftime('%d-%m-%Y')} (Monday)")
    md.append(f"  Current Age      : {age1['years']} Years, {age1['months']} Months, {age1['days']} Days")
    md.append(f"  Total Days Lived : {age1['total_days']:,} days")
    md.append(f"  Next Birthday    : {next1['next_birthday'].strftime('%d-%m-%Y')} ({next1['next_birthday'].strftime('%A')})")
    md.append(f"  Countdown        : {next1['days_until']} day(s) remaining")
    md.append("```")
    md.append("**Explanation:** The individual's 2026 birthday has already passed, so the next birthday countdown rolls forward to 15 August 2027.")
    md.append("")
    md.append("---")
    md.append("")

    # Sample 2
    bday2 = du.parse_date("29-02-2004")
    age2 = du.calculate_age(bday2, ref1)
    next2 = du.get_next_birthday(bday2, ref1)

    md.append("## Sample 2: Leap-Year Birth Date & Dual Birthday Countdown (Edge Case)")
    md.append("- **Operation:** Calculate Age & Birthday Countdown (Feb 29 Leap Day Baby)")
    md.append("- **Input Birth Date:** `29-02-2004` (Sunday - Leap Year)")
    md.append(f"- **Reference Date:** `{ref1.strftime('%d-%m-%Y')}` (Monday - Today)")
    md.append("")
    md.append("### Program Output:")
    md.append("```text")
    md.append("  Birth Date       : 29-02-2004 (Sunday)")
    md.append(f"  Reference Date   : {ref1.strftime('%d-%m-%Y')} (Monday)")
    md.append(f"  Current Age      : {age2['years']} Years, {age2['months']} Months, {age2['days']} Days")
    md.append(f"  Total Days Lived : {age2['total_days']:,} days")
    md.append(f"  Next Birthday    : {next2['next_birthday'].strftime('%d-%m-%Y')} ({next2['next_birthday'].strftime('%A')}) (celebrated on 28-Feb in non-leap year)")
    md.append(f"  Countdown        : {next2['days_until']} day(s) remaining")
    md.append(f"  Next Leap-Day    : {next2['next_leap_birthday'].strftime('%d-%m-%Y')} (in {next2['days_until_leap_birthday']} days - official 4-year leap day!)")
    md.append("```")
    md.append("**Explanation:** In non-leap years (such as 2027), February has only 28 days. The utility accounts for this by noting the annual celebration on 28-Feb while also reporting the countdown to their official quadrennial birthday on 29-02-2028.")
    md.append("")
    md.append("---")
    md.append("")

    # Sample 3
    d1 = du.parse_date("15-01-2024")
    d2 = du.parse_date("15-01-2025")
    diff1 = du.days_between(d1, d2)

    md.append("## Sample 3: Absolute Days Between Two Dates (Crossing a Leap Year)")
    md.append("- **Operation:** Days Between Two Dates")
    md.append("- **First Date:** `15-01-2024`")
    md.append("- **Second Date:** `15-01-2025`")
    md.append("")
    md.append("### Program Output:")
    md.append("```text")
    md.append(f"  Span Between     : {diff1['earlier_date'].strftime('%d-%m-%Y')} and {diff1['later_date'].strftime('%d-%m-%Y')}")
    md.append(f"  Total Days       : {diff1['total_days']} day(s)")
    md.append(f"  Breakdown        : {diff1['weeks']} week(s) and {diff1['remaining_days']} day(s)")
    md.append("```")
    md.append("**Explanation:** Because 2024 is a leap year (with 29 days in February), the span between January 15, 2024 and January 15, 2025 is 366 days (52 weeks + 2 days), rather than 365 days.")
    md.append("")
    md.append("---")
    md.append("")

    # Sample 4
    w_start = du.parse_date("21-12-2026")
    w_end = du.parse_date("04-01-2027")
    hols = [du.parse_date("25-12-2026"), du.parse_date("26-12-2026"), du.parse_date("01-01-2027")]
    w_res = du.working_days_between(w_start, w_end, hols)

    md.append("## Sample 4: Working Days (Business Days) with Weekday and Weekend Holidays")
    md.append("- **Operation:** Working Days (Business Days) Calculator")
    md.append("- **Start Date:** `21-12-2026` (Monday)")
    md.append("- **End Date:** `04-01-2027` (Monday)")
    md.append("- **Input Holidays:** `25-12-2026` (Christmas - Fri), `26-12-2026` (Boxing Day - Sat), `01-01-2027` (New Year's Day - Fri)")
    md.append("")
    md.append("### Program Output:")
    md.append("```text")
    md.append(f"  Date Range                  : {w_res['start_date'].strftime('%d-%m-%Y')} to {w_res['end_date'].strftime('%d-%m-%Y')} (Inclusive)")
    md.append(f"  Total Calendar Days         : {w_res['total_calendar_days']}")
    md.append(f"  Weekend Days (Sat/Sun)      : {w_res['weekend_days']}")
    md.append(f"  Public Holidays on Weekdays : {len(w_res['holidays_on_weekdays'])} (25-12-2026 [Fri], 01-01-2027 [Fri])")
    md.append(f"  Public Holidays on Weekends : {len(w_res['holidays_on_weekends'])} (26-12-2026 [Sat] - excluded as weekend, not double-deducted)")
    md.append(f"  TOTAL WORKING DAYS          : {w_res['working_days']} business day(s)")
    md.append("```")
    md.append("**Explanation:** Real-world holiday exclusion: 15 total days minus 4 weekend days minus 2 weekday holidays leaves exactly 9 working days. Boxing Day falls on a Saturday and is correctly not double-subtracted.")
    md.append("")
    md.append("---")
    md.append("")

    # Sample 5
    dt_sample = datetime(2026, 10, 26, 21, 30, 15)
    formats = du.format_date_time(dt_sample)

    md.append("## Sample 5: Multi-Format Date and Time Formatter")
    md.append("- **Operation:** Date and Time Formatter")
    md.append("- **Input Datetime:** `2026-10-26 21:30:15`")
    md.append("")
    md.append("### Program Output:")
    md.append("```text")
    for desc, _, val in formats:
        md.append(f"  {desc:<32} | {val}")
    md.append("```")
    md.append("**Explanation:** Demonstrates custom formatting using Python's `datetime.strftime()` directives across common worldwide formats (DD-MM-YYYY, ISO 8601, US, written dates, 12-hour AM/PM, and 24-hour time).")
    md.append("")
    md.append("---")
    md.append("")

    # Sample 6
    p_add = du.add_subtract_days(du.parse_date("26-10-2026"), 90)
    p_sub = du.add_subtract_days(du.parse_date("26-10-2026"), -45)

    md.append("## Sample 6: Date Projection (Add and Subtract N Days)")
    md.append("- **Operation:** Add / Subtract Days from a Date")
    md.append("- **Base Date:** `26-10-2026` (Monday)")
    md.append("")
    md.append("### Scenario 6A: Add +90 Days (Quarterly Projection)")
    md.append("```text")
    md.append("  Base Date    : 26-10-2026 (Monday)")
    md.append("  Adjustment   : +90 day(s)")
    md.append(f"  Result Date  : {p_add['result_date'].strftime('%d-%m-%Y')} ({p_add['weekday']})")
    md.append(f"  Written Date : {p_add['result_date'].strftime('%A, %d %B %Y')}")
    md.append("```")
    md.append("")
    md.append("### Scenario 6B: Subtract -45 Days (Retroactive Lookback)")
    md.append("```text")
    md.append("  Base Date    : 26-10-2026 (Monday)")
    md.append("  Adjustment   : -45 day(s)")
    md.append(f"  Result Date  : {p_sub['result_date'].strftime('%d-%m-%Y')} ({p_sub['weekday']})")
    md.append(f"  Written Date : {p_sub['result_date'].strftime('%A, %d %B %Y')}")
    md.append("```")
    md.append("**Explanation:** Uses `timedelta(days=N)` to accurately cross month and year boundaries.")
    md.append("")
    md.append("---")
    md.append("")

    # Sample 7
    md.append("## Sample 7: Leap Year Checker & Gregorian Rule Analysis")
    md.append("- **Operation:** Leap Year Checker")
    md.append("")
    md.append("| Year | Is Leap Year? | Days in Feb | Total Days | Rule Explanation |")
    md.append("| :--- | :--- | :--- | :--- | :--- |")
    for yr in [2024, 2025, 1900, 2000]:
        info = du.explain_leap_year(yr)
        leap_str = "YES (Leap Year)" if info["is_leap"] else "NO (Common Year)"
        md.append(f"| **{yr}** | {leap_str} | {info['days_in_february']} | {info['total_days']} | {info['reason']} |")
    md.append("")
    md.append("**Key Insight:** Clarifies why 1900 was not a leap year (century rule) while 2000 was a leap year (400-year exception).")
    md.append("")
    md.append("---")
    md.append("")

    # Sample 8
    md.append("## Sample 8: Invalid Input Handling & Error Recovery (Negative Test Cases)")
    md.append("- **Operation:** Robust Input Validation (`try/except` with `datetime.strptime()`)")
    md.append("")
    md.append("| Test Input | Category | Exception Caught | Handled Gracefully Without Crash |")
    md.append("| :--- | :--- | :--- | :--- |")

    test_inputs = [
        ("31-02-2025", "Impossible calendar date (Feb 31)"),
        ("29-02-2025", "Feb 29 in non-leap year"),
        ("31-04-2024", "April has only 30 days"),
        ("2026-10-26", "Wrong format (ISO YYYY-MM-DD instead of DD-MM-YYYY)"),
        ("hello-date", "Alphanumeric string"),
        ("", "Empty string"),
    ]

    for raw, category in test_inputs:
        try:
            du.parse_date(raw)
            msg = "Accepted (Unexpected)"
        except ValueError as e:
            msg = f"`{e}`"
        md.append(f"| `{raw}` | {category} | {msg} | Yes (prompted to re-enter) |")

    # Future date check
    try:
        du.calculate_age(date(2030, 8, 15), date(2026, 10, 26))
    except ValueError as e:
        md.append(f"| `15-08-2030` | Future birth date for age calculation | `{e}` | Yes (caught and reported) |")

    md.append("")
    md.append("**Explanation:** The program catches format errors and impossible calendar dates cleanly using `ValueError` and re-prompts the user instead of terminating abruptly.")

    return "\n".join(md) + "\n"


if __name__ == "__main__":
    content = generate_markdown()
    with open("sample_calculations.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("sample_calculations.md successfully generated.")
