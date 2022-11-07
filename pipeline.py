import json
import string

from nltk import word_tokenize

import globals
from nltk.corpus import PlaintextCorpusReader

class Pipeline:

    def __init__(self):
        self.text = self.extract_text()

    def change_pipe(self, text):
        self.text = text

    def extract_text(self):
        print("Fetching text...")
        def remove_formatting_error(word):
            new_str = ""
            in_tag = False
            for char in word:
                if not in_tag:
                    if char == '&':
                        in_tag = True
                    else:
                        new_str += char
                elif in_tag:
                    if char == ';':
                        in_tag = False
            return new_str

        def check_for_multiple_tags(i, char, word):
            # To check if there are multiple tags in a word. This function adds a space
            # if the next character is the start of another tag to be able to split
            # any words that might be contained in these two tags.

            if i + 1 < len(word) and word[i + 1] == '<':
                return char + " "
            else:
                return char

        # Get the whole documents text
        wordlists = PlaintextCorpusReader(globals.corpus_root, globals.file_pattern, encoding='latin-1')

        # Split them into words
        corpus = wordlists.raw()

        # Clean the text
        to_throw = True
        clean_corpus = ""
        for word in corpus.split():
            # If we were going to throw the word
            if to_throw:

                # Check for particulars we need to keep
                if "NEWID" in word:
                    to_throw = False

            # If we weren't going to keep it
            if not to_throw:

                # Once we get to the end, we signal that we have finished
                if word == '</REUTERS>':
                    to_throw = True
                else:
                    word = remove_formatting_error(word)

                    # remove any tags from the text that we are going to keep
                    clean_str = ""
                    in_tag = False
                    for i, char in enumerate(word):  # Look at each letter in the word
                        if not in_tag:  # If we haven't seen the start of the tag

                            # Signal that we are in the tag
                            if char == '<':
                                in_tag = True
                            else:
                                # Keep everything else until we signal that we have seen the end of the tag
                                clean_str += check_for_multiple_tags(i, char, word)

                        elif in_tag:
                            if char == '>':
                                in_tag = False

                    # Reassemble the rest of the string
                    clean_corpus += clean_str + " "

        # Returns a really long string that has the form:
        # NEWID="x"> [ARTICLE TEXT]
        # for each document we process

        return clean_corpus

    def save_subcorpus(self, text):
        f = open("subcorpus.txt", "w")
        f.write(text)
        f.close()

    def extract_first_10k(self, text):
            print("Constructing sub-corpus with the first 10K pairs...")
            # The idea for this function is to create a postings list before hand, then
            # create a subcorpus containg x amount of tokens, so that we can then
            # pass this subcorpus to the functions responsible for creating the lists
            self.postings = []
            article_line = text.split("NEWID=\"")

            new_corpus = str()
            for article in article_line:
                if article:
                    article_words = article.split()
                    id_from_text = article_words[0]
                    newid = int(id_from_text[:-2])
                    words = article_words[1:]

                    # Kept for when we are limiting the indexer to 10000 tokens
                    rebuild_article = "NEWID=\"" + str(newid) + "\"> "

                    # Reassemble the list:
                    # article_text = " ".join(words)
                    #
                    # # Remove any punctuation
                    # translator = str.maketrans(dict.fromkeys(string.punctuation))
                    # article_text = article_text.translate(translator)
                    # words = word_tokenize(article_text)

                    for word in words:
                        rebuild_article += word + " "
                        if len(self.postings) == 10000:
                            new_corpus += rebuild_article
                            self.save_subcorpus(new_corpus)
                            return new_corpus

                        self.postings.append([newid, word])

                    # If we reached the end of the article then we include it in the new corpus
                    new_corpus += rebuild_article


def save_index(method, index):
    file_path = "indexers/" + method + ".txt"
    f = open(file_path, "w")
    f.write(json.dumps(index, indent=1))
    f.close()


def save_query_results(method, type, query, result):
    file_path = "queries/" + method.replace(" ", "_") + "/" + type + "/" + "/" + query.replace(" ", "_") + ".txt"
    f = open(file_path, "w")

    if type == "and" or type == "or":
        f.write(json.dumps(result))
    else:
        f.write(json.dumps(result, indent=1))

    f.close()


