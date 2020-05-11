import os

from fake_news_classifier import get_tests_results
from get_similar_articles import main

from translate_text_with_array import translate_text


if __name__ == '__main__':
    print("""Now AI has such functions: 
        1. Find similar articles to my article title
        2. Look at the training and tests results of the AI fake_new_finder
        3. Translate on english""")

    user_choice = input("Choose number of the function to try it: ")
    while not user_choice.isdigit():
        print("Enter only numbers from range [1, 2]")
        user_choice = input("Choose number of the function to try it:")

    if user_choice == "1":
        user_title = "Народ Криму зробив свій вибір на користь Росії"
        main(user_title)

    elif user_choice == "2":
        get_tests_results()

    elif user_choice == "3":
        user_text = input("Type text to translate:\n")
        print(translate_text(user_text, "en"))
