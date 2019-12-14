"""Google Cloud Speech API sample application using the streaming API.
NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:
    pip install pyaudio
Example usage:
    python transcribe_streaming_indefinite.py
"""

# [START speech_transcribe_infinite_streaming]
# from __future__ import division

import time
import re
import sys
import os
import multiprocessing

from google.cloud import speech_v1p1beta1 as speech
import pyaudio
# from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1 import enums
from six.moves import queue

from src import mainProcess
from src.QuestionType import questionType
from src.QA import test as qa
from src.combineQA import combineQA
from src.seperateProjects import separateProjects as sep
from src.TextClassifier.BERT import run_classifier

# Audio recording parameters
STREAMING_LIMIT = 200000
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

final_transcript = []
threadList = []
index = 0
inputSentences = None
usefulSentences = None
completedIndexes = None
minutes = None
queueQA = None  # shared memory queue to find answers to questions
arr = None  # arr used to update classifications of sentences 1-useful,2-PA,3-NA,4-useless
mainQueue = None  # queue used to update the tkinter minutes page
queueTranscripts = None  # all text forms of transcription are stored here
Transcripts = []
queueSpeakerTags = []
stop_loop = None
transition_points = None  # positions in the final minutes where paragraphs are separated
q_convo = None
queueThread = None  # queue of created threads. Needed to kill when thread finishes


def sample_long_running_recognize(storage_uri):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_final/FYP-key.json"

    client = speech.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    # sample_rate_hertz = 16000

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        # "sample_rate_hertz": sample_rate_hertz,
        "enable_speaker_diarization": True,
        "enable_automatic_punctuation": True,
        "language_code": language_code,
        "encoding": encoding,
        "audio_channel_count": 2,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    result = response.results[-1]

    words_info = result.alternatives[0].words

    tag = 1
    tag_prev = 1
    speaker = ""
    transcript = ""

    for word_info in words_info:
        if tag_prev == tag:
            tag_prev = tag
            tag = word_info.speaker_tag
            speaker = speaker + " " + word_info.word
        elif not (speaker[-1] == "." or speaker[-1] == "?"):
            speaker = speaker + " " + word_info.word
        else:
            transcript += "speaker {}: {}".format(tag_prev, speaker) + '\n'
            tag_prev = tag
            tag = word_info.speaker_tag
            speaker = "" + word_info.word

    transcript += "speaker {}: {}".format(tag_prev, speaker)
    print("transcript : ", transcript)
    f = open("transcript.txt", "a")
    f.write(transcript)
    f.close()


def get_current_time():
    """Return Current Time in MS."""

    return int(round(time.time() * 1000))


