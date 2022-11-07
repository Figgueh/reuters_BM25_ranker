import math
import time

from itertools import groupby

from nltk import word_tokenize


class BM25:

    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
        self.scores = {}
        self.idf_values = {}
        self.build_idf_table()

        print("Currently getting total document length...")
        self.total_length = self.get_total_length()

    def build_idf_table(self):
        for token in self.inverted_index.inverted_index:
            N = self.inverted_index.articles_processed
            dft = len(set(self.inverted_index.inverted_index[token]))
            self.idf_values[token] = math.log(N/dft, 10)

    def get_termdoc_freq(self, token, articleid):
        # Returns the number of times that token appears in the specified article.
        data_pair = (token, articleid)
        if data_pair in self.inverted_index.term_frequency:
            return self.inverted_index.term_frequency[data_pair]
        return 0

    def get_doc_length(self, articleid):
        # Returns the number of tokens in that article
        return self.inverted_index.article_length[articleid]

    def get_total_length(self):
        # Gets the number of tokens produced overall

        total_tokens = 0
        for article in range(1, self.inverted_index.articles_processed, 1):
            total_tokens += self.get_doc_length(article)

        return total_tokens

    def get_ave_length(self, articleid):
        # Returns the average length for that article
        return self.total_length / self.get_doc_length(articleid)
        # return self.total_length / len(self.inverted_index.article_length)

    # def get_idft_val(self, token, articleid):
    #     return math.log(self.articles_processed/self.get_doc_freq(token, articleid), 10)

    def get_document_frequency(self, token):
        if token in self.inverted_index.inverted_index:
            return len(set(self.inverted_index.inverted_index[token]))



    def generate_BM25_value(self, token, articleid):
        k1 = 1.2
        b = 1

        tftd = self.get_termdoc_freq(token, articleid)
        # tftd = self.inverted_index.term_frequency[(token, articleid)]

        ld = self.get_doc_length(articleid)

        lave = self.get_ave_length(articleid)

        if token in self.idf_values:
            first_part = self.idf_values[token]
        else:
            first_part = 0
        numerator = (k1 + 1) * tftd
        denominator = (k1*((1 - b) + b * (ld / lave)) + tftd)

        if denominator == 0:
            return 0

        second_part = numerator/denominator

        return first_part * second_part

    # def get_doc_score(self):
    #     doc_score = {}
    #     for tokens, articleids in self.inverted_index.inverted_index.items():
    #         for articleid in articleids:
    #             score = self.generate_BM25_value(tokens, articleid)
    #             articleid = str(articleid)
    #             if articleid in doc_score:
    #                 doc_score[articleid] += score
    #             else:
    #                 doc_score[articleid] = score
    #     return doc_score

    # def fit(self):
    #     for token, articleids in self.inverted_index.inverted_index.items():
    #         for article in articleids:
    #             if article in self.scores:
    #                 self.scores[article] += self.generate_BM25_value(token, article)
    #             else:
    #                 self.scores[article] = self.generate_BM25_value(token, article)

    def predict(self, tokens):
        result = {}
        tokens = word_tokenize(tokens)
        for token in tokens:
            if token in self.inverted_index.inverted_index:
                for articleid in self.inverted_index.inverted_index[token]:
                    result[articleid] = self.generate_BM25_value(token, articleid)

        return sorted(result.items(), key=lambda rank:rank[1], reverse=True)