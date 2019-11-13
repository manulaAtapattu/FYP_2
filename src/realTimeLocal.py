import io
import os

def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_2/FYP_01/key.json"
    client = speech.SpeechClient()

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print(u'Transcript: {}'.format(alternative.transcript))

stream_file = r'C:\Users\RedLine\Desktop\Semester 8\FYP\FYP_2\FYP_0.1\data\Bdb001.interaction.wav'
# with io.open(stream_file, 'r', encoding="utf8") as audio_file:
#     content = audio_file.read()

from pydub import AudioSegment
newAudio = AudioSegment.from_wav(stream_file)
i=0
def generator(newAudio):
    while (True):
        global i
        yield newAudio[1000*i:1000*(i+1)]
        i+=1

gen = generator(stream_file)
transcribe_streaming(next(gen))