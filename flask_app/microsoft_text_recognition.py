import sqlite3

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from app import Article, ArticleFakeChecker2, ArticleKeyWord, db


def key_phrase_extraction_example(documents):
    key = "e0ad072721ac448e8ecfe797c3b220a7"
    endpoint = "https://sea-ucu.cognitiveservices.azure.com/"

    def authenticate_client():
        ta_credential = AzureKeyCredential(key)
        text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
        return text_analytics_client

    client = authenticate_client()

    title_keywords = []

    try:
        for title_id in range(len(documents)):
            response = client.extract_key_phrases(documents=documents)[title_id]

            if not response.is_error:
                print()
                print(documents[title_id])
                print("\tKey Phrases:")
                title_keywords = []
                for phrase in response.key_phrases:
                    print("\t\t", phrase)
                    title_keywords.append(phrase)

        else:
            print(response.id, response.error)

    except Exception as err:
        pass
        # print("Encountered exception. {}".format(err))

    return title_keywords


def get_data_from_db(table_name):
    string_for_request = ""
    n_articles = 100
    if table_name == "ArticleFakeChecker2":
        n_articles = 676

    elif table_name == "Article":
        n_articles = 650

    strings = []

    for article_id in range(1, n_articles):
        print("article_id", article_id)
        article_from_db = ''
        if table_name == "ArticleFakeChecker2":
            article_from_db = ArticleFakeChecker2.query.filter_by(id=article_id).first()

        elif table_name == "Article":
            article_from_db = Article.query.filter_by(id=article_id).first()

        if article_from_db is not None:
            strings.append(article_from_db.title_en)
            documents = [article_from_db.title_en]
            if documents != []:
                key_words = key_phrase_extraction_example(documents)
                key_words = ', '.join(key_words)
                print("key_words", key_words)
                article_key_words = ArticleKeyWord(title_en=article_from_db.title_en,
                                                   key_words=key_words)
                article_from_db.key_words.append(article_key_words)
                db.create_all()
                try:
                    db.session.commit()
                except sqlite3.IntegrityError:
                    continue

    return strings


if __name__ == '__main__':
    # string_lst = get_data_from_db()
    # for string in string_lst:
    #     documents = [string]
    documents = ["The DPRK has tested a heavy multi-charge launcher.",
                 "North Korea fired on the South's border post in the demilitarized zone",
                 "North Korea fired on a South Korean border crossing",
                 "Russia will go all-bank: an expert on the celebration of Victory Day in Moscow",
                 "What turned Russia into Victory Day - Antizombie, 06.02.2020"]

    documents = get_data_from_db("ArticleFakeChecker2")
    documents = get_data_from_db("Article")
    # article_id = 0
    # result_string = ""
    # for title in documents:
    #     article_id += 1
    #     result_string += title + "DENYS" + str(article_id) + "\n"

    # print(key_phrase_extraction_example(client, documents))
