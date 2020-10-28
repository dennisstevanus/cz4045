import os

from utils.PairGetter import PairGetter


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
        mult = 0.1
        for pair in self.common_pairs:
            noun = pair[0]
            noun_count = pair[1]["counter"]
            for adj, adj_count in pair[1]["adj_list"].items():
                adj_weight = self.get_word_sentiment(adj)
                negative_multiplier = -1 if adj_weight < 0 else 1
                count = noun_count * adj_count
                score = ((abs(adj_weight) * count) * mult + count * (1-mult)) * negative_multiplier
                weighted_result.append((score, (noun, adj)))
        result = sorted(weighted_result, reverse=True)
        print(result[:5])
        print(result[-5:])




if __name__ == "__main__":
    pair_getter = PairGetter()
    noun_adj_pairs, _ = pair_getter.get_nouns_adj_pair()
    pair_ranker = PairRanker(noun_adj_pairs)
    pair_ranker.calculate_weighted_rank()
