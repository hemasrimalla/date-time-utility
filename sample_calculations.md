# Sample Calculations and Verification Runs

This document records verified sample calculations generated directly by executing the functions in `date_utility.py`. It showcases standard operations, edge cases (leap-year births, cross-year spans, and weekend holiday deductions), and error-handling scenarios.

---

## Sample 1: Standard Age Calculation & Birthday Countdown
- **Operation:** Calculate Age & Birthday Countdown
- **Input Birth Date:** `15-08-1997` (Friday)
- **Reference Date:** `26-10-2026` (Monday - Today)

### Program Output:
```text
  Birth Date       : 15-08-1997 (Friday)
  Reference Date   : 26-10-2026 (Monday)
  Current Age      : 29 Years, 2 Months, 11 Days
  Total Days Lived : 10,664 days
  Next Birthday    : 15-08-2027 (Sunday)
  Countdown        : 293 day(s) remaining
```
**Explanation:** The individual's 2026 birthday has already passed, so the next birthday countdown rolls forward to 15 August 2027.

---

## Sample 2: Leap-Year Birth Date & Dual Birthday Countdown (Edge Case)
- **Operation:** Calculate Age & Birthday Countdown (Feb 29 Leap Day Baby)
- **Input Birth Date:** `29-02-2004` (Sunday - Leap Year)
- **Reference Date:** `26-10-2026` (Monday - Today)

### Program Output:
```text
  Birth Date       : 29-02-2004 (Sunday)
  Reference Date   : 26-10-2026 (Monday)
  Current Age      : 22 Years, 7 Months, 27 Days
  Total Days Lived : 8,275 days
  Next Birthday    : 28-02-2027 (Sunday) (celebrated on 28-Feb in non-leap year)
  Countdown        : 125 day(s) remaining
  Next Leap-Day    : 29-02-2028 (in 491 days - official 4-year leap day!)
```
**Explanation:** In non-leap years (such as 2027), February has only 28 days. The utility accounts for this by noting the annual celebration on 28-Feb while also reporting the countdown to their official quadrennial birthday on 29-02-2028.

---

## Sample 3: Absolute Days Between Two Dates (Crossing a Leap Year)
- **Operation:** Days Between Two Dates
- **First Date:** `15-01-2024`
- **Second Date:** `15-01-2025`

### Program Output:
```text
  Span Between     : 15-01-2024 and 15-01-2025
  Total Days       : 366 day(s)
  Breakdown        : 52 week(s) and 2 day(s)
```
**Explanation:** Because 2024 is a leap year (with 29 days in February), the span between January 15, 2024 and January 15, 2025 is 366 days (52 weeks + 2 days), rather than 365 days.

---

