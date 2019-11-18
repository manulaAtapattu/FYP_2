# copyright to M.R.Atapattu

This project is an Automatic minute maker. It takes as input a conversation between multiple people at a meeting.
The minutes will be the output of the system. The minutes will contain the most important parts of the conversation.

# starting the application

Step 1:

run the homepage.py file in the "pages"  directory
output - the "homepage" user interface will open

Step 2:

Click "real time" button in homepage. Then another page will open.
In the newly open page, press the "start"  button.
At this point the meeting will begin to record and process in real-time(real time application not done at present).

Step 3:

Say the words "stop recording" in the conversation to stop the recording process.
(problem - stop recording should be said independently)

# technical explanation of the process

src/homepage.py => src/RTT2.py (transcribe voice into conversation in real time)
=> src/mainProcess.py (process conversation)

