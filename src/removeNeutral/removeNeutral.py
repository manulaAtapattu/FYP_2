# remove neutral phrases / useless  phrases from sentences
# comes into being only when a senetence of the conversation shows high amount of complete sentence and neutral sentence

def main(sentence):
    s_1 = sentence
    f = open("../src/removeNeutral/neutral.txt","r")
    arr = f.readlines()
    f.close()
    for i in arr:
        i = i.rstrip("\n\r")
        if i in s_1:
            print("removing neutral sentence")
            s_1.replace(i,"")
            return s_1, True
    return s_1, False

print (main("Good morning Everyone"))
