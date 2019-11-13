from pydub import AudioSegment

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

sound = AudioSegment.from_file("m0001_us_m0001_00001.wav", "wav")
normalized_sound = match_target_amplitude(sound, -32.0)
normalized_sound.export("nomrmalizedAudio_m1_1.wav", format="wav")