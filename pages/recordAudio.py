from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
# from trainrecord import *
# from record_module import *
# from GMM1 import *

fname = ''


class RecordAudio:
    def __init__(self):
        global root
        root = Toplevel()
        root.title("Recognizing speakers")
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry("%dx%d" % (width, height))
        root.state('zoomed')

        ## Resizable Image

        image = Image.open(r'../images/microphone.jpg')
        global copy_of_image
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        global label
        label = Label(root, image=photo)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.bind('<Configure>', self.resize_image)

        ## Adding TextBoxes

        # Entering filename
        user_label = Label(root, bg="black", fg="white", text="Enter Output filename")
        user_label.config(font=("Courier", 25))
        user_label.place(relx=0.3, rely=0.4, anchor='w')
        global v1
        v1 = StringVar()
        user_entry = self.EntryWithPlaceholder(root, "Eg:-audioFile1...", "grey", textvariable=v1)
        user_entry.config(font=("Courier", 20, 'italic'))
        user_entry.place(relx=0.75, rely=0.4, anchor='e')


        ## Adding Buttons

        global stop_record_button
        stop_record_button = Button(root, text="Stop Recording", bg="#CA6F1E", fg="white", font=("Courier", 30, 'bold'), command=lambda : self.stop_reco(), state=DISABLED)
        stop_record_button.place(relx=0.7, rely=0.6, anchor=CENTER)

        rec_button = Button(root, text="Start Recording", bg="#CA6F1E", fg="white", font=("Courier", 30, 'bold'))
        rec_button.config(command=lambda : self.reco(stop_record_button))
        rec_button.place(relx=0.4, rely=0.6, anchor=CENTER)


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

    def reco(self, stop_record_button):
        global fname
        global v1

        print("Recording audio")
        stop_record_button['state'] = NORMAL

        import pyaudio
        import wave

        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        global RATE
        RATE = 44100
        global CHUNK
        CHUNK = 1024

        global recording
        recording = TRUE
        WAVE_OUTPUT_FILENAME = "file.wa.v"

        global audio
        audio = pyaudio.PyAudio()

        # start Recording
        global stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print("recording...")
        global frames
        frames = []
        self.recording()

        try:
            print("in try")
            # while recording:

                # data = stream.read(CHUNK)
                # frames.append(data)

            #self.recording()

            # stop Recording
            #if (recording==FALSE):
                # stream.stop_stream()
                # stream.close()
                # audio.terminate()
                #
                # waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                # waveFile.setnchannels(CHANNELS)
                # waveFile.setsampwidth(audio.get_sample_size(FORMAT))
                # waveFile.setframerate(RATE)
                # waveFile.writeframes(b''.join(frames))
                # waveFile.close()
                #print("finished recording")


        except:
            print("Recording Failed")
            #fname = testr(v1.get())

    def stop_reco(self):
        print("Stoping record....")
        global recording
        global stop_record_button
        recording = FALSE
        stop_record_button['state'] = DISABLED

    def recording(self):
        global frames
        global CHUNK
        global stream
        global root
        if recording == TRUE:
            for i in range(0, int(RATE / CHUNK)):
                data = stream.read(CHUNK)
                frames.append(data)
            print(f"still recording {len(frames)}....")
            root.after(1000, self.recording)
        else:
            print("stopping recording")
            # stop Recording
            if (recording == FALSE):
                stream.stop_stream()
                stream.close()
                global audio
                audio.terminate()

                import wave
                import pyaudio
                CHANNELS = 2
                FORMAT = pyaudio.paInt16

                WAVE_OUTPUT_FILENAME = "output_recording.wav"
                waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                waveFile.setnchannels(CHANNELS)
                waveFile.setsampwidth(audio.get_sample_size(FORMAT))
                waveFile.setframerate(RATE)
                waveFile.writeframes(b''.join(frames))
                frames = waveFile.getnframes()
                rate = waveFile.getframerate()
                print(f"duration of audio = {frames/float(rate)}")
                waveFile.close()
                from tkinter import messagebox
                messagebox.showinfo("Automatic Minute Maker", f"Finished recording. Audio has been saved in file {WAVE_OUTPUT_FILENAME}")
                print("finished recording")