class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk_size):
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = get_current_time()
        self.restart_counter = 0
        self.audio_input = []
        self.last_audio_input = []
        self.result_end_time = 0
        self.is_final_end_time = 0
        self.final_request_end_time = 0
        self.bridging_offset = 0
        self.last_transcript_was_final = False
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

    def __enter__(self):

        self.closed = False
        return self

    def __exit__(self, type, value, traceback):

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, *args, **kwargs):
        """Continuously collect data from the audio stream, into the buffer."""

        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Stream Audio from microphone to API and to local buffer"""

        while not self.closed:
            data = []

            if self.new_stream and self.last_audio_input:

                chunk_time = STREAMING_LIMIT / len(self.last_audio_input)

                if chunk_time != 0:

                    if self.bridging_offset < 0:
                        self.bridging_offset = 0

                    if self.bridging_offset > self.final_request_end_time:
                        self.bridging_offset = self.final_request_end_time

                    chunks_from_ms = round((self.final_request_end_time -
                                            self.bridging_offset) / chunk_time)

                    self.bridging_offset = (round((
                                                          len(self.last_audio_input) - chunks_from_ms)
                                                  * chunk_time))

                    for i in range(chunks_from_ms, len(self.last_audio_input)):
                        data.append(self.last_audio_input[i])

                self.new_stream = False

            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            self.audio_input.append(chunk)

            if chunk is None:
                return
            data.append(chunk)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)

                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)

                except queue.Empty:
                    break

            yield b''.join(data)


def findAnswer2(index, question, contextList):
    print("finding answer")
    # assume answer is within proceeding ten statements
    context = ""
    for i in contextList:
        context += i
    answer = qa.main(question, context)
    # need to implement a system to remove an existing answer
    return answer


# For non real time scenarios. Process the whole transcript
def process_transcripts(transcripts):
    global Transcripts
    global arr
    global queueTranscripts
    global queueSpeakerTags
    global q_convo
    print("starting process transcripts")
    num_processors = 3
    t_len = len(transcripts)
    stop = False
    e = -1
    while True:
        print("starting thread set ", e)
        thread_list = []
        for i in range(num_processors):
            if e == t_len - 1:
                stop = True
                break
            e += 1
            Transcripts.append(transcripts[e][0])
            queueTranscripts.put(transcripts[e][0])
            queueSpeakerTags.put(transcripts[e][1])
            q_convo.put(transcripts[e][0])
            q_convo.put("person " + str(transcripts[e][1]) + " : ")
            # print(transcripts[e][0])
            thread = multiprocessing.Process(target=mainProcess.main, args=(transcripts[e][0], e, arr,))
            thread_list.append(thread)
        for t in thread_list:
            t.start()
            time.sleep(1)
        for t in thread_list:
            t.join()
        if stop == True:
            break
    return arr


# main classification part happens here
def calculation(arr, queueQA, queueTranscripts, queueSpeakerTags, mainQueue, stop_loop, queueThread):
    global index
    print("Started Calculation")
    while True:
        if stop_loop == 1:
            mainQueue.put("stop recording")
            print("separating into paragraphs")
            global transition_points
            transition_points = sep.separate(queueTranscripts, arr)
            break
        time.sleep(.5)
        # print("in calculation ... index ", index)
        global Transcripts
        tempArr = arr[:]
        # print("tempArr", tempArr)
        if tempArr[index] == 0:
            # print("waiting")
            continue
        if not queueSpeakerTags.empty() and not queueTranscripts.empty():
            speaker_tag = queueSpeakerTags.get()
            sentence = queueTranscripts.get()
        if tempArr[index] == 1:
            print("Adding Useful statement  : ", sentence)
            mainQueue.put("person " + str(speaker_tag) + " : ")
            mainQueue.put(sentence)
        elif tempArr[index] == 2:
            print("Positive response : ", sentence)
            mainQueue.put(sentence)
        elif tempArr[index] == 3:
            print("Negative response : ", sentence)
            mainQueue.put(sentence)
        elif tempArr[index] == 4:
            print("useless statement : ", sentence)
        elif tempArr[index] == 5:
            print("short answer identified")
        else:
            print("Question identified")
            q_type = questionType.main(sentence)
            q_buffer = [index, sentence, []]
            for i in range(1, 4):
                while True:
                    tempArr = arr[:]
                    print("tempArr", tempArr)
                    if stop_loop == 1:
                        print("stopping question finding process")
                    if tempArr[index + i] != 0:
                        print("answer added")
                        q_buffer[2].append(queueTranscripts.get())
                        break
                    else:
                        print("waiting for ", i, 'th answer')
                    time.sleep(1.5)
            # finding answer to question using question answer model
            answer = findAnswer2(index, q_buffer[1], q_buffer[2])
            print('answer : ', answer)
            answers = q_buffer[2]
            if q_type != None:
                if q_type == False:
                    print("As question is useless, Answer is also useless")
                    r_i = 1
                    for sentence in answers:
                        if answer['answer'] in sentence:
                            arr[index + r_i] = -1
                            continue
                        r_i += 1
                else:
                    answer_score = run_classifier.main(answer)
                    answer_score_value = max(answer_score)
                    answer_index = answer_score.index(answer_score_value)
                    if answer_index == 3 and answer_score_value > 0.9:
                        print("Question is regarded as not useless but answer is highly useless.")
                        print("Therefore consider question as useless ")
                        continue
                    comb_statement = combineQA.main(q_buffer[1].lstrip(),
                                                    answer['answer'])  # combining answer and question
                    print("comb_statement : ", comb_statement)
                    # calculating usefullness of considered options
                    mainProcess.main(comb_statement, index, arr, queueQA)
                    if arr[index] == 1:
                        mainQueue.put(comb_statement)
                    r_i = 1
                    for sentence in answers:
                        if answer['answer'] in sentence:
                            arr[index + r_i] = -1
                            continue
                        r_i += 1
                        # main(sentence)
            for i in range(0, 3):
                if arr[index + i + 1] == 1:
                    mainQueue.put(q_buffer[2][i])
                if i == 2:
                    index += 3

            else:
                print("Error in calculating q_type. q_type is None. ")
            continue
        index += 1
        # queueThread.get().terminate()   # kill thread process once finished


def listen_print_loop(responses, stream):
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
    is provided by the server.
    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.
    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """

    for response in responses:

        if get_current_time() - stream.start_time > STREAMING_LIMIT:
            stream.start_time = get_current_time()
            break

        if not response.results:
            continue

        result = response.results[-1]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        # for diarization
        transcript_words = result.alternatives[0].words

        result_seconds = 0
        result_nanos = 0

        if result.result_end_time.seconds:
            result_seconds = result.result_end_time.seconds

        if result.result_end_time.nanos:
            result_nanos = result.result_end_time.nanos

        stream.result_end_time = int((result_seconds * 1000)
                                     + (result_nanos / 1000000))

        corrected_time = (stream.result_end_time - stream.bridging_offset
                          + (STREAMING_LIMIT * stream.restart_counter))

        if result.is_final:
            print(transcript)
            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True

            transcripts = re.split(', |\. |\?  ', transcript)  # seperating paragraphs into multiple sentences/ phrases
            # getting speaker tags
            len_transcripts = len(transcripts)
            i = -1
            j = -1
            for x in range(len_transcripts):
                st = transcript_words[i].speaker_tag
                transcripts[j] = [transcripts[j], st]
                length = len(transcripts[j][0].split())
                i -= length
                j -= 1
            print("transcripts : ", transcripts)
            global index
            global inputSentences
            global usefulSentences
            global completedIndexes
            global minutes
            global Transcripts
            global arr
            global queueTranscripts
            global queueSpeakerTags
            global q_convo
            global queueThread

            print("index ", index)
            for transcript in transcripts:
                Transcripts.append(transcript[0])
                queueTranscripts.put(transcript[0])
                queueSpeakerTags.put(transcript[1])
                q_convo.put(transcript[0])
                q_convo.put("person " + str(transcript[1]) + " : ")
                thread = multiprocessing.Process(target=mainProcess.main, args=(transcript[0], index, arr, queueQA,))
                thread.start()
                # queueThread.put(thread)
                # threadList.append(thread)
                index += 1
            # Minutes.updateStart(transcript)
            # final_transcript.append(transcript_words)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.

            if re.search(r'\b(exit|quit)\b', transcript[0], re.I):
                print('Exiting..')
                global stop_loop
                stop_loop = 1
                # printing out transcription
                transcript_temp = ""
                tag = 1
                speaker = ""
                print('Final Transcription')
                for word_info in transcript_words:
                    if word_info.speaker_tag == tag:
                        speaker = speaker + " " + word_info.word
                    else:
                        transcript_temp += "speaker {}: {}".format(tag, speaker) + '\n'
                        # print(transcript_temp)
                        tag = word_info.speaker_tag
                        speaker = "" + word_info.word
                transcript_temp += "speaker {}: {}".format(tag, speaker)  # To add last word
                print(transcript_temp)
                f = open("transcription.txt", "w+")
                f.write(transcript_temp)
                f.close()
                # os.system("mainProcess.py")    #for non real time scenarios
                stream.closed = True
                break
        else:
            sys.stdout.write(str(corrected_time) + ': ' + transcript + '\r')
            stream.last_transcript_was_final = False


