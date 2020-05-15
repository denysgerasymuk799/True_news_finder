import json
import sqlite3
import time

import sqlalchemy
from googletrans import Translator

import requests
from bs4 import BeautifulSoup

from app import db, Article

MAIN_URL = "https://fakty.com.ua/ua/news/"
MAIN_URL_PAGE_FROM2 = "https://fakty.com.ua/ua/news/page/"
NUMBER_PAGES = 1000


def parse_main_pages():
    try:
        last_article = db.session.query(Article).order_by(Article.id.desc()).first()
        max_id_pos_start = str(last_article).find("id=")
        max_id_pos_end = str(last_article).find("title=")
        max_id = str(last_article)[max_id_pos_start + 3: max_id_pos_end - 2]
        max_id = int(max_id) + 1
    except ValueError:
        max_id = 1

    urls_article = []
    n_article = -1

    print("max_id", max_id)
    for n_page in range(20, NUMBER_PAGES):
        print("n_page", n_page + 1)
        if n_page + 1 == 1:
            url = MAIN_URL

        else:
            url = MAIN_URL_PAGE_FROM2 + str(n_page + 1) + '/'

        stop_requests = 0
        flag_bad_request_for_page = 0

        while str(requests.get(url,
                               headers={
                                   "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0)"
                                                 "Gecko/20100101 Firefox/74.0"})).strip() != "<Response [200]>":
            time.sleep(3)
            stop_requests += 1
            if stop_requests == 10:
                print()
                print("error!!!!!!!!!!!!!!!", requests.get(url))
                flag_bad_request_for_page = 1
                break

        if flag_bad_request_for_page == 1:
            continue

        html_page = requests.get(url,
                                 headers={
                                     "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0)"
                                                   "Gecko/20100101 Firefox/74.0"}).text
        soup = BeautifulSoup(html_page, 'html.parser')
        # all_articles = soup.find_all("article")
        # # flag_video = 0
        #
        # for article in all_articles:
        all_span = soup.find_all("a", {"class": "lbn_link"})
        n_article += 1
        for span in all_span:
            # print("span", span)
            if "Відео" in str(span):
                # flag_video = 1
                # break
                continue
            #
            # if flag_video == 1:
            #     flag_video = 0
            #     continue
            # all_a = article.find_all("a")
            url_article = span.get("href")
            print()
            article_title, article_date, article_text = parse_article_pages(url_article)
            article_text = str(article_text).strip()
            print("article_title", article_title)
            try:
                db.session.rollback()
                if db.session.query(Article.id).filter_by(title=article_title).scalar() is not None:
                    print("Found in db")
                    continue

            except sqlite3.IntegrityError:
                continue
            except sqlalchemy.exc.IntegrityError:
                continue

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

            resource_end_pos = url_article.find("/ua")
            resource = url_article[:resource_end_pos + 3]
            print("article_text", article_text)

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

        try:
            db.session.rollback()
            db.session.commit()
            db.create_all()
        except sqlalchemy.exc.IntegrityError:
            continue
        # with open("stopfake_data.json", "w", encoding="utf-8") as file:
        #     json.dump(json_data, file, indent=4, ensure_ascii=False)


def parse_article_pages(url):
    html_page = requests.get(url).text

    soup = BeautifulSoup(html_page, 'html.parser')

    try:
        all_h1 = soup.find_all("h1")
        title = all_h1[0].string
    except IndexError as error:
        print("error", error)
        title = ""

    try:
        all_span = soup.find_all("time")
        date = all_span[0].string
    except IndexError as error:
        print("error", error)
        date = ""

    try:
        all_text = soup.find_all("div", {"class": "kv-post-content-text"})
        clean_text = BeautifulSoup(str(all_text[0]), "lxml").text
        end_text_pos = clean_text.find("var googletag")
        clean_text = clean_text[:end_text_pos].strip()
    except IndexError as error:
        print("error", error)
        clean_text = ""

    return title, date, clean_text


if __name__ == '__main__':
    parse_main_pages()
