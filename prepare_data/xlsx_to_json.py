import json

import os

import excel2json
import pandas


temp_dir = os.getcwd()
os.chdir("..")
excel2json.convert_from_file(os.path.join('.ipynb_checkpoints', 'Fakes List - List2.xlsx'))
os.chdir(temp_dir)
# with open(os.path.join(os.getcwd(), '.ipynb_checkpoints', 'Лист1.json'), "r", encoding="utf-8") as file:
#     data = json.load(file)

# print(data[0]["Sour\u0441e"])
# print(data[0]["FN Title"])
