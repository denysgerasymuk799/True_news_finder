import nltk
import string
from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

from app import Article, ArticleFakeChecker2, db
from data_structures.linked_list import LinkedList

from site_parse.parse_true_sites.parse_tsn import translate_title


def stem_tokens(tokens):
    # nltk.download('punkt')  # if necessary...
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


def get_data_from_db(user_title, table_name, n_start_article, n_finish_article, same_articles=""):
    for article_id in range(n_start_article, n_finish_article):
        print("article_id", article_id)
        article_from_db = ''
        if table_name == "ArticleFakeChecker2":
            article_from_db = ArticleFakeChecker2.query.filter_by(id=article_id).first()

        elif table_name == "Article":
            article_from_db = Article.query.filter_by(id=article_id).first()

        if article_from_db is not None:
            # start_key_words = str(article_from_db.key_words).find("key_words=") + 10
            # end_key_words = str(article_from_db.key_words).find("key_words>") - 1
            # key_words_article = str(article_from_db.key_words)[start_key_words: end_key_words]
            # article_title_from_db = ' '.join(str(key_words_article).split(", "))

            blob = TextBlob(article_from_db.title)
            title_key_words = blob.noun_phrases
            title_key_words = ' '.join(title_key_words)

            same_articles_num = cosine_sim(user_title, title_key_words)
            # n_same_words = 0
            #
            # flag_same_articles = 0
            # article_title_from_db = str(article_from_db.title)
            # same_words = []
            #
            # for word in key_words_article.split():
            #     if word in user_title:
            #         n_same_words += 1
            #         same_words.append(word)
            #
            #     if n_same_words >= 2:
            #         flag_same_articles = 1
            #         break

            print()
            print("article_title_from_db", article_from_db.title)
            print(article_from_db.title_en)
            print("same_articles_num", same_articles_num)
            # if flag_same_articles == 1:

            if same_articles_num >= 0.2:
                print("same article", article_from_db.title, article_from_db.url)
                str_article_from_db = str(article_from_db.text).split(".")
                if len(str_article_from_db) == 2:
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


def main(user_title):
    user_title = translate_title(user_title)

    blob = TextBlob(user_title)
    user_title_key_words = blob.noun_phrases
    user_title_key_words = ' '.join(user_title_key_words)
    print(user_title_key_words)

    user_title_key_words = user_title
    print(user_title_key_words)

    same_articles = get_data_from_db(user_title_key_words, "ArticleFakeChecker2", 1, 926)

    same_articles = get_data_from_db(user_title_key_words, "Article", 1, 2000, same_articles)
    same_articles = get_data_from_db(user_title_key_words, "Article", 42000, 42800, same_articles)

    print(same_articles)


if __name__ == '__main__':
    main("Кремль готує росіян до повернення Криму Україні?")

    # for user_title in ["How Big is the Kremlin's Obsession with Ukraine? Spoiler: Very Big",
    #                    'Ukraine will turn into a banana republic": Ukrainian Elections on Russian TV',
    #                    "Attacking the Church of Ukraine: The Kremlin Turns the Orthodox World into a Battlefield"]:
    #     blob = TextBlob(user_title)
    #     user_title_key_words = blob.noun_phrases
    #     user_title_key_words = ' '.join(user_title_key_words)
    #     print(user_title_key_words)
