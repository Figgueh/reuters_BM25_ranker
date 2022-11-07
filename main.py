import time

import globals
from pipleline import Pipeline
from postingList import PostingsList
from invertexIndex import InvertedIndex

from BM25 import BM25

# Extracted text will be use for both version of the indexers
# Some preprocessing TODO:: FILL
text_extractor = Pipeline()
first_10k = text_extractor.extract_first_10k(text_extractor.text)
text_extractor.change_pipe(first_10k)


def sub1_partA(verbose=False):
    # Start of the SPIMI indexer
    start_time = time.time()
    inverted_index_SPIMI = InvertedIndex(pipeline=text_extractor, compression=True)
    end_time = time.time()

    if verbose:
        print(inverted_index_SPIMI.inverted_index)
    print("It took ", (end_time - start_time), " to generate the first 10000 token pairs with the SPIMI indexer")


    # Start of the naive indexer
    naive_start_time = time.time()
    posting = PostingsList(text_extractor, compression=True)
    inverted_index_naive = InvertedIndex(posting_list=posting)
    naive_end_time = time.time()

    if verbose:
        print(inverted_index_naive.inverted_index)
    print("It took ", (naive_end_time - naive_start_time), " to generate the first 10000 token pairs with the naive indexer")

    return inverted_index_naive

def sub1_partB(verbose=False):
    globals.file_pattern = r'reut2-0[0-9][0-9].sgm'
    text_extractor.change_pipe(text_extractor.extract_text())

    fullcorpus_start_time = time.time()
    inverted_index = InvertedIndex(pipeline=text_extractor, compression=False, track_frequency=False)
    fullcorpus_end_time = time.time()

    if verbose:
        print(inverted_index.inverted_index)
    print("It took ", (fullcorpus_end_time - fullcorpus_start_time), " to generate the invertex index with the SPIMI indexer")

    return inverted_index

# with_compression = sub1_partA()
# without_compression = sub1_partB()

#subproject2
def subproject2():
    globals.file_pattern = r'reut2-0[0-9][0-9].sgm'
    text_extractor.change_pipe(text_extractor.extract_text())
    without_compression = InvertedIndex(pipeline=text_extractor, compression=False, track_frequency=True)
    scorer = BM25(without_compression)

    print(scorer.get_termdoc_freq("to", 1))
    print(scorer.get_doc_length(1))
    print(scorer.get_ave_length(1))
    print("doc freq:", scorer.get_document_frequency("Comissaria"))

    print(scorer.generate_BM25_value("Comissaria", 1))
    print(scorer.generate_BM25_value("and", 1))

    print(without_compression.single_term_lookup("and"))
    print(without_compression.single_term_lookup("or"))
    tokens = ["and", "or"]
    # print(without_compression.multiple_term_lookup(tokens, method="and"), "\n")

    start_time = time.time()
    print("Generating BM25 for each article...")
    scorer.fit()
    end_time = time.time()
    print("It took ", (end_time - start_time), " to generate the BM25 rank for all the articles.")


    print(scorer.get_doc_score())


    def query_lookup():
        # CHANGE AFTER
        SPIMI_indexer = without_compression
        indexer = SPIMI_indexer
        queries = [
            "Democrats' welfare and healthcare reform policies",
            "Drug company bankruptcies",
            "George Bush",
            "alleviating the drought since"
        ]

        # unranked boolean retrieval
        for query in queries:
            print(f'"{query}" documents where all keywords are found: {indexer.multiple_term_lookup(query.split(" "), "and")}')
            print(f'"{query}" documents where at least one keyword is found: {indexer.multiple_term_lookup(query.split(" "), "or")} \n')


    # query_lookup()




subproject2()
