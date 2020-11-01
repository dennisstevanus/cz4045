import os
from pprint import pprint

from utils.NLPToolkit import NLPToolkit


class PairGetter:
    def __init__(self, filename="Noun-Adjective Pairs - Trustpilot.txt"):
        data_directory = "data"
        parent_dir = os.path.dirname(os.getcwd())
        with open(os.path.join(parent_dir, data_directory, filename), "r", encoding="utf-16") as f:
            lines = f.readlines()
        self.review_list = []
        for line in lines:
            self.review_list.append(line.strip())
        # print(self.review_list)
        # self.review_list = self.review_list[:2]

        self.tk = NLPToolkit()

    def get_noun_phrases(self):
        noun_phrase_map = dict()
        for review_no, review in enumerate(self.review_list, start=0):
            sentence_list = self.tk.sentence_segmentation(review)
            for sentence_no, sentence in enumerate(sentence_list, start=0):
                noun_phrases = self.tk.noun_phrase_getter(sentence)
                for noun_phrase in noun_phrases:
                    if noun_phrase in noun_phrase_map:
                        noun_phrase_map[noun_phrase]["counter"] += 1
                        if noun_phrase_map[noun_phrase]["occurrences"][-1][0] != review_no:
                            noun_phrase_map[noun_phrase]["review_appearance"] += 1
                        noun_phrase_map[noun_phrase]["occurrences"].append((review_no, sentence_no))
                    else:
                        noun_phrase_map[noun_phrase] = {
                            "counter": 1,
                            "review_appearance": 1,
                            "occurrences": [(review_no, sentence_no), ]
                        }
        noun_phrase_list = [(k, {"counter": v["counter"], "review_appearance": v["review_appearance"]}) for k, v in
                            sorted(noun_phrase_map.items(), key=lambda item: item[1]["review_appearance"],
                                   reverse=True)]
        # pprint(noun_phrase_list)
        return noun_phrase_list

    def get_nouns(self):
        noun_map = dict()
        for review_no, review in enumerate(self.review_list, start=0):
            sentence_list = self.tk.sentence_segmentation(review)
            for sentence_no, sentence in enumerate(sentence_list, start=0):
                tag_list = self.tk.pos_tagger(sentence)
                for i in range(len(tag_list)):
                    if tag_list[i][1] in {"NN", "NNS", "NNP", "NNPS"}:
                        noun = tag_list[i][0]
                        if noun in noun_map:
                            noun_map[noun]["counter"] += 1
                            if noun_map[noun]["occurrences"][-1][0] != review_no:
                                noun_map[noun]["review_appearance"] += 1
                            noun_map[noun]["occurrences"].append((review_no, sentence_no))
                            # noun_map[noun]["occurrences"].append((review_no, sentence_no))
                        else:
                            noun_map[noun] = {
                                "counter": 1,
                                "review_appearance": 1,
                                "adj_list": dict(),
                                "adj_count": 0,
                                "occurrences": [(review_no, sentence_no), ]
                            }
        # pprint(noun_map)
        noun_list = sorted(noun_map.items(), key=lambda item: item[1]["counter"], reverse=True)

        return noun_list, noun_map

    def get_nouns_adj_pair(self):
        _, result_map = self.get_nouns()
        for review_no, review in enumerate(self.review_list, start=0):
            sentence_list = self.tk.sentence_segmentation(review)
            for sentence_no, sentence in enumerate(sentence_list, start=0):
                tag_list = self.tk.pos_tagger(sentence)

                for i in range(len(tag_list)):
                    if tag_list[i][1] in {"JJ", "JJR", "JJS"}:
                        adj = tag_list[i][0]
                        nouns = set()
                        for j in range(len(tag_list)):
                            if tag_list[j][1] in {"NN", "NNS", "NNP", "NNPS"}:
                                noun = tag_list[j][0]
                                if noun in nouns:
                                    continue
                                nouns.add(noun)
                                result_map[noun]["adj_count"] += 1
                                if adj in result_map[noun]["adj_list"]:
                                    result_map[noun]["adj_list"][adj] += 1
                                else:
                                    result_map[noun]["adj_list"][adj] = 1

        result_list = sorted(result_map.items(), key=lambda item: item[1]["adj_count"] * item[1]["counter"],
                             reverse=True)
        # pprint(result_list[:10])
        return result_list, result_map


if __name__ == "__main__":
    pair_getter = PairGetter()
    result, _ = pair_getter.get_nouns_adj_pair()
    pprint(result[:10])
