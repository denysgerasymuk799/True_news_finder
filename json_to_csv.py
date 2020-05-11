import csv
import json
import os


def write_to_csv(json_with_article):
    rows_list = [["title", "text", "label"]]
    for fact_index in json_with_article.keys():
        try:
            row = [fact_index, json_with_article[fact_index]["title"], json_with_article[fact_index]["text"],
                   json_with_article[fact_index]["label"]]
        except KeyError:
            continue

        rows_list.append(row)

    path_to_write = os.path.join('.ipynb_checkpoints', 'train_model.csv')
    with open(path_to_write, "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(rows_list)


if __name__ == '__main__':
    path_to_write = os.path.join('.ipynb_checkpoints', 'train_model.json')
    with open(path_to_write, "r", encoding="utf-8") as file:
        json_with_articles = json.load(file)

    write_to_csv(json_with_articles)
