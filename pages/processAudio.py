from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from pydub import AudioSegment
from scipy.io import wavfile
import wave
import pyaudio
import pickle
from sklearn.mixture import GaussianMixture
import scipy.io.wavfile as wav
import statistics as stat
import numpy as np
import datetime
from pydub import AudioSegment

# from trainrecord import *
# from record_module import *
# from GMM1 import *

fname = ''

class ProcessAudio:
    def __init__(self):
        root = Toplevel()
        root.title("Recognizing speakers")
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry("%dx%d" % (width, height))
        root.state('zoomed')

        ## Resizable Image

        image = Image.open(r'../images/startpage.jpg')
        global copy_of_image
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        global label
        label = Label(root, image=photo)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.bind('<Configure>', self.resize_image)

        ## Adding TextBoxes

        # Entering filename
        user_label = Label(root, bg="#CA6F40", fg="white", text="File Name")
        user_label.config(font=("Courier", 30))
        user_label.place(relx=0.35, rely=0.4, anchor='w')

        rec_button = Button(root, text="Attach audio file", bg="white", fg="black", font=("Courier", 20, 'italic'), command=self.attach_file)
        rec_button.place(relx=0.6, rely=0.4, anchor=CENTER)


        ## Adding Buttons

        process_button = Button(root, text="Process", bg="#CA6F40", fg="white", font=("Courier", 35), command=self.process)
        process_button.place(relx=0.4, rely=0.6, anchor=CENTER)


    ## Class for a placeholder

    class EntryWithPlaceholder(Entry):
        def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', textvariable=None):
            super().__init__(master, textvariable=textvariable)

            self.placeholder = placeholder
            self.placeholder_color = color
            self.default_fg_color = self['fg']

            self.bind("<FocusIn>", self.foc_in)
            self.bind("<FocusOut>", self.foc_out)

            self.put_placeholder()

        def put_placeholder(self):
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

        def foc_in(self, *args):
            if self['fg'] == self.placeholder_color:
                self.delete('0', 'end')
                self['fg'] = self.default_fg_color

        def foc_out(self, *args):
            if not self.get():
                self.put_placeholder()

    ## Function for resizing the Image

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        global copy_of_image
        image = copy_of_image.resize((new_width, new_height))
        global photo
        photo = ImageTk.PhotoImage(image)
        global label
        label.config(image=photo)
        label.image = photo

    ## Recording

    def reco(self):
        global fname
        global v1, v2
        try:
            print("Recording")
            #fname = testr(str(v1.get()), float(v2.get()))
        except:
            print("Recording Failed")
            #fname = testr(v1.get())

    def saveAudioData(self, fname, fs, data):
        CHUNK = 1024
        p = pyaudio.PyAudio()
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        outputName = "training_data\\audioData.wav"

        print('Saving data of', fname,' in file : ', outputName)
        wf = wave.open(fname, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(fs)
        wf.writeframes(data)
        wf.close()

    def writeAudio(self, rate, data, i):
        writeDestn = 'training_data/sample'+str(i)+'.wav'
        wav.write(writeDestn, rate, data)
        return

    def attach_file(self):
        print("attaching file")
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("wav files","*.wav"),("all files","*.*")))
        #fs, data = wavfile.read(filename)
        #self.saveAudioData(filename, fs, data)

        with wave.open(filename, "rb") as wav_file:  # Open WAV file in read-only mode.
            # Get basic information.
            n_channels = wav_file.getnchannels()  # Number of channels. (1=Mono, 2=Stereo).
            sample_width = wav_file.getsampwidth()  # Sample width in bytes.
            framerate = wav_file.getframerate()  # Frame rate.
            n_frames = wav_file.getnframes()  # Number of frames.
            comp_type = wav_file.getcomptype()  # Compression type (only supports "NONE").
            comp_name = wav_file.getcompname()  # Compression name.
            frames = wav_file.readframes(n_frames)  # Read n_frames new frames.

            with wave.open("training_data\\inputAudio.wav", "wb") as wav_file:  # Open WAV file in write-only mode.
                # Write audio data.
                params = (n_channels, sample_width, framerate, n_frames, comp_type, comp_name)
                wav_file.setparams(params)
                wav_file.writeframes(frames)

        # training created file 'inputAudio'
        self.trainAudio()


    def trainAudio(self):
        source = 'training_data/'
        path = 'inputAudio.wav'
        dest = 'models/'

        rate, sig = wav.read(source + path)
        mfcc_feat = mfeatures.extract_features(sig, rate)

        gmm = GaussianMixture(n_components=16, covariance_type='diag', n_init=10)
        gmm.fit(mfcc_feat)

        # dumping the trained gaussian model
        print('Creating trained gmm file')
        picklefile = path.split("-")[0] + ".gmm"
        pickle.dump(gmm, open(dest + picklefile, 'wb'))

    def getSquareArray_1by2(self, Array):
        Sum = 0
        for arr1 in Array:
            for arr2 in arr1:
                Sum += arr2 ** 2
        return Sum.sum()

    def process(self):
        #get AudioFile for processing
        print('Start processing audio file')

        # obj = wave.open('training_data/inputAudio.wav', 'r')
        # nframes = obj.getnframes()
        # framerate = obj.getframerate()
        # print ('nframes : ', nframes, '| type : ', type(nframes))
        # print('framerate : ', framerate, '| type : ', type(framerate))
        # return

        rate, sig = wav.read('training_data/inputAudio.wav')
        print('Length of Audio : ', len(sig), ' | sample rate : ', rate)

        speakerNo = 0
        speakerModels = []
        scoreList = []
        power_spectrum_list = []
        varience_list = []
        i = 0
        while i < len(sig):
            # print(sig[i])
            # i+=10
            # if i>(len(sig)-1):
            #     break
            # else:
            #     continue
            if abs(sig[i])>=1500:
                print('sound identified')
                temp_mean = stat.mean(abs(sig[i:i + 8000]))
                print ('mean : ',temp_mean)
                if temp_mean>650:
                    print ('sound identified as voice')
                    tempRate = rate
                    tempSig = sig[i:i + 15000]
                    self.writeAudio(tempRate, tempSig, i)
                    #print('Created partition ...')

                    i += 15001
                    if speakerNo == 0:
                        print ('Adding first speaker')
                        frames = processing.stack_frames(tempSig, sampling_frequency=tempRate,
                                                         frame_length=0.020,
                                                         frame_stride=0.01,
                                                         filter=lambda x: np.ones((x,)),
                                                         zero_padding=True)
                        power_spectrum = processing.power_spectrum(frames, fft_points=512)
                        power_spectrum_list.append(power_spectrum)
                        speakerNo = 1
                    else :
                        frames = processing.stack_frames(tempSig, sampling_frequency=tempRate,
                                                         frame_length=0.020,
                                                         frame_stride=0.01,
                                                         filter=lambda x: np.ones((x,)),
                                                         zero_padding=True)
                        power_spectrum = processing.power_spectrum(frames, fft_points=512)
                        for ps in power_spectrum_list:
                            PSdif = ps - power_spectrum
                            variance = self.getSquareArray_1by2(PSdif)
                            print('Power Spectrum variance : ', variance)

                            if variance > 2.2 * (10**20):
                                power_spectrum_list.append(power_spectrum)
                                print('Adding Speaker')
                                speakerNo+=1
                                break

            print('progress', i, '/', len(sig),' | signal strength : ', sig[i])
            i+=100
        print('Number of Speakers : ', speakerNo)
        print('\nProcess completed at time : ', datetime.datetime.now())