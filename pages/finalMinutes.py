# from pages.processAudio import *
# from pages.realTimeProcess import *
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import time
from src import RTT2 as realTimeTranscriptionInfinite
from pages.createMinutes import Conversation
import multiprocessing

index = 0
q = None
root = None
convo = None
q_convo = None
mylist_index = -1


class Minutes:

    def updateStart(self, text):
        global root
        print("new root : ", root)
        if root != None:
            print("root finally updated")
            root.after(2000, self.updateMinute(text))
        else:
            import time
            print("root not updated....")
            time.sleep(0.5)
            self.updateStart(text)

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
        global mylist_index
        stop_process = False
        # print("starting Minute startProcess")
        if not q.empty():
            print("not empty q")
            speaker_tag = q.get()
            mylist_index += 1
            while not q.empty:
                time.sleep(1)
            info = q.get()      #  in format [sentence, sentence_type]
            mylist_index += 1
            text = info[0]
            tag = info[1]
            text = speaker_tag + text
            if text == "stop recording":
                stop_process = True
            global myList
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            myList.insert(ANCHOR, current_time, text)
            myList.yview(END)
            if tag == 2:
                myList.itemconfig(mylist_index, {'fg': 'green'})
            elif tag == 3:
                myList.itemconfig(mylist_index, {'fg': 'red'})
        if stop_process == False:
            root.after(2000, self.startProcess)
        else:
            print("StartProcess is Stopped....")

    def main(self, real_time=True, file_path=None):
        print("Creating minute page  ... ")
        global root
        root = Toplevel()
        root.title("The Minute")
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

        user_label = Label(root, bg="black", fg="white", text="The Minute")
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

        def show_convo():
            global q_convo
            global convo
            print("Showing Full Minutes")
            convo.main(q_convo)


        show_conversation_button = Button(root, fg="white", background="#9E5B37", activebackground="#BC7F5E",
                                          font=("Courier", 18, 'bold'), activeforeground="white",
                                          text='Show Full Minutes', padx=15, pady=15, command=show_convo)
        show_conversation_button.place(relx=0.88, rely=0.7, anchor=CENTER)

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

        global q
        global q_convo
        global convo
        convo = Conversation()
        q = multiprocessing.Queue()  # queue to update interface
        q_convo = multiprocessing.Queue()  # queue to update full conversation page

        thread_1 = multiprocessing.Process(target=realTimeTranscriptionInfinite.main, args=(q, q_convo, real_time, file_path,))
        #thread_2 = multiprocessing.Process(target=convo.main, args=(q_convo,))

        thread_1.start()
        #thread_2.start()

        print("starting Minute startProcess")
        self.startProcess()
#
# if __name__ == '__main__':
#     minutePage = Minutes()
# minutePage.main()
