import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()
print(sr.Microphone.list_microphone_names())
mic = sr.Microphone()
with mic as source:
    print("adjusting for Ambient Noise ")
    r.adjust_for_ambient_noise(source)
    print("listening ....")
    audio = r.listen(source)
print(r.recognize_google(audio))