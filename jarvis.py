import pyttsx3
import speech_recognition
import datetime
import pywhatkit
import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller
from time import sleep
import pyautogui
import speech_recognition as sr
import random
import googletrans
from googletrans import Translator



engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

keyboard = Controller()

def speak(audio, rate=200):
    engine.setProperty("rate", rate)
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

def translateText(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def getHoroscope(zodiac_sign):
    url = f"https://aztro.sameerkumar.website/?sign={zodiac_sign}&day=today"
    response = requests.post(url)

    if response.status_code == 200:
        data = response.json()
        horoscope = data['description']
        speak(f"Today's horoscope for {zodiac_sign} is: {horoscope}")
    else:
        speak("Sorry, I couldn't fetch the horoscope at the moment.")

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


def greetMe():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    if 0 <= hour < 12:
        speak(f"Good Morning, sir. The time is {hour}:{minute} o'clock.")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon, sir. The time is {hour}:{minute} o'clock.")
    else:
        speak(f"Good Evening, sir. The time is {hour}:{minute} o'clock.")

    speak("Please tell me, How can I help you?")
    
def news():
    main_url = 'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=c00e6acd14ef49c786858974d72bbb2c'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth"]

    for i in range(len(day)):
        head.append(articles[i]["title"])
        speak(f"today's {day[i]} news is: {head[i]}")


def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 1)
            speak(result)
        except:
            speak("No speakable output available")


def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("jarvis", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")



def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from wikipedia....")
        query = query.replace("wikipedia", "")
        query = query.replace("search wikipedia", "")
        query = query.replace("jarvis", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to wikipedia..")
        speak(results)

def searchTemperature(query):
    search = "temperature in kathmandu"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    speak(f"current {search} is {temp}")

def searchWeather(query):
    search = "temperature in kathmandu"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    speak(f"current {search} is {temp}")

def showTime():
    strTime = datetime.datetime.now().strftime("%H:%M")
    speak(f"Sir, the time is {strTime}")

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def openAppWeb(query):
    if "open facebook" in query:
        webbrowser.open("https://www.facebook.com/")
        speak("Opening Facebook, sir")
    elif "open github" in query:
        webbrowser.open("https://github.com/")
        speak("Opening GitHub, sir")
    elif "open youtube" in query:  # Add a specific condition for opening YouTube
        query = query.replace("jarvis", "")
        query = query.replace("open", "")
        query = query.replace("youtube", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")
    else:
        speak("Sorry, I don't know how to open that.")



def handleUnknownCommand():
    speak("I'm sorry, I didn't understand, sir. Do you have any other work?")

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            greetMe()

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir, You can call me anytime")
                    break
                if "tell me a joke" in query:
                    tellJoke()

                if "daily horoscope" in query:
                    speak("Sure, please tell me your zodiac sign.")
                    zodiac_sign = takeCommand().lower()
                    getHoroscope(zodiac_sign)
                if "translate" in query:
                    speak("Sure, what would you like to translate?")
                    text_to_translate = takeCommand()
                    speak("To which language?")
                    target_language = takeCommand().lower()

                    translated_text = translateText(text_to_translate, target_language)
                    speak(f"The translation is: {translated_text}")


                elif "hello jarvis" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine jarvis" in query:
                    speak("that's great sir, do you have any work for me?")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you jarvis" in query:
                    speak("you are welcome sir, do you have any other work for me")

                elif "haha nice one jarvis" in query:
                    speak("I hope you liked it sir, do you have any other work for me?")
                elif "yes I did" in query:
                    speak("I'm glad. Do you have any other work sir?")
                elif "google" in query:
                    searchGoogle(query)
                elif "youtube" in query:
                    searchYoutube(query)
                elif "wikipedia" in query:
                    searchWikipedia(query)
                elif "temperature" in query:
                    searchTemperature(query)
                elif "weather" in query:
                    searchWeather(query)
                elif "tell me the news" in query:
                    speak("please wait sir, fetching the latest news")
                    news()
                elif "where i am" in query or "where we are" in query:
                    speak("wait sir, let me check")
                    try:
                        ipAdd = requests.get('https://api.ipify.org').text
                        print(ipAdd)
                        url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                        geo_requests = requests.get(url)
                        geo_data = geo_requests.json()
                        city = geo_data['city']
                        country = geo_data['country']
                        speak(f"sir i am not sure, but i think we are in {city} city of {country} country")
                    except Exception as e:
                        speak("sorry sir, due to the network issue I am not able to find where we are.")
                        pass
                

                elif "ip address" in query:
                    try:
                        ip = requests.get('https://api.ipify.org').text
                        speak(f"Your IP address is {ip}")
                    except requests.RequestException as e:
                        speak("Sorry, I couldn't fetch the IP address at the moment.")
                elif "the time" in query:
                    showTime()
                elif "finally sleep" in query:
                    speak("Going to sleep, sir")
                    exit()
                elif "open" in query:
                    openAppWeb(query)
                elif "close" in query:
                    closeAppWeb(query)
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                elif "volume up" in query:
                    volumeup()
                elif "volume down" in query:
                    volumedown()
                elif "jarvis, i am sad" in query:
                    playFavoriteSong()
                elif "tell me one joke" in query:
                    speak(f"Hope you like this one sir")
                    joke = get_random_joke()
                    speak(joke)
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(joke)
                elif "give me one random advice" in query:
                    speak(f"Here's an advice for you, sir")
                    advice = get_random_advice()
                    speak(advice)
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(advice)
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "").strip()
                    rememberMessage = rememberMessage.replace("jarvis", "").strip()
                    speak("You told me to remember that " + rememberMessage)  # Added space after "that"
                    file_path = r"C:\Users\ACER\OneDrive\Desktop\remember.txt"
                    with open(file_path, "a") as remember:
                        remember.write(rememberMessage + "\n")

                elif "what do you remember" in query:
                    file_path = r"C:\Users\ACER\OneDrive\Desktop\remember.txt"
                    with open(file_path, "r") as remember:
                        content = remember.read()
                        if content:
                            speak("You told me to remember the following:\n" + content)
                        else:
                            speak("I don't have any remembered information.")

                else:

                    handleUnknownCommand()
               
                speak("Do you have any other work, sir?")
                response = takeCommand().lower()
                if "no jarvis" in response:
                    speak("Alright, sir. Let me know if you need anything.")

                    break

                elif "yes" not in response:

                    speak("I'm sorry, I didn't understand. Do you have any other work, sir?")
