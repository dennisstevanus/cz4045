# %%

import pandas as pd
import requests
import numpy as np
import json
import codecs

# %%

token = []
stemmed_token = []
segmented_sentence = []

for x in range(1, 21):
    file_name = 'results/Python StackOverflow/' + str(x) + '.json'
    with open(file_name, 'r', encoding='utf-16') as json_file:
        data = json.load(json_file)
        for y in data['token']:
            token.append(y)
        for z in data['stemmed_token']:
            stemmed_token.append(z)
        for a in data['segmented_sentence']:
            segmented_sentence.append(a)

tokens = list(set(token))
stemmed_tokens = list(set(stemmed_token))

df_token = pd.DataFrame(
    {
        "token": tokens
    }
)

df_stemmed_token = pd.DataFrame(
    {
        "stemmed_token": stemmed_tokens
    }
)

# %%

token_dict = dict.fromkeys(tokens, 0)
stemmed_token_dict = dict.fromkeys(stemmed_tokens, 0)

for sentence in segmented_sentence:
    for token in tokens:
        counted_token = sentence.count(token)
        token_dict[token] += counted_token
    for stemmed_token in stemmed_tokens:
        counted_stemmed_token = sentence.count(stemmed_token)
        stemmed_token_dict[stemmed_token] += counted_stemmed_token

df_token['count_token'] = df_token['token'].map(token_dict)

df_stemmed_token['count_stemmed_token'] = df_stemmed_token['stemmed_token'].map(stemmed_token_dict)

# %%

token_sorted_values = df_token.sort_values(by=['count_token'], ascending=False)
hundred_token_sorted_values = token_sorted_values['token'].head(100).tolist()
# token_sorted_values.head(100)

# %%

stemmed_token_sorted_values = df_stemmed_token.sort_values(by=['count_stemmed_token'], ascending=False)
hundred_stemmed_token_sorted_values = stemmed_token_sorted_values['stemmed_token'].head(100).tolist()
# stemmed_token_sorted_values.head(100)

# %%

# Percentage existence of tokens also in stemmed tokens
set_token = set(hundred_token_sorted_values)
set_stemmed_token = set(hundred_stemmed_token_sorted_values)
intersection_of_token = set_token.intersection(set_stemmed_token)
print("Stemmed Token of Top 100 that is part of Token of Top 100")
print(len(intersection_of_token) / len(hundred_token_sorted_values))

# %%

set_tokens = set(tokens)
set_stemmed_tokens = set(stemmed_tokens)
reduced_tokens = set_tokens - set_stemmed_tokens
print("Reduced_tokens divided by Set of tokens")
len(reduced_tokens) / len(set_tokens)

# %%

length_token = 0
length_of_token = []
for x in tokens:
    if (len(x) > length_token):
        length_token = len(x)

for x in range(1, length_token + 1):
    length_of_token.append(x)

df_length_of_token = pd.DataFrame(
    {
        "length": length_of_token
    })

length_of_token_dict = dict.fromkeys(length_of_token, 0)

for x in tokens:
    length_of_token_dict[len(x)] += 1

df_length_of_token['count'] = df_length_of_token['length'].map(length_of_token_dict)

print("X axis: Length of Token. Y axis: Number of tokens each length")
df_length_of_token.plot(kind='bar', x='length', y='count')

# %%

print("Row that has highest count")
df_length_of_token['count'].argmax()

# %%

print("Row that has highest count")
df_length_of_token.loc[[6]]

# %%

length_stemmed_token = 0
length_of_stemmed_token = []
for x in stemmed_tokens:
    if (len(x) > length_stemmed_token):
        length_stemmed_token = len(x)

for y in range(1, length_stemmed_token + 1):
    length_of_stemmed_token.append(y)

df_length_of_stemmed_token = pd.DataFrame(
    {
        "length": length_of_stemmed_token
    })

length_of_stemmed_token_dict = dict.fromkeys(length_of_stemmed_token, 0)

for z in stemmed_tokens:
    length_of_stemmed_token_dict[len(z)] += 1

df_length_of_stemmed_token['count'] = df_length_of_stemmed_token['length'].map(length_of_stemmed_token_dict)

print("X axis: Length of Stemmed Token. Y axis: Number of Stemmed tokens each length")
df_length_of_stemmed_token.plot(kind='bar', x='length', y='count')

# %%

print("Row that has highest count")
df_length_of_stemmed_token['count'].argmax()

# %%

print("Row that has highest count")
df_length_of_stemmed_token.loc[[3]]

# %%

length_sentence_per_token = 0
length_of_sentence_per_token = []

for x in segmented_sentence:
    # Length per sentence using token
    length_per_sentence = 0
    for y in tokens:
        if y in x:
            length_per_sentence += 1
    if (length_per_sentence > length_sentence_per_token):
        length_sentence_per_token = length_per_sentence

for z in range(1, length_sentence_per_token + 1):
    length_of_sentence_per_token.append(z)

print(length_of_sentence_per_token)

df_length_of_sentence = pd.DataFrame(
    {
        "length": length_of_sentence_per_token
    })

length_of_sentence_per_token_dict = dict.fromkeys(length_of_sentence_per_token, 0)

for s in segmented_sentence:
    length_per_sentence = 0
    for t in tokens:
        if t in s:
            length_per_sentence += 1
    length_of_sentence_per_token_dict[length_per_sentence] += 1

df_length_of_sentence['count'] = df_length_of_sentence['length'].map(length_of_sentence_per_token_dict)
print("X axis: Length of a sentence in tokens. Y axis: Number of sentences that has this number of tokens")
df_length_of_sentence.plot(kind='hist', bins=30, x='length', y='count')

# %%

print("Row that has highest count")
df_length_of_sentence['count'].argmax()

# %%

print("Highest count with the length of the tokens inside in the sentence")
df_length_of_sentence.loc[[35]]

# %%


