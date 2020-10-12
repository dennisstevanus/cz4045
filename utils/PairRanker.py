import os


class PairRanker:
    negative_words = set()
    positive_words = set()

    def __init__(self, common_pairs: list):
        data_directory = "data"
        parent_dir = os.path.dirname(os.getcwd())

        self.common_pairs = common_pairs

        # Taken from http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
        with open(os.path.join(parent_dir, data_directory, 'negative-words.txt'), 'r') as negative_txt:
            negative_words = negative_txt.readlines()[31:]
            self.negative_words = set(i.strip() for i in negative_words)
            print(self.negative_words)
        with open(os.path.join(parent_dir, data_directory, 'positive-words.txt'), 'r') as negative_txt:
            positive_words = negative_txt.readlines()[31:]
            self.positive_words = set(i.strip() for i in positive_words)
            print(self.positive_words)

    def get_word_sentiment(self, word):
        if word in self.positive_words:
            return 10
        elif word in self.negative_words:
            return -10
        else:
            return 0

    def calculate_weighted_rank(self):
        weighted_result = []
        for pair in self.common_pairs:
            word_1 = pair[0][0]
            word_2 = pair[0][1]
            weight_1 = self.get_word_sentiment(word_1)
            weight_2 = self.get_word_sentiment(word_2)
            count = pair[1]
            score = (weight_1+weight_2)*count
            weighted_result.append((score, (word_1, word_2)))
        print(sorted(weighted_result))


if __name__ == "__main__":
    pair_ranker = PairRanker([(('day', 'pay'), 5), (('films', 'foreign'), 5), (('movies', 'same'), 3), (('day', 'fine'), 3), (('movie', 'different'), 3)]	)
    pair_ranker.calculate_weighted_rank()
