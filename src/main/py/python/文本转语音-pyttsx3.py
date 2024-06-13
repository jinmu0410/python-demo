import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.7)

engine.say("这里是杭州，一个来了不想走的城市，电商之都。")
engine.runAndWait()