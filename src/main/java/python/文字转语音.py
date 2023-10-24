from gtts import gTTS

file = open("abc.txt", "r").read()

speech = gTTS(text=file, lang='zh-CN', slow=False)
speech.save("voice1.mp3")
