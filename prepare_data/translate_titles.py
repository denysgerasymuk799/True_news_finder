import json

from flask_app.app import Article, ArticleFakeChecker2, db
from site_parse.parse_true_sites.parse_tsn import translate_title


def write_in_json(table_name):
    n_articles = 100
    if table_name == "ArticleFakeChecker2":
        # last_article = db.session.query(ArticleFakeChecker2).order_by(ArticleFakeChecker2.id.desc()).first()
        n_articles = 926

    elif table_name == "Article":
        last_article = db.session.query(Article).order_by(Article.id.desc()).first()
        n_articles = 42169

    titles_dict = {}
    for article_id in range(42000, 42900):
        print("article_id", article_id)
        article_from_db = ''
        if table_name == "ArticleFakeChecker2":
            article_from_db = ArticleFakeChecker2.query.filter_by(id=article_id).first()

        elif table_name == "Article":
            article_from_db = Article.query.filter_by(id=article_id).first()

        if article_from_db is not None:
            titles_dict[str(article_id)] = {}
            titles_dict[str(article_id)]["title"] = article_from_db.title

    with open("titles_en2.json", "w", encoding="utf-8") as file:
        json.dump(titles_dict, file, indent=4, ensure_ascii=False)


def translate_titles():
    with open("titles_en2.json", "r", encoding="utf-8") as file:
        titles_dict = json.load(file)

    i = 0
    for article_id in range(42711, 42900):
        i += 1
        print("article_id", article_id)
        article_id = str(article_id)
        try:
            title_en = translate_title(titles_dict[article_id]["title"])
        except KeyError:
            print("continue")
            continue
        titles_dict[article_id]["title_en"] = title_en
        # if i == 10:
        #     break

        with open("titles_en2.json", "w", encoding="utf-8") as file:
            json.dump(titles_dict, file, indent=4, ensure_ascii=False)


def write_in_db():
    with open("titles_en2.json", "r", encoding="utf-8") as file:
        titles_dict = json.load(file)

    for article_id in titles_dict.keys():
        print("article_id", article_id)
        article_from_db = Article.query.filter_by(id=int(article_id)).first()
        article_from_db.title_en = titles_dict[article_id]["title_en"]

        db.session.commit()


if __name__ == '__main__':
    # write_in_json("Article")
    # translate_titles()
    # write_in_db()
    article_from_db = Article.query.filter_by(id=int(24)).first()
    # article_from_db.title = "Карантин в Україні - все, що потрібно знати"
    # db.session.commit()
    print(article_from_db.title)
    print(article_from_db.title_en)
