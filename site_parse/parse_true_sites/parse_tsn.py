import json
import sqlite3
import sqlalchemy
import requests

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from bs4 import BeautifulSoup

from flask_app.app import Article, db

MAIN_URL = "https://tsn.ua/news"
MAIN_URL2 = "https://www.obozrevatel.com/ukr/main-item.htm?utm_source=obozrevatel&utm_medium=self_promo&utm_campaign=mi_header_btn"
MAIN_URL_PAGE_FROM2 = "https://tsn.ua/ajax/show-more/news?page=1"
NUMBER_PAGES = 78


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

    for url in urls_article["urls_tsn"]:
        html_page = requests.get(url,
                                 headers={
                                     "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0)"
                                                   "Gecko/20100101 Firefox/74.0"}).text
        soup = BeautifulSoup(html_page, 'html.parser')

        try:
            all_h = soup.find_all("h1", {"class": "p-name c-post-title u-uppercase js-si-title"})
            article_title = all_h[0].string
        except Exception as e:
            print(str(e))
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
            all_div = soup.find_all("div", {"class": "e-content"})
            article_text = all_div[0]
            article_text = BeautifulSoup(str(article_text).strip(), "lxml").text
            article_text = str(article_text).strip()

        except Exception as e:
            print(str(e))
            article_text = ""

        print("article_text", article_text)

        try:
            article_date = soup.find_all("time", {"class": "dt-published c-post-time"})[0].get("datetime")
            article_date = str(article_date).strip()

        except Exception as e:
            article_date = ""

        print("article_date", article_date)

        resource = "https://tsn.ua/"

        new_article = Article(id=max_id,
                              title=article_title,
                              title_en="",
                              text=article_text,
                              date=article_date,
                              resource=resource,
                              url=url)

        max_id += 1
        print("article_title_en", "")

        try:
            db.session.rollback()
            db.session.add(new_article)
            db.session.commit()
            db.session.flush()
            db.create_all()
        except sqlalchemy.exc.IntegrityError:
            continue
        except sqlalchemy.exc.DataError:
            continue


def get_html_pages():
    binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    driver = webdriver.Firefox(firefox_binary=binary,
                               executable_path=r'C:\Program Files\geckodriver-v0.26.0-win64\\geckodriver.exe')
    driver.get(MAIN_URL)

    flag_error = 0

    while flag_error != 1:
        urls_dict = dict()
        urls_dict["urls_tsn"] = []
        try:
            html = driver.page_source
            links = driver.find_elements_by_class_name('u-url.u-uid.c-post-img-wrap')

            for link in links:
                url_article = link.get_attribute('href')
                print(url_article)
                urls_dict["urls_tsn"].append(url_article)

            other_page_move = driver.find_element_by_css_selector('a.btn.btn-default.btn-lg').click()
        except Exception as e:
            flag_error = 1

        if len(urls_dict["urls_tsn"]) >= 2000:
            urls_1 = dict()
            urls_1["urls_tsn"] = urls_dict["urls_tsn"][:2000]
            with open("files_for_parse_true_sites/links_tsn_articles.json", "w", encoding="utf-8") as file:
                json.dump(urls_1, file, indent=4)

            urls_1["urls_tsn"] = urls_dict["urls_tsn"][2000:]
            with open("files_for_parse_true_sites/links_tsn_articles2.json", "w", encoding="utf-8") as file:
                json.dump(urls_1, file, indent=4)
        else:
            with open("files_for_parse_true_sites/links_tsn_articles.json", "w", encoding="utf-8") as file:
                json.dump(urls_dict, file, indent=4)

        if len(urls_dict["urls_tsn"]) >= 4000:
            break


if __name__ == '__main__':
    get_html_pages()
    parse_all_pages("files_for_parse_true_sites/links_tsn_articles.json")
    parse_all_pages("files_for_parse_true_sites/links_tsn_articles2.json")
