# main process file in automatic minute maker
# reeds from the transcription.txt file and feeds each line into the deep learning models
# final output will be of the minutes
# arr[index] => indexes -> 0 - not processed yet, 1 - useful,
# 2 - Positive answer, 3 - negative answer, 4 - useless,
# 5 - short answer, -2 - useless question, -1 = question

from src.TextClassifier import testModel, testModel_q_s
from src.TextClassifier.BERT import run_classifier
from src.shortAnswerChecker import shortAnswer
from src.combineQA import combineQA
from src.removeNeutral import removeNeutral
from src.QA import test as qa
from src.QuestionType import questionType

from pages import realTimeProcess as RTP
# import pages.finalMinutes as Minutes
import numpy as np
import time

# convo_length = len(convo)
questions = []
short_answers = []
neg_ans = []
pos_ans = []
scores = []
sorted_output = []
index = 0
# finalMinutes=[None]*convo_length
MAX_CONVO_LENGTH = 50
finalMinutes = [None] * MAX_CONVO_LENGTH
minute_entry = []
inQuestion = False
# inputSentences = [None] * MAX_CONVO_LENGTH
# usefulSentences = [True] * MAX_CONVO_LENGTH
# completedIndexes = [None] * MAX_CONVO_LENGTH
q_buffer = []
q_type = None


# index = 0


def main(sentence, index, arr):
    # print("Starting the main process in index ", index, ' and sentence ', sentence)

    # global index
    global finalMinutes
    global inQuestion
    global q_buffer
    global q_type

    # global inputSentences

    # inputSentences[index] = sentence

    # function to identify questions
    def isQuestion(sentence):
        # return QItest.main(sentence)
        x = testModel_q_s.main([sentence])
        if x[0][0] > 0.75:
            print("Question identified")
            return True
        elif x[0][1] > 0.65:
            print("Non Question identified")
            return False
        else:
            print("Cannot be classified accurately as Question or not | p(Q) = ", x[0])
            return False

    # identify short answers
    def isShortAnswer(sentence):
        return shortAnswer.main(sentence)

    # removing neutral part of complete AND neutral sentences
    def remNeutral(sentence):
        print("removing neutral component of sentence")
        return removeNeutral.main(sentence)

    def findAnswer2(index, question, contextList):
        print("finding answer")
        # assume answer is within proceeding ten statements
        context = ""
        for i in contextList:
            context += i
        answer = qa.main(question, context)
        # need to implement a system to remove an existing answer
        return answer

    def combineAnswer(question, answer):
        print("Combining answer and question")
        question = question.lstrip()
        print('q : ', question)
        print('a : ', answer)
        return combineQA.main(question, answer)

    def getScore(statement, index):
        return run_classifier.main(statement, index)  # using BERT

    def createMinute(index, statement):
        print("Adding item to minutes")

    def isCompleteSentence(score):
        if np.where(score == max(score)) == 3 and max(score) > 0.5:
            return True
        else:
            return False

    # preprocess input sentence
    def preprocessSent(sentence):
        sentence = sentence.lstrip()
        return sentence

    def QuestionType(sentence):
        return questionType.main(sentence)

    # sentence = preprocessSent(sentence)
    # while True:
    #     if inQuestion == True:
    #         print('Wait till answer to latest question is calculated ... ')
    #         time.sleep(2)
    #     else:
    #         break
    if isQuestion(sentence):
        # check if useless question
        print("Question identified")
        arr[index] = -1

    elif isShortAnswer(sentence):
        print("Short answer identified")
        arr[index] = 5
        # no need to interact here. This is considered in the question identifier section
    else:
        score = getScore(sentence, index)
        # from pages.realTimeProcess import keywords
        # if keyword is in sentence => increase complete/useful sentence score
        if RTP.keywords != None:
            for kw in RTP.keywords:
                if kw in sentence:
                    print("keyword in sentence")
                    score[0] = score[0] * 1.3

        # score = score[0]       # comment when using BERT
        if score[0] > 0.25 and score[3] > 0.2:
            print("Belong to complete AND neutral sentences")
            updSent, flag = remNeutral(sentence)
            if flag == True:
                updated_score = getScore(updSent)
                if isCompleteSentence(updated_score):
                    finalMinutes[index] = [index, 0, sentence, False]
                    arr[index] = 1
            else:
                print("Neutral part not present or cannot be separated from sentence")
        elif score[0] > 0.25 and score[1] > 0.25:
            print("identified complete and positive sentence")
        elif score[0] > 0.25 and score[2] > 0.25:
            print("identified complete and negative sentence")
        elif max(score) < 0.5:
            print("sentence cannot be classified accurately")
        else:
            max_index = list(score).index(max(score))
            if max_index == 0:
                print("Useful sentence ", sentence)
                minute_entry = [index, 0, sentence, False]
                arr[index] = 1
                #print("arr in MP: ", arr[:])
                # while True:
                #     if index == 0 or (completedIndexes[index - 1] == True and usefulSentences[index] == True):
                #         Minutes.updateStart(sentence + ":" + str(index))
                #         completedIndexes[index] = True
                #         break
                #     else:
                #         time.sleep(1)
            elif max_index == 1:
                #print("Positive Answer")
                minute_entry = [index, 1, sentence, False]
                arr[index] = 2

            elif max_index == 2:
                #print("Negative Answer")
                minute_entry = [index, 2, sentence, False]
                arr[index] = 3

            else:
                #print("Useless statement")
                arr[index] = 4
                # usefulSentences[index] = False
                # completedIndexes[index] = True

    # completedIndexes[index] = True
    print("completed index", index)
    return 0
