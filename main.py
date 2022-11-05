import time

import globals
from pipleline import Pipeline
from postingList import PostingsList
from invertexIndex import InvertedIndex

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
    inverted_index = InvertedIndex(pipeline=text_extractor, compression=False)
    fullcorpus_end_time = time.time()

    if verbose:
        print(inverted_index.inverted_index)
    print("It took ", (fullcorpus_end_time - fullcorpus_start_time), " to generate the invertex index with the SPIMI indexer")

    return inverted_index

with_compression = sub1_partA()
without_compression = sub1_partB()

#subproject2
def subproject2():
    print(with_compression.get_doc_freq("to", 1))
    print(with_compression.get_doc_length(1))


subproject2()
