# True_news_finder

![Fake news](my_static/fake_news.gif)


# Project name: 
True news finder

![](https://img.shields.io/badge/-status:wip-5319e7.svg)
![](https://img.shields.io/github/license/damoklov/nasa.svg)
![](https://img.shields.io/github/languages/code-size/denysgerasymuk799/True_news_finder.svg)
![](https://img.shields.io/github/last-commit/denysgerasymuk799/True_news_finder.svg)
    
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


# Broad description: :sparkler:

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
  - my_config.py
  - try_data_structures.py

- my_docs

- site_parse

- prepare_data

- static

- files for hosting


### Description of each component

- .ipynb_checkpoints - the main folder with files for training the model

- flask_app - Flask web application and all files and modules associated with it
  - data_structures - a folder of modules with classes Array and LinkedList
  - templates - templates for web application
  - app.py - the main module that contains all the movements on the pages of the web application, as well as models and tables for the database
  - fake_news_classifier.py - fake data recognition model that also visualizes the result
  - get_similar_articles.py - a module that retrieves information from a database and finds similar articles by keywords
  - my_config.py- master keys and configuration of web application and database
  - try_data_structures.py- module for testing all data structures in the project

- my_docs - documentation for this project, in build dir you can find html pages

- site_parse - folder with fake checker parsing modules and the truest news sites in Ukraine

- prepare_data - a directory for creating data for ML algorithm, which finds fake news

- static -folder for saving the main documents about the project



### Description of test examples to check the functionality of the program

To test fake_news_classifier.py, several changes were used in the test articles after randomly distributing a plurality of articles from the train_model.csv file and replacing the first article of the array to test the health of the my_test_model.csv file.

Several similar examples were used to verify the correctness of the found similar articles. This is one of them:

`КНДР обстріляла прикордонний пункт Південної Кореї: що відомо - введений заголовок`


Received articles from various news portals:

`Північна Корея обстріляла прикордонний пункт Південної у демілітаризованій зоні`

`КНДР обстріляла прикордонний пункт Південної Кореї`

# Installation: :pushpin:

The application is fully functional if run locally. Also you can see my web application at the link - https://true-news-finder.herokuapp.com/. You can enter any news, but the algorithm will find better those headlines,
which have been popular recently approximately one month, for example:

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

# Usage: :computer:

- Open https://true-news-finder.herokuapp.com/ or run flask_app/app.py from this repo
- Read welcome page
- Push Input title button on the right top corner
- Input a title and text of your article. which you want to checker and find similar articles
- Choose the best articles for use or use sort by date button
- Enjoy:)

# Documentation  :notebook_with_decorative_cover:

Documentation for this application can be found in my_docs/build/html/index.html


# Contribution:

# Credits:

# License:
[MIT](https://choosealicense.com/licenses/mit/)
