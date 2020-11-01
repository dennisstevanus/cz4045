from utils.NLPToolkit import NLPToolkit
from collections import Counter


# count occurrence of all possible noun-adjective pairs in a sentence
def count_noun_adj_pairs_all(noun_adj_pairs_map, tag_list):
    for x in range(len(tag_list)):
        for y in range(x + 1, len(tag_list)):
            if (tag_list[y][0], tag_list[x][0]) in noun_adj_pairs_map:
                noun_adj_pairs_map[(tag_list[y][0], tag_list[x][0])] += 1
            elif tag_list[x][1] in {"JJ", "JJR", "JJS"} and tag_list[y][1] in {"NN", "NNS", "NNP", "NNPS"}:
                noun_adj_pairs_map[(tag_list[y][0], tag_list[x][0])] = 1
    return noun_adj_pairs_map


# count occurrence of noun-adjective bigram pairs
def count_noun_adj_pairs_bigram(noun_adj_pairs_map, tag_list):
    tag_bigrams = tk.generate_bigrams(tag_list)
    for (a, b) in tag_bigrams:
        if (b[0], a[0]) in noun_adj_pairs_map:
            noun_adj_pairs_map[(b[0], a[0])] += 1
        elif a[1] in {"JJ", "JJR", "JJS"} and b[1] in {"NN", "NNS", "NNP", "NNPS"}:
            noun_adj_pairs_map[(b[0], a[0])] = 1
    return noun_adj_pairs_map


tk = NLPToolkit()

with open("../../data/Noun-Adjective Pairs - Trustpilot.txt", "r") as f:
    lines = f.readlines()

text_list = []
for line in lines:
    text_list.append(line.strip())

noun_adj_pairs_map_all = {}
noun_adj_pairs_map_bigram = {}
for text in text_list:
    sentence_list = tk.sentence_segmentation(text)
    for sentence in sentence_list:
        tag_list = tk.pos_tagger(sentence)
        count_noun_adj_pairs_all(noun_adj_pairs_map_all, tag_list)
        count_noun_adj_pairs_bigram(noun_adj_pairs_map_bigram, tag_list)

counter_all = Counter(noun_adj_pairs_map_all)
counter_bigrams = Counter(noun_adj_pairs_map_bigram)

print("Most common noun-adjective pairs")
print(counter_all.most_common(25))
print("Most common noun-adjective bigrams")
print(counter_bigrams.most_common(25))
