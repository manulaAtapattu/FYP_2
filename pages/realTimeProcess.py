from tkinter import *
from PIL import Image, ImageTk
# from trainrecord import *
# from record_module import *
# from GMM1 import *
import threading
# from src import RTT2 as realTimeTranscriptionInfinite
#from pages.finalMinutes import Minutes


fname = ''
inProcess = False
keywords = None
minutes = None


class RealTimeProcess:
    def __init__(self):
        global root
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

        ## Adding Buttons

        # global stop_record_button
        # stop_record_button = Button(root, text="Stop", bg="#CA6F1E", fg="white", font=("Courier", 30, 'bold'), command=lambda : self.stopProcess(), state=DISABLED)
        # stop_record_button.place(relx=0.7, rely=0.6, anchor=CENTER)

        # start recording button
        rec_button = Button(root, text="Start", bg="#CA6F1E", fg="white", font=("Courier", 30, 'bold'))
        rec_button.config(command=lambda: self.startProcess(input_box))
        rec_button.place(relx=0.4, rely=0.6, anchor=CENTER)

        # keywords input box
        # these keywords will be given a higher weight
        user_label = Label(root, fg="black", text="Enter Keywords : Keywords should be separated by a comma",
                           font=("Courier", 15, 'bold'))
        user_label.place(relx=0.18, rely=0.32, anchor='w')
        input_box = Entry(root, bg="#CA6F1E", fg="white", font=("Courier", 20, 'bold'), width=40)
        input_box.place(relx=0.4, rely=0.4, anchor=CENTER)

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

    def startProcess(self, input_box):
        # stop_record_button['state'] = NORMAL
        print("starting processes")
        global keywords
        #global minutes
        keywords = (input_box.get()).split(',')
        print("keywords : ", keywords)
        #global minutes
        minutes = Minutes()
        minutes.main()
        #realTimeTranscriptionInfinite.main()
        #process = threading.Thread(target=minutes.main, args=())
        #process2 = threading.Thread(target=realTimeTranscriptionInfinite.main, args=())
        # realTimeTranscriptionInfinite.main()
        # process.start()
        # process2.start()

    # def stopProcess(self):
        # stop_record_button['state'] = DISABLED
        #realTimeTranscriptionInfinite.stop_process()

