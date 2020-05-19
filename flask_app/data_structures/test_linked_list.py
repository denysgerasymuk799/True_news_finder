import copy
import unittest

from flask_app.data_structures.linked_list import LinkedList


class TestLinked(unittest.TestCase):
    """class to test the main functions of class Flower"""

    def setUp(self):
        """Set up different examples to attributes to detect error"""

        text1 = """Контрольно-пропускной пункт "Шегини" в Мостицком районе Львовской области (на границе с Польшей)
         возобновит свою работу. Такое решение было принято сегодня"""
        text2 = """At least 6 of Madagascar’s presidential candidates were offered money by Russians"""

        same_articles = LinkedList("h1",
                                   "2020-01-1",
                                   0.01,
                                   "https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg",
                                   "https://tsn.ua/",
                                   text1)
        same_articles.add("h2",
                          "2020-01-01",
                          0.011,
                          "https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg",
                          "https://fakty.com.ua/ua",
                          text2)

        same_articles.add("h3",
                          "2020-03-1",
                          0.03,
                          "https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg",
                          "https://fakty.com.ua/ua",
                          text2)

        same_articles.add("h3",
                          "2019-01-1",
                          0.03,
                          "https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg",
                          "https://fakty.com.ua/ua",
                          text2)

        same_articles.add("h3",
                          "2020-9-1",
                          -0.03,
                          "https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg",
                          "https://fakty.com.ua/ua",
                          text2)

        self.same_articles = copy.deepcopy(same_articles)

    def test_sort(self):
        """Test type of attributes, which class has"""
        self.same_articles.int_head = self.same_articles.merge_sort(self.same_articles.int_head, "similarity")
        self.assertEqual(repr(self.same_articles),
                         """{
1:(
    "title": h3,
    "date": 2020-03-1,
    "similarity": 0.03,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://fakty.com.ua/ua
),
2:(
    "title": h3,
    "date": 2019-01-1,
    "similarity": 0.03,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://fakty.com.ua/ua
),
3:(
    "title": h2,
    "date": 2020-01-01,
    "similarity": 0.011,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://fakty.com.ua/ua
),
4:(
    "title": h1,
    "date": 2020-01-1,
    "similarity": 0.01,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://tsn.ua/
),
5:(
    "title": h3,
    "date": 2020-9-1,
    "similarity": -0.03,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://fakty.com.ua/ua
)
}""",
                         'Problem with merge_sort by similarity')

        self.same_articles.int_head = self.same_articles.merge_sort(self.same_articles.int_head, "date")
        self.assertEqual(repr(self.same_articles),
                         """{
1:(
    "title": h3,
    "date": 2020-9-1,
    "similarity": -0.03,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://fakty.com.ua/ua
),
2:(
    "title": h3,
    "date": 2020-03-1,
    "similarity": 0.03,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://fakty.com.ua/ua
),
3:(
    "title": h2,
    "date": 2020-01-01,
    "similarity": 0.011,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://fakty.com.ua/ua
),
4:(
    "title": h1,
    "date": 2020-01-1,
    "similarity": 0.01,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://tsn.ua/
),
5:(
    "title": h3,
    "date": 2019-01-1,
    "similarity": 0.03,
    "url": https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg,
    "resource": https://fakty.com.ua/ua
)
}""", "Problem with merge_sort by date")
