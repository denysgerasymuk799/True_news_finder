"""

app.py

====================================

The core module of my example project

"""
# coding=utf8
import copy
import os
import sqlite3
import time

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob

from flask_app.get_similar_articles import cosine_sim
from flask_app.my_config import Config

from flask_app.data_structures.linked_list import LinkedList
from site_parse.translate_title import translate_title

from rq import Queue
from ..worker import conn
from ..utils import count_words_at_url

q = Queue(connection=conn)

result = q.enqueue(count_words_at_url, 'http://heroku.com')

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)

article_to_key_words = db.Table('article_to_key_words', db.Model.metadata,
                                db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                                db.Column('key_words_id', db.Integer, db.ForeignKey('article_key_word.id'))
                                )

article_fake_checker2_to_key_words = db.Table('article_fake_checker2_to_key_words', db.Model.metadata,
                                              db.Column('article_id', db.Integer,
                                                        db.ForeignKey('article_fake_checker2.id')),
                                              db.Column('key_words_id', db.Integer,
                                                        db.ForeignKey('article_key_word.id'))
                                              )


class ArticleKeyWord(db.Model):
    """
    Class for keywords of the article titles
    """
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(400), unique=False, nullable=False)
    key_words = db.Column(db.String(400), unique=False, nullable=False)

    def __repr__(self):
        return '<ArticleKeyWord id={}, title_en={}, key_words={}>'.format(self.id, self.title_en, self.key_words)


class Article(db.Model):
    """
    Class for articles
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), unique=False, nullable=False)
    title_en = db.Column(db.String(400), unique=False, nullable=False)
    text = db.Column(db.String(15000), unique=False, nullable=False)
    date = db.Column(db.String(30), unique=False, nullable=True)
    resource = db.Column(db.String(80), unique=False, nullable=True)
    url = db.Column(db.String(300), unique=False, nullable=True)
    key_words = db.relationship("ArticleKeyWord",
                                secondary=article_to_key_words)

    def __repr__(self):
        return '<Article id={}, title={}, title_en={}, text={}, date={}, resource={}, url={}>'.format(self.id,
                                                                                                      self.title,
                                                                                                      self.title_en,
                                                                                                      self.text,
                                                                                                      self.date,
                                                                                                      self.resource,
                                                                                                      self.url)


class ArticleFakeChecker2(db.Model):
    """
    Class for articles_fakecheckers
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), unique=False, nullable=False)
    title_en = db.Column(db.String(400), unique=False, nullable=False)
    text = db.Column(db.String(15000), unique=False, nullable=False)
    resource = db.Column(db.String(80), unique=False, nullable=True)
    date = db.Column(db.String(30), unique=False, nullable=True)
    url = db.Column(db.String(300), unique=False, nullable=True)
    key_words = db.relationship("ArticleKeyWord",
                                secondary=article_fake_checker2_to_key_words)

    def __repr__(self):
        return '<ArticleFakeChecker2 id={}, title={}, title_en={}, text={}, date={}, resource={}, url={}>'.format(
            self.id, self.title,
            self.title_en,
            self.text, self.date,
            self.resource, self.url)


IMAGES_DICT = {
    "https://tsn.ua/": "https://img.tsn.ua/cached/1533907550/tsn-5c161a41b1f154cd63aedacab6e94568/thumbs/1340x530/e7/99/66245e5c11cc2f5381880995ae9199e7.png",
    "https://fakty.com.ua/ua": "https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg",
    "https://euvsdisinfo.eu/": "https://www.google.com/imgres?imgurl=https%3A%2F%2Feuvsdisinfo.eu%2Fuploads%2F2018%2F01%2FImg1.jpg&imgrefurl=https%3A%2F%2Feuvsdisinfo.eu%2Fchange-of-terminology-in-the-euvsdisinfo-database%2F&tbnid=p2XjjS_sGNZy0M&vet=12ahUKEwjXh9TRorvpAhUBIX0KHSOHBJUQMygBegUIARDXAQ..i&docid=oVHhzpSthlhTaM&w=1302&h=647&q=euvsdisinfo&client=firefox-b-d&ved=2ahUKEwjXh9TRorvpAhUBIX0KHSOHBJUQMygBegUIARDXAQ",
    "https://www.stopfake.org/uk": "data:image/jpeg;base64,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ctG6IOJNgA480Ek6AkXUN3gU7anaSkpZruidHTgtvYWdLKXjszZQD2AdSyd8WzVJDQxzwU0UT2zMiPIxtjDmOZJdrg0WOrQbnX2lWwiuWTjaTa+kw5zG1T3NMwc5mWJ0lw0gG+UG3lBaul3nYXI8M8Jc0uNgZIZI2A/hOLbNHadFX28Cqzx4LNOc2elilmJGbMD4M6QkdN7nTpXO3+MYNPShmH07BPyjMroaQ09m65gTlbnvwDddSFO6MlyYti8FJCZ6iVscY0zO6SeAaBq4nqFyoxT708Le/IZ3subB0kD2s9ZtzR2myg23tJLlwWjqXOvyUUUwzahznQRvJPS4AkX9PWpXj8uz9HK2lqaaFkkPJyAR0chI1Dm3kjbzr21BJv03uowMlhMcCLjgdRbVcrqpKhssbJWG7ZWtkYbEXa4BzTY6jQhdqqWCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiALSbZY/8AU6ifV8kZOTLBlDsg5zg0FzrHK0X42K3a4IugKW2urJ3VFDtHFTOMRihL2G55MxySEh7gNGua/mvtb2gHo2x23+rccdDQ0kpcZGyOByudcNc1oAYSA27yS9xFrK8QuGsA4AC/GwsrZK4KW3l0AgkwekeQ4RRR0zr8HBj6dh06QbLK3n4IzC5qXFKGCOJsUjWSMjYI2Z2nOwkAWGYB7Cfkq3yOxckJknBVG9GCSpjocXo2GWKECXmguIDnRyxuc0a5btId1adtoxtptZT4w2OOloHCqMjHSPaxkkjmtje3kmuZd7m3c0628ngr+C4awDUAC/GwtdEyMGFgMDo6SCN4s6OGCN4uDZzY2hwuO0LORFUsEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREB/9k=",
    "https://www.obozrevatel.com/": "data:image/jpeg;base64,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"
}


