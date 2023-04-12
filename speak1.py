from gtts import gTTS
import os
import playsound
speak = gTTS(text="message_you_want",lang='vi',slow=False)
print(speak)
speak.save('sound.mp3')

