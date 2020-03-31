import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from pprint import pprint

import boto3
import requests
from bs4 import BeautifulSoup
from slugify import slugify


def dir_for_save_html(dir_name):
    """

    :param dir_name: a name of directory to save
    :return: a root path for html pages
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    root_path = os.path.join(os.getcwd(), "html_pages", dir_name, timestamp).replace("\\", "/")
    return root_path


def cache_page(url, root_path, site_parse_name):
    """

    :param url: str
    :param root_path: str
    :param site_parse_name: str
    :return: cache page to parse in later
    """
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://fra1.digitaloceanspaces.com',
                            aws_access_key_id='4X7VNYMKWLTZV5G5JXEV',
                            aws_secret_access_key='dmifQIBG5a8hzPcBXsohAnDeJCfMrY2W5ryOE87U1fE')

    filename = slugify(url) + ".html"
    temp_directory = Path(os.path.join(os.path.join(os.getcwd(), 'html_pages', site_parse_name)))
    temp_directory.mkdir(exist_ok=True)
    html_pages_path = os.path.join(os.path.join(os.path.join(os.getcwd(), 'html_pages'),
                                                site_parse_name))
    if filename not in os.listdir(html_pages_path):
        while True:
            try:
                r = requests.get(url)
                break
            except Exception as e:
                print(e.with_traceback())
                time.sleep(1)
        with open(os.path.join(html_pages_path, filename), "w", encoding="utf-8") as f:
            f.write(r.text)
    with open(os.path.join(html_pages_path, filename), encoding="utf-8") as f:
        text = f.read()

    tmp_file = os.path.join(html_pages_path, filename)
    client.upload_file(tmp_file, 'ai-scrapper', os.path.join(root_path, filename).replace("\\", "/"))
    return text


def clean_html(raw_html):
    """

    :param raw_html: str
    :return: clean the raw from tags
    """
    clean_raw = re.compile('<.*?>')
    clean_text = re.sub(clean_raw, '', raw_html)
    return clean_text


def parse_course_pages(url, table):
    """

    :param url: str
    :param table: a dict to save parsed information
    :return: a dict with parsed information
    """
    html_page = cache_page(url, os.getcwd(), 'html_pages_ictv')

    soup = BeautifulSoup(html_page, 'html.parser')

    # today_news in json
    try:
        all_main_today_news = soup.find_all("div", {"class": "fn_list_wrap"})
        all_main_today_news_a = all_main_today_news[0].find_all("a")
        for num, news_a0 in enumerate(all_main_today_news_a):
            news_dict = dict()
            news_a = str(news_a0)
            start_link = news_a.find('http')
            end_link = news_a.find('">')
            news_dict['link'] = news_a[start_link: end_link]

            news_dict['news'] = clean_html(news_a)
            table['today_news' + str(num + 1)] = news_dict
    except:
        pass

    return table


def find_today_news(url):
    """

    :param url: a url to parse
    :return: a dictionary with parsed today's news
    """
    today_news_dict = dict()
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")

    root_path = os.path.join('html_pages', timestamp).replace("\\", "/")

    today_news_dict = parse_course_pages(url, today_news_dict)
    pprint(today_news_dict)
    # with open(os.path.join(os.getcwd(), 'facty_ictv_today_news', 'facty_main_today_news' + str(now) + '.json'), "w",
    #           encoding="utf-8") as f:
    #     json.dump(courses_for_profession, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    url = "https://fakty.com.ua/ua/"
    data = requests.get(url,
                        headers={
                            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0)"
                                          "Gecko/20100101 Firefox/74.0"})

    find_today_news(url)
