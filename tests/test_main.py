import unittest
from datetime import datetime, timedelta

from denton import main

from . import eq_


class TestInterpolate_date(unittest.TestCase):
    def test_today(self):
        data = [
            ('', ''),
            ('%Y-%m-%d', datetime.now().strftime('%Y-%m-%d'))
        ]
        for text, expected in data:
            eq_(main.interpolate_date(text), expected)

    def test_another_day(self):
        date = datetime.now() - timedelta(days=7)

        data = [
            ('', ''),
            ('%Y-%m-%d', date.strftime('%Y-%m-%d'))
        ]
        for text, expected in data:
            eq_(main.interpolate_date(text, date=date), expected)
