import json

from flask_app.app import Article, ArticleFakeChecker2, db
from site_parse.translate_title import translate_title


def write_in_json(table_name, start_id, finish_id):
    titles_dict = {}
    for article_id in range(start_id, finish_id):
        print("article_id", article_id)
        article_from_db = ''
        if table_name == "ArticleFakeChecker2":
            article_from_db = ArticleFakeChecker2.query.filter_by(id=article_id).first()

        elif table_name == "Article":
            article_from_db = Article.query.filter_by(id=article_id).first()

        if article_from_db is not None:
            titles_dict[str(article_id)] = {}
            titles_dict[str(article_id)]["title"] = article_from_db.title

    with open("files_for_prepare_data/titles_en2.json", "w", encoding="utf-8") as file:
        json.dump(titles_dict, file, indent=4, ensure_ascii=False)


def translate_titles(start_id, finish_id):
    with open("files_for_prepare_data/titles_en2.json", "r", encoding="utf-8") as file:
        titles_dict = json.load(file)

    for article_id in range(start_id, finish_id):
        print("article_id", article_id)
        article_id = str(article_id)
        try:
            title_en = translate_title(titles_dict[article_id]["title"])
        except KeyError:
            print("continue")
            continue
        titles_dict[article_id]["title_en"] = title_en

        with open("files_for_prepare_data/titles_en2.json", "w", encoding="utf-8") as file:
            json.dump(titles_dict, file, indent=4, ensure_ascii=False)


def write_in_db():
    with open("files_for_prepare_data/titles_en2.json", "r", encoding="utf-8") as file:
        titles_dict = json.load(file)

    for article_id in titles_dict.keys():
        print("article_id", article_id)
        article_from_db = Article.query.filter_by(id=int(article_id)).first()
        article_from_db.title_en = titles_dict[article_id]["title_en"]

        db.session.commit()


if __name__ == '__main__':
    write_in_json("Article", 1, 100)
    translate_titles(42711, 42900)
    write_in_db()
