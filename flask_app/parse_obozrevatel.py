import json
import sqlite3
import time

import sqlalchemy
# from googletrans import Translator
# from slugify import slugify
# from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date

# from flask_app.app import db, Article
from app import Article, db
from googletrans import Translator

# from site_parse.parse_true_sites.parse_tsn import translate_title

MAIN_URL = "https://www.obozrevatel.com/main-item.htm?utm_source=obozrevatel&utm_medium=self_promo&utm_campaign=mi_header_btn"
MAIN_URL2 = "https://www.obozrevatel.com/main-item/"


def translate_title(article_title):
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

    return article_title_en


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def parse_all_pages(filename):
    with open(filename, "r", encoding="utf-8") as file:
        urls_article = json.load(file)

    try:
        last_article = db.session.query(Article).order_by(Article.id.desc()).first()
        max_id_pos_start = str(last_article).find("id=")
        max_id_pos_end = str(last_article).find("title=")
        max_id = str(last_article)[max_id_pos_start + 3: max_id_pos_end - 2]
        max_id = int(max_id) + 1
    except ValueError:
        max_id = 1
    print("max_id", max_id)

    # i = 0
    for url in urls_article["urls_explorer"]:
        html_page = requests.get(url,
                                 headers={
                                     "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0)"
                                                   "Gecko/20100101 Firefox/74.0"}, verify=False).text
        soup = BeautifulSoup(html_page, 'html.parser')

        try:
            all_h = soup.find_all("h1", {"class": "news-full__title"})
            article_title = all_h[0].string
            article_title = str(article_title).strip()
        except:
            continue
        print()
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

        try:
            all_div = soup.find_all("div", {"class": "news-full__text io-article-body"})
            article_text = all_div[0]
            article_text = BeautifulSoup(str(article_text).strip(), "lxml").text
            article_text = str(article_text).strip()

        except:
            article_text = ""

        print("article_text", article_text)

        try:
            article_date = soup.find_all("time", {"class": "news-full__date--create"})[0].string
            article_date = str(article_date).strip()

        except:
            article_date = ""

        print("article_date", article_date)
        resource = "https://www.obozrevatel.com/"

        if article_title != "":
            article_title_en = translate_title(article_title)
        else:
            article_title_en = ""

        new_article = Article(id=max_id,
                              title=article_title,
                              title_en=article_title_en,
                              text=article_text,
                              date=article_date,
                              resource=resource,
                              url=url)

        max_id += 1
        print("article_title_en", article_title_en)

        # i += 1
        # if i == 5:
        #     break

        try:
            db.session.add(new_article)
            db.session.rollback()
            db.session.commit()
            db.session.flush()
            db.create_all()
        except sqlalchemy.exc.IntegrityError:
            continue
        except sqlalchemy.exc.DataError:
            continue


def get_html_pages(url_main, driver, urls_dict):
    driver.get(url_main)

    flag_error = 0

    i = 0
    while flag_error != 1:
        i += 1
        print("n_page_scroll", i)

        # try:
        driver.execute_script("window.scrollTo(0,  document.body.scrollHeight)")
        driver.implicitly_wait(5)
        if i == 500:
            links = driver.find_elements_by_class_name('news-title-img-text__title')

            for link in links:
                url_article = link.get_attribute('href')
                print(url_article)
                urls_dict["urls_explorer"].append(url_article)

            break
        #
        # if i == 5:
        #     break

    return urls_dict


# def parse_all_main_pages():
#     binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
#     driver = webdriver.Firefox(firefox_binary=binary,
#                                executable_path=r'C:\Program Files\geckodriver-v0.26.0-win64\\geckodriver.exe')
#     start_date = date(2019, 1, 1)
#     end_date = date(2020, 5, 14)
#
#     urls_dict = dict()
#     urls_dict["urls_explorer"] = []
#     get_html_pages(MAIN_URL, driver, urls_dict)
#
#     for n_main_page, single_date in enumerate(daterange(start_date, end_date)):
#         print("n_main_page", n_main_page)
#         date_page = single_date.strftime("%d-%m-%Y")
#         url_main = MAIN_URL2 + date_page + ".htm"
#         urls_dict = get_html_pages(url_main, driver, urls_dict)
#
#         if len(urls_dict["urls_explorer"]) >= 2000:
#             urls_1 = dict()
#             urls_1["urls_explorer"] = urls_dict["urls_explorer"][:2000]
#             with open("links_explorer_articles.json", "w", encoding="utf-8") as file:
#                 json.dump(urls_1, file, indent=4)
#
#             if len(urls_dict["urls_explorer"]) <= 4000:
#                 urls_1["urls_explorer"] = urls_dict["urls_explorer"][2000:]
#                 with open("links_explorer_articles2.json", "w", encoding="utf-8") as file:
#                     json.dump(urls_1, file, indent=4)
#
#             elif 4000 < len(urls_dict["urls_explorer"]):
#                 urls_1["urls_explorer"] = urls_dict["urls_explorer"][2000:4000]
#                 with open("links_explorer_articles2.json", "w", encoding="utf-8") as file:
#                     json.dump(urls_1, file, indent=4)
#
#                 urls_1["urls_explorer"] = urls_dict["urls_explorer"][4000:]
#                 with open("links_explorer_articles3.json", "w", encoding="utf-8") as file:
#                     json.dump(urls_1, file, indent=4)
#
#         else:
#             with open("links_explorer_articles.json", "w", encoding="utf-8") as file:
#                 json.dump(urls_dict, file, indent=4)
#
#         if len(urls_dict["urls_explorer"]) >= 5000:
#             break


if __name__ == '__main__':
    # parse_all_main_pages()
    parse_all_pages("links_explorer_articles.json")
    parse_all_pages("links_explorer_articles2.json")
    parse_all_pages("links_explorer_articles3.json")
