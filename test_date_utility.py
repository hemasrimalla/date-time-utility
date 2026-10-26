"""
=============================================================================
UNIT TESTS FOR DATE AND TIME UTILITY (test_date_utility.py)
=============================================================================
Comprehensive test suite covering core operations, boundary conditions,
and edge cases for Level 1 Internship Task 26.

Run with:
    python -m unittest test_date_utility.py -v
=============================================================================
"""

import unittest
from datetime import date, datetime

from date_utility import (
    parse_date,
    is_leap_year,
    explain_leap_year,
    calculate_age,
    get_next_birthday,
    days_between,
    working_days_between,
    add_subtract_days,
    format_date_time,
)


class TestParseDate(unittest.TestCase):
    """Test date parsing and validation in DD-MM-YYYY format."""

    def test_valid_dates(self):
        self.assertEqual(parse_date("26-10-2026"), date(2026, 10, 26))
        self.assertEqual(parse_date("01-01-2000"), date(2000, 1, 1))
        self.assertEqual(parse_date("29-02-2024"), date(2024, 2, 29))  # Leap year
        self.assertEqual(parse_date("31-12-1999"), date(1999, 12, 31))

    def test_whitespace_handling(self):
        self.assertEqual(parse_date("  15-08-1947  "), date(1947, 8, 15))

    def test_empty_string(self):
        with self.assertRaises(ValueError) as ctx:
            parse_date("")
        self.assertIn("cannot be empty", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            parse_date("   ")
        self.assertIn("cannot be empty", str(ctx.exception))

    def test_invalid_formats(self):
        invalid_formats = [
            "2026-10-26",   # ISO format instead of DD-MM-YYYY
            "26/10/2026",   # Slashes instead of dashes
            "10-26-2026",   # MM-DD-YYYY
            "26-Oct-2026",  # Named month
            "invalid_text", # Plain text
            "26-10",        # Missing year
        ]
        for val in invalid_formats:
            with self.subTest(val=val):
                with self.assertRaises(ValueError) as ctx:
                    parse_date(val)
                self.assertIn("Expected DD-MM-YYYY", str(ctx.exception))

    def test_impossible_calendar_dates(self):
        impossible = [
            "31-02-2025",  # Feb 31 does not exist
            "29-02-2025",  # 2025 is not a leap year
            "31-04-2024",  # April has only 30 days
            "31-06-2024",  # June has only 30 days
            "31-09-2024",  # September has only 30 days
            "31-11-2024",  # November has only 30 days
            "32-01-2024",  # Day 32 out of range
            "00-05-2024",  # Day 00 out of range
        ]
        for val in impossible:
            with self.subTest(val=val):
                with self.assertRaises(ValueError) as ctx:
                    parse_date(val)
                self.assertTrue(
                    "That day does not exist" in str(ctx.exception)
                    or "Expected DD-MM-YYYY" in str(ctx.exception)
                )


class TestLeapYear(unittest.TestCase):
    """Test leap year identification and Gregorian calendar explanation."""

    def test_standard_leap_years(self):
        for year in [2016, 2020, 2024, 2028, 2032]:
            with self.subTest(year=year):
                self.assertTrue(is_leap_year(year))

    def test_standard_common_years(self):
        for year in [2019, 2021, 2022, 2023, 2025, 2026]:
            with self.subTest(year=year):
                self.assertFalse(is_leap_year(year))

    def test_century_non_leap_years(self):
        # Divisible by 100 but NOT by 400
        for year in [1700, 1800, 1900, 2100, 2200, 2300]:
            with self.subTest(year=year):
                self.assertFalse(is_leap_year(year))

    def test_century_leap_years(self):
        # Divisible by 400
        for year in [1600, 2000, 2400]:
            with self.subTest(year=year):
                self.assertTrue(is_leap_year(year))

    def test_explain_leap_year(self):
        info_2024 = explain_leap_year(2024)
        self.assertTrue(info_2024["is_leap"])
        self.assertEqual(info_2024["days_in_february"], 29)
        self.assertEqual(info_2024["total_days"], 366)
        self.assertEqual(info_2024["previous_leap_year"], 2020)
        self.assertEqual(info_2024["next_leap_year"], 2028)

        info_1900 = explain_leap_year(1900)
        self.assertFalse(info_1900["is_leap"])
        self.assertEqual(info_1900["days_in_february"], 28)
        self.assertEqual(info_1900["total_days"], 365)
        self.assertIn("100 but not by 400", info_1900["reason"])


class TestCalculateAge(unittest.TestCase):
    """Test age calculations in years, months, and days."""

    def test_standard_age(self):
        birth = date(1995, 5, 15)
        ref = date(2026, 10, 26)
        res = calculate_age(birth, ref)
        self.assertEqual(res["years"], 31)
        self.assertEqual(res["months"], 5)
        self.assertEqual(res["days"], 11)

    def test_same_day_age(self):
        today = date(2026, 10, 26)
        res = calculate_age(today, today)
        self.assertEqual(res["years"], 0)
        self.assertEqual(res["months"], 0)
        self.assertEqual(res["days"], 0)
        self.assertEqual(res["total_days"], 0)

    def test_exact_one_year(self):
        birth = date(2025, 10, 26)
        ref = date(2026, 10, 26)
        res = calculate_age(birth, ref)
        self.assertEqual(res["years"], 1)
        self.assertEqual(res["months"], 0)
        self.assertEqual(res["days"], 0)

    def test_future_birth_date_raises_error(self):
        birth = date(2030, 1, 1)
        ref = date(2026, 10, 26)
        with self.assertRaises(ValueError) as ctx:
            calculate_age(birth, ref)
        self.assertIn("cannot be in the future", str(ctx.exception))

    def test_leap_day_baby_common_year(self):
        # Born on Feb 29, 2024
        birth = date(2024, 2, 29)
        # On Feb 28, 2025 (1 full common year)
        res_feb28 = calculate_age(birth, date(2025, 2, 28))
        self.assertEqual(res_feb28["years"], 1)
        self.assertEqual(res_feb28["months"], 0)
        self.assertEqual(res_feb28["days"], 0)

        # On March 1, 2025
        res_mar1 = calculate_age(birth, date(2025, 3, 1))
        self.assertEqual(res_mar1["years"], 1)
        self.assertEqual(res_mar1["months"], 0)
        self.assertEqual(res_mar1["days"], 1)

    def test_leap_day_baby_leap_year(self):
        # Born Feb 29, 2024 -> On Feb 29, 2028 (exactly 4 years)
        birth = date(2024, 2, 29)
        ref = date(2028, 2, 29)
        res = calculate_age(birth, ref)
        self.assertEqual(res["years"], 4)
        self.assertEqual(res["months"], 0)
        self.assertEqual(res["days"], 0)

    def test_month_end_transitions(self):
        # Born August 31, 1990 -> On Feb 28, 1991 (6 full months)
        birth = date(1990, 8, 31)
        res1 = calculate_age(birth, date(1991, 2, 28))
        self.assertEqual(res1["years"], 0)
        self.assertEqual(res1["months"], 6)
        self.assertEqual(res1["days"], 0)

        # On March 1, 1991 -> 6 months and 1 day
        res2 = calculate_age(birth, date(1991, 3, 1))
        self.assertEqual(res2["years"], 0)
        self.assertEqual(res2["months"], 6)
        self.assertEqual(res2["days"], 1)


class TestNextBirthday(unittest.TestCase):
    """Test upcoming birthday countdown and leap year birthday handling."""

    def test_birthday_later_this_year(self):
        birth = date(2000, 12, 25)
        ref = date(2026, 10, 26)
        res = get_next_birthday(birth, ref)
        self.assertEqual(res["next_birthday"], date(2026, 12, 25))
        self.assertEqual(res["days_until"], 60)
        self.assertFalse(res["is_today"])
        self.assertFalse(res["is_leap_adjusted"])

    def test_birthday_already_passed_this_year(self):
        birth = date(1998, 5, 10)
        ref = date(2026, 10, 26)
        res = get_next_birthday(birth, ref)
        # Should roll over to 2027
        self.assertEqual(res["next_birthday"], date(2027, 5, 10))
        self.assertEqual(res["days_until"], (date(2027, 5, 10) - ref).days)
        self.assertFalse(res["is_today"])

    def test_birthday_is_today(self):
        birth = date(1995, 10, 26)
        ref = date(2026, 10, 26)
        res = get_next_birthday(birth, ref)
        self.assertEqual(res["next_birthday"], date(2026, 10, 26))
        self.assertEqual(res["days_until"], 0)
        self.assertTrue(res["is_today"])

    def test_leap_day_baby_next_birthday(self):
        # Born on Feb 29, 2000; Reference date is 26-10-2026
        birth = date(2000, 2, 29)
        ref = date(2026, 10, 26)
        res = get_next_birthday(birth, ref)
        # Next annual observation in 2027 (non-leap) is 28-02-2027
        self.assertEqual(res["next_birthday"], date(2027, 2, 28))
        self.assertTrue(res["is_leap_adjusted"])
        # Next actual leap birthday is in 2028 (2028-02-29)
        self.assertEqual(res["next_leap_birthday"], date(2028, 2, 29))
        self.assertEqual(res["days_until_leap_birthday"], (date(2028, 2, 29) - ref).days)


class TestDaysBetween(unittest.TestCase):
    """Test days and weeks difference calculation."""

    def test_same_day(self):
        d = date(2026, 10, 26)
        res = days_between(d, d)
        self.assertEqual(res["total_days"], 0)
        self.assertEqual(res["weeks"], 0)
        self.assertEqual(res["remaining_days"], 0)
        self.assertTrue(res["is_same_day"])

    def test_chronological_order(self):
        d1 = date(2026, 10, 26)
        d2 = date(2026, 11, 5)
        res = days_between(d1, d2)
        self.assertEqual(res["total_days"], 10)
        self.assertEqual(res["weeks"], 1)
        self.assertEqual(res["remaining_days"], 3)
        self.assertTrue(res["is_chronological"])

    def test_inverted_order_gives_absolute_difference(self):
        d1 = date(2026, 11, 5)
        d2 = date(2026, 10, 26)
        res = days_between(d1, d2)
        self.assertEqual(res["total_days"], 10)
        self.assertEqual(res["weeks"], 1)
        self.assertEqual(res["remaining_days"], 3)
        self.assertFalse(res["is_chronological"])

    def test_across_leap_year(self):
        # 2024 is a leap year (366 days)
        d1 = date(2024, 1, 1)
        d2 = date(2025, 1, 1)
        res = days_between(d1, d2)
        self.assertEqual(res["total_days"], 366)
        self.assertEqual(res["weeks"], 52)
        self.assertEqual(res["remaining_days"], 2)


class TestWorkingDays(unittest.TestCase):
    """Test working/business days counting with weekend and holiday deductions."""

    def test_standard_work_week(self):
        # Monday to Friday (26-10-2026 to 30-10-2026)
        start = date(2026, 10, 26)
        end = date(2026, 10, 30)
        res = working_days_between(start, end)
        self.assertEqual(res["total_calendar_days"], 5)
        self.assertEqual(res["working_days"], 5)
        self.assertEqual(res["weekend_days"], 0)

    def test_full_week_with_weekend(self):
        # Monday to Sunday (26-10-2026 to 01-11-2026)
        start = date(2026, 10, 26)
        end = date(2026, 11, 1)
        res = working_days_between(start, end)
        self.assertEqual(res["total_calendar_days"], 7)
        self.assertEqual(res["working_days"], 5)
        self.assertEqual(res["weekend_days"], 2)

    def test_weekday_holiday_deduction(self):
        start = date(2026, 10, 26)  # Monday
        end = date(2026, 10, 30)    # Friday
        holidays = [date(2026, 10, 28)]  # Wednesday is holiday
        res = working_days_between(start, end, holidays)
        self.assertEqual(res["working_days"], 4)
        self.assertEqual(len(res["holidays_on_weekdays"]), 1)

    def test_weekend_holiday_not_double_deducted(self):
        start = date(2026, 10, 26)  # Monday
        end = date(2026, 11, 1)     # Sunday
        # Saturday Oct 31 is entered as a holiday
        holidays = [date(2026, 10, 31)]
        res = working_days_between(start, end, holidays)
        self.assertEqual(res["total_calendar_days"], 7)
        self.assertEqual(res["weekend_days"], 2)
        self.assertEqual(res["working_days"], 5)  # Still 5, not 4!
        self.assertEqual(len(res["holidays_on_weekends"]), 1)
        self.assertEqual(len(res["holidays_on_weekdays"]), 0)

    def test_inverted_start_and_end(self):
        start = date(2026, 10, 30)
        end = date(2026, 10, 26)
        res = working_days_between(start, end)
        self.assertTrue(res["is_inverted"])
        self.assertEqual(res["working_days"], 5)

    def test_same_day_working_day(self):
        # Monday
        mon = date(2026, 10, 26)
        res_mon = working_days_between(mon, mon)
        self.assertEqual(res_mon["working_days"], 1)
        self.assertEqual(res_mon["weekend_days"], 0)

        # Saturday
        sat = date(2026, 10, 31)
        res_sat = working_days_between(sat, sat)
        self.assertEqual(res_sat["working_days"], 0)
        self.assertEqual(res_sat["weekend_days"], 1)


class TestAddSubtractDays(unittest.TestCase):
    """Test date projection with positive and negative day deltas."""

    def test_add_positive_days(self):
        base = date(2026, 10, 26)
        res = add_subtract_days(base, 10)
        self.assertEqual(res["result_date"], date(2026, 11, 5))
        self.assertEqual(res["weekday"], "Thursday")

    def test_subtract_days(self):
        base = date(2026, 10, 26)
        res = add_subtract_days(base, -10)
        self.assertEqual(res["result_date"], date(2026, 10, 16))
        self.assertEqual(res["weekday"], "Friday")

    def test_leap_year_boundary(self):
        base = date(2024, 2, 28)
        res = add_subtract_days(base, 1)
        self.assertEqual(res["result_date"], date(2024, 2, 29))

    def test_year_boundary_crossing(self):
        base = date(2026, 12, 31)
        res = add_subtract_days(base, 1)
        self.assertEqual(res["result_date"], date(2027, 1, 1))


class TestFormatDateTime(unittest.TestCase):
    """Test multi-format date/time outputs."""

    def test_formats_generation(self):
        sample_dt = datetime(2026, 10, 26, 14, 30, 45)
        formats = format_date_time(sample_dt)
        format_map = {desc: val for desc, _, val in formats}

        self.assertEqual(format_map["Standard Date (Indian/British)"], "26-10-2026")
        self.assertEqual(format_map["ISO 8601 (International)"], "2026-10-26")
        self.assertEqual(format_map["US Format"], "10/26/2026")
        self.assertEqual(format_map["Full Written Date"], "26 October 2026")
        self.assertEqual(format_map["Day and Abbreviated Date"], "Monday, 26 Oct 2026")
        self.assertEqual(format_map["Complete Long Date"], "Monday, October 26, 2026")
        self.assertEqual(format_map["24-Hour Military Time"], "14:30:45")
        self.assertEqual(format_map["12-Hour Time with AM/PM"], "02:30:45 PM")


if __name__ == "__main__":
    unittest.main()
