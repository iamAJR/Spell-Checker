from gtts import gTTS
import os
import playsound


def say(textg):
    tts = gTTS(text=textg, lang='en',tld='co.in')
    tts.save('audio.mp3')
    playsound.playsound('audio.mp3')

    os.remove('audio.mp3')

# say('hi')
# say('good')
