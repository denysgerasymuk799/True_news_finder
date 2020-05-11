import json

import os

import excel2json
import pandas


excel2json.convert_from_file(os.path.join(os.getcwd(), '.ipynb_checkpoints', 'fake_list.xlsx'))
with open(os.path.join(os.getcwd(), '.ipynb_checkpoints', 'Лист1.json'), "r", encoding="utf-8") as file:
    data = json.load(file)

print(data[0]["Sour\u0441e"])
print(data[0]["FN Title"])
