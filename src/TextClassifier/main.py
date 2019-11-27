import matplotlib.pyplot as plt
import numpy as np
import os
import re
import string
import keras
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import random

plt.style.use('seaborn')

# WORD-level
MAX_NUM_WORDS = 1000
# MAX_NUM_WORDS     = 100000
EMBEDDING_DIM = 200
# MAX_SEQ_LENGTH    = 500
MAX_SEQ_LENGTH = 15
USE_GLOVE = True
# KERNEL_SIZES      = [3,4,5]
KERNEL_SIZES = [2, 3]
# FEATURE_MAPS      = [100,100,100]
FEATURE_MAPS = [20, 20]

# CHAR-level
USE_CHAR = False
ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}"
ALPHABET_SIZE = len(ALPHABET)
CHAR_MAX_LENGTH = 1600
CHAR_KERNEL_SIZES = [5, 10, 20]
CHAR_FEATURE_MAPS = [100, 100, 100]

# GENERAL
DROPOUT_RATE = 0.5
HIDDEN_UNITS = 200
NB_CLASSES = 4

# LEARNING
BATCH_SIZE = 16
NB_EPOCHS = 10
RUNS = 5
VAL_SIZE = 0.01


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
    # Read in all files in directory
    if os.path.isdir(path):
        for filename in os.listdir(path):
            with open('%s/%s' % (path, filename), encoding="utf8") as f:
                doc = f.read()
                doc = clean_doc(doc)
                documents.append(doc)

    # Read in all lines in a txt file
    if os.path.isfile(path):
        with open(path, encoding='iso-8859-1') as f:
            doc = f.readlines()
            for line in doc:
                documents.append(clean_doc(line))
    return documents


## Sentence polarity dataset v1.0
# negative_docs = read_files('data/rt-polaritydata/rt-polarity.neg')
# positive_docs = read_files('data/rt-polaritydata/rt-polarity.pos')

## IMDB
# negative_docs = read_files('data/imdb/train/neg/')
# positive_docs = read_files('data/imdb/train/pos')
# negative_docs_test = read_files('data/imdb/test/neg')
# positive_docs_test = read_files('data/imdb/test/pos')

# ## FYP
negative_docs = read_files('data/fyp/train/negative.txt')
positive_docs = read_files('data/fyp/train/positive.txt')
complete_docs = read_files('data/fyp/train/complete.txt')
neutral_docs = read_files('data/fyp/train/neutral.txt')

# question and statement classifier
# questions = read_files('data/q_s/train/questions.txt')
# statements = read_files('data/q_s/train/statements.txt')


# negative_docs_test = read_files('data/fyp/test/negative.txt')
# positive_docs_test = read_files('data/fyp/test/positive.txt')
# complete_docs_test = read_files('data/fyp/test/complete.txt')
# neutral_docs_test = read_files('data/fyp/test/neutral.txt')


## Yelp
# negative_docs = read_files('data/yelp/neg.txt')
# positive_docs = read_files('data/yelp/pos.txt')
# negative_docs_test = negative_docs[300000:]
# positive_docs_test = positive_docs[300000:]
# negative_docs = negative_docs[:300000]
# positive_docs = positive_docs[:300000]


# equalize length
# arr = [negative_docs,positive_docs,complete_docs,neutral_docs]

# maxLength = int(max([len(i) for i in arr]))
# adjustments = []
# for j in arr:
#     adjustments.append(int(maxLength/len(j)))
#
# negative_docs *=adjustments[0]
# positive_docs *=adjustments[1]
# complete_docs *=adjustments[2]
# neutral_docs *=adjustments[3]


# docs   = negative_docs + positive_docs
docs = negative_docs + positive_docs + complete_docs + neutral_docs
# docs = questions + statements

# labels = [0 for _ in range(len(negative_docs))] + [1 for _ in range(len(positive_docs))]
labels = [0 for _ in range(len(negative_docs))] + [1 for _ in range(len(positive_docs))] + [2 for _ in range(
    len(complete_docs))] + [3 for _ in range(len(neutral_docs))]
# labels = [0 for _ in range(len(questions))] + [1 for _ in range(len(statements))]

c = list(zip(docs, labels))
import random

random.shuffle(c)

docs, labels = zip(*c)

labels = keras.utils.to_categorical(labels)
print('labels : ', labels)
print('Training samples: %i' % len(docs))

tokenizer = keras.preprocessing.text.Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(docs)
sequences = tokenizer.texts_to_sequences(docs)

word_index = tokenizer.word_index

result = [len(x.split()) for x in docs]

# Plot histogram
plt.figure(figsize=(20, 5))
plt.title('Document length')
plt.hist(result, 200, density=False, range=(0, np.max(result)))
# plt.show()


print('Text informations:')
print('max length: %i / min length: %i / mean length: %i / limit length: %i' % (np.max(result),
                                                                                np.min(result),
                                                                                np.mean(result),
                                                                                MAX_SEQ_LENGTH))
print('vacobulary size: %i / limit: %i' % (len(word_index), MAX_NUM_WORDS))

# Padding all sequences to same length of `MAX_SEQ_LENGTH`
word_data = keras.preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LENGTH, padding='post')

