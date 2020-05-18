import datetime
import re
from datetime import datetime

from sqlalchemy import desc

from flask_app.app import Article, ArticleFakeChecker2, db
from flask_app.data_structures.linked_list import LinkedList
from site_parse.parse_true_sites.parse_tsn import translate_title


def transform_date(date_string):
    try:
        if re.match(r"[A-z]", date_string[0]):
            try:
                date = str(datetime.strptime(date_string, "%B %d, %Y")).split()[0]

            except ValueError:
                date = "2020-04-01"

        elif re.match(r"[A-я]", date_string[0]) or not date_string[3].isdigit():
            en_months = ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"]

            ua_months = ["січень", "лютий", "березень", "квітень", "травень", "червень",
                         "липень", "серпень", "вересень", "жовтень", "листопад", "грудень"]

            ru_months = ["январь", "февраль", "март", "апрель", "май", "июнь",
                         "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]

            # if re.match(r"[A-я]", date_string[0]):
            #     date = str(date_string).split()[:-2]
            # else:
            #     end_date = date_string.find("-")
            #     date = date_string[:end_date].strip().split()
            #     print("date_string =", date_string)

            date = str(date_string).split()[:-2]
            print("date", date)

            try:
                month = date[1][:3].lower()
            except IndexError:
                date = str(date_string).split()[:-1]
                month = date[1][:3].lower()

            month_index = 0
            if re.match(r"[A-я]", date_string[0]):
                month = date[0][:3].lower()

            flag_find_month = 0
            for i in range(len(ua_months)):
                if ua_months[i][:3] == month:
                    month_index = i
                    flag_find_month = 1
                    break

            if flag_find_month != 1:
                month = date[1][:3].lower()

                for i in range(len(ru_months)):
                    if ru_months[i][:3] == month:
                        month_index = i
                        break

            if re.match(r"[A-я]", date_string[0]):
                date[0] = en_months[month_index]

                if "2020" not in date_string and "2019" not in date_string and \
                        "2019" not in date_string:
                    date.append("2020")
                    date = " ".join(date)

                    date = str(datetime.strptime(date, "%B  %d %Y")).split()[0]
                else:
                    date = " ".join(date)
                    print(date)

                    date = str(datetime.strptime(date, "%B  %d, %Y")).split()[0]

            else:
                date[1] = en_months[month_index]

                if "2020" not in date_string and "2019" not in date_string and \
                        "2019" not in date_string:
                    date.append("2020")

                date = " ".join(date)
                print(date)

                date = str(datetime.strptime(date, "%d %B %Y")).split()[0]

        elif date_string[:4] == "2020" or date_string[:4] == "2019" or date_string[:4] == "2018":
            print("2020")
            date = date_string[:date_string.find("T")]

        else:
            date = date_string.split(",")[1]
            date = date.split(".")
            date[0] = date[0].strip()
            date[2], date[0] = date[0], date[2]
            date = "-".join(date)
            date = date.strip()
        return date

    except:
        print("ERROR_____________________")
        return date_string


def create_date_form(table_name):
    n_articles = 100
    if table_name == "ArticleFakeChecker2":
        # last_article = db.session.query(ArticleFakeChecker2).order_by(ArticleFakeChecker2.id.desc()).first()
        n_articles = 926

    elif table_name == "Article":
        last_article = db.session.query(Article).order_by(Article.id.desc()).first()
        n_articles = 42169

    for article_id in range(42000, 42900):
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
                    print("1 -0")
                    date_object += "1"

                elif date_object.endswith("-"):
                    print("0 -")
                    date_object += "01"

                elif date_object.count("-") == 1:
                    print("1 -")
                    date_object += "-10"

                else:
                    date_object = "2019-10-10"
                print("date_object2222", date_object)
                # print(article_from_db)
                print()
            # if table_name == "Article":
            #     article_title = article_from_db.title
            #     print(translate_title(article_title))

            article_from_db.date = date_object
            # print("result", date_object)
            print()
            db.session.commit()


if __name__ == '__main__':
    # create_date_form("Article")
    # date_string2 = "16:05, 14.11.2019"
    # date_string3 = "2020-05-14T19:11:00+03:00"
    # date_string = "Грудень, 06, 2019 о 14:12"
    # date1 = "Травень, 08 в 8:56"
    # date2 = "29 Квітня, 2020 - 19:09"
    # date2 = "October 03, 2019"
    # print(transform_date(date_string2))
    # print(transform_date(date_string3))
    # print(transform_date(date_string))
    # print(transform_date(date1))
    # print(transform_date(date2))
    # entities = Article.query.order_by(desc(Article.time)).limit(3).all()
    entities2 = Article.query.order_by(desc(Article.date)).limit(1000).all()
    print(entities2)
