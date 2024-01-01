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

def greetMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good Morning, sir. The time is {hour} o'clock.")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon, sir. The time is {hour} o'clock.")
    else:
        speak(f"Good Evening, sir. The time is {hour} o'clock.")

    speak("Please tell me, How can I help you?")

def news():
    main_url = 'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=c00e6acd14ef49c786858974d72bbb2c'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]

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

def playFavoriteSong():
    favorite_songs = [
        "Despacito",  # Replace with the name of your favorite songs
        "Shape of You",
        "Believer",
        # Add more songs as needed
    ]
    song = random.choice(favorite_songs)
    speak(f"Playing your favorite song, {song} on YouTube")
    query = f"play {song} on YouTube"
    searchYoutube(query)

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

def playFavoriteSong():
    favorite_song = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"  # Replace with the link of your favorite song
    speak("Playing your favorite song on YouTube")
    try:
        print(f"Opening {favorite_song} in the browser...")
        webbrowser.open(favorite_song)
        print("Song opened successfully.")
    except Exception as e:
        print(f"Error playing the song: {e}")
        speak("I encountered an error while playing the song. Sorry for the inconvenience.")

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


def openAppWeb(query):
    if "open facebook" in query:
        webbrowser.open("https://www.facebook.com/")
        speak("Opening Facebook, sir")
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube, sir")
    elif "open github" in query:
        webbrowser.open("https://github.com/")
        speak("Opening GitHub, sir")
    # Add more conditions for other apps or websites as needed
    else:
        speak("Sorry, I don't know how to open that.")

def closeAppWeb(query):
    if "close facebook" in query:
        # You may need to implement a method to close the Facebook tab or window.
        speak("Closing Facebook, sir")
    elif "close youtube" in query:
        # You may need to implement a method to close the YouTube tab or window.
        speak("Closing YouTube, sir")
    elif "close github" in query:
        # You may need to implement a method to close the GitHub tab or window.
        speak("Closing GitHub, sir")
    # Add more conditions for other apps or websites as needed
    else:
        speak("Sorry, I don't know how to close that.")



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
                elif "hello jarvis" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine jarvis" in query:
                    speak("that's great sir, do you have any work for me?")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
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
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "")
                    rememberMessage = rememberMessage.replace("jarvis", "")
                    speak("You told me to remember that" + rememberMessage)
                    remember = open("Remember.txt", "a")
                    remember.write(rememberMessage + "\n")
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt", "r")
                    speak("You told me to remember the following:\n" + remember.read())
                    remember.close()
                elif "jarvis, i am sad" in query:
                    print(f"Recognized query: {query}")
                    playFavoriteSong()
                else:
                    handleUnknownCommand()
                    response = takeCommand().lower()
                    if "yes" in response:
                        speak("What can I do for you, sir?")
                    elif "no" in response:
                        speak("Alright, sir. Let me know if you need anything.")
                        break
                    else:
                        speak("I'm sorry, I didn't understand. Do you have any other work, sir?")