def main(input_queue, q_conversation, realTime=True, speech_file=None):
    global stop_loop
    global queueQA
    global arr
    global queueTranscripts
    global queueSpeakerTags
    global q_convo
    global queueThread
    q_convo = q_conversation

    max_conv_length = 1000
    stop_loop = multiprocessing.Value('i')  # used to stop all processes/loops when 'stop recording' is said
    stop_loop = 0
    queueQA = multiprocessing.Queue()
    queueTranscripts = multiprocessing.Queue()
    queueSpeakerTags = multiprocessing.Queue()
    queueThread = multiprocessing.Queue()
    arr = multiprocessing.Array('i', max_conv_length)

    process = multiprocessing.Process(target=calculation,
                                      args=(arr, queueQA, queueTranscripts, queueSpeakerTags, input_queue, stop_loop,
                                            queueThread,))
    process.start()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_final/FYP-key.json"

    if realTime == True:
        print("Starting real time process")

        client = speech.SpeechClient()
        config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=SAMPLE_RATE,
            language_code='en-US',
            enable_speaker_diarization=True,
            enable_automatic_punctuation=True,
            max_alternatives=1
            # enable_word_time_offsets=True
        )
        streaming_config = speech.types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        mic_manager = ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE)

        print('Say "Quit" or "Exit" to terminate the program.')

        with mic_manager as stream:

            while not stream.closed:
                sys.stdout.write('\n' + str(
                    STREAMING_LIMIT * stream.restart_counter) + ': NEW REQUEST\n')

                stream.audio_input = []
                audio_generator = stream.generator()

                requests = (speech.types.StreamingRecognizeRequest(
                    audio_content=content) for content in audio_generator)

                responses = client.streaming_recognize(streaming_config,
                                                       requests)

                # Now, put the transcription responses to use.
                listen_print_loop(responses, stream)

                if stream.result_end_time > 0:
                    stream.final_request_end_time = stream.is_final_end_time
                stream.result_end_time = 0
                stream.last_audio_input = []
                stream.last_audio_input = stream.audio_input
                stream.audio_input = []
                stream.restart_counter = stream.restart_counter + 1

                if not stream.last_transcript_was_final:
                    sys.stdout.write('\n')
                stream.new_stream = True

    else:
        print("Starting Non real time process")

        client = speech.SpeechClient()

        storage_uri = 'gs://fyp_1/BEP313-Scrum-Meetings1_1.wav'

        # Sample rate in Hertz of the audio data sent
        # sample_rate_hertz = 16000

        # The language of the supplied audio
        language_code = "en-US"

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        config = {
            # "sample_rate_hertz": sample_rate_hertz,
            "enable_speaker_diarization": True,
            "enable_automatic_punctuation": True,
            "language_code": language_code,
            "encoding": encoding,
            "audio_channel_count": 2,
        }
        audio = {"uri": storage_uri}

        operation = client.long_running_recognize(config, audio)

        print(u"Waiting for operation to complete...")
        response = operation.result()

        result = response.results[-1]

        x = result.alternatives[0]
        words_info = x.words

        tag = 1
        tag_prev = 1
        speaker = ""
        transcript = ""

        for word_info in words_info:
            if tag_prev == tag:
                tag_prev = tag
                tag = word_info.speaker_tag
                speaker = speaker + " " + word_info.word
            elif not (speaker[-1] == "." or speaker[-1] == "?"):
                speaker = speaker + " " + word_info.word
            else:
                transcript += "speaker {}: {}".format(tag_prev, speaker) + '\n'
                tag_prev = tag
                tag = word_info.speaker_tag
                speaker = "" + word_info.word

        transcript += "speaker {}: {}".format(tag_prev, speaker)
        print("transcript_1\n", transcript)
        f = open("transcript_1.txt", "w")
        f.write(transcript)
        f.close()

        f = open("transcript_1.txt")
        transcript = f.readlines()
        print("transcript_2\n", transcript)
        f.close()
        output = []
        for i in transcript:
            x = i.split(': ')
            sentence = x[-1]
            speaker_tag = x[0][-1]
            sentences = re.split(', |\. |\?  ', sentence)
            for j in sentences:
                output.append([j.rstrip(), speaker_tag])

        print('x: ', output)
        print(process_transcripts(output)[:])

#
# if __name__ == '__main__':
#     main(realTime=False)
