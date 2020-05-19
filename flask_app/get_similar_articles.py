import sqlite3

import nltk
import string
from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

# from app import Article, ArticleFakeChecker2, db
from flask_app.data_structures.linked_list import LinkedList

# from flask_app.app import ArticleKeyWord
# from site_parse.parse_true_sites.parse_tsn import translate_title


def stem_tokens(tokens):
    nltk.download('punkt')  # if necessary...
    stemmer = nltk.stem.porter.PorterStemmer()
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    """remove punctuation, lowercase, stem"""
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


# def get_data_from_db(user_title, table_name, n_start_article, n_finish_article,
#                      same_articles="", additional=""):
#     for article_id in range(n_start_article, n_finish_article):
#         print("article_id", article_id)
#         article_from_db = ''
#         if table_name == "ArticleFakeChecker2":
#             # try:
#             article_from_db = ArticleFakeChecker2.query.filter_by(id=article_id).first()
#             # except sqlalchemy.orm.exc.FlushError:
#
#         elif table_name == "Article":
#             article_from_db = Article.query.filter_by(id=article_id).first()
#
#         if article_from_db is not None:
#             # start_key_words = str(article_from_db.key_words).find("key_words=") + 10
#             # end_key_words = str(article_from_db.key_words).find("key_words>") - 1
#             # key_words_article = str(article_from_db.key_words)[start_key_words: end_key_words]
#             # article_title_from_db = ' '.join(str(key_words_article).split(", "))
#
#             # if additional == "keywords_in_db":
#             blob = TextBlob(article_from_db.title)
#             title_key_words = blob.noun_phrases
#             # key_words = ', '.join(title_key_words)
#             # print("key_words", key_words)
#             # article_key_words = ArticleKeyWord(title_en=article_from_db.title_en,
#             #                                    key_words=key_words)
#             # article_from_db.key_words.append(article_key_words)
#             # db.create_all()
#             # try:
#             #     db.session.commit()
#             # except sqlite3.IntegrityError:
#             #     continue
#
#             title_key_words = ' '.join(title_key_words)
#
#             # else:
#             #     article_key_words = ArticleKeyWord.query.filter_by(id=article_id).first()
#             #     title_key_words = str(article_key_words)
#
#             same_articles_num = cosine_sim(user_title, title_key_words)
#
#             print()
#             print("article_title_from_db", article_from_db.title)
#             print("title_key_words", title_key_words)
#             print(article_from_db.title_en)
#             print("same_articles_num", same_articles_num)
#             # if flag_same_articles == 1:
#
#             if same_articles_num >= 0.2:
#                 print("same article", article_from_db.title, article_from_db.url)
#                 str_article_from_db = str(article_from_db.text).split(".")
#                 if len(str_article_from_db) == 2:
#                     article_from_db.text = str_article_from_db[0]
#
#                 else:
#                     article_from_db.text = str_article_from_db[0] + '.' + str_article_from_db[1]
#
#                 if not isinstance(same_articles, LinkedList):
#                     same_articles = LinkedList(article_from_db.title,
#                                                article_from_db.date,
#                                                same_articles_num,
#                                                article_from_db.url,
#                                                article_from_db.resource,
#                                                article_from_db.text)
#
#                 else:
#                     same_articles.add(article_from_db.title,
#                                       article_from_db.date,
#                                       same_articles_num,
#                                       article_from_db.url,
#                                       article_from_db.resource,
#                                       article_from_db.text)
#
#         if article_id == 3000:
#             break
#
#     return same_articles
#
#
# def main(user_title, additional_function=""):
#     user_title = translate_title(user_title)
#
#     blob = TextBlob(user_title)
#     user_title_key_words = blob.noun_phrases
#     user_title_key_words = ' '.join(user_title_key_words)
#     print(user_title_key_words)
#
#     user_title_key_words = user_title
#     print(user_title_key_words)
#
#     same_articles = get_data_from_db(user_title_key_words, "ArticleFakeChecker2", 1, 926, additional=additional_function)
#
#     same_articles = get_data_from_db(user_title_key_words, "Article", 1, 2000, same_articles,
#                                      additional=additional_function)
#     same_articles = get_data_from_db(user_title_key_words, "Article", 42000, 42800, same_articles,
#                                      additional=additional_function)
#
#     print(same_articles)


if __name__ == '__main__':
    main("Кремль готує росіян до повернення Криму Україні?",
         additional_function="keywords_in_db")
    print("result1")
    main("Це наша політика: Зеленський назвав помилкою відкликання посла Грузії")
    print("result2")
    main("Стало відомо, яка країна першою отримає від Японії ймовірні ліки від Covid-19")
    print("result3")
    main("Шмыгаль обсудит меморандум Украины по 'зеленой' энергетике с инвесторами из США, Швеции, Канады и Норвегии")

    # for user_title in ["How Big is the Kremlin's Obsession with Ukraine? Spoiler: Very Big",
    #                    'Ukraine will turn into a banana republic": Ukrainian Elections on Russian TV',
    #                    "Attacking the Church of Ukraine: The Kremlin Turns the Orthodox World into a Battlefield"]:
    #     blob = TextBlob(user_title)
    #     user_title_key_words = blob.noun_phrases
    #     user_title_key_words = ' '.join(user_title_key_words)
    #     print(user_title_key_words)
