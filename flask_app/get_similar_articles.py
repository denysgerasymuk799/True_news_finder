"""
Import ML libraries
"""
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer


def stem_tokens(tokens):
    """

    :param tokens: tokens for training
    :return: a list of tokens
    """
    nltk.download('punkt')  # if necessary...
    stemmer = nltk.stem.porter.PorterStemmer()
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    """remove punctuation, lowercase, stem"""
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2):
    """

    :param text1: str
    :param text2: str
    :return: a possibility of simplicity
    """
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    return (tfidf * tfidf.T).A[0, 1]


if __name__ == '__main__':
    pass
