import json
import time

import boto3
import requests
import os
from slugify import slugify

import requests
from bs4 import BeautifulSoup

from flask_app.app import db, Article

MAIN_URL = "https://tsn.ua/news"
MAIN_URL2 = "https://www.obozrevatel.com/ukr/main-item.htm?utm_source=obozrevatel&utm_medium=self_promo&utm_campaign=mi_header_btn"
MAIN_URL_PAGE_FROM2 = "https://tsn.ua/ajax/show-more/news?page=1"
NUMBER_PAGES = 78


def cache_page(url, root_path, dir_name):
    filename = slugify(url) + ".html"
    my_cwd = os.getcwd()
    os.chdir("..")
    os.chdir("..")
    html_pages_path = os.path.join(os.getcwd(), "html_pages", dir_name)
    if filename not in os.listdir(html_pages_path):
        while True:
            try:
                r = requests.get(url)
                break
            except Exception as e:
                print(e.with_traceback())
                time.sleep(1)
        with open(os.path.join(html_pages_path, filename + ".json"), "w", encoding="utf-8") as f:
            # print(r.)
            f.write(r.text)
    with open(os.path.join(html_pages_path, filename + ".json"), "r", encoding="utf-8") as f:
        json_data = json.load(f)
        text = json_data["html"]
    os.chdir(my_cwd)

    tmp_file = os.path.join(html_pages_path, filename)
    return text


# def parse_main_pages():
#     # json_data = json.loads("{}")
#     # with open("stopfake_data.json", "w", encoding="utf-8") as file:
#     #     json.dump(json_data, file, indent=4, ensure_ascii=False)
#
#     urls_article = []
#     n_article = -1
#     try:
#         last_article = db.session.query(Article).order_by(Article.id.desc()).first()
#         max_id_pos_start = str(last_article).find("id=")
#         max_id_pos_end = str(last_article).find("title=")
#         max_id = str(last_article)[max_id_pos_start + 3: max_id_pos_end - 2]
#         max_id = int(max_id) + 1
#     except ValueError:
#         max_id = 1
#     print("max_id", max_id)
#     # db.session.query(func.max(Article.id))
#     for n_page in range(9, NUMBER_PAGES):
#         print("n_page", n_page + 1)
#         if n_page + 1 == 1:
#             url = MAIN_URL
#
#         else:
#             url = MAIN_URL_PAGE_FROM2 + str(n_page + 1) + '/'
#
#         html_page = cache_page(url, "html_pages", "html_pages_stopfake")
#         soup = BeautifulSoup(html_page, 'html.parser')
#         all_articles = soup.find_all("article")
#         flag_video = 0
#
#         # with open("stopfake_data.json", "r", encoding="utf-8") as file:
#         #     json_data = json.load(file)
#
#         for article in all_articles:
#             all_span = article.find_all("span", {"class": "post-category"})
#             # print(all_span)
#             n_article += 1
#             for span in all_span:
#                 if "Відео" in str(span):
#                     flag_video = 1
#                     break
#
#             if flag_video == 1:
#                 flag_video = 0
#                 continue
#
#             all_a = article.find_all("a")
#             url_article = all_a[0].get("href")
#             urls_article.append(url_article)
#             print()
#             article_title, article_date = parse_article_pages(url_article)
#             print("article_title", article_title)
#             if db.session.query(Article.id).filter_by(title=article_title).scalar() is not None:
#                 print("Found in db")
#                 continue
#
#             resource_end_pos = url_article.find("/uk")
#             resource = url_article[:resource_end_pos + 3]
#
#             str_n_article = str(n_article)
#             # json_data[str_n_article] = {}
#             # json_data[str_n_article]["title"] = article_title
#             # json_data[str_n_article]["date"] = article_date
#             # json_data[str_n_article]["url_article"] = url_article
#             new_article = Article(id=max_id,
#                                   title=article_title,
#                                   date=article_date,
#                                   resource=resource,
#                                   url=url_article)
#
#             max_id += 1
#
#             db.session.add(new_article)
#             db.session.flush()
#
#         db.session.commit()
#
#         # with open("stopfake_data.json", "w", encoding="utf-8") as file:
#         #     json.dump(json_data, file, indent=4, ensure_ascii=False)
#
#
# def parse_article_pages(url):
#     html_page = cache_page(url, "html_pages", os.path.join("html_pages_stopfake",
#                                                            "html_stopfake_articles"))
#     soup = BeautifulSoup(html_page, 'html.parser')
#
#     all_h1 = soup.find_all("h1", {"class": "entry-title"})
#     title = all_h1[0].string
#
#     all_span = soup.find_all("span", {"class": "post-date date updated"})
#     date = all_span[0].string
#
#     return title, date


if __name__ == '__main__':
    print(cache_page(MAIN_URL2, "html_pages", "html_pages_tsn"))
