# coding=utf8
from googletrans import Translator
from flask_app.data_structures.array import Array


def translate_text(article, src_lang, dest_lang):
    article_array = Array(1)
    new_rows = Array(50)

    # translator = Translator()
    # articles_array[0] = article
    # src_lang = translator.translate(article[0][0]).src
    if '\n' in article[0]:
        for line in article_array.split('\n'):
            if line != "":
                # REINITIALIZE THE API
                translator = Translator()
                try:
                    # translate the 'text' column
                    translated = translator.translate(line, src=src_lang, dest=dest_lang)
                    new_rows.append_array(translated.text)
                except Exception as e:
                    print(str(e))
                    continue
            else:
                break
    else:
        translator = Translator()
        try:
            # translate the 'text' column
            translated = translator.translate(article, src=src_lang, dest=dest_lang)
            new_rows.append_array(translated.text)
        except Exception as e:
            print(str(e))

    return new_rows.join_array('\n')


if __name__ == '__main__':
    articles_array = Array(15)
    string = "Північна Корея провела випробування надважкої багатозарядної пускової установки.\n\nДжерело: DW\n\nДеталі: В рамках випробувань Пхеньян перевіряв тактико-технічні характеристики пускової установки. Випробування пройшли успішно, найближчим часом установку планують поставити до військових частин. \n\nНагадаємо:\n\n    КНДР 9 березня провела пуск трьох невпізнаних снарядів у напрямку Японського моря. \n    За даними Об'єднаного комітету начальників штабів Південної Кореї, запуск був проведений з району міста Сондок в провінції Хамген-Намдо і пролетіли близько 200 км.\n"
    # print(articles_array.split('\n'))
    print(translate_text(string, "ua", "en"))
