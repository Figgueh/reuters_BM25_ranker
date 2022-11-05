import string
from nltk import word_tokenize


class PostingsList:
    def __init__(self, pipeline, compression=False):
        print("Generating a postings list of the first 10000 pairs...")
        self.generate_postings(pipeline.text, compression)


    def generate_postings(self, text, compression="True"):
        # Takes a really long string of the form
        # NEWID="x"> [ARTICLE TEXT]
        # Then sets the postings list

        self.postings = []
        article_line = text.split("NEWID=\"")

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
                    self.postings.append([newid, word])




