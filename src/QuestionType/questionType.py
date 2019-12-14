from src.StringSimilarity import sorensen_dice_test_app as ss


def main(sentence):
    print("Finding question type of : ", sentence)
    s = sentence.lower()
    f = open("../src/removeNeutral/neutral.txt","r")
    #f = open("questions.txt", "r")  # local testing
    arr = f.readlines()
    f.close()
    for i in arr:
        i = i.rstrip("\n\r")
        i = i.lower()
        similarity = ss.main(s, i)
        if similarity > 0.8:
            print("Question is Useless")
            return False
    print("Question is useful")
    return True
