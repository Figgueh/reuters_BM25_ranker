import string

from nltk import word_tokenize

class InvertedIndex:
    def __init__(self, posting_list=None, pipeline=None, compression=False):
        self.inverted_index = {}
        if posting_list:
            self.generate_inverted_naive(posting_list)
        if pipeline:
            self.generate_inverted_SPIMI(pipeline, compression=compression)

    def generate_inverted_naive(self, posting_list):
        print("Generating inverted index from postings list...")
        for pair in posting_list.postings:
            if pair[1] in self.inverted_index:
                self.inverted_index[pair[1]].append(pair[0])
            else:
                self.inverted_index[pair[1]] = [pair[0]]

    def generate_inverted_SPIMI(self, pipeline, compression):
        print("Generating inverted index with SPIMI method...")
        article_line = pipeline.text.split("NEWID=\"")

        for article in article_line:
            if article:
                article_words = article.split()
                id_from_text = article_words[0]
                newid = int(id_from_text[:-2])
                words = article_words[1:]

                if compression:
                    # Reassemble the list:
                    article_text = " ".join(words)

                    # Remove any punctuation
                    translator = str.maketrans(dict.fromkeys(string.punctuation))
                    article_text = article_text.translate(translator)
                    words = word_tokenize(article_text)

                for word in words:
                    if word in self.inverted_index:
                        self.inverted_index[word].append(newid)
                    else:
                        self.inverted_index[word] = [newid]


    def get_doc_freq(self, token, articleid):
        # Returns the number of times that token appears in the specified article.

        frequency = 0
        for tokens, newids in self.inverted_index.items():
            if token == tokens:
                for newid in newids:
                    if newid == articleid:
                        frequency += 1
        return frequency

    def get_doc_length(self, articleid):
        length = 0
        for tokens, newids in self.inverted_index.items():
            for newid in newids:
                if newid == articleid:
                    length += 1

        return length



