from pages.recordAudio import*
from pages.processAudio import *
from pages.realTimeProcess import *

root = Tk()
root.title("Speaker Identification")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.state('zoomed')

## Function for resizing the Image

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo

## Resizable Image

image = Image.open(r'../images/homepage.jpg')
global copy_of_image
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo)
label.place(x=0, y=0, relwidth=1, relheight=1)
label.bind('<Configure>', resize_image)

user_label = Label(root, bg="black", fg="white", text="Automatic Minute Maker")
user_label.config(font=("Courier", 55, 'bold'))
user_label.place(relx=0.2, rely=0.25, anchor='w')


## Function

def real_time_process():
    print('Opening page to real_time_process....')
    RealTimeProcess()

def record_audio():
    print('Opening page to record audio....')
    RecordAudio()

def process():
    print('Opening page to process an existing audio recording....')
    ProcessAudio()

## Adding Buttons

real_time_button = Button(root, fg="white", background="#9E5B37", activebackground="#BC7F5E",font=("Courier",22,'bold'), activeforeground="white", text='Real Time Processing', padx=15, pady=15, command = real_time_process)
real_time_button.place(relx=0.2, rely=0.75, anchor=CENTER)

# record_audio_button = Button(root, fg="white", background="#9E5B37", activebackground="#BC7F5E",font=("Courier",22,'bold'), activeforeground="white", text='Create New Recording', padx=15, pady=15, command = record_audio)
# record_audio_button.place(relx=0.5, rely=0.75, anchor=CENTER)

audio_file_button = Button(root, fg="white", background="#9E5B37", activebackground="#BC7F5E",font=("Courier",22,'bold'), activeforeground="white", text='Use Existing Recording', padx=15, pady=15, command = process)
audio_file_button.place(relx=0.8, rely=0.75, anchor=CENTER)

quit_button = Button(root, fg="white", background="red", activebackground="red",font=("Helvetica",20,'bold italic'), text='QUIT', padx=10, pady=10, command = root.destroy)
quit_button.place(relx=0.92, rely=0.1, anchor=CENTER)

root.mainloop()
