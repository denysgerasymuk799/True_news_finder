"""
Libraries for reform all date in special form
"""
import datetime
import re
from datetime import datetime

from sqlalchemy import desc

from flask_app.app import Article, ArticleFakeChecker2, db
from prepare_data.transform_date import transform_date


def create_date_form(table_name, start_id, finish_id):
    """

    :param table_name: a name of database table
    :param start_id: int
    :param finish_id: int
    :return: reformed dates and add in database
    """
    for article_id in range(start_id, finish_id):
        print("article_id", article_id)
        article_from_db = ''
        if table_name == "ArticleFakeChecker2":
            article_from_db = ArticleFakeChecker2.query.filter_by(id=article_id).first()

        elif table_name == "Article":
            article_from_db = Article.query.filter_by(id=article_id).first()

        if article_from_db is not None:
            date = str(article_from_db.date)
            date_object = transform_date(date)

            date_object = date_object.strip()
            if not re.match(r"^((19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[1-9]|[12][0-9]|3[01]))$", date_object):
                print("date_object", date_object)
                if date_object == "2020-0":
                    date_object = "2020-01-10"

                elif date_object == "2020-":
                    date_object = "2020-01-01"

                elif date_object.endswith("-0"):
                    print("make correct -0")
                    date_object += "1"

                elif date_object.endswith("-"):
                    print("make correct -")
                    date_object += "01"

                elif date_object.count("-") == 1:
                    print("make correct 1 -")
                    date_object += "-10"

                else:
                    date_object = "2019-10-10"
                print("date_object2222", date_object)
                print()

            article_from_db.date = date_object
            print("result", date_object)
            print()
            db.session.commit()


if __name__ == '__main__':
    # create_date_form("Article", 42000, 42900)
    # entities = Article.query.order_by(desc(Article.time)).limit(3).all()
    # entities2 = Article.query.order_by(desc(Article.date)).limit(1000).all()
    # print(entities2)
    date_string2 = "16:05, 14.11.2019"
    date_string3 = "2020-05-14T19:11:00+03:00"
    date_string = "Грудень, 06, 2019 о 14:12"
    date1 = "Травень, 08 в 8:56"
    date2 = "29 Квітня, 2020 - 19:09"
    date2 = "October 03, 2019"
    print(transform_date(date_string2))
    print(transform_date(date_string3))
    print(transform_date(date_string))
    print(transform_date(date1))
    print(transform_date(date2))
