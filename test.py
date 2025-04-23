import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.say("Hello! This is a test from Sōma.ai.")
engine.runAndWait()
