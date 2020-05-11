import json
import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

from my_config import Config

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)

article_to_key_words = db.Table('article_to_key_words', db.Model.metadata,
                                db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                                db.Column('key_words_id', db.Integer, db.ForeignKey('article_key_word.id'))
                                )

article_fake_checker2_to_key_words = db.Table('article_fake_checker2_to_key_words', db.Model.metadata,
                                db.Column('article_id', db.Integer, db.ForeignKey('article_fake_checker2.id')),
                                db.Column('key_words_id', db.Integer, db.ForeignKey('article_key_word.id'))
                                )


class ArticleKeyWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(400), unique=False, nullable=False)
    key_words = db.Column(db.String(400), unique=False, nullable=False)

    def __repr__(self):
        return '<ArticleKeyWord id={}, title_en={}, key_words={}>'.format(self.id, self.title_en, self.key_words)


class Article(db.Model):
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
        return '<Article id={}, title={}, title_en={}, text={}, date={}, resource={}, url={}>'.format(self.id, self.title,
                                                                                                      self.title_en,
                                                                                         self.text, self.date,
                                                                                         self.resource, self.url)


class ArticleFakeChecker2(db.Model):
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


@app.route('/', methods=['POST', 'GET'])
def input_profession():
    if request.method == 'POST':
        user_article_title = request.values.get("user_article_title").lower()

        # return redirect(url_for("middle"))
    else:
        return render_template("input_article.html")


if __name__ == "__main__":
    pass
