import json
import sqlite3
import time

import lxml
import sqlalchemy
from googletrans import Translator

import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml.html.clean import Cleaner
from io import StringIO

from lxml.html import document_fromstring

from flask_app.app import db, Article, ArticleFakeChecker2

MAIN_URL = "https://www.segodnya.ua/allnews.html"
MAIN_URL_PAGE_FROM2 = "https://www.segodnya.ua/allnews/p"
BASE_URL = "https://www.segodnya.ua/"

# cleaner = Cleaner(
#     javascript=True,
#     comments=True,  # True = remove comments
#     meta=True,  # True = remove meta tags
#     scripts=True,  # True = remove script tags
#     embedded=True,  # True = remove embeded tags
# )

cleaner = Cleaner()
cleaner.javascript = True  # This is True because we want to activate the javascript filter
cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter


def parse_main_pages():
    try:
        last_article = db.session.query(Article).order_by(Article.id.desc()).first()
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
            url = MAIN_URL_PAGE_FROM2 + str(n_page) + '.html'

        html_page = requests.get(url,
                                 headers={
                                     "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0)"
                                                   "Gecko/20100101 Firefox/74.0"}).text

        soup = BeautifulSoup(html_page, 'html.parser')
        soup = soup.find_all("div", {"class": "st__news-list"})
        all_articles = soup[0].find_all("li", {"class": ""})
        all_articles2 = soup[0].find_all("li", {"class": "st__news  st__hot-news_with-photo"})
        all_articles3 = soup[0].find_all("li", {"class": "st__news st__news_with-photo"})
        for li_link_article in all_articles2:
            all_articles.append(li_link_article)

        for li_link_article2 in all_articles3:
            all_articles.append(li_link_article2)

        print("all_articles", all_articles)

        for article in all_articles:

            print()
            all_url_tag = article.find_all("a")
            # if all_url_tag is None or all_url_tag == "":

            print("all_url_tag", all_url_tag)
            try:
                url_article = all_url_tag[0].get("href")
                url_article = BASE_URL + str(url_article)
                print("url_article", url_article)

            except:
                print("CONTINUE")
                continue

            article_title, article_date, article_text = parse_article_pages(url_article)
            article_text = str(article_text).strip()
            print("article_title", article_title)
            if article_title == "":
                continue

            try:
                db.session.rollback()
                if db.session.query(Article.id).filter_by(title=article_title).scalar() is not None:
                    print("Found in db")
                    continue

            except sqlite3.IntegrityError:
                continue
            except sqlalchemy.exc.IntegrityError:
                continue

            resource = "https://euvsdisinfo.eu/"
            print("article_text", article_text)
            print("article_date", article_date)

            translator = Translator()
            try:
                src_lang = translator.translate(article_title).src
            except json.decoder.JSONDecodeError:
                time.sleep(3)
                translator = Translator()
                src_lang = translator.translate(article_title).src

            # REINITIALIZE THE API
            translator = Translator()
            try:
                translated = translator.translate(article_title, src=src_lang, dest="en")
                article_title_en = translated.text
            except Exception as e:
                print(str(e))
                article_title_en = ""

            print("article_title_en", article_title_en)
            article_text = str(article_text).strip()
            article_date = str(article_date).strip()

            new_article = Article(id=max_id,
                                              title=article_title,
                                              title_en=article_title_en,
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

        if n_page >= 700:
            flag_old_news = 1


def parse_article_pages(url):
    html_page = requests.get(url).text

    soup = BeautifulSoup(html_page, 'html.parser')

    try:
        all_h1 = soup.find_all("h1", {"class": "article__header_title"})
        title = all_h1[0].string
    except IndexError as error:
        print("error title", error)
        title = ""

    try:
        all_span = soup.find_all("p", {"class": "time"})
        date = all_span[0].string
    except IndexError as error:
        print("error date", error)
        date = ""

    try:
        all_text = soup.find_all("div", {"class": "article__body"})
        # print("all_text", all_text)
        clean_text = BeautifulSoup(str(all_text[0]), "lxml").text
        # clean_text = cleaner.clean_html(str(clean_text))
    except IndexError as error:
        print("error", error)
        clean_text = ""

    return title, date, clean_text


if __name__ == '__main__':
    parse_main_pages()
