# Remove error messages. Activate only for demonstration. Remove when development
# import warnings
# warnings.filterwarnings("always")
# import tensorflow as tf
# tf.logging.set_verbosity(tf.logging.ERROR)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
import time

from pages.recordAudio import *
from pages.processAudio import *
from pages.realTimeProcess import *
from src.TextClassifier.BERT import run_classifier


class HomePage:
    def __init__(self):
        print("creating homepage")
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
            label.config(image=photo)
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

        def NRT_process():
            print('Opening page to process an existing audio recording....')
            ProcessAudio()

        ## Adding Buttons

        real_time_button = Button(root, fg="white", background="#9E5B37", activebackground="#BC7F5E",
                                  font=("Courier", 18, 'bold'), activeforeground="white", text='Real Time Processing',
                                  padx=15, pady=15, command=real_time_process)
        real_time_button.place(relx=0.15, rely=0.75, anchor=CENTER)

        # record_audio_button = Button(root, fg="white", background="#9E5B37", activebackground="#BC7F5E",font=("Courier",22,'bold'), activeforeground="white", text='Create New Recording', padx=15, pady=15, command = record_audio)
        # record_audio_button.place(relx=0.5, rely=0.75, anchor=CENTER)

        audio_file_button = Button(root, fg="white", background="#9E5B37", activebackground="#BC7F5E",
                                   font=("Courier", 18, 'bold'), activeforeground="white",
                                   text='Use Existing Recording', padx=15, pady=15, command=NRT_process)
        audio_file_button.place(relx=0.48, rely=0.75, anchor=CENTER)

        # show minutes of recorded Minutes
        show_minutes_button = Button(root, fg="white", background="#9E5B37", activebackground="#BC7F5E",
                                   font=("Courier", 18, 'bold'), activeforeground="white",
                                   text='Show minutes', padx=15, pady=15, command=real_time_process)
        show_minutes_button.place(relx=0.78, rely=0.75, anchor=CENTER)

        quit_button = Button(root, fg="white", background="red", activebackground="red",
                             font=("Helvetica", 20, 'bold italic'), text='QUIT', padx=10, pady=10, command=root.destroy)
        quit_button.place(relx=0.92, rely=0.1, anchor=CENTER)

        root.mainloop()


if __name__ == '__main__':
    homepage = HomePage()
    # testing text classifier
    # s = time.time()
    # run_classifier.main()
    # print('duration : ', time.time()-s)

# test the BERT system
#     test_sentences = ['good morning Everyone', 'We are hear to talk about the Nero project.',
#                       'It will be completed in about two weeks time.', 'We need to reduce the costs.',
#                       'That all right.', 'Moving on', "let's  talk about the airline project.",
#                       "Costs are way too high there.", 'And also', ' we must reduce the number of staff by half.',
#                       'staff costs are high.', 'Okay. The next item we need to talk about is hiring of employees.',
#                       'We need to a hire an interactive game developer.', 'That is to design VR projects.',
#                       'Okay then thats all for now.',
#                       'Thank you all for coming.']
# index = 0
# length = len(test_sentences)
# arr = [0]*length
# scores=[]
# for i in test_sentences:
#     score = run_classifier.main(i)
#     scores.append(score)
#     print(i,':',score)
# print(scores)
# # array([0.00157025, 0.00136921, 0.00137314, 0.9956874 ], dtype=float32), array([9.9536043e-01, 9.8726084e-04, 7.3049188e-04, 2.9218742e-03],
# #       dtype=float32), array([9.9642676e-01, 1.1628346e-03, 4.4006226e-04, 1.9702879e-03],
# #       dtype=float32), array([9.9830049e-01, 4.8582777e-04, 5.7173305e-04, 6.4205576e-04],
# #       dtype=float32), array([0.0019024 , 0.9934442 , 0.00251208, 0.0021413 ], dtype=float32), array([0.00491076, 0.00485543, 0.00386089, 0.98637295], dtype=float32), array([0.0288415 , 0.00346703, 0.00160185, 0.9660896 ], dtype=float32), array([9.9686384e-01, 7.1003922e-04, 1.0816418e-03, 1.3445070e-03],
# #       dtype=float32), array([0.06491866, 0.5677923 , 0.01678403, 0.35050505], dtype=float32), array([9.9798054e-01, 4.9951469e-04, 6.5302732e-04, 8.6690794e-04],
# #       dtype=float32), array([9.9813855e-01, 4.6544682e-04, 5.6460768e-04, 8.3141722e-04],
# #       dtype=float32), array([9.8381710e-01, 2.1649073e-03, 7.9770118e-04, 1.3220272e-02],
# #       dtype=float32), array([9.9779838e-01, 6.2227622e-04, 6.7736750e-04, 9.0189005e-04],
# #       dtype=float32), array([9.9694556e-01, 1.0282756e-03, 7.8883191e-04, 1.2374189e-03],
# #       dtype=float32), array([0.00120994, 0.00367936, 0.00150884, 0.99360186], dtype=float32), array([0.00158301, 0.00117431, 0.00153223, 0.9957105 ], dtype=float32)]
#
# [4,1,1,1,2,4,4,1,1,1,1,1,1,1,4,4]