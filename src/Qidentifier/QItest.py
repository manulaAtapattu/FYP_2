import pickle
import nltk

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

def main(sentence):
    #f = open('../src/Qidentifier/statements_classifier.pickle', 'rb')
    f = open('../src/Qidentifier/statements_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

    result = classifier.classify(dialogue_act_features(sentence))
    if result == "whQuestion" or  "ynQuestion":
        print("Question identified ")
        return True
    else:
        return False

main("Good morning")