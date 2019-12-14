# This code is used to recognize users.

import pyaudio
import wave
import os
from google.cloud import speech_v1p1beta1 as speech


def main(speech_file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/janaranjana/Documents/Untitled Folder/Fyp/FYP_final/FYP-key.json"

    print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

    client = speech.SpeechClient()

    # = '52223351.wav'

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    # storage_uri = 'gs://fyp_1/BEP313-Scrum-Meetings1.wav'

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=8000,
        language_code='en-US',
        enable_speaker_diarization=True,
        # diarization_speaker_count=2,
        audio_channel_count=2,
    )
    # audio = {"uri": storage_uri}

    print('Waiting for operation to complete...')
    response = client.recognize(config, audio)
    # response = client.long_running_recognize(config, audio)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]

    words_info = result.alternatives[0].words

    # Printing out the output:
    # for word_info in words_info:
    #     print(u"word: '{}', speaker_tag: {}".format(
    #         word_info.word, word_info.speaker_tag))

    tag = 1
    speaker = ""
    transcript = ""

    for word_info in words_info:
        if word_info.speaker_tag == tag:
            speaker = speaker + " " + word_info.word
        else:
            transcript += "speaker {}: {}".format(tag, speaker) + '\n'
            tag = word_info.speaker_tag
            speaker = "" + word_info.word

    transcript += "speaker {}: {}".format(tag, speaker)
    print(transcript)


def recordVoice(filename, time):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = time


    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

#Save User
def saveFile(username):
    num_lines = 0
    try:
        num_lines = sum(1 for line in open('deofile3.txt'))
    except OSError as e:
        print(e.errno)
    print(num_lines)
    lastid = id =int(filetolist()[-1][0])
    id = lastid+1
    filename = str(id)+".wav"
    text  = "Hello" #shoud be the output
    recordVoice(filename,5)
    if(text == "Hello"):
        f = open("deofile3.txt", "a")
        f.write(str([id, filename,username])+"\n")
        f.close()

#merge voices with source file
def mergeFile(SourceFile):
    allList = filetolist()
    allList = allList[::-1]
    cnt = 0
    names = []
    outfile = "updated" + SourceFile
    for line in allList:
        if line != '':
            names.append(line[2])
            cnt += 1
            print(cnt)
            if cnt == 1:
                infiles = [line[1].strip("'"), SourceFile]
            else:
                infiles = [line[1].strip("'"), outfile]

            data = []

            for infile in infiles:
                w = wave.open(infile, 'rb')
                data.append([w.getparams(), w.readframes(w.getnframes())])
                w.close()

            output = wave.open(outfile, 'wb')
            output.setparams(data[0][0])
            output.writeframes(data[0][1])
            output.writeframes(data[1][1])
            output.close()
    result = [outfile, names[::-1]]
    return result


def filetolist():
    with open("deofile3.txt") as fp:
        line = fp.readline().rstrip()
        cnt = 1
        reList = []
        while line:
            # print("Line {}: {}".format(cnt, line.strip()))


            if line != '':
                res = line.strip('][').split(', ')
                print(res)
                reList.append(res)
            line = fp.readline()
            line = line.rstrip()
        return reList


# print(filetolist())
# saveFile("jana4")
# saveFile("Sena4")
# mergeFile("1.wav")
# result = mergeFile("5.wav")
# print(result)
main("1.wav")