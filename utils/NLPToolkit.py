import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import *
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters


class NLPToolkit:

    def __init__(self, document, save_file="", unique_identifier=""):
        self.json_dict = {
            'unique_identifier': "",
            'token': [],
            'stemmed_token': [],
            'segmented_sentence': [],
            'pos_tagger': [],
        }
        if unique_identifier != "":
            self.json_dict['unique_identifier'] = unique_identifier
        word_tokenize_set = self.word_tokenizer(document)
        for x in word_tokenize_set:
            self.json_dict['token'].append(x)

        stemmed_token = self.stemmer(self.json_dict['token'])
        for x in stemmed_token:
            self.json_dict['stemmed_token'].append(x)

        segmented_sentence = self.sentence_segmentation(document)
        for x in segmented_sentence:
            self.json_dict['segmented_sentence'].append(x)

        for i in segmented_sentence:
            pos_tagged_tokens = self.pos_tagger(i)
            self.json_dict['pos_tagger'].append(pos_tagged_tokens)

        # print(self.json_dict)
        if save_file != "":
            self.json_converter(self.json_dict, save_file)

    def get_json(self):
        return self.json_dict

    # Tokenizer will have text as an input, inputting the token into a json_file and returning a status.
    @staticmethod
    def word_tokenizer(document):
        word_tokenize_set = set(word_tokenize(document))
        return word_tokenize_set

    # Sentence Segmentation will sentence
    @staticmethod
    def sentence_segmentation(document):
        sentence_tokenizer = PunktSentenceTokenizer()
        sentence_tokenizer.train(document)
        sentence_tokenizer._params.abbrev_types
        segmented_sentence = sentence_tokenizer.tokenize(document)
        return segmented_sentence

    # Stemmer will stemming the set of token into the set of stemmed_token
    @staticmethod
    def stemmer(tokens):
        porter_stemmer = PorterStemmer()
        stemmed_token = [porter_stemmer.stem(token) for token in tokens]
        return stemmed_token

    # Pos tagging (Choose 3 sentences by yourself and add it on the global variable
    @staticmethod
    def pos_tagger(sentence):
        tokens = nltk.word_tokenize(sentence)
        pos_tagged_tokens = nltk.pos_tag(tokens)
        return pos_tagged_tokens

    # Json_converter will make the dictionary into a json format.
    # Change the file name when you are inputting the different file
    @staticmethod
    def json_converter(dictionary, filename='json_file_1.json'):
        with open(filename, 'w+', encoding='utf16') as json_file:
            json.dump(dictionary, json_file)