## Sample 4: Working Days (Business Days) with Weekday and Weekend Holidays
- **Operation:** Working Days (Business Days) Calculator
- **Start Date:** `21-12-2026` (Monday)
- **End Date:** `04-01-2027` (Monday)
- **Input Holidays:** `25-12-2026` (Christmas - Fri), `26-12-2026` (Boxing Day - Sat), `01-01-2027` (New Year's Day - Fri)

### Program Output:
```text
  Date Range                  : 21-12-2026 to 04-01-2027 (Inclusive)
  Total Calendar Days         : 15
  Weekend Days (Sat/Sun)      : 4
  Public Holidays on Weekdays : 2 (25-12-2026 [Fri], 01-01-2027 [Fri])
  Public Holidays on Weekends : 1 (26-12-2026 [Sat] - excluded as weekend, not double-deducted)
  TOTAL WORKING DAYS          : 9 business day(s)
```
**Explanation:** Real-world holiday exclusion: 15 total days minus 4 weekend days minus 2 weekday holidays leaves exactly 9 working days. Boxing Day falls on a Saturday and is correctly not double-subtracted.

---

## Sample 5: Multi-Format Date and Time Formatter
- **Operation:** Date and Time Formatter
- **Input Datetime:** `2026-10-26 21:30:15`

### Program Output:
```text
  Standard Date (Indian/British)   | 26-10-2026
  ISO 8601 (International)         | 2026-10-26
  US Format                        | 10/26/2026
  Full Written Date                | 26 October 2026
  Day and Abbreviated Date         | Monday, 26 Oct 2026
  Complete Long Date               | Monday, October 26, 2026
  24-Hour Military Time            | 21:30:15
  12-Hour Time with AM/PM          | 09:30:15 PM
  Full Date & Time (12-Hour)       | 26 October 2026, 09:30:15 PM
  Day of Year & Week               | Day 299 of year, Week 43
```
**Explanation:** Demonstrates custom formatting using Python's `datetime.strftime()` directives across common worldwide formats (DD-MM-YYYY, ISO 8601, US, written dates, 12-hour AM/PM, and 24-hour time).

---

## Sample 6: Date Projection (Add and Subtract N Days)
- **Operation:** Add / Subtract Days from a Date
- **Base Date:** `26-10-2026` (Monday)

### Scenario 6A: Add +90 Days (Quarterly Projection)
```text
  Base Date    : 26-10-2026 (Monday)
  Adjustment   : +90 day(s)
  Result Date  : 24-01-2027 (Sunday)
  Written Date : Sunday, 24 January 2027
```

### Scenario 6B: Subtract -45 Days (Retroactive Lookback)
```text
  Base Date    : 26-10-2026 (Monday)
  Adjustment   : -45 day(s)
  Result Date  : 11-09-2026 (Friday)
  Written Date : Friday, 11 September 2026
```
**Explanation:** Uses `timedelta(days=N)` to accurately cross month and year boundaries.

---

## Sample 7: Leap Year Checker & Gregorian Rule Analysis
- **Operation:** Leap Year Checker

| Year | Is Leap Year? | Days in Feb | Total Days | Rule Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **2024** | YES (Leap Year) | 29 | 366 | 2024 is divisible by 4 and not a century year (not divisible by 100), so it IS a leap year. |
| **2025** | NO (Common Year) | 28 | 365 | 2025 is not divisible by 4, so it is NOT a leap year. |
| **1900** | NO (Common Year) | 28 | 365 | 1900 is divisible by 100 but not by 400. It is a century year, so it is NOT a leap year. |
| **2000** | YES (Leap Year) | 29 | 366 | 2000 is divisible by 400. Century years divisible by 400 ARE leap years (Gregorian quadricentennial rule). |

**Key Insight:** Clarifies why 1900 was not a leap year (century rule) while 2000 was a leap year (400-year exception).

---

## Sample 8: Invalid Input Handling & Error Recovery (Negative Test Cases)
- **Operation:** Robust Input Validation (`try/except` with `datetime.strptime()`)

| Test Input | Category | Exception Caught | Handled Gracefully Without Crash |
| :--- | :--- | :--- | :--- |
| `31-02-2025` | Impossible calendar date (Feb 31) | `Invalid calendar date '31-02-2025': That day does not exist in the specified month/year.` | Yes (prompted to re-enter) |
| `29-02-2025` | Feb 29 in non-leap year | `Invalid calendar date '29-02-2025': That day does not exist in the specified month/year.` | Yes (prompted to re-enter) |
| `31-04-2024` | April has only 30 days | `Invalid calendar date '31-04-2024': That day does not exist in the specified month/year.` | Yes (prompted to re-enter) |
| `2026-10-26` | Wrong format (ISO YYYY-MM-DD instead of DD-MM-YYYY) | `Invalid format '2026-10-26': Expected DD-MM-YYYY (e.g., 26-10-2026).` | Yes (prompted to re-enter) |
| `hello-date` | Alphanumeric string | `Invalid format 'hello-date': Expected DD-MM-YYYY (e.g., 26-10-2026).` | Yes (prompted to re-enter) |
| `` | Empty string | `Date string cannot be empty.` | Yes (prompted to re-enter) |
| `15-08-2030` | Future birth date for age calculation | `Birth date (15-08-2030) cannot be in the future relative to reference date (26-10-2026).` | Yes (caught and reported) |

**Explanation:** The program catches format errors and impossible calendar dates cleanly using `ValueError` and re-prompts the user instead of terminating abruptly.
