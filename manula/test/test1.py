from tkinter import *
from datetime import datetime
import time

index = 0
q = None
root = None
convo = None
q_convo = None


class Minutes:

    def main(self, real_time=True, file_path=None):
        print("Creating page  ... ")
        global root
        root = Tk()
        root.title("The Test")
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry("%dx%d" % (width, height))
        root.state('zoomed')

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

        quit_button = Button(root, fg="white", background="red", activebackground="red",
                             font=("Helvetica", 20, 'bold italic'), text='BACK', padx=10, pady=10)
        quit_button.place(relx=0.92, rely=0.8, anchor=CENTER)

        scrollbar = Scrollbar(root)
        # scrollbar.pack( side = RIGHT, fill = Y )
        scrollbar.place(x=1040, y=130, width=20, height=600)

        global myList
        myList = Listbox(root, yscrollcommand=scrollbar.set, font=("Courier", 15))
        myList.place(relx=0.1, rely=0.2)
        myList.pack(fill=BOTH, )
        myList.place(x=40, y=130, width=1000, height=600)
        scrollbar.config(command=myList.yview)
        scrollbar.config(command=myList.see("end"))

        _list = [1, 2, 3, 4, 5]
        for text in _list:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            myList.insert(ANCHOR, current_time, text)
            myList.itemconfig(text, {'fg': 'red'})
            #myList.yview(END)
        #myList.itemconfig(1, {'fg': 'red'})

        root.mainloop()

if __name__ == '__main__':
    minutePage = Minutes()
    minutePage.main()
