
corpus_root = r'reuters21578'
file_pattern = r'reut2-000.sgm'
limit = 10000

stopword30 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "page", "you've", "you'll",
              "get", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
              'her', 'hers', 'herself', 'it', "ago", 'its', 'itself']

stopword150 = ["is", "reuter", "reut", "don't", 'should', "should've", 'now', 'can', 'y', 'will', 'just', 'this',
               "could", 'that', "didn't", "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
               'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
               'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
               'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
               'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
               'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
               'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'they',
               'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'describe', 'c', 't', '-', 'u', 'f',
               'd', "appear", 'back', 'became', 'consequently', 'consider', 'cry', 'done', 'downwards', 'high', 'home', 'html',
               'interest', 'kind', 'old', 'obtain', 'fact', 'said', 'second', 'take', 'two', 'one', 'want', 'whom',
               'half', 'great', 'general', 'closer', 'four', 'dare', 'date', 'came', 'call', 'caption',
               'concerning', 'began']