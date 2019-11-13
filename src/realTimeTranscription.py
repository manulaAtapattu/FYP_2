from __future__ import division

import re
import sys
import os

from google.cloud import speech_v1p1beta1 as speech
# from google.cloud.speech import enums
# from google.cloud.speech import types
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
stop_process = False
final_text = []
final_text_2 = []

class MicrophoneStream(object):

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

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

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):

        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self,root):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        print("Detected .... ")
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            #root.after(1000, self.generator())

            yield b''.join(data)


def listen_print_loop(responses):

    num_chars_printed = 0
    print("starting listen_print_loop")
    for response in responses:
        print("starting response loop")

        global stop_process
        if (stop_process == True):
            print('Exiting..')
            break

        if not response.results:
            print("not response.results")
            continue

        #-------------------------------
        # result = response.results[0]
        # result_2 = result.alternatives[0]
        # words_info = result_2.words
        # for word_info in words_info:
        #     print("speaker : ", word_info.speaker_tag)
        #-------------------------------

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            print("not rresult.alternatives")
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0]
        transcript2 = transcript.transcript
        #print("transcript2 : ",transcript2)
        transcript3 = transcript.words
        print("transcript3 : ",transcript3)
        transcript = transcript.transcript


        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            print("not result.is_final")
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)


        else:
            print("final")
                #print (f"word : {word_info.word} | person_tag : {word_info.speaker_tag}")
            #print(transcript + overwrite_chars)
            global final_text
            final_text.append(transcript + overwrite_chars)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(stop recording)\b', transcript, re.I):
                global final_text_2
                # for word_info in transcript3:
                #     final_text_2.append([word_info.word, word_info.speaker_tag])
                transcript4 = ""
                tag = 1
                speaker = ""
                for word_info in transcript3:
                    if word_info.speaker_tag == tag:
                        speaker = speaker + " " + word_info.word
                    else:
                        transcript4 += "speaker {}: {}".format(tag, speaker) + '\n'
                        tag = word_info.speaker_tag
                        speaker = "" + word_info.word
                transcript4 += "speaker {}: {}".format(tag, speaker)  # To add last word
                print(transcript4)
                print('Exiting..')
                #print(final_text_2)
                break

            num_chars_printed = 0

#
# def stop_process():
#     global stop_process
#     stop_process = True
#     print("Stopping process ....")

def main(root):
    print("starting main")
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_2/FYP_01/key.json"

    client = speech.SpeechClient()
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        enable_speaker_diarization=True,
        language_code=language_code)
    streaming_config = speech.types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        print("Starting MicrophoneStream")
        audio_generator = stream.generator(root)
        requests = (speech.types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)
        # Now, put the transcription responses to use.
        listen_print_loop(responses)

# if __name__ == '__main__':
#     main()