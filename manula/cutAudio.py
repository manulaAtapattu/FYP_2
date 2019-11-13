from pydub import AudioSegment
from pathlib import Path

files_path = 'C://Users//RedLine//Desktop//Semester 8//FYP//FYP_2//FYP_01//data\Bdb001.interaction.wav'

startMin = 00
startSec = 50

endMin = 10
endSec = 00

# Time to miliseconds
startTime = startMin*60*1000+startSec*1000
endTime = endMin*60*1000+endSec*1000

# Opening file and extracting segment
song = AudioSegment.from_wav( files_path )
extract = song[startTime:endTime]

# Saving
extract.export( 'Bdb001.interaction_1.1'+'-extract.wav', format="wav")
print("finished")