import os
from google.cloud import speech_v1p1beta1 as speech
import time

def main(speech_file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_final/FYP-key.json"

    print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

    client = speech.SpeechClient()

    # = '52223351.wav'

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=8000,
        language_code='en-US',
        enable_speaker_diarization=True,
        # diarization_speaker_count=2,
        audio_channel_count=2,
    )

    print('Waiting for operation to complete...')
    response = client.recognize(config, audio)

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


if __name__ == '__main__':
    s = time.time()
    main("52223351.wav")
    print(time.time()-s)