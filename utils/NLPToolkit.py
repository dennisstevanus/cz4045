import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import *
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters


class NLPToolkit:
    json_dict = {
        'token': [],
        'stemmed_token': [],
        'segmented_sentence': [],
    }

    def __init__(self, document, save_file=""):
        self.word_tokenizer(document)
        self.stemmer(self.json_dict['token'])
        self.sentence_segmentation(document)
        self.pos_tagger(document, 'pos_tagged_document')
        # self.pos_tagger(pos_tagging_text_1, 'pos_tagged_sentence_1')
        # self.pos_tagger(pos_tagging_text_2, 'pos_tagged_sentence_2')
        # self.pos_tagger(pos_tagging_text_3, 'pos_tagged_sentence_3')
        print(self.json_dict)
        if save_file != "":
            self.json_converter(self.json_dict, save_file)

    # Tokenizer will have text as an input, inputting the token into a json_file and returning a status.
    def word_tokenizer(self, document):
        word_tokenize_set = set(word_tokenize(document))
        for x in word_tokenize_set:
            self.json_dict['token'].append(x)

    # Sentence Segmentation will sentence
    def sentence_segmentation(self, document):
        sentence_tokenizer = PunktSentenceTokenizer()
        sentence_tokenizer.train(document)
        sentence_tokenizer._params.abbrev_types
        segmented_sentence = sentence_tokenizer.tokenize(document)
        for x in segmented_sentence:
            self.json_dict['segmented_sentence'].append(x)

    # Stemmer will stemming the set of token into the set of stemmed_token
    def stemmer(self, tokens):
        porter_stemmer = PorterStemmer()
        stemmed_token = [porter_stemmer.stem(token) for token in tokens]
        for x in stemmed_token:
            self.json_dict['stemmed_token'].append(x)

    # Pos tagging (Choose 3 sentences by yourself and add it on the global variable
    def pos_tagger(self, sentence, dict_key):
        tokens = nltk.word_tokenize(sentence)
        pos_tagged_tokens = nltk.pos_tag(tokens)
        self.json_dict[dict_key] = []
        for x in pos_tagged_tokens:
            self.json_dict[dict_key].append(x)

    # Json_converter will make the dictionary into a json format.
    # Change the file name when you are inputting the different file
    @staticmethod
    def json_converter(dictionary, filename ='json_file_1.json'):
        with open(filename, 'w') as json_file:
            json.dump(dictionary, json_file)

