from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1 import enums
import os
import time

def sample_long_running_recognize(storage_uri):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_final/FYP-key.json"

    client = speech_v1p1beta1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    #sample_rate_hertz = 16000

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        #"sample_rate_hertz": sample_rate_hertz,
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
        elif not(speaker[-1] == "." or speaker[-1] == "?"):
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

s = time.time()
sample_long_running_recognize("gs://fyp_1/BEP313-Scrum-Meetings1_1.wav")
print(s - time.time())