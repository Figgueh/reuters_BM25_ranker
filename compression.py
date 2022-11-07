import string
import globals
from nltk import word_tokenize


def to_lower(text):
    return text.lower()


def remove_punctuation(text):
    translator = str.maketrans(dict.fromkeys(string.punctuation))
    clean_text = text.translate(translator)
    return clean_text


def remove_stopwords(text, stopwords):
    text_without_stopwords = []
    for token in text:
        if token not in stopwords:
            text_without_stopwords.append(token)

    return text_without_stopwords


def tokenize(text):
    return word_tokenize(text)


def compress(text):
    return tokenize(remove_punctuation(text))


def heavy_compress(text):
    return remove_stopwords(tokenize(remove_punctuation(to_lower(text))), globals.stopword150)