if USE_CHAR:
    char2idx_dict = {}
    idx2char_dict = {}

    for idx, char in enumerate(ALPHABET):
        char2idx_dict[char] = idx + 1

    idx2char_dict = dict([(i + 1, char) for i, char in enumerate(char2idx_dict)])

    # Get informations about char length
    result = [len(x) for x in docs]
    plt.figure(figsize=(20, 5))
    plt.title('Char length')
    plt.hist(result, 200, density=False, range=(0, np.max(result)))
    plt.show()
    print('Text informations:')
    print('max length: %i / min length: %i / mean length: %i / limit length: %i' % (np.max(result),
                                                                                    np.min(result),
                                                                                    np.mean(result),
                                                                                    CHAR_MAX_LENGTH))


def char_vectorizer(X):
    str2idx = np.zeros((len(X), CHAR_MAX_LENGTH), dtype='int64')
    for idx, doc in enumerate(X):
        max_length = min(len(doc), CHAR_MAX_LENGTH)
        for i in range(0, max_length):
            c = doc[i]
            if c in char2idx_dict:
                str2idx[idx, i] = char2idx_dict[c]
    return str2idx


def create_glove_embeddings():
    print('Pretrained embeddings GloVe is loading...')

    embeddings_index = {}
    f = open('glove.twitter.27B.%id.txt' % EMBEDDING_DIM, encoding="utf8")
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    print('Found %s word vectors in GloVe embedding' % len(embeddings_index))

    embedding_matrix = np.zeros((MAX_NUM_WORDS, EMBEDDING_DIM))

    for word, i in tokenizer.word_index.items():
        if i >= MAX_NUM_WORDS:
            continue
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return keras.layers.Embedding(
        input_dim=MAX_NUM_WORDS,
        output_dim=EMBEDDING_DIM,
        input_length=MAX_SEQ_LENGTH,
        weights=[embedding_matrix],
        trainable=True,
        name="word_embedding"
    )


# TRAINING ----------------------------------------------------------------------------------

from cnn_model import CNN

histories = []

for i in range(RUNS):
    print('Running iteration %i/%i' % (i + 1, RUNS))
    random_state = np.random.randint(1000)

    X_train, X_val, y_train, y_val = train_test_split(word_data, labels, test_size=VAL_SIZE, random_state=random_state)


    if USE_CHAR:
        X_train_c, X_val_c, _, _ = train_test_split(char_vectorizer(docs), labels, test_size=VAL_SIZE,
                                                    random_state=random_state)
        X_train = [X_train, X_train_c]
        X_val = [X_val, X_val_c]

    emb_layer = None
    if USE_GLOVE:
        emb_layer = create_glove_embeddings()

    model = CNN(
        embedding_layer=emb_layer,
        num_words=MAX_NUM_WORDS,
        embedding_dim=EMBEDDING_DIM,
        kernel_sizes=KERNEL_SIZES,
        feature_maps=FEATURE_MAPS,
        max_seq_length=MAX_SEQ_LENGTH,
        use_char=USE_CHAR,
        char_max_length=CHAR_MAX_LENGTH,
        alphabet_size=ALPHABET_SIZE,
        char_kernel_sizes=CHAR_KERNEL_SIZES,
        char_feature_maps=CHAR_FEATURE_MAPS,
        dropout_rate=DROPOUT_RATE,
        hidden_units=HIDDEN_UNITS,
        nb_classes=NB_CLASSES
    ).build_model()

    model.compile(
        loss='categorical_crossentropy',
        optimizer=keras.optimizers.Adam(),
        metrics=['accuracy']
    )

    # model.summary()

    history = model.fit(
        X_train, y_train,
        epochs=NB_EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_val, y_val),
        callbacks=[
            keras.callbacks.ModelCheckpoint(
                'model-%i.h5' % (i + 1), monitor='val_loss', verbose=1, save_best_only=True, mode='min'
            ),
            # keras.callbacks.TensorBoard(log_dir='./logs/temp', write_graph=True)
        ]
    )
    print()
    histories.append(history.history)


# EVALUATION -------------------------------------------------------------------

def get_avg(histories, his_key):
    tmp = []
    for history in histories:
        tmp.append(history[his_key][np.argmin(history['val_loss'])])
    return np.mean(tmp)


print('Training: \t%0.4f loss / %0.4f acc' % (get_avg(histories, 'loss'),
                                              get_avg(histories, 'acc')))
print('Validation: \t%0.4f loss / %0.4f acc' % (get_avg(histories, 'val_loss'),
                                                get_avg(histories, 'val_acc')))


def plot_acc_loss(title, histories, key_acc, key_loss):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    # Accuracy
    ax1.set_title('Model accuracy (%s)' % title)
    names = []
    for i, model in enumerate(histories):
        ax1.plot(model[key_acc])
        ax1.set_xlabel('epoch')
        names.append('Model %i' % (i + 1))
        ax1.set_ylabel('accuracy')
    ax1.legend(names, loc='lower right')
    # Loss
    ax2.set_title('Model loss (%s)' % title)
    for model in histories:
        ax2.plot(model[key_loss])
        ax2.set_xlabel('epoch')
        ax2.set_ylabel('loss')
    ax2.legend(names, loc='upper right')
    fig.set_size_inches(20, 5)
    plt.show()


plot_acc_loss('training', histories, 'acc', 'loss')
plot_acc_loss('validation', histories, 'val_acc', 'val_loss')
