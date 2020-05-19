from flask_app.app import get_similar
from flask_app.fake_news_classifier import get_tests_results

from flask_app.translate_text_with_array import translate_text


if __name__ == '__main__':
    print("""Now AI has such functions: 
        1. Find similar articles to an example article title
        2. Look at the training and tests results of the AI fake_new_finder
        3. Translate on english""")

    user_choice = input("Choose number of the function to try it: ")
    while user_choice.strip() != "1" and user_choice.strip() != "2" and \
            user_choice.strip() != "3":
        print("Enter only numbers from range [1, 2, 3]")
        user_choice = input("Choose number of the function to try it:")

    if user_choice == "1":
        user_title = "Народ Криму зробив свій вибір на користь Росії"
        get_similar(user_title)

    elif user_choice == "2":
        get_tests_results()

    elif user_choice == "3":
        all_user_text = ""
        print("Type text to translate")
        print("If you want to stop typing text put ENTER 4 times in a row")
        flag_break = 0
        while flag_break != 2:
            user_input = input()
            if user_input.strip() == "":
                flag_break += 1
            else:
                flag_break = 0
            all_user_text += user_input
        print(translate_text(all_user_text, "en"))
