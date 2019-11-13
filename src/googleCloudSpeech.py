import io
import os

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech import enums
#from google.cloud.speech import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_2/FYP_01/key.json"
print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])


# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    'Data_set/samples/new',
    'nomrmalizedAudio2_f1_1_m1_1.wav')

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = speech.types.RecognitionAudio(content=content)

config = speech.types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    #sample_rate_hertz=44100,
    #audio_channel_count=1,
    enable_automatic_punctuation=True,
    #enable_speaker_diarization=True,
    language_code='en-US')

# Detects speech in the audio file
response = client.recognize(config, audio)

result = response.results

f = open("C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_2/FYP_01/output/transcriptions/EN2001a.txt", "a")
for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
    f.write(result.alternatives[0].transcript)
f.close()
