import sqlite3

import sqlalchemy

import requests
from bs4 import BeautifulSoup

from app import db, Article, ArticleFakeChecker2

MAIN_URL = "https://euvsdisinfo.eu/news/"
MAIN_URL_PAGE_FROM2 = "https://euvsdisinfo.eu/news/page/"


def parse_main_pages():
    try:
        last_article = db.session.query(ArticleFakeChecker2).order_by(ArticleFakeChecker2.id.desc()).first()
        max_id_pos_start = str(last_article).find("id=")
        max_id_pos_end = str(last_article).find("title=")
        max_id = str(last_article)[max_id_pos_start + 3: max_id_pos_end - 2]
        max_id = int(max_id) + 1
    except ValueError:
        max_id = 1

    print("max_id", max_id)
    flag_old_news = 0
    n_page = 0
    while flag_old_news != 1:
        n_page = n_page + 1
        article_date = ""
        print("n_page", n_page)
        if n_page == 1:
            url = MAIN_URL

        else:
            url = MAIN_URL_PAGE_FROM2 + str(n_page + 1) + '/'

        html_page = requests.get(url,
                                 headers={
                                     "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0)"
                                                   "Gecko/20100101 Firefox/74.0"}, verify=False).text

        soup = BeautifulSoup(html_page, 'html.parser')
        all_articles = soup.find_all("a", {"class": "b-post__link"})

        for article in all_articles:

            print()
            url_article = article.get("href")

            article_title, article_date, article_text = parse_article_pages(url_article)
            article_text = str(article_text).strip()
            print("article_title", article_title)
            try:
                db.session.rollback()
                if db.session.query(ArticleFakeChecker2.id).filter_by(title=article_title).scalar() is not None:
                    print("Found in db")
                    continue

            except sqlite3.IntegrityError:
                continue
            except sqlalchemy.exc.IntegrityError:
                continue

            resource = "https://euvsdisinfo.eu/"
            print("article_text", article_text)
            print("article_date", article_date)

            new_article = ArticleFakeChecker2(id=max_id,
                                              title=article_title,
                                              title_en=article_title,
                                              text=article_text,
                                              date=article_date,
                                              resource=resource,
                                              url=url_article)

            max_id += 1

            try:
                db.session.add(new_article)
                db.session.commit()
                db.session.flush()
                db.create_all()
            except sqlalchemy.exc.IntegrityError:
                continue
            except sqlalchemy.exc.DataError:
                continue

        if str(article_date).split(", ")[-1].strip() == "2018" or n_page >= 700:
            flag_old_news = 1

        try:
            db.session.rollback()
            db.session.commit()
            db.create_all()
        except sqlalchemy.exc.IntegrityError:
            continue


def parse_article_pages(url):
    html_page = requests.get(url).text

    soup = BeautifulSoup(html_page, 'html.parser')

    try:
        all_title = soup.find_all("h1", {"class": "entry-title"})
        title = BeautifulSoup(str(all_title[0]), "lxml").text
    except IndexError as error:
        print("error", error)
        title = ""

    try:
        all_span = soup.find_all("span", {"class": "et_pb_post_date"})
        date = BeautifulSoup(str(all_span[0]), "lxml").text
    except IndexError as error:
        print("error", error)
        date = ""

    try:
        all_text = soup.find_all("div", {"class": "entry-content"})
        clean_text = BeautifulSoup(str(all_text[0]), "lxml").text
    except IndexError as error:
        print("error", error)
        clean_text = ""

    return title, date, clean_text


if __name__ == '__main__':
    parse_main_pages()
