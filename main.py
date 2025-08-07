import datetime
import os
import sys
import time
import webbrowser
import subprocess
import pyttsx3
import speech_recognition as sr
import pyautogui
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil

# from test_model import input_text

with open('intents.json') as file:
    data = json.load(file)

model = load_model('chat_model.h5')

with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open('label_encoder.pkl', 'rb') as encoder_file:
    label_encoder = pickle.load(encoder_file)


def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()


def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print('Listening......', end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit=10
        audio = r.listen(source)
    try:
        print("\r",  end="", flush=True)
        print('Recognizing.......',  end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r", end="", flush=True)
        print(f"user said : {query}\n")
    except Exception as e:
        print("say that again please")
        return "None"
    return query

def call_day():
    day = datetime.datetime.now().today().weekday() + 1
    day_dict ={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    day_of_week = day_dict.get(day, "Unknown")
    print(day_of_week)
    return day_of_week


def wish_command():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = call_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning, it's {day} and the time is {t}")
    elif(hour>=12) and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon, it's {day} and the time is {t}")
    else:
        speak(f"Good evening, it's {day} and the time is {t}")


def social_media(command):
    if 'facebook' in command:
        speak('Opening facebook')
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak('Opening whatsapp')
        webbrowser.open("https://www.whatsapp.com/")
    elif 'instagram' in command:
        speak('Opening instagram')
        webbrowser.open("https://www.instagram.com/")
    elif 'youtube' in command:
        speak('Opening youtube')
        webbrowser.open("https://www.youtube.com/")
    elif 'github' in command:
        speak('Opening github')
        webbrowser.open("https://www.github.com/")



def schedule():
    day = call_day().lower()
    speak("Your today's schedule is ")
    week = {
        "monday": "today is a holiday, so enjoy",
        "tuesday": "12 o'clock is lunchtime. From 3:50 to 5:35 you have classes",
        "wednesday": "From 11:30 to 1:10 you  have class. From 1:15 to 3:50 you have break. From 3:50 to 5:35 you have classes",
        "thursday": "From 11:30 to 1:10 you  have class. From 1:15 to 3:50 you have break. From 3:50 to 6:25 you have classes",
        "friday": "From 8:00 to 11:25 you  have class. From 11:25 to 1:15 you have break. From 1:15 to 6:25 you have classes",
        "saturday": "From 8:00 to 11:25 you  have class. From 11:25 to 1:15 you have break. From 1:15 to 4:40 you have classes",
        "sunday": "today is a holiday, so enjoy"
    }
    if day in week.keys():
        speak(week[day])

def openapp(command):
    if 'calculator' in command:
        speak('Opening calculator')
        os.startfile(r"C:\Windows\System32\calc.exe")
    elif 'notepad' in command:
        speak('Opening notepad')
        os.startfile(r"C:\Windows\System32\notepad.exe")
    elif 'vs' in command:
        speak('Opening vs code')
        os.startfile(r"C:\Users\Akhlaque Ahmad\AppData\Local\Programs\Microsoft VS Code\Code.exe")
    elif 'android studio' in command:
        speak('Opening android studio')
        os.startfile(r"C:\Program Files\Android\Android Studio\bin\studio64.exe")
    # elif 'vlc media player' in query:
    #     speak('Opening vlc')
    #     os.startfile(r"C:\Program Files\VideoLAN\VLC\vlc.exe")


def closeapp(command):
    if 'calculator' in command:
        speak('closing calculator')
        os.system('taskkill /f /im.calc.exe')
    elif 'notepad' in command:
        speak('closing notepad')
        os.system("taskkill /f /im notepad.exe")
    elif 'vs' in command:
        speak('closing vs code')
        os.system("taskkill /f /im Code.exe")
    elif 'android studio' in command:
        speak('closing android studio')
        os.system("taskkill /f /im studio64.exe")

def browsing(query):
    if 'google' in query:
        speak('hey buddy, what should i search on google..')
        search = command().lower()
        webbrowser.open(f"{search}")


def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage.")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"The battery is at {percentage} percent.")

    if percentage >= 50:
        speak('There is enough battery to be continue.')
    elif percentage >= 35 and percentage >= 45:
        speak('Connect the system for charging.')
    else:
        speak('The system has low battery, please connect it to charge.')


if __name__ == '__main__':
    wish_command()
    while True:
        # query = command().lower()
        query = input("Enter the command --> ")
        if('facebook' in query) or ('whatsapp' in query) or ('instagram' in query) or ('youtube' in query) or ('github' in query):
            social_media(query)
        elif('university time table' in query) or ('schedule' in query):
            schedule()
        elif('volume up' in query) or ('increase volume' in query):
            pyautogui.press('volumeup')
            speak('volume increased')
        elif ('volume down' in query) or ('decrease volume' in query):
            pyautogui.press('volumedown')
            speak('volume decreased')
        elif ('mute' in query) or ('mute the sound' in query):
            pyautogui.press('volumemute')
            speak('volume muted')
        elif('open calculator' in query) or ('open notepad' in query) or ('open pycharm' in query) or ('open vs' in query) or ('open android studio' in query) or ('open vlc media player' in query):
            openapp(query)
        elif ('close calculator' in query) or ('close notepad' in query) or ('close pycharm' in query) or ('close vs' in query) or ('close android studio' in query) or ('close vlc media player' in query):
            closeapp(query)
        elif('what' in query) or ('who' in query) or ('how' in query) or ('hi' in query) or ('thanks' in query) or ('hello' in query):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])
            tag = tag[0]

            for i in data['intents']:
                if i['tag'] == tag:
                    speak(np.random.choice(i['responses']))
        elif('open google' in query):
            browsing(query)
        elif('system condition' in query):
            speak('checking the system condition')
            condition()
        elif "exit" in query:
            sys.exit()

# speak("Hello I am Buddy Your AI Assistant")
