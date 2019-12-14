from pages.processAudio import *
#from pages.realTimeProcess import *
from datetime import datetime
import time
#from src import RTT2 as realTimeTranscriptionInfinite
import multiprocessing

index = 0
q = None
#root = None
delay = 100
transcription_list = []


class Conversation:

    def highlight_searched(self, *args):
        global all_listbox_items
        all_listbox_items = ()
        all_listbox_items = myList.get(0, END)

        search = search_var.get()

        for i, item in enumerate(all_listbox_items):
            if search.lower() in item.lower():
                myList.selection_set(i)
            else:
                myList.selection_clear(i)
        if search == '':
            myList.selection_clear(0, END)
            # root.after(1000,highlight_searched())

    def startProcess(self):
        global root
        global q
        global delay
        global transcription_list
        stop_process = False
        print("starting conversation startProcess")
        if not q.empty():
            print("not empty q")
            text = q.get()
            while not q.empty:
                time.sleep(1)
            speaker_tag = q.get()
            text = speaker_tag + text
            transcription_list.append(text)
            if text == "stop recording":
                stop_process = True
            global myList
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            myList.insert(ANCHOR, current_time, text)
            myList.yview(END)
        if stop_process == False:
            root.after(500, self.startProcess)
        else:
            print("StartProcess is Stopped ... ")

    def main(self, q_conversation):
        print("Creating Conversation page  ... ")
        global q
        q = q_conversation

        global root
        root = Toplevel()
        root.title("The Full Conversation")
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry("%dx%d" % (width, height))
        root.state('zoomed')

        # image = Image.open('C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_final/images/homepage.jpg')
        #
        # global copy_of_image
        # copy_of_image = image.copy()
        # photo = ImageTk.PhotoImage(image)
        # label = Label(root, image=photo)
        # label.place(x=0, y=0, relwidth=1, relheight=1)

        user_label = Label(root, bg="black", fg="white", text="The Full Conversation")
        user_label.config(font=("Courier", 50, 'bold'))
        user_label.pack(fill=Y)
        # Date
        date = Label(root, bg="yellow", fg="black", text="Date:" + datetime.now().strftime("%m/%d/%Y"))
        date.config(font=("Courier", 20, 'bold'))
        date.place(x=40, y=70, width=300, height=25)
        # Starting time
        start_time = Label(root, bg="pink", fg="black", text="Start:" + time.strftime("%H:%M:%S", time.localtime()))
        start_time.config(font=("Courier", 20, 'bold'))
        start_time.place(x=40, y=100, width=300, height=25)

        # search lable
        search_lable = Label(root, text="Search:", bg="pink", fg="black")
        search_lable.place(x=500, y=100, width=150, height=25)
        search_lable.config(font=("Courier", 20, 'bold'))

        search_button = Button(root, text="Go:", bg="pink", fg="black")
        search_button.place(x=870, y=100, width=50, height=25)

        quit_button = Button(root, fg="white", background="red", activebackground="red",
                             font=("Helvetica", 20, 'bold italic'), text='BACK', padx=10, pady=10)
        quit_button.place(relx=0.92, rely=0.8, anchor=CENTER)

        scrollbar = Scrollbar(root)
        # scrollbar.pack( side = RIGHT, fill = Y )
        scrollbar.place(x=1040, y=130, width=20, height=600)

        global search_var
        search_var = StringVar()
        search_var.trace('w', self.highlight_searched)
        entry_1 = Entry(root, textvariable=search_var)
        entry_1.place(x=700, y=100, width=150, height=25)

        global myList
        myList = Listbox(root, yscrollcommand=scrollbar.set, font=("Courier", 15))
        myList.place(relx=0.1, rely=0.2)
        myList.pack(fill=BOTH, )
        myList.place(x=40, y=130, width=1000, height=600)
        scrollbar.config(command=myList.yview)
        scrollbar.config(command=myList.see("end"))

        # filling things up to current point
        print("Adding initial items to MyList")
        global transcription_list
        for text in transcription_list:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            myList.insert(ANCHOR, current_time, text)
            myList.yview(END)
        self.startProcess()


# if __name__ == '__main__':
#     minutePage = Conversation()
#     minutePage.main(None)
