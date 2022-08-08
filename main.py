import webbrowser
import pyjokes
import pyttsx3
import datetime
import speech_recognition as sr
import psutil
import subprocess
import requests
import json
import wikipedia
import pywhatkit as kit
import smtplib
import pyautogui
import pprint

engine = pyttsx3.init()
# getter method(gets the current value
# of engine property)

# Set voice (Female/Male)
# setter method .[0]=male voice and [1]=female voice in set Property.

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# Set Rate
newVoiceRate = 190
engine.setProperty('rate', newVoiceRate)


# for intro and indication of starting of system

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("the current date is")
    speak(date)
    speak(month)
    speak(year)
# Greet
def wishMe():
    """Greets the user according to the time"""
    speak("Welcome back sir !")
    hour = datetime.datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak("Good Morning Sir")
    elif (hour >= 12) and (hour < 16):
        speak("Good afternoon Sir")
    elif (hour >= 16) and (hour < 21):
        speak("Good Evening Sir")
    else:
        speak("Good Night")
    speak("Arcii at your service. How may I assist you?")
#screenshot
def screenshot():
    name = input("enter name of file :")
    speak("Alright sir, taking the screenshot")
    img = pyautogui.screenshot()
    name = f"{name}.png"
    img.save(name)
#Battery and CPU percent
def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at" + usage)
    battery = psutil.sensors_battery()
    speak("battery is at")
    speak(battery.percent)
# Email
def sendmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("abc@gmail.com", "Password")
    server.sendmail("abc@gmail.com", to,  content)
    server.close()
#jokes
def jokes():
    speak(pyjokes.get_joke())
#news
def get_news():
    url = 'http://newsapi.org/v2/top-headlines?country=in&apiKey=120a06450bf74e7e9752732fdc7dd0d2'
    news = requests.get(url).text
    news_dict = json.loads(news)
    articles = news_dict['articles']
    try:
        return articles
    except:
        return False
def getNewsUrl():
    return 'https://newsapi.org/v2/top-headlines?country=in&apiKey=120a06450bf74e7e9752732fdc7dd0d2'

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)
# Takes user input, recognizes it using Speech Recognition module and converts it into text

def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    # it converts the audio input into String
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        return 'None'
    return query


if __name__ == "__main__":
    wishMe()
    while True:
        query = take_user_input().lower()
        if query is None:
            speak('Sorry, could not hear anything,say that again !!')
            continue
        # logic for executing tasks based on query
        elif "how are you" in query:
            speak("I'm fine sir, how can i help you ?")
        elif "who are you" in query:
            speak("Sir I am Arcii personal assistant ")
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...please wait')
            query = query.replace('wikipedia', "")
            results = wikipedia.summary(query, sentences=2)
            print(results)
            speak(results)
        elif 'google chrome' in query or 'browser' in query:
            subprocess.call('google-chrome')
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open('https://www.google.co.in/')
        elif 'open stackoverflow' in query or 'stackoverflow' in query:
            webbrowser.open('https://stackoverflow.com/')
        elif 'play music' in query:
            webbrowser.open('https://wynk.in/music?icid=wynk_banner')
        elif 'the time' in query or 'time' in query or 'clock' in query:
            time()
        elif 'date' in query:
            date()
        elif 'screenshot' in query or 'snap' in query or 'take ss' in query:
            screenshot()
            speak("Done!")
        elif 'search in chrome' in query or 'search on chrome' in query:
            speak("What should I search?")
            chromepath = "C:\Program Files\Google\Chrome\Application\chrome.exe %s"
            search = take_user_input().lower()
            webbrowser.get(chromepath).open_new_tab(search+ ".com")
        elif 'take a note' in query or 'write a note' in query:
            speak('What should I write?')
            note_text = take_user_input()
            if note_text is not None:
                f = open('notes.txt', 'a')
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                f.write(timestamp + '\n')
                note = note_text + '\n\n'
                f.write(note)
                f.close()

        elif 'remember that' in query or 'secret' in query or 'reminder' in query:
            speak("what should i remember?")
            data = take_user_input()
            speak("you said me too remember" + data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "do you know anything" in query or "personal info" in query:
            remember = open("data.txt", "r")
            speak("you said me to remember that" + remember.read())

        elif "cpu" in query or "battery" in query:
            cpu()

        elif 'weather' in query or 'climate' in query:
            speak('Which city')
            city = take_user_input()
            apiKey = '05c03cf5c074804c446c16613a3e73f8'
            response = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric')
            x = response.json()
            if x["cod"] != "404":
                y = x['main']
                temperature = x['main']["temp"]
                pressure = x['main']["pressure"]
                humidity = x['main']["humidity"]
                desc = x["weather"][0]["description"]
                weather_detail = f'Current temperature is {temperature}, pressure is {pressure} hPa, humidity is {humidity} %, Weather condition is {desc}'
                speak(weather_detail)
            else:
                speak('Sorry, could not find the city')
        elif 'joke' in query or 'entertain' in query:
            jokes()
        elif "buzzing" in query or "news" in query or "headlines" in query:
            news_res = get_news()
            speak('Source: India News API')
            speak('Todays Headlines are..')
            for index, articles in enumerate(news_res):
                pprint.pprint(articles['title'])
                speak(articles['title'])
                if index == len(news_res) - 2:
                    break
            speak('These were the top headlines, Have a nice day Sir!!..')

        elif "send whatsapp message" in query or 'send message' in query or 'whatsapp' in query:
            speak('On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message sir?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif "send an email" in query or 'email' in query or 'mail' in query:
            try:
                speak("wait a second sir!! ")
                to = "xyz@gmail.com"
                speak("What is the message sir?")
                content = take_user_input()
                sendmail(to, content)
                if sendmail(to, content):
                    speak("I've sent the email sir.")
                else:
                    speak("Sorry sir. Couldn't send your mail. Please try again")
            except Exception as e:
                speak(e)
                speak("Unable to send the message")

        elif 'Arcii quit' in query or 'exit' in query or 'close' in query or 'offline' in query or 'bye' in query:
            speak("Thanks you for using Arcii Sir")
            exit()
