import unittest

from prepare_data.create_date_filtering import transform_date


class TestDate(unittest.TestCase):
    """class to test the main functions of class Flower"""

    def setUp(self):
        """Set up different examples to attributes to detect error"""
        self.date1 = "16:05, 14.11.2019"
        self.date2 = "2020-05-14T19:11:00+03:00"
        self.date3 = "Грудень, 06, 2019 о 14:12"
        self.date4 = "Травень, 08 в 8:56"
        self.date5 = "29 Квітня, 2020 - 19:09"
        self.date6 = "October 03, 2019"

    def test_transform_date(self):
        """Test type of attributes, which class has"""

        self.assertEqual(transform_date(self.date1), "2019-11-14",
                         'Problem with recognizing date form from tsn.ua')
        self.assertEqual(transform_date(self.date2), "2020-05-14",
                         'Problem with recognizing date form from ictv')
        self.assertEqual(transform_date(self.date3), "2019-12-06",
                         'Problem with recognizing date form from obozrevatel')
        self.assertEqual(transform_date(self.date4), "2020-05-08",
                         'Problem with recognizing date form from eudisinfo')
        self.assertEqual(transform_date(self.date5), "2020-04-29",
                         'Problem with recognizing date form from tsn.ua')
        self.assertEqual(transform_date(self.date6), "2019-10-03",
                         'Problem with recognizing date form from stopfake')
