# this page is used to separate the final minutes based on the topics
# it will take in as input the list of all output sentences. But only separate the minutes

from src.StringSimilarity import sorensen_dice_test_app as ss
from src.Summarizer import summarizer
from multiprocessing import Process, Array


def threadSep(temp_arr, i, arr, output_list):
    print("starting thread ", i, "on transition detection ")
    for element in temp_arr:
        similarities = []
        for j in arr:
            element[1] = element[1].rstrip("\n\r")
            element[1] = element[1].lower()
            similarity = ss.main(element[1], j)
            similarities.append(similarity)
        output_list[element[0]] = max(similarities)


def separate(transcription_list, class_arr):
    length = len(transcription_list)
    if length < 5:
        threads = length
    else:
        threads = 5
    output_list = Array('d', length)
    sample = int(length / threads)
    print("Finding categories")
    # f = open("../src/separateProjects/transitions.txt", "r")
    f = open("transitions.txt", "r")  # local testing
    arr = f.readlines()
    f.close()
    index = 0
    for i in transcription_list:
        transcription_list[index] = [index, i]
        index += 1

    thread_list = []
    for i in range(threads):
        temp_arr = transcription_list[i * sample:(i + 1) * sample]
        t = Process(target=threadSep, args=(temp_arr, i, arr, output_list,))
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()

    output_list = output_list[:]
    print("output_list", output_list)
    paragraphs = []
    para = ''
    length = len(output_list)
    for i in range(length):
        skip = False
        if i != length - 1:
            if output_list[i] > 0.75:
                paragraphs.append(para)
                para = ''
                print("possible transition point")
                output_list[i] = 1
                if arr[i + 1] == 1:
                    if output_list[i] > 0.6:
                        print("possible transition point")
                    else:
                        print("not a transition point")
                else:
                    if not para == '':
                        paragraphs.append(para)
                    para = ''
                    print("possible transition point")
                    skip = True
                    output_list[i] = 1
            if not skip:
                if transcription_list[i][1][-1] == '.' or transcription_list[i][1][-1] == ',':
                    para += transcription_list[i][1]
                else:
                    para += (transcription_list[i][1] + '.')  # adding fullstops and comma
        else:
                paragraphs.append(para)

    return paragraphs
    # return output_list


def main(test_sentences, arr):
    # for local testing
    # test_sentences = ["good morning Everyone", "We are hear to talk about the Nero project.",
    #                   "It will be completed in about two weeks time.", "We need to reduce the costs.",
    #                   "That all right.", "Moving on", "let's  talk about the airline project.",
    #                   "Costs are way too high there.", "And also", " we must reduce the number of staff by half.",
    #                   "staff costs are high.", "Okay. The next item we need to talk about is hiring of employees.",
    #                   "We need to a hire an interactive game developer.", "That is to design VR projects.",
    #                   "Okay then that's all for now.",
    #                   "Thank you all for coming."]
    #
    # arr = [4, 1, 1, 1, 2, 4, 4, 1, 1, 1, 1, 1, 1, 1, 4, 4]

    paragraphs = separate(test_sentences, arr)
    print("Separated paragraphs", paragraphs)
    print("Identifying keywords in paragraphs ... ")
    keywords = []
    for para in paragraphs:
        keys = summarizer.getKeywords(para)
        keywords.append(keys)
    print("keywords of the paragraphs : ", keywords)