@app.route('/', methods=['POST', 'GET'])
def welcome():
    """welcome page"""
    if request.method == 'GET':
        return render_template("welcome.html")


@app.route('/input_article', methods=['POST', 'GET'])
def input_article():
    """input page"""
    if request.method == 'POST':
        user_article_title = request.values.get("user_article_title").lower()
        user_article_text = request.values.get("user_article_text").lower()
        print(user_article_title)
        print(user_article_text)

        return redirect(url_for("get_sites", user_article_title=user_article_title,
                                user_article_text=user_article_text))
    else:
        return render_template("request.html")


@app.route('/get_sites', methods=['POST', 'GET'])
def get_sites():
    """sites page"""
    if request.method == 'GET':
        user_article_title = request.args['user_article_title']
        user_article_text = request.args['user_article_text']
        print("user_article_title2", user_article_title)
        print("user_article_title23", user_article_text)
        same_articles = None
        same_articles = get_similar(user_article_title)

        print(same_articles)
        if same_articles is not None:
            same_articles.int_head = same_articles.merge_sort(same_articles.int_head, "similarity")

            same_articles2 = copy.deepcopy(same_articles)
            same_articles2.int_head = same_articles.merge_sort(same_articles2.int_head, "date")

        else:
            same_articles = LinkedList("Сервіс не зміг знайти статті на подібну тему за останній місця(",
                                       "2020-05-19",
                                        0.0,
                                       "https://ictv.ua/wp-content/uploads/from_old/2014/07/28/20140728175312.jpg",
                                       "https://tsn.ua/",
                                        "")
            same_articles2 = copy.deepcopy(same_articles)

        time.sleep(3)
        return render_template("one_section.html", articles=same_articles,
                               articles2=same_articles2,
                               images_dict=IMAGES_DICT)


def get_data_from_db(user_title, table_name, n_start_article, n_finish_article,
                     same_articles="", additional=""):
    """

    :param user_title: str, a title of input news
    :param table_name: str, a table from which to get data for searching
    :param n_start_article: int, a start id
    :param n_finish_article: int, a finish id
    :param same_articles: a LinkedList of same articles
    :param additional: flag if it should be writing in database
    :return: same_articles with new found articles similar for input title
    """
    for article_id in range(n_start_article, n_finish_article):
        print("article_id", article_id)
        article_from_db = ''
        if table_name == "ArticleFakeChecker2":
            article_from_db = ArticleFakeChecker2.query.filter_by(id=article_id).first()

        elif table_name == "Article":
            article_from_db = Article.query.filter_by(id=article_id).first()

        if article_from_db is not None:

            if additional == "keywords_in_db" and db.session.query(ArticleKeyWord.title_en).filter_by(
                    title_en=article_from_db.title_en).scalar() is None:
                blob = TextBlob(article_from_db.title_en)
                title_key_words = blob.noun_phrases
                key_words = ', '.join(title_key_words)
                print("key_words", key_words)
                article_key_words = ArticleKeyWord(title_en=article_from_db.title_en,
                                                   key_words=key_words)
                article_from_db.key_words.append(article_key_words)
                db.create_all()
                try:
                    db.session.commit()
                except sqlite3.IntegrityError:
                    continue

            same_articles_num = cosine_sim(user_title, article_from_db.title_en)

            print()
            print("article_title_from_db", article_from_db.title)
            print(article_from_db.title_en)
            print("same_articles_num", same_articles_num)

            if same_articles_num >= 0.2:
                print("same article", article_from_db.title, article_from_db.url)
                str_article_from_db = str(article_from_db.text).split(".")
                if len(str_article_from_db) <= 2:
                    article_from_db.text = str_article_from_db[0]

                else:
                    article_from_db.text = str_article_from_db[0] + '.' + str_article_from_db[1]

                if not isinstance(same_articles, LinkedList):
                    same_articles = LinkedList(article_from_db.title,
                                               article_from_db.date,
                                               same_articles_num,
                                               article_from_db.url,
                                               article_from_db.resource,
                                               article_from_db.text)

                else:
                    same_articles.add(article_from_db.title,
                                      article_from_db.date,
                                      same_articles_num,
                                      article_from_db.url,
                                      article_from_db.resource,
                                      article_from_db.text)

        if article_id == 3000:
            break

    return same_articles


def get_similar(user_title, additional_function=""):
    """

    :param user_title: str, a table from which to get data for searching
    :param additional_function: str, flag which say if we should start writing in database
    :return: same_articles with new found articles similar for input title
    """
    user_title = translate_title(user_title)

    blob = TextBlob(user_title)
    user_title_key_words = blob.noun_phrases
    user_title_key_words = ' '.join(user_title_key_words)
    print(user_title_key_words)

    user_title_key_words = user_title
    print(user_title_key_words)

    same_articles = get_data_from_db(user_title_key_words, "ArticleFakeChecker2", 1, 926)
    same_articles = get_data_from_db(user_title_key_words, "Article", 1, 1451, same_articles)
    # same_articles = get_data_from_db(user_title_key_words, "Article", 42000, 42800, same_articles)

    return same_articles


if __name__ == "__main__":
    app.run(debug=True, port=33507)
