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
            # print(self.negative_words)
        with open(os.path.join(parent_dir, data_directory, 'positive-words.txt'), 'r') as negative_txt:
            positive_words = negative_txt.readlines()[31:]
            self.positive_words = set(i.strip() for i in positive_words)
            # print(self.positive_words)

    def get_word_sentiment(self, word):
        if word in self.positive_words:
            return 10
        elif word in self.negative_words:
            return -10
        else:
            return 0

    def calculate_weighted_result_with_heuristic(self):
        weighted_result = []
        mult = 0.1
        for pair in self.common_pairs:
            noun = pair[0]
            noun_count = pair[1]["review_appearance"]
            cum_pos_adj = 0
            cum_neg_adj = 0
            cum_net_adj = 0
            for adj, adj_count in pair[1]["adj_list"].items():
                adj_weight = self.get_word_sentiment(adj)
                if adj_weight < 0:
                    cum_neg_adj += 1
                elif adj_weight > 0:
                    cum_pos_adj += 1
                else:
                    cum_net_adj += 1
            for adj, adj_count in pair[1]["adj_list"].items():
                adj_weight = self.get_word_sentiment(adj)
                if adj_weight < 0:
                    adj_count += cum_neg_adj
                elif adj_weight > 0:
                    adj_count += cum_pos_adj
                else:
                    adj_count += cum_net_adj
                negative_multiplier = -1 if adj_weight < 0 else 1
                count = noun_count * adj_count
                score = ((abs(adj_weight) * count) * mult + count * (1 - mult)) * negative_multiplier
                weighted_result.append((score, (noun, adj)))
        result = sorted(weighted_result, reverse=True)
        # print(result[:10])
        # print(result[-10:])
        return result

    def calculate_weighted_result(self):
        weighted_result = []
        mult = 0.1
        for pair in self.common_pairs:
            noun = pair[0]
            noun_count = pair[1]["review_appearance"]

            for adj, adj_count in pair[1]["adj_list"].items():
                adj_weight = self.get_word_sentiment(adj)
                negative_multiplier = -1 if adj_weight < 0 else 1
                count = noun_count * adj_count
                score = ((abs(adj_weight) * count) * mult + count * (1 - mult)) * negative_multiplier
                weighted_result.append((score, (noun, adj)))
        result = sorted(weighted_result, reverse=True)
        # print(result[:10])
        # print(result[-10:])
        return result

    @staticmethod
    def pprint_rank_result(rankings):
        for rank, item in enumerate(rankings):
            score, (noun, adj) = item
            print("{}. < {} - {} > with score of {}".format(rank+1, noun, adj, score))

    def get_top_5(self, weighted_results):
        top_5_positive = self.get_distinct_top_5(weighted_results)
        top_5_negative = self.get_distinct_top_5(reversed(weighted_results))
        print("top 5 positive:")
        self.pprint_rank_result(top_5_positive)
        print("top 5 negative=")
        self.pprint_rank_result(top_5_negative)
        abs_score = sorted([(abs(i[0]), i[1]) for i in top_5_positive + top_5_negative], reverse=True)
        final = self.get_distinct_top_5(abs_score, max_duplicate=2)
        print("Final results:")
        self.pprint_rank_result(final)
        return [i[1] for i in final]

    def get_distinct_top_5(self, weighted_results, max_duplicate=1):
        nouns = dict()
        result = []
        for i in weighted_results:
            if i[1][0] not in nouns:
                nouns[i[1][0]] = 1
                result.append(i)
            else:
                if nouns[i[1][0]] < max_duplicate:
                    result.append(i)
                nouns[i[1][0]] += 1
            if len(result) >= 5:
                break
        return result


if __name__ == "__main__":
    pair_getter = PairGetter()
    noun_adj_pairs, _ = pair_getter.get_nouns_adj_pair()
    pair_ranker = PairRanker(noun_adj_pairs)

    weighted_list = pair_ranker.calculate_weighted_result()
    print("Top 5 pairs with original scoring system:")
    result1 = pair_ranker.get_top_5(weighted_list)

    print()
    weighted_list_with_heuristic = pair_ranker.calculate_weighted_result_with_heuristic()
    print("Top 5 pairs with heuristic: ")
    result2 = pair_ranker.get_top_5(weighted_list_with_heuristic)

