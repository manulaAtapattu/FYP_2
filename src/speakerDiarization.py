import os
import scipy.io.wavfile as wav
from google.cloud import speech_v1p1beta1 as speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_2/FYP_01/key.json"
#key.json

print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

client = speech.SpeechClient()

#location  of input audio file
#speech_file = 'data/'+file_name+'.wav'
#destination_file = 'divisions/'+file_name+'part_'

audio_divisions=[]

#rate, sig = wav.read(speech_file)
#audio_length = len(sig)
#num_of_divisions = 6   # how you want to divide the audio
#avg = int(audio_length/float(num_of_divisions))

file_name =  'Bdb001.interaction_1.1-extract'
gcs_uri = 'gs://fyp1_bucket/'+file_name+'.wav'

# for i in range(num_of_divisions):
#     wav.write(destination_file+str(i)+'.wav', rate, sig[i*avg:(i+1)*avg])
#     with open(destination_file+str(i)+'.wav', 'rb') as audio_file:
#         content = audio_file.read()
#         audio = speech.types.RecognitionAudio(content=content)
#         audio_divisions.append(audio)


config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    #sample_rate_hertz=8000,
    language_code='en-US',
    enable_speaker_diarization=True,
    enable_automatic_punctuation=True,
    #diarization_speaker_count=2
    )

print(f'Starting operation on {file_name}.... ')
responses = []

audio = speech.types.RecognitionAudio(uri=gcs_uri)
#print(f'Operating on part_{i}...')
operation = client.long_running_recognize(config, audio)
response = operation.result()
responses.append(response)

result = response.results[-1]
result_2 = result.alternatives[0]
words_info = result_2.words

# Printing out the output:
# for word_info in words_info:
#     print(u"word: '{}', speaker_tag: {}".format(
#         word_info.word, word_info.speaker_tag))`

tag=1
speaker = ""
transcript = ""

for word_info in words_info:
        if word_info.speaker_tag==tag:
            speaker = speaker+" "+word_info.word
        else:
            transcript += "speaker {}: {}".format(tag,speaker) + '\n'
            tag = word_info.speaker_tag
            speaker = ""+word_info.word

transcript += "speaker {}: {}".format(tag,speaker) #To add last word
output_file = 'output/transcriptions/'+file_name
file = open(output_file,"w")
file.write(transcript)
file.close()
print("finished")
#print(transcript)


