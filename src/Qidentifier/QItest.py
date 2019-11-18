import pickle
import nltk

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

def main(sentence):
    f = open('statements_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

    result = classifier.classify(dialogue_act_features("Give me an example of a problem you faced on the job"))
    if result == "whQuestion" or  "ynQuestion":
        return True
    else:
        return False