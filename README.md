# Date and Time Utility (`date-time-utility`)

> **Level 1 Internship Task 26: Build a Date and Time Utility**  
> A beginner-friendly, robust, menu-driven command-line tool for practical date and time operations built **strictly using Python's standard `datetime` module** (no manual date approximations, no third-party libraries).

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Supported Operations](#supported-operations)
3. [Design Principles & Architecture](#design-principles--architecture)
4. [Project File Structure](#project-file-structure)
5. [Getting Started & How to Run](#getting-started--how-to-run)
6. [Running the Test Suite](#running-the-test-suite)
7. [Example Walkthroughs](#example-walkthroughs)
8. [Interview Discussion Questions & Answers](#interview-discussion-questions--answers)

---

## Project Overview

Working with calendar dates and timestamps is one of the most common yet deceptive tasks in software engineering. Irregular month lengths (28, 29, 30, 31 days), leap years, century rules, weekend boundaries, and formatting variations make naive date arithmetic error-prone.

The **Date and Time Utility** provides an interactive, menu-driven terminal interface and a modular Python library to perform everyday calendar operations accurately and safely.

---

## Supported Operations

The utility implements all required and bonus operations:

| # | Operation | Description |
|---|---|---|
| **1** | **Age & Birthday Calculator** | Computes exact age in **years, months, and days**, total days lived, and an upcoming birthday countdown. Intelligently handles **Feb 29 leap-day births** (reporting both the non-leap annual celebration on Feb 28 and the countdown to the next official 4-year leap birthday). |
| **2** | **Days Between Two Dates** | Calculates the absolute difference between any two dates in **total days** and formatted as **weeks + remaining days**. Supports both chronological and inverted inputs. |
| **3** | **Working Days (Business Days)** | Counts business days (**Monday through Friday**), excluding weekend days and optional user-entered public holidays. Prevents double-deduction if a holiday falls on a Saturday or Sunday. |
| **4** | **Date & Time Formatter** | Formats current system time or a custom user-entered date into diverse international formats (ISO 8601, British/Indian DD-MM-YYYY, US MM/DD/YYYY, full written text, 12-hour AM/PM, 24-hour military, and day of year). |
| **5A** | **Add / Subtract Days (Bonus)** | Projects a future or past date by adding or subtracting an arbitrary integer number of days using `timedelta`, displaying the resulting calendar date and day of the week. |
| **5B** | **Leap Year Checker (Bonus)** | Checks whether any year (1–9999) is a leap year, explains the underlying Gregorian calendar rules (divisible by 4, century rule, quadricentennial rule), and reports adjacent leap years. |

---

## Design Principles & Architecture

### 1. Strict Standard Library Compliance
This project relies **exclusively** on Python's built-in `datetime` module:
- `datetime.date`: Calendar representations (year, month, day).
- `datetime.datetime`: Timestamps with both date and time components.
- `datetime.timedelta`: Exact durations and date arithmetic offsets.
- `datetime.strptime()`: Strict string-to-date parsing with validation.
- `datetime.strftime()`: Safe and portable date-to-string formatting directives.

### 2. Separation of Concerns (Testability)
All calculation functions are decoupled from console I/O (`input()` and `print()`):
- **Core Engine:** Pure functions (`calculate_age`, `days_between`, `working_days_between`, `add_subtract_days`, `is_leap_year`, `format_date_time`, `parse_date`) accept standard parameters and return structured dictionaries or tuples.
- **CLI Layer:** Interactive handlers (`prompt_for_date`, `handle_age_calculator`, etc.) manage user interaction, input sanitization, and pretty terminal printing.
- **Benefit:** 100% of the core calculation logic is testable via automated unit tests without mocking terminal streams.

### 3. Bulletproof Input Validation & Error Recovery
All dates require the `DD-MM-YYYY` format (e.g., `26-10-2026`). Input validation catches both formatting errors (e.g., `2026-10-26`, `invalid_str`) and impossible calendar dates (e.g., `31-02-2025`, `29-02-2025` in non-leap years, `31-04-2024`) using `try/except ValueError`. The CLI provides friendly guidance and prompts the user again without crashing. Users can also type `cancel` at any prompt to return to the main menu.

### 4. Edge Cases Handled
- **Leap-Day Babies (Feb 29):** Tested for birthdays in non-leap years (observed Feb 28) and leap years (Feb 29).
- **Future Birth Dates:** Prevented with an explicit error message (`Birth date cannot be in the future`).
- **Inverted Date Ranges:** Start date later than end date is automatically normalized with an informative user notice.
- **Same-Day Inputs:** Properly outputs 0 days difference and 1 working day (if on a weekday).
- **Weekend Holidays:** If a holiday falls on a Saturday or Sunday, it is not double-subtracted from the business day count.

---

## Project File Structure

```text
date-time-utility/
│
├── date_utility.py          # Main application: core functions and menu CLI
├── test_date_utility.py     # Comprehensive unit tests (36 test cases)
├── sample_calculations.md   # Verified calculation runs & edge case demonstrations
├── generate_samples.py      # Automated generator for sample calculations
└── README.md                # Documentation, guide, and interview answers
```

---

## Getting Started & How to Run

### Prerequisites
- Python 3.8 or higher (tested on Python 3.14).
- No external packages required (`pip install` is not needed).

### Running the Application
From the project folder, execute:

```powershell
python date_utility.py
```

You will see the main interactive menu:

```text
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
======================================================================
Select an option (1-7):
```

---

## Running the Test Suite

The project includes a complete test suite written using Python's built-in `unittest` framework, covering normal execution paths and edge cases.

To run all tests with verbose output:

```powershell
python -m unittest test_date_utility.py -v
```

### Test Coverage Summary:
- **`TestParseDate`**: Valid dates, leap day parsing, whitespace stripping, empty inputs, format mismatches, and impossible calendar dates (`31-02-2025`, `29-02-2025`, `31-04-2024`).
- **`TestLeapYear`**: Common years, standard leap years, century non-leap years (`1700`, `1800`, `1900`, `2100`), century leap years (`1600`, `2000`, `2400`), and rule explanations.
- **`TestCalculateAge`**: Standard birth dates, same-day birth dates, exact 1-year boundaries, month-end transitions (Aug 31 to Feb 28), future date rejection, and Feb 29 births.
- **`TestNextBirthday`**: Birthdays remaining in the same year, rolled over to next year, birthday today (0 days), and leap-day birthday countdowns.
- **`TestDaysBetween`**: Same day, chronological spans, non-chronological spans, and leap-year spans (366 days).
- **`TestWorkingDays`**: Full working weeks (5 days), full weeks with weekends (5 working, 2 weekend), weekday holiday deduction, weekend holiday non-double-deduction, inverted ranges, and single-day ranges.
- **`TestAddSubtractDays`**: Positive day additions, negative day subtractions, month/year crossings, and leap-day crossings.
- **`TestFormatDateTime`**: Multi-format dictionary validation and format compliance.

---

## Example Walkthroughs

### 1. Age & Birthday Countdown
```text
Enter your birth date (DD-MM-YYYY): 15-08-1997

=======================================================
  Birth Date      : 15-08-1997 (Friday)
  Reference Date  : 26-10-2026 (Today)
-------------------------------------------------------
  Current Age     : 29 Years, 2 Months, 11 Days
  Total Days Lived: 10,664 days
-------------------------------------------------------
  Next Birthday   : 15-08-2027 (Sunday)
  Countdown       : 293 day(s) remaining until your next birthday!
=======================================================
```

### 2. Working Days with Holidays
```text
Enter start date (DD-MM-YYYY): 21-12-2026
Enter end date (DD-MM-YYYY): 04-01-2027
Enter public holidays: 25-12-2026, 26-12-2026, 01-01-2027

=======================================================
  Date Range        : 21-12-2026 to 04-01-2027 (Inclusive)
-------------------------------------------------------
  Total Calendar Days: 15
  Weekend Days (Sat/Sun): 4
  Public Holidays on Weekdays: 2
    -> Deducted: 25-12-2026 (Fri), 01-01-2027 (Fri)
  Public Holidays on Weekends: 1 (Already excluded as weekends)
    -> Non-deducted: 26-12-2026 (Sat)
-------------------------------------------------------
  TOTAL WORKING DAYS: 9 business day(s)
=======================================================
```

*(See [sample_calculations.md](sample_calculations.md) for 8 verified calculation runs.)*

---

## Interview Discussion Questions & Answers

### Question 1: What is the `datetime` module?
**Answer:**  
The `datetime` module is Python's built-in standard library for working with dates, times, and intervals. It provides several core object types:
1. **`date`**: Represents an idealized calendar date (year, month, day) in the Gregorian calendar, independent of time of day.
2. **`time`**: Represents idealized time of day (hour, minute, second, microsecond, and optional timezone info), independent of any date.
3. **`datetime`**: Combines both date and time attributes into a single object.
4. **`timedelta`**: Represents a duration expressing the exact difference between two date or datetime instances (resolution down to microseconds).
5. **`timezone` / `tzinfo`**: Abstract and concrete classes for timezone adjustments and UTC offsets.

It also distinguishes between:
- **Naive objects:** Objects that lack timezone information (assuming local or undefined context).
- **Aware objects:** Objects with attached timezone/daylight saving information.

Key conversion methods include:
- `datetime.strptime(string, format)`: **P**arses a formatted string into a datetime object while enforcing calendar validity.
- `datetime.strftime(format)`: **F**ormats a datetime object into a human-readable string using format directives (e.g. `%d`, `%B`, `%Y`).

---

### Question 2: How do you calculate the difference between two dates?
**Answer:**  
In Python, the simplest and most accurate way to calculate the difference between two `date` or `datetime` objects is by using the subtraction operator (`-`):

```python
from datetime import date

date1 = date(2026, 10, 26)
date2 = date(2026, 11, 5)

delta = date2 - date1  # Produces a timedelta object
total_days = delta.days  # 10 days
```

Key technical considerations:
1. **Result Type:** Subtracting two `date` objects yields a `timedelta` object. Calling `delta.days` provides the integer count of days.
2. **Handling Order / Direction:** If `date2 < date1`, `delta.days` will be negative. To find the absolute duration regardless of input order, use `abs((date2 - date1).days)`.
3. **Weeks and Days Breakdown:** You can break down total days into weeks and remainder days using integer division and modulo:
   ```python
   weeks = total_days // 7
   remaining_days = total_days % 7
   ```
4. **Why Not Divide by 365 or 30 for Age?**  
   Naive division like `total_days // 365` fails for calendar age because leap years have 366 days and months vary from 28 to 31 days. To compute true human age in years, months, and days, one must anchor the calculation to the actual calendar month boundaries.

---

### Question 3: Why should date calculations use standard libraries?
**Answer:**  
Date and time calculations should **always** use standard or battle-tested libraries rather than manual arithmetic for several critical reasons:

1. **Irregular Month Lengths:**  
   Months do not have a constant length: 7 months have 31 days, 4 have 30 days, and February has 28 or 29 days. Manual approximations (such as `days // 30`) introduce compounding errors into financial, payroll, and billing systems.

2. **Complex Leap Year Rules:**  
   A leap year is not simply "every 4 years." Under the Gregorian calendar:
   - A year divisible by 4 is a leap year,
   - **Except** century years (divisible by 100), which are **not** leap years,
   - **Unless** the century year is divisible by 400 (e.g., 2000 was a leap year, but 1900 and 2100 are not).  
   Standard libraries have these rules embedded natively.

3. **Input Validation & Impossible Dates:**  
   Standard parsers (`datetime.strptime`) validate real-world calendar constraints automatically, preventing bugs caused by inputs like `31-02-2025` or `31-04-2024`.

4. **Timezones, Daylight Saving Time (DST), and Historical Shifts:**  
   Real-world timestamps deal with 1-hour spring-forward/fall-back DST shifts, 30-minute and 45-minute timezone offsets (e.g., India UTC+5:30, Nepal UTC+5:45), and historical calendar skips (such as the 1752 British calendar reform). Writing custom date math to handle these is virtually guaranteed to introduce subtle bugs.

5. **Maintainability & Security:**  
   Using Python's standard library guarantees cross-platform reliability, optimized C-level execution speed, and ongoing maintenance without introducing external supply chain dependencies.

---

## Author & Project Info
- **Project Name:** `date-time-utility`
- **Level:** Level 1 Internship Task 26
- **Language:** Python 3.8+
- **License:** Open Source / Educational
