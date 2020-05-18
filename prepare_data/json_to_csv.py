import csv
import json
import os


def write_to_csv(filename, result_filename):
    path_to_write = os.path.join('.ipynb_checkpoints', filename)
    temp_dir = os.getcwd()
    os.chdir("..")
    with open(path_to_write, "r", encoding="utf-8") as file:
        json_with_articles = json.load(file)
        
    rows_list = [["title", "text", "label"]]
    for fact_index in json_with_articles.keys():
        try:
            row = [fact_index, json_with_articles[fact_index]["title"], json_with_articles[fact_index]["text"],
                   json_with_articles[fact_index]["label"]]
        except KeyError:
            continue

        rows_list.append(row)

    path_to_write = os.path.join('.ipynb_checkpoints', result_filename)
    with open(path_to_write, "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(rows_list)

    os.chdir(temp_dir)


if __name__ == '__main__':
    write_to_csv('train_model.json', 'train_model2.csv')
    # write_to_csv('package.json', 'package.csv')
