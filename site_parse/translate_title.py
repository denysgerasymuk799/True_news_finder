import json
import time

from googletrans import Translator


def translate_title(article_title):
    """translate title on english"""
    translator = Translator()
    try:
        src_lang = translator.translate(article_title).src
    except json.decoder.JSONDecodeError:
        time.sleep(3)
        translator = Translator()
        src_lang = translator.translate(article_title).src

    # REINITIALIZE THE API
    translator = Translator()
    try:
        translated = translator.translate(article_title, src=src_lang, dest="en")
        article_title_en = translated.text
    except Exception as e:
        print(str(e))
        article_title_en = ""

    return article_title_en
