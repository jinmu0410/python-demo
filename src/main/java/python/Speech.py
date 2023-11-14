import speech_recognition as sr

r = sr.Recognizer()
audio = "/Users/jinmu/Downloads/111.mp3"
text = r.recognize_google(audio_data = audio,language='zh-CN')

print(text)
