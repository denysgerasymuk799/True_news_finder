import json
import os
import time

from googletrans import Translator

from prepare_data.translate_text import translate_text


def write_in_json(title, text, label, n_last_article=0):
    temp_dir = os.getcwd()
    os.chdir("..")
    path_to_write = os.path.join(os.getcwd(), '.ipynb_checkpoints', 'package.json')
    with open(path_to_write, "r", encoding="utf-8") as file:
        json_data_write = json.load(file)

    with open(os.path.join(os.getcwd(), '.ipynb_checkpoints', 'second_list.json'), "r", encoding="utf-8") as file:
        data = json.load(file)

    start_from = 0
    for row in data:
        start_from += 1

        if start_from < 139:
            n_last_article += 1
            continue

        translator = Translator()
        print("num_row", n_last_article)
        print("row[title]0", row[title])
        stop_words = ['(video file)', "(VIDEO)", "Video file", "(IMAGE)", "(DOC)",
                      "(TEXT)"]

        if row[text].strip() not in stop_words:
            print("row[text]1", row[text])

            str_num_row = str(n_last_article)
            if str_num_row not in json_data_write.keys():

                try:
                    lang = translator.translate(row[title]).src
                except json.decoder.JSONDecodeError:
                    time.sleep(3)
                    translator = Translator()
                    lang = translator.translate(row[title]).src

                print("lang", lang)
                if lang == "en" or lang == "ua" or lang == "ru":
                    print("not video file")
                    json_data_write[str_num_row] = dict()
                    if lang == "ua" or lang == "ru":
                        row[title] = translate_text(row[title], lang, 'en')
                        print("row[title]", row[title])
                        row[text] = translate_text(row[text], lang, 'en')
                        print("row[text]2", row[text])

                    json_data_write[str_num_row]["title"] = row[title]
                    json_data_write[str_num_row]["text"] = row[text]
                    json_data_write[str_num_row]["label"] = label

            else:
                print("Found in json\n")

            with open(path_to_write, "w", encoding="utf-8") as file:
                json.dump(json_data_write, file, indent=4, ensure_ascii=False)
        #
        # except:
        #     continue
        n_last_article += 1

    os.chdir(temp_dir)
    return n_last_article


def main():
     num_last_article = write_in_json("Article", "Disproof text", "REAL")
     num_last_article = write_in_json("FN Title", "FN text", "FAKE", num_last_article)


if __name__ == '__main__':
    main()
    # temp_dir = os.getcwd()
    # os.chdir("..")
    # path_to_write = os.path.join(os.getcwd(), '.ipynb_checkpoints', 'train_model2.json')
    # di = {}
    # with open(path_to_write, "w", encoding="utf-8") as file:
    #     json.dump(di, file, indent=4, ensure_ascii=False)