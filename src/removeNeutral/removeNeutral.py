# remove neutral phrases / useless  phrases from sentences
# comes into being only when a senetence of the conversation shows high amount of complete sentence and neutral sentence

def main(sentence):
    s_1 = sentence.lower()
    f = open("../src/removeNeutral/neutral.txt","r")
    #f = open("neutral.txt", "r")  # local testing
    arr = f.readlines()
    f.close()
    for i in arr:
        i = i.rstrip("\n\r")
        i = i.lower()
        if i in s_1:
            print("removing neutral sentence : ", i)
            s_1 = s_1.replace(i, "")
            return s_1, True
    return s_1, False


#print(main("By the way the project is 10 million"))
