import math
import string
import collections
from itertools import groupby

from nltk import word_tokenize

class InvertedIndex:
    def __init__(self, posting_list=None, pipeline=None, compression=False, track_frequency=False):
        if track_frequency:
            self.article_length = {}
            self.articles_processed = 0
            self.term_frequency = {}
        self.inverted_index = {}
        if posting_list:
            self.generate_inverted_naive(posting_list)
        if pipeline:
            self.generate_inverted_SPIMI(pipeline, compression=compression, track_frequency=track_frequency)

    def generate_inverted_naive(self, posting_list):
        print("Generating inverted index from postings list...")
        for pair in posting_list.postings:
            if pair[1] in self.inverted_index:
                self.inverted_index[pair[1]].append(pair[0])
            else:
                self.inverted_index[pair[1]] = [pair[0]]

        # Update the total documents processed
        self.articles_processed = posting_list.postings[-1][0]

    def generate_inverted_SPIMI(self, pipeline, compression, track_frequency):
        print("Generating inverted index with SPIMI method...")
        article_line = pipeline.text.split("NEWID=\"")

        for article in article_line:
            if article:
                article_words = article.split()
                id_from_text = article_words[0]
                newid = int(id_from_text[:-2])
                words = article_words[1:]
                freq = collections.Counter(words)

                if compression:
                    # Reassemble the list:
                    article_text = " ".join(words)

                    # Remove any punctuation
                    translator = str.maketrans(dict.fromkeys(string.punctuation))
                    article_text = article_text.translate(translator)
                    words = word_tokenize(article_text)


                if track_frequency:
                    self.article_length[newid] = len(words)

                for word in words:
                    if word in self.inverted_index:
                        self.inverted_index[word].append(newid)
                    else:
                        self.inverted_index[word] = [newid]
                    if track_frequency:
                        # Save the amount of times that word appeared in the article.
                        data_pair = (word, newid)
                        # if data_pair in self.term_frequency:
                            # self.term_frequency[word].append(freq[word])
                        self.term_frequency[data_pair] = freq[word]
                        # else:
                        #     self.term_frequency[word] = [freq[word]]
                        # if newid in self.term_frequency:
                        #     self.term_frequency[newid][word] = freq[word]
                        # else:
                        #     self.term_frequency[newid] = dict()

        # Update the total documents processed
        if track_frequency:
            self.articles_processed = newid

    def single_term_lookup(self, token):
        if token in self.inverted_index:
            return self.inverted_index[token]
        return

    def multiple_term_lookup(self, tokens, method="or"):
        result = []
        for token in tokens:
            lookup = self.single_term_lookup(token)
            if lookup:
                if result:
                    # Intersection
                    if method == "and":
                        result = [x for x in result if x in self.single_term_lookup(token)]

                    # Union
                    if method == "or":
                        result += self.single_term_lookup(token)
                else:
                    result = lookup
            else:
                # Anything intersecting with nothing is nothing
                if method == "and":
                    return None

        # Sort the output for the 'or' operator, so that the document with the most occurrences are first
        if method == "or":
            sorted_results = sorted(result, key=collections.Counter(result).get, reverse=True)
            result = sorted_results
        return result


