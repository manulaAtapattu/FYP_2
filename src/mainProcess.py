# main process file in automatic minute maker
# reeds from the transcription.txt file and feeds each line into the deep learning models
# final output will be of the minutes

from pathlib import Path
from TextClassifier import testModel
from Qidentifier import QItest
from shortAnswerChecker import shortAnswer
from combineQA import combineQA
from removeNeutral import removeNeutral
from QA import test as qa

print("Starting the main process")
trans_path = Path("../pages/transcription.txt")
f  =  open(trans_path)
convo = f.readlines()

# arrange convo in list [[speakerID, sentence][..][..]...]
output=[]
for i in convo:
    i=i.split(' : ')
    output.append([i[0][-1],i[1].rstrip()])
print(output)
f.close()

convo = []
for i in output:
    temp = i[1].split('.')
    for j in temp:
        j = j.split(',')
        for z in j:
            convo.append(z)

print('convo : ',convo)

# function to identify questions
def isQuestion(sentence):
    return QItest.main(sentence)

# identify short answers
def isShortAnswer(sentence):
    return shortAnswer.main(sentence)

#removing neutral part of complete AND neutral sentences
def removeNeutral(sentence):
    print("removing neutral component of sentence")
    return removeNeutral.main(sentence)


def findAnswer(index, question):
    print("finding answer")
    # assume answer is within proceeding ten statements
    context = ""
    for i in range(index, index+10):
        x = sorted_output[i]
        context+=x[1]
    answer = qa.main(question, context)
    return answer

def combineAnswer(question, answer):
    print("Combining answer and question")
    return combineQA(question, answer)

def getScore(statement):
    print("calculating statement score")
    return testModel.main([sentence])

def createMinute(index, statement):
    print("Adding item to minutes")

def isCompleteSentence(score):
    if score.index(max(score))==3 and max(score)>0.5:
        return True
    else:
        return False

convo_length = len(convo)
questions = []
short_answers = []
neg_ans = []
pos_ans = []
scores = []
sorted_output = []
index=0
finalMinutes=[None]*convo_length

for sentence in convo:
    #seperate  questions
    if isQuestion(sentence):
        print("Question identified")
        questions.append([index,sentence,4])    #here change to append([index,sentence]) # 4 used ot represent questions
        sorted_output.append([index,sentence,4])
        index+=1
    elif isShortAnswer(sentence):
        print("Short answer identified")
        short_answers.append([index,sentence,5])    #same as above  # 5 used to represent short answers
        sorted_output.append([index,sentence,5])
        index+=1
    else:
        score = getScore(sentence)
        scores.append([index,score])          #add index
        sorted_output.append([index, sentence,score])
        index+=1

# process scores into classes
# output = [sentence, score, score_index]
max_probs=[]
for output in sorted_output:
    if  output[2][2]>0.3 and score[2][3]>0.3:
        print("Belong to complete AND neutral sentences")
        updSent, flag = removeNeutral(convo[score[0]])
        if flag==True:
            updated_score = getScore(updSent)
            if isCompleteSentence(updated_score):
                finalMinutes.append([output[0],3,output[1]])
        else:
            print("Neutral part not present or cannot be seperated from sentence")
    elif max(score[1])<0.5:
        print("sentence cannot be classified accurately")
    else:
        max_index = score.index(max(score))
        print("sentence belongs to : "+ str(max_index))
        if max_index==2:
            print("Useful sentence")
            finalMinutes[output[0]]=[3,output[1]]
        elif  max_index==1:
            print("Positive Answer")
            finalMinutes[output[0]]=[1,output[1]]
        elif max_index==0:
            print("Negative Answer")
            finalMinutes[output[0]]=[0,output[1]]
        else:
            print("Useless statement")

# Question Answering models
# find answers to questions and combine
for q in questions:
    answer = findAnswer(q[0], q[1])
    comb_statement = combineAnswer(answer, q[1])
    comb_score = getScore(comb_statement)
    if isCompleteSentence(comb_score):
        finalMinutes[q[0]] = [3,comb_statement]











