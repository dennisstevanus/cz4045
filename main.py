import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import *
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

text = """"The lightning-struck tower. Calamity. Disaster. Coming nearer all the time."—Prediction of the battle[src] The Battle of the Astronomy Tower,[2] also known as the Battle of the Lightning-Struck Tower, was the second major conflict of the Second Wizarding War. It took place in the topmost part of the Astronomy Tower, a few corridors of the 7th Floor, the Marble Staircase, the Great Hall, the Entrance Hall, and the grounds of Hogwarts School of Witchcraft and Wizardry, in the mountainous region of Scotland, Great Britain on the evening of 30 June, 1997.[1][3] Lord Voldemort secretly organised the attack by ordering sixteen-year-old Death Eater and Hogwarts student Draco Malfoy to assassinate Albus Dumbledore, the only wizard in the world who Voldemort feared. Although his previous attempts at assassination had failed, Draco managed to sneak a number of Death Eaters into Hogwarts via a pair of Vanishing Cabinets in the Room of Requirement, and they encountered a number of Hogwarts teachers, students, Dumbledore's Army members, and Order of the Phoenix members, who had been standing guard at the school at the request of both Dumbledore and Harry Potter. As the Order of the Phoenix and the Death Eaters battled,[3] Severus Snape killed Dumbledore,[4] an act that was later discovered to have been secretly planned between Dumbledore and Snape, as Dumbledore would soon afterwards still have died after putting on Marvolo Gaunt's cursed ring, which was a Horcrux, and was afflicted with a deadly curse that would have eventually killed him anyway.[5]"""

# Please input your pos tagging text, manually from the data set
pos_tagging_text_1 = "The 1994 Triwizard Tournament was the short-lived revival of a magical contest held in 1994 between the three largest wizarding schools of Europe: Hogwarts School of Witchcraft and Wizardry, Durmstrang Institute, and Beauxbatons Academy of Magic, each school being represented by one Champion, although a second champion represented Hogwarts for the first time."
pos_tagging_text_2 = "Selected Champions compete in three tasks — traditionally judged by the Headmasters or Headmistresses of the competing schools — designed to test magical ability, intelligence, and courage. Champions competed for the honour and glory of winning the Tournament, for the Triwizard Cup, and a monetary prize."
pos_tagging_text_3 = "Unlike previous tournaments, this one had restrictions in place in an attempt to stop potential deaths. One of these restrictions was that all applicants had to be over the wizarding age of majority (which is 17), or else they would not be allowed to apply to be Champion."

json_dict = {
    'token': [],
    'stemmed_token': [],
    'segmented_sentence': [],
    'pos_tagged_sentence_1': [],
    'pos_tagged_sentence_2': [],
    'pos_tagged_sentence_3': []
}


# Tokenizer will have text as an input, inputting the token into a json_file and returning a status.
def word_tokenizer(document):
    word_tokenize_set = set(word_tokenize(document))
    for x in word_tokenize_set:
        json_dict['token'].append(x)


# Sentence Segmentation will sentence
def sentence_segmentation(document):
    sentence_tokenizer = PunktSentenceTokenizer()
    sentence_tokenizer.train(document)
    sentence_tokenizer._params.abbrev_types
    segmented_sentence = sentence_tokenizer.tokenize(document)
    for x in segmented_sentence:
        json_dict['segmented_sentence'].append(x)


# Stemmer will stemming the set of token into the set of stemmed_token
def stemmer(tokens):
    porter_stemmer = PorterStemmer()
    stemmed_token = [porter_stemmer.stem(token) for token in tokens]
    for x in stemmed_token:
        json_dict['stemmed_token'].append(x)


# Pos tagging (Choose 3 sentences by yourself and add it on the global variable
def pos_tagger(sentence, dict_key):
    tokens = nltk.word_tokenize(sentence)
    pos_tagged_tokens = nltk.pos_tag(tokens)
    for x in pos_tagged_tokens:
        json_dict[dict_key].append(x)


# Json_converter will make the dictionary into a json format.
# Change the file name when you are inputting the different file
def json_converter(dictionary):
    with open('json_file_1.json', 'w') as json_file:
        json.dump(dictionary, json_file)

# Main Function, just add more function here, to do the stuff
def main():
    word_tokenizer(text)
    stemmer(json_dict['token'])
    sentence_segmentation(text)
    pos_tagger(pos_tagging_text_1, 'pos_tagged_sentence_1')
    pos_tagger(pos_tagging_text_2, 'pos_tagged_sentence_2')
    pos_tagger(pos_tagging_text_3, 'pos_tagged_sentence_3')
    print(json_dict)
    json_converter(json_dict)


if __name__ == "__main__":
    main()
