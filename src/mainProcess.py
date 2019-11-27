# main process file in automatic minute maker
# reeds from the transcription.txt file and feeds each line into the deep learning models
# final output will be of the minutes

from pathlib import Path
from src.TextClassifier import testModel, testModel_q_s
# from src.Qidentifier import QItest
from src.shortAnswerChecker import shortAnswer
from src.combineQA import combineQA
from src.removeNeutral import removeNeutral
from src.QA import test as qa
import pages.finalMinutes as Minutes
import numpy as np

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
Qbuffer = []

index = 0


def main(sentence):
    print("Starting the main process")

    global index
    global finalMinutes
    global inQuestion
    global Qbuffer

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

    def getScore(statement):
        print("calculating statement score")
        return testModel.main([statement])

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

    #sentence = preprocessSent(sentence)
    if inQuestion == True:
        print('in question...')
        # Qbuffer = [index, question, [answers] ]
        print('adding to Qbuffer')
        Qbuffer[2].append(sentence)
        if len(Qbuffer[2]) != 3:
            return
        else:
            print('added Qbuffer to maximum capacity')
            answer = findAnswer2(index, Qbuffer[1], Qbuffer[2])
            print('answer : ', answer)
            comb_statement = combineAnswer(Qbuffer[1], answer['answer'])
            print("comb_statement : ", comb_statement)
            # calculating usefullness of considered options
            inQuestion = False
            answers = Qbuffer[2]
            Qbuffer = []
            main(comb_statement)
            for sentence in answers:
                if answer['answer'] in sentence:
                    continue
                main(sentence)
    else:
        if isQuestion(sentence):
            # print("Question identified")
            inQuestion = True
            Qbuffer = [index, sentence, []]
        elif isShortAnswer(sentence):
            print("Short answer identified")
            # no need to interact here. This is considered in the question identifier section
        else:
            score = getScore(sentence)
            score = score[0]
            if score[2] > 0.3 and score[3] > 0.3:
                print("Belong to complete AND neutral sentences")
                updSent, flag = remNeutral(sentence)
                if flag == True:
                    updated_score = getScore(updSent)
                    if isCompleteSentence(updated_score):
                        finalMinutes[index] = [index, 3, sentence, False]
                else:
                    print("Neutral part not present or cannot be separated from sentence")
            elif max(score) < 0.5:
                print("sentence cannot be classified accurately")
            else:
                max_index = list(score).index(max(score))
                print("sentence belongs to : " + str(max_index))
                if max_index == 2:
                    print("Useful sentence")
                    minute_entry = [index, 3, sentence, False]
                    Minutes.updateStart(sentence + ":" + str(index))
                elif max_index == 1:
                    print("Positive Answer")
                    minute_entry = [index, 1, sentence, False]
                    Minutes.updateStart(sentence + ":" + str(index))
                elif max_index == 0:
                    print("Negative Answer")
                    minute_entry = [index, 0, sentence, False]
                    Minutes.updateStart(sentence + ":" + str(index))
                else:
                    print("Useless statement")
    index += 1
