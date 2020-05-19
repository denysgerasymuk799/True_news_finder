# Fake_news_finder
Містить результати виконання домашніх завдань. 

![Fake news](static/fake_news.gif)


# Project name: 
Fake news finder
    
# Description: 
Demo video - part1 - https://youtu.be/BbioWtKkl5Y, part2 - https://youtu.be/-n4ETxvYnPU
The project aims to identify how reliable the news is in 4 categories: lies, cunning news, maybe true, true.
Users also have the opportunity to receive news-confirmation or proof-refutation of the entered link to the news.

# Table of Contents: 
1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contribution)
5. [Credits](#credits)
6. [License](#license)


# Broad description:

### Purpose and brief description of the program

This program is designed to visualize the result of training the model on whether the articles are true or fake, as well as to search for articles on a similar topic that confirm or refute this. The project uses a proprietary data type based on SQLachemy and data structures such as LinkedList - a linked list and Array - an array

 
### Input and output data of the program

First, the user selects the function I want to use. If it is a search for similar articles, it enters the title and text of the article in str format. He then receives several articles on the subject that can help him find the truth in the subject.

If it is a visualization of the research result, then the user does not enter anything and receives a prediction for each test article and a schedule of distribution of the veracity of the articles.

### The structure of the program with a brief description of modules, functions, classes and methods

- .ipynb_checkpoints 

- flask_app:
  - data_structures
  - templates 
  - аpp.py 
  - fake_news_classifier.py
  - get_similar_articles.py
  - microsoft_text_recognition.py
  - my_config.py
  - translate_text_with_array.py
  - try_data_structers.py

- site_parse

- static

- create_train_json.py

- json_to_csv.py

- xlsx_to_json.py





### Description of each component
- .ipynb_checkpoints - the main folder with files for training the model

- flask_app - Flask web application and all files and modules associated with it
  - data_structures - a folder of modules with classes Array and LinkedList
  - templates - templates for web application
  - app.py - the main module that contains all the movements on the pages of the web application, as well as models and tables for the database
  - fake_news_classifier.py - fake data recognition model that also visualizes the result
  - get_similar_articles.py - a module that retrieves information from a database and finds similar articles by keywords
  - microsoft_text_recognition.py- a module that interacts with the Azure Cognitive Service to write in the table of keywords for each article and get keywords for the article entered by the user
  - my_config.py- master keys and configuration of web application and database
  - translate_text_with_array.py - English translator from any googletrans library
  - try_data_structers.py- module for testing all data structures in the project

- site_parse- folder with fake checker parsing modules and the truest news sites in Ukraine

- static-folder for saving the main documents about the project

- create_train_json.py - a module that reads json with news for model training and translates it into English in order to conduct more accurate research as in English libraries use in the project work more accurately

- json_to_csv.py- module that converts json to csv for training module Fake_news_classifier.py

- xlsx_to_json.py - a module that converts xlsx to json to check the correctness of read data from csv



### Description of test examples to check the functionality of the program

To test fake_news_classifier.py, several changes were used in the test articles after randomly distributing a plurality of articles from the train_model.csv file and replacing the first article of the array to test the health of the my_test_model.csv file.

Several similar examples were used to verify the correctness of the found similar articles. This is one of them:

`КНДР обстріляла прикордонний пункт Південної Кореї: що відомо - введений заголовок`


Received articles from various news portals:

`Північна Корея обстріляла прикордонний пункт Південної у демілітаризованій зоні`

`КНДР обстріляла прикордонний пункт Південної Кореї`

# Installation:

# Usage:

I was unable to run the web application on heroku due to timeout restrictions, however
the application is fully functional if run locally. You can see my efforts to launch the web application at the link - https://true-news-finder.herokuapp.com/, but it falls on page 3 via TIMEOUT. You can enter any news, but the algorithm will find better those headlines,
which have been popular recently, for example:

```
- Кремль готує росіян до повернення Криму Україні?

- Це наша політика: Зеленський назвав помилкою відкликання посла Грузії

- Стало відомо, яка країна першою отримає від Японії ймовірні ліки від Covid-19
```

IN GENERAL, ALL DATA STRUCTURES AND TYPES CAN BE TESTED in flask_app / try_data_structures.py - all you need to do is install the repository and run this module. You also need to enable VPN on your computer when running this module for the translator to work properly.
Personally, I use this - https://protonvpn.com/download

You also need to enter commands to launch the web application

Windows:
```
pip install -r requirements.txt 
python flask_app/app.py
```

UNIX:
```
sudo pip install -r requirements.txt
python3 flask_app/app..py
```


# Contribution:

# Credits:

# License:
[MIT](https://choosealicense.com/licenses/mit/)
