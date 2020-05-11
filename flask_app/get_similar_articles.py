import json
import os
import time

import nltk, string
from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer

from app import Article, ArticleFakeChecker2, db
from data_structures.linked_list import LinkedList

from microsoft_text_recognition import key_phrase_extraction_example


def main(user_title):
    # nltk.download('punkt')  # if necessary...
    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    def stem_tokens(tokens):
        return [stemmer.stem(item) for item in tokens]

    def normalize(text):
        """remove punctuation, lowercase, stem"""
        return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

    def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0, 1]

    def get_data_from_db(user_title, table_name, same_articles="", list_same=[]):
        n_articles = 100
        if table_name == "ArticleFakeChecker2":
            # last_article = db.session.query(ArticleFakeChecker2).order_by(ArticleFakeChecker2.id.desc()).first()
            n_articles = 676

        elif table_name == "Article":
            last_article = db.session.query(Article).order_by(Article.id.desc()).first()
            n_articles = 650
        #
        # max_id_pos_start = str(last_article).find("id=")
        # max_id_pos_end = str(last_article).find("title=")
        # max_id = str(last_article)[max_id_pos_start + 3: max_id_pos_end - 2]
        # n_articles = int(max_id) + 1

        for article_id in range(1, n_articles):
            article_from_db = ''
            if table_name == "ArticleFakeChecker2":
                article_from_db = ArticleFakeChecker2.query.filter_by(id=article_id).first()

            elif table_name == "Article":
                article_from_db = Article.query.filter_by(id=article_id).first()

            if article_from_db is not None:
                start_key_words = str(article_from_db.key_words).find("key_words=") + 10
                end_key_words = str(article_from_db.key_words).find("key_words>") - 1
                key_words_article = str(article_from_db.key_words)[start_key_words: end_key_words]
                # article_title_from_db = ' '.join(str(key_words_article).split(", "))

                # same_articles_num = cosine_sim(user_title, article_title_from_db)
                n_same_words = 0

                flag_same_articles = 0
                article_title_from_db = str(article_from_db.title)
                same_words = []

                for word in key_words_article.split():
                    if word in user_title:
                        n_same_words += 1
                        same_words.append(word)

                    if n_same_words >= 2:
                        flag_same_articles = 1
                        break

                # print()
                # print("article_title_from_db", article_title_from_db)
                # print(article_from_db.title_en)
                # print("same_articles_num", same_articles_num)
                if flag_same_articles == 1:

                    # if same_articles_num >= 0.2:
                    if not isinstance(same_articles, LinkedList):
                        same_articles = LinkedList(article_from_db.title,
                                                   same_words,
                                                   article_from_db.date,
                                                   article_from_db.url,
                                                   article_from_db.resource)

                    else:
                        same_articles.add(article_from_db.title,
                                          same_words,
                                          article_from_db.date,
                                          article_from_db.url,
                                          article_from_db.resource)

                    list_same.append(article_from_db.title)

        return same_articles, list_same

    def translate_user_input(user_title):
        # user_title = "Народ Криму зробив свій вибір на користь Росії"
        translator = Translator()
        try:
            src_lang = translator.translate(user_title).src
        except json.decoder.JSONDecodeError:
            time.sleep(3)
            translator = Translator()
            src_lang = translator.translate(user_title).src

        if src_lang != "en":
            # REINITIALIZE THE API
            translator = Translator()
            try:
                translated = translator.translate(user_title, src=src_lang, dest="en")
                user_title = translated.text
            except Exception as e:
                print(str(e))
                user_title = ""

        return user_title

    user_title = translate_user_input(user_title)
    try:
        user_title_key_words = key_phrase_extraction_example([user_title])
        user_title_key_words = ' '.join(user_title_key_words)

    except:
        user_title_key_words = user_title

    # print("user_title_key_words", user_title)
    same_articles, list_same = get_data_from_db(user_title_key_words, "ArticleFakeChecker2")
    same_articles, list_same = get_data_from_db(user_title_key_words, "Article", same_articles, list_same)
    print(same_articles)
    # print(list_same)


if __name__ == '__main__':
    main()
    # print((articles_json["-2"]["title"], articles_json["-1"]["title"]))
    # print(cosine_sim(articles_json["-2"]["title"], articles_json["-1"]["title"]))
    # print(cosine_sim(articles_json["-2"]["text"], articles_json["-1"]["text"]))
    # print((articles_json["-4"]["title"], articles_json["-1"]["title"]))
    # print(cosine_sim(articles_json["-4"]["title"], articles_json["-1"]["title"]))
    # --------
    # print((articles_json["-5"]["title"], articles_json["-5"]["text"]))
    # print(cosine_sim(articles_json["-5"]["title"], articles_json["-5"]["text"]))
    #
    # print((articles_json["-5"]["text1"], articles_json["-5"]["text2"]))
    # print(cosine_sim(articles_json["-5"]["text1"], articles_json["-5"]["text2"]))
    #
    # print((articles_json["-5"]["title"], articles_json["-5"]["text1"]))
    # print(cosine_sim(articles_json["-5"]["title"], articles_json["-5"]["text1"]))
    #
    # print("-" * 30)
    #
    # print((articles_json["-7"]["title"], articles_json["-7"]["text1"]))
    # print(cosine_sim(articles_json["-7"]["title"], articles_json["-7"]["text1"]))
    # print(cosine_sim(articles_json["-7"]["title"], articles_json["-7"]["text"]))
    # print(cosine_sim(articles_json["-7"]["text2"], articles_json["-7"]["text3"]))
    #
    # print(cosine_sim(articles_json["-3"]["text"], articles_json["-1"]["text"]))
    # print("test.json other article topic", cosine_sim(articles_json["-4"]["text"], articles_json["-1"]["text"]))
