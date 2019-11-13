import matplotlib.pyplot as plt
import numpy as np
import os
import re
import string
import keras
from pathlib import Path

from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
plt.style.use('seaborn')
# MAX_NUM_WORDS     = 15000
MAX_NUM_WORDS     = 1200
EMBEDDING_DIM     = 300
#MAX_SEQ_LENGTH    = 500
MAX_SEQ_LENGTH    = 15
USE_GLOVE         = True
#KERNEL_SIZES      = [3,4,5]
KERNEL_SIZES      = [2,3]
#FEATURE_MAPS      = [100,100,100]
FEATURE_MAPS      = [20,20]

# CHAR-level
USE_CHAR          = False
ALPHABET          = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}"
ALPHABET_SIZE     = len(ALPHABET)
CHAR_MAX_LENGTH   = 1600
CHAR_KERNEL_SIZES = [5,10,20]
CHAR_FEATURE_MAPS = [300,300,300]

# GENERAL
DROPOUT_RATE      = 0.6
HIDDEN_UNITS      = 200
#NB_CLASSES        = 2
NB_CLASSES        = 4

# LEARNING
#BATCH_SIZE        = 64
BATCH_SIZE        =16
NB_EPOCHS         = 10
RUNS              = 5
VAL_SIZE          = 0.3


def clean_doc(doc):
    """
    Cleaning a document by several methods:
        - Lowercase
        - Removing whitespaces
        - Removing numbers
        - Removing stopwords
        - Removing punctuations
        - Removing short words
    """
    # stop_words = set(stopwords.words('english'))

    # Lowercase
    doc = doc.lower()
    # Remove numbers
    # doc = re.sub(r"[0-9]+", "", doc)
    # Split in tokens
    tokens = doc.split()
    # Remove Stopwords
    # tokens = [w for w in tokens if not w in stop_words]
    # Remove punctuation
    # tokens = [w.translate(str.maketrans('', '', string.punctuation)) for w in tokens]
    # Tokens with less then two characters will be ignored
    # tokens = [word for word in tokens if len(word) > 1]
    return ' '.join(tokens)


def read_files(path):
    documents = list()
    file_path = Path(path)
    # Read in all lines in a txt file
    if file_path.is_file():
        with open(path, encoding='iso-8859-1') as f:
            doc = f.readlines()
            for line in doc:
                documents.append(clean_doc(line))
    return documents


def main(convo):

    negative_docs = read_files('TextClassifier/data/fyp/train/negative.txt')
    positive_docs = read_files('TextClassifier/data/fyp/train/positive.txt')
    complete_docs = read_files('TextClassifier/data/fyp/train/complete.txt')
    neutral_docs = read_files('TextClassifier/data/fyp/train/neutral.txt')

    arr = [negative_docs,positive_docs,complete_docs,neutral_docs]
    maxLength = int(max([len(i) for i in arr]))
    adjustments = []
    for j in arr:
        adjustments.append(int(maxLength/len(j)))

    negative_docs *=adjustments[0]
    positive_docs *=adjustments[1]
    complete_docs *=adjustments[2]
    neutral_docs *=adjustments[3]

    docs   = negative_docs + positive_docs + complete_docs + neutral_docs

    X_test2 = convo #array  if input strings to classify

    tokenizer = keras.preprocessing.text.Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(docs)
    # sequences = tokenizer.texts_to_sequences(docs)

    word_index = tokenizer.word_index
    sequences_test = tokenizer.texts_to_sequences(X_test2)
    X_test_word = keras.preprocessing.sequence.pad_sequences(sequences_test, maxlen=MAX_SEQ_LENGTH, padding='post')


    X_test = X_test_word

    test_loss = []
    test_accs = []
    model_path = Path('TextClassifier/model-4.h5')
    cnn_ = keras.models.load_model(model_path)
    score = cnn_.predict(X_test)
    print('score', score)
    return score

if __name__ == '__main__':

    main()
