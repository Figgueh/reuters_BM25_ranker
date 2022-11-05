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


def sub1_partA():
    # Start of the SPIMI indexer
    start_time = time.time()
    inverted_index_SPIMI = InvertedIndex(pipeline=text_extractor, compression=True)
    end_time = time.time()

    print(inverted_index_SPIMI.inverted_index)
    print("It took ", (end_time - start_time), " to generate the first 10000 token pairs with the SPIMI indexer")


    # Start of the naive indexer
    naive_start_time = time.time()
    posting = PostingsList(text_extractor, compression=True)
    inverted_index_naive = InvertedIndex(posting_list=posting)
    naive_end_time = time.time()


    print(inverted_index_naive.inverted_index)
    print("It took ", (naive_end_time - naive_start_time), " to generate the first 10000 token pairs with the naive indexer")

def sub1_partB():
    globals.file_pattern = r'reut2-0[0-9][0-9].sgm'
    text_extractor.change_pipe(text_extractor.extract_text())

    fullcorpus_start_time = time.time()
    inverted_index = InvertedIndex(pipeline=text_extractor, compression=False)
    fullcorpus_end_time = time.time()

    print(inverted_index.inverted_index)
    print("It took ", (fullcorpus_end_time - fullcorpus_start_time), " to generate the invertex index with the SPIMI indexer")

sub1_partA()
sub1_partB()
