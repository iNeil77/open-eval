from datetime import datetime
import pytz

# Constants
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def task_func(unix_timestamp, target_timezone):
    """
    Converts a Unix timestamp to a formatted date and time string in a specified timezone.

    Parameters:
    unix_timestamp (int): The Unix timestamp representing the number of seconds since the Unix Epoch (January 1, 1970, 00:00:00 UTC).
    target_timezone (str): The string identifier of the target timezone (e.g., 'America/New_York').

    Returns:
    str: A string representing the date and time in the target timezone, formatted as '%Y-%m-%d %H:%M:%S'.

    Requirements:
    - datetime.datetime
    - pytz

    Example:
    >>> unix_timestamp = 1609459200
    >>> target_timezone = 'America/New_York'
    >>> task_func(unix_timestamp, target_timezone)
    '2020-12-31 19:00:00'
    """
    datetime_utc = datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=pytz.utc)
    datetime_in_target_timezone = datetime_utc.astimezone(pytz.timezone(target_timezone))
    formatted_datetime = datetime_in_target_timezone.strftime(DATE_FORMAT)
    return formatted_datetime

import unittest
class TestCases(unittest.TestCase):
    def test_case_1(self):
        result = task_func(1347517370, 'America/New_York')
        self.assertEqual(result, "2012-09-13 02:22:50")
    def test_case_2(self):
        result = task_func(0, 'UTC')
        self.assertEqual(result, "1970-01-01 00:00:00")
    def test_case_3(self):
        result = task_func(1609459200, 'Asia/Tokyo')
        self.assertEqual(result, "2021-01-01 09:00:00")
    def test_case_4(self):
        result = task_func(0, 'Asia/Kolkata')
        self.assertEqual(result, "1970-01-01 05:30:00")
    def test_case_5(self):
        result = task_func(1672531199, 'Australia/Sydney')
        self.assertEqual(result, "2023-01-01 10:59:59")
    def test_case_6(self):
        result = task_func(1609459200, 'America/New_York')
        self.assertEqual(result, "2020-12-31 19:00:00")
