# Identify different kinds of statements using supervised learning mechanisms.
# Need to improve further to identify questions more accurately

import nltk

# Some packages need to be installed
# nltk.download('punkt')

# get online corpus
posts = nltk.corpus.nps_chat.xml_posts()[:10000]
# print(posts[10000])

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
print(train_set[:10])
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))

# identifying a sample statement
print(classifier.classify(dialogue_act_features("when can you finish the project")))

print("finished")