from pprint import pprint

from nltk.corpus import wordnet
import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import *
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters


class NLPToolkit:

    def __init__(self, document=None, save_file="", unique_identifier="", print=False):
        if document is not None:
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

            if print:
                pprint(self.json_dict)
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

    # Generate bigrams iterator of a sequence/text
    @staticmethod
    def generate_bigrams(sequence):
        bigrams = nltk.bigrams(sequence)
        return bigrams

    # Json_converter will make the dictionary into a json format.
    # Change the file name when you are inputting the different file
    @staticmethod
    def json_converter(dictionary, filename='json_file_1.json'):
        with open(filename, 'w+', encoding='utf16') as json_file:
            json.dump(dictionary, json_file)

    @staticmethod
    def noun_phrase_getter(sentence):
        lemmatizer = nltk.WordNetLemmatizer()
        tokens = [nltk.word_tokenize(sent) for sent in [sentence]]
        postag = [nltk.pos_tag(sent) for sent in tokens][0]

        # Rule for NP chunk and VB Chunk
        grammar = r"""
            NBAR:
                {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
                
            NP:
                {<NBAR>}
                {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        """
        # Chunking
        cp = nltk.RegexpParser(grammar)

        # the result is a tree
        tree = cp.parse(postag)

        def leaves(tree):
            """Finds NP (nounphrase) leaf nodes of a chunk tree."""
            for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
                yield subtree.leaves()

        def get_word_postag(word):
            if nltk.pos_tag([word])[0][1].startswith('J'):
                return wordnet.ADJ
            if nltk.pos_tag([word])[0][1].startswith('V'):
                return wordnet.VERB
            if nltk.pos_tag([word])[0][1].startswith('N'):
                return wordnet.NOUN
            else:
                return wordnet.NOUN

        def normalise(word):
            """Normalises words to lowercase and stems and lemmatizes it."""
            word = word.lower()
            postag = get_word_postag(word)
            word = lemmatizer.lemmatize(word, postag)
            return word

        def get_terms(tree):
            for leaf in leaves(tree):
                terms = [normalise(w) for w, t in leaf]
                yield terms

        terms = get_terms(tree)

        features = []
        for term in terms:
            _term = ''
            for word in term:
                _term += ' ' + word
            features.append(_term.strip())
        # pprint(features)
        return features


if __name__ == "__main__":
    text = """"The lightning-struck tower. Calamity. Disaster. Coming nearer all the time."—Prediction of the battle[src] The Battle of the Astronomy Tower,[2] also known as the Battle of the Lightning-Struck Tower, was the second major conflict of the Second Wizarding War. It took place in the topmost part of the Astronomy Tower, a few corridors of the 7th Floor, the Marble Staircase, the Great Hall, the Entrance Hall, and the grounds of Hogwarts School of Witchcraft and Wizardry, in the mountainous region of Scotland, Great Britain on the evening of 30 June, 1997.[1][3] Lord Voldemort secretly organised the attack by ordering sixteen-year-old Death Eater and Hogwarts student Draco Malfoy to assassinate Albus Dumbledore, the only wizard in the world who Voldemort feared. Although his previous attempts at assassination had failed, Draco managed to sneak a number of Death Eaters into Hogwarts via a pair of Vanishing Cabinets in the Room of Requirement, and they encountered a number of Hogwarts teachers, students, Dumbledore's Army members, and Order of the Phoenix members, who had been standing guard at the school at the request of both Dumbledore and Harry Potter. As the Order of the Phoenix and the Death Eaters battled,[3] Severus Snape killed Dumbledore,[4] an act that was later discovered to have been secretly planned between Dumbledore and Snape, as Dumbledore would soon afterwards still have died after putting on Marvolo Gaunt's cursed ring, which was a Horcrux, and was afflicted with a deadly curse that would have eventually killed him anyway.[5]"""
    NLPToolkit(text, save_file="../results/result_test.json", print=True)
