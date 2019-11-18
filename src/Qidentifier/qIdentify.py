import nltk
import csv
import random

nltk.download('nps_chat')
posts = nltk.corpus.nps_chat.xml_posts()[:10000]

whlist = []
with open('whdb.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        whlist.append(row[0])

ynlist = []
with open('yndb.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        ynlist.append(row[0])

with open('dataSet.csv', mode='w', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for j in nltk.corpus.nps_chat.xml_posts():
        if j.get('class') == "whQuestion":
            data_writer.writerow([j.text, j.get('class')])
        elif j.get('class') == "ynQuestion":
            data_writer.writerow([j.text, j.get('class')])
        elif j.get('class') == "Statement":
            data_writer.writerow([j.text, j.get('class')])
        else:
            data_writer.writerow([j.text, "Other"])
    for j in whlist:
        data_writer.writerow([j, "whQuestion"])
    for j in ynlist:
        data_writer.writerow([j, "ynQuestion"])

fid = open("dataSet.csv", "r")
li = fid.readlines()
fid.close()

random.shuffle(li)

fid = open("shuffled_dataSet.csv", "w")
writer = csv.DictWriter(
    fid, fieldnames=["st", "type"])
writer.writeheader()
fid.writelines(li)
fid.close()

datalist = []
with open("shuffled_dataSet.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nwList = []
        nwList.append(dict(row)['st'])
        nwList.append(dict(row)['type'])
        datalist.append(nwList)
csvfile.close()

nltk.download('punkt')


def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features


featuresets = [(dialogue_act_features(post[0]), post[1]) for post in datalist]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(f"accuracy : {nltk.classify.accuracy(classifier, test_set)}")

#print(classifier.classify(dialogue_act_features("Can you do it?")))

import pickle
f = open('statements_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()