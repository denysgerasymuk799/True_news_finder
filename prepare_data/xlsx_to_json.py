import os
import excel2json

temp_dir = os.getcwd()
os.chdir("..")
excel2json.convert_from_file(os.path.join('.ipynb_checkpoints', 'Fakes List - List2.xlsx'))
os.chdir(temp_dir)
