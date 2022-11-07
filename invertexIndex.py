import collections
import compression

class InvertedIndex:
    def __init__(self, posting_list=None, pipeline=None, is_compressed=False, track_frequency=False):
        self.inverted_index = {}
        self.is_compressed = is_compressed

        if track_frequency:
            self.article_length = {}
            self.articles_processed = 0
            self.term_frequency = {}

        if posting_list:
            self.generate_inverted_naive(posting_list)
        if pipeline:
            self.generate_inverted_SPIMI(pipeline, is_compressed=is_compressed, track_frequency=track_frequency)


    def generate_inverted_naive(self, posting_list):
        print("Generating inverted index from postings list...")
        for pair in posting_list.postings:
            if pair[1] in self.inverted_index:
                self.inverted_index[pair[1]].append(pair[0])
            else:
                self.inverted_index[pair[1]] = [pair[0]]

        # Update the total documents processed
        self.articles_processed = posting_list.postings[-1][0]

    def generate_inverted_SPIMI(self, pipeline, is_compressed, track_frequency):
        if track_frequency:
            print("Generating inverted index and tracking frequency with SPIMI method...")
        else:
            print("Generating inverted index with SPIMI method...")

        article_line = pipeline.text.split("NEWID=\"")

        for article in article_line:
            if article:
                article_words = article.split()
                id_from_text = article_words[0]
                newid = int(id_from_text[:-2])
                words = article_words[1:]

                if is_compressed:
                    # Reassemble the list:
                    article_text = " ".join(words)

                    # Check the compression level
                    if is_compressed == "heavy":
                        words = compression.heavy_compress(article_text)
                    else:
                        words = compression.compress(article_text)

                    # Remove any punctuation
                    # translator = str.maketrans(dict.fromkeys(string.punctuation))
                    # article_text = article_text.translate(translator)
                    # words = word_tokenize(article_text)

                if track_frequency:
                    # Update the length of that article
                    self.article_length[newid] = len(words)

                freq = collections.Counter(words)
                for word in words:
                    if word in self.inverted_index:
                        self.inverted_index[word].append(newid)
                    else:
                        self.inverted_index[word] = [newid]

                    if track_frequency:
                        # Save the amount of times that word appeared in the article.
                        data_pair = (word, newid)
                        self.term_frequency[data_pair] = freq[word]

        if track_frequency:
            # Update the total documents processed
            self.articles_processed = newid

    def single_term_lookup(self, token):
        if token in self.inverted_index:
            return self.inverted_index[token]
        return

    def multiple_term_lookup(self, tokens, method="or"):
        result = []
        if self.is_compressed:
            if self.is_compressed == "heavy":
                tokens = compression.heavy_compress(tokens)
            else:
                tokens = compression.compress(tokens)
        else:
            tokens = tokens.split(" ")

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


