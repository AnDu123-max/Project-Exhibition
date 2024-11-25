from gtts import gTTS
from playsound import playsound


text = "Hello , how are you?"

tss = gTTS(text=text,lang="en")
tss.save("output.mp3")

playsound("output.mp3")

