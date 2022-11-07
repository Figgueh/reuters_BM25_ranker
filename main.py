import time
import globals
import pipeline
from pipeline import Pipeline
from postingList import PostingsList
from invertexIndex import InvertedIndex

from BM25 import BM25

# Extracted text will be use for both version of the indexers
text_extractor = Pipeline()

# Preprocess the text in our pipeline to first produce a postings list
# consisting of the first 10k pairs, Then reconstructs the data to form
# a sub-corpus that will be used by both indexing methods to ensure that
# the work done by both methods is fair.
first_10k = text_extractor.extract_first_10k(text_extractor.text)
text_extractor.change_pipe(first_10k)

def sub1_partA():
    # Start of the SPIMI indexer
    start_time = time.time()
    inverted_index_SPIMI = InvertedIndex(pipeline=text_extractor, is_compressed=True)
    end_time = time.time()

    print("It took ", (end_time - start_time), " to generate the first 10000 token pairs with the SPIMI indexer")

    # Start of the naive indexer
    naive_start_time = time.time()
    posting = PostingsList(text_extractor, compression=True)
    inverted_index_naive = InvertedIndex(posting_list=posting)
    naive_end_time = time.time()

    print("It took ", (naive_end_time - naive_start_time),
          " to generate the first 10000 token pairs with the naive indexer")

    # Save results to a file
    print("Currently saving the results for the first 10K... \n\n")
    pipeline.save_index("first10K/SPIMI_index", inverted_index_SPIMI.inverted_index)
    pipeline.save_index("first10K/naive_postings", posting.postings)
    pipeline.save_index("first10K/naive_index", inverted_index_naive.inverted_index)


def sub1_partB(verbose=False):
    print("Start of subproject 1 part B:")

    # Prepare the pipeline to get all the documents in the reuters corpus
    globals.file_pattern = r'reut2-0[0-9][0-9].sgm'
    text_extractor.change_pipe(text_extractor.extract_text())

    # Generate a new index without any compression
    fullcorpus_start_time = time.time()
    uncompressed_index = InvertedIndex(pipeline=text_extractor, is_compressed=False, track_frequency=False)
    fullcorpus_end_time = time.time()

    print("It took", (fullcorpus_end_time - fullcorpus_start_time),
          "to generate the uncompressed index with the SPIMI indexer")

    print("Currently saving the results for the uncompressed index... \n\n")
    pipeline.save_index("uncompressed/SPIMI_index", uncompressed_index.inverted_index)


# Execute subproject 1
sub1_partA()
sub1_partB()


def subproject2():
    compression_level = "heavy"
    # compression_level = True

    indexers = {
        "with compression": InvertedIndex(pipeline=text_extractor, is_compressed=compression_level, track_frequency=True),
        "without compression": InvertedIndex(pipeline=text_extractor, is_compressed=False, track_frequency=True)
    }
    queries = [
        # "Democrats' welfare and healthcare reform policies",
        # "Drug company bankruptcies",
        # "George Bush",
        # "alleviating drought",
        "president Lincon",
        # "Inc said they plan to form a venture to manage the money market"
    ]
    bool_methods = ["and", "or"]

    for method, indexer in indexers.items():
        print(f'Currently ranking results {method}... ')
        scorer = BM25(indexer)


        # Start of ranked retrial
        print("Currently calculating rank of queries...")
        for query in queries:
            result = scorer.predict(query)
            print(f'Saved ranked results for query "{query}"')
            pipeline.save_query_results(method, "ranked", query, result)
        print("\n")

        # Start of boolean retrial
        print("Currently generating unranked boolean retrieval of queries...")
        for query in queries:
            for bool_operation in bool_methods:
                result = indexer.multiple_term_lookup(query, bool_operation)
                pipeline.save_query_results(method, bool_operation, query, result)


subproject2()
