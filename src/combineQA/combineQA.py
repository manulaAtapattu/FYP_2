import spacy

q1 = "What is the cost?"
q2 = "When will the project be finished?"
q3 = "Will the project be completed on time?"
q4 = "How many members in the project?"
q5 = "Who is the team leader."
q6 = "Did you complete phase two?"
q7 = "How long will the the project take?"
q8 = "Who will join your team?"
q9 = "At what time will you start building?"
a1 = "Ten million"
a2 = "On the 5th of July"
a3 = "Yes"
a4 = "Five"
a5 = "Jack"
a6 = "No"
a7 = "Two weeks"
a8 = "Jack and Sam"
a9 = "At 9.00 am"
q_s = [q3.lower(), q7.lower(), q8.lower(), q9.lower()]
a_s = [a3.lower(), a7.lower(), a8.lower(), a9.lower()]


def main(question, answer):
    yn = False
    success = False
    result = ""
    nlp = spacy.load("en_core_web_sm")


    q = question.lower()
    a = answer.lower()

    # docs=[]
    # for i in q:
    #     docs.append(nlp(i))
    # for doc in docs:
    #     print('\n')
    #     for token in doc:
    #         print(token.text, token.pos_, token.dep_)

    doc = nlp(q)
    # for token in doc:
    #     print(token.text, token.pos_, token.dep_)

    if (doc[0].dep_ == "aux"):
        yn = True
    # print (yn)

    verb = ""
    for i in range(0, len(doc) - 1):
        if doc[i].dep_ == "ROOT":
            verb = i
    #print(verb)

    splitq = []
    deps = []
    for token in doc:
        splitq.append(token.text.lower())
        deps.append(token.dep_.lower())
    if (doc[-1].dep_ == "punct"):
        del splitq[-1]
    #print(deps[1])
    if "auxpass" in deps:
        verb = deps.index("auxpass")
    if yn:
        aux = splitq.pop(0)
        if (a == "no"):
            splitq.insert(verb - 1, "not")
        splitq.insert(verb - 1, aux)
        success = True
    # elif splitq[0] == "at" and splitq[1] == "what" and splitq[2] == "time":
    #     noun = splitq.pop(verb)
    #     print(noun)
    #     splitq = [noun] + splitq[3:] + [a]
    elif splitq[0] == "how" and splitq[1] == "many":
        if a == "one":
            splitq = ["there", "is", "a"] + splitq[2:]
        else:
            splitq = ["there", "are", a] + splitq[2:]
    elif splitq[0] == "who":
        splitq = [a] + splitq[1:]
    elif splitq[0] == "what":
        #print("d0")
        if deps[1] == "root":
            #print("d")
            wh = splitq.pop(0)
            aux = splitq.pop(0)
            splitq.append(aux)
            splitq.append(a)
            success = True
        elif "aux" in deps:
            #print("d1")
            i = deps.index("aux")
            splitq = splitq[i:]
            aux = splitq.pop(0)
            splitq.insert(verb - 1 - i, aux)
            splitq.append(a)
            success = True
    elif "aux" in deps:
        #print("d2")
        i = deps.index("aux")
        splitq = splitq[i:]
        aux = splitq.pop(0)
        splitq.insert(verb - 1 - i, aux)
        splitq.append(a)
        success = True
    result = " ".join(splitq) + "."
    # print(result)
    # print(success)
    print('Combined sentence : ', result)
    return result

#main("What is the cost of construction project?","10 million")
