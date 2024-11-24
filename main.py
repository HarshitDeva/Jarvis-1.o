import subprocess
import spotipy
import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import subprocess as subp
import wolframalpha
import pyautogui
import webbrowser
import time
import random
from datetime import datetime
from dotenv import load_dotenv

from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast, \
    schedule, condition, closeApp, room_service_request, send_room_service_email, check_room_availability, book_room, \
    recall_memory, remember_this, send_msg_wa


def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 140)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine

load_dotenv()

USER = os.getenv('USER')
HOSTNAME = os.getenv('BOT')


def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = int(datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = cal_day()

    if (hour >= 0) and (hour <= 12) and ('AM' in t):
        speak(f"Good morning {USER}, it's {day} and the time is {t}.")
    elif (hour >= 12) and (hour <= 16) and ('PM' in t):
        speak(f"Good afternoon {USER}, it's {day} and the time is {t}.")
    elif (hour >= 16) and (hour < 23) and ('PM' in t):
        speak(f"Good evening {USER}, it's {day} and the time is {t}.")
    speak(f"I am {HOSTNAME}. How may I assist you,?")


listening = False


def cal_day():
    day = datetime.today().weekday() + 1
    day_dict = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
    return day_of_week


engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 220)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def start_listening():
    global listening
    listening = True
    print("started listening ")


def pause_listening():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 2000
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        if not 'stop' in query or 'exit' in query:
            speak(random.choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir,take care!")
            else:
                speak("Have a good day sir!")
            exit()

    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        query = 'None'
    return query


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine sir. What about you")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "room service" in query:
                room_service_request()

            elif 'check room availability' in query:
                check_room_availability()

            elif 'book room' in query:
                book_room()

            elif ("system condition" in query) or ("condition of the system" in query):
                speak("checking the system condition")
                condition()

            elif "remember that" in query:

                remember_this(query)

            elif "what do you remember" in query:

                recall_memory()

            elif ("volume up" in query) or ("increase volume" in query):
                pyautogui.press("volumeup")
                speak("Volume increased")

            elif ("volume down" in query) or ("decrease volume" in query):
                pyautogui.press("volumedown")
                speak("Volume decrease")

            elif ("volume mute" in query) or ("mute the sound" in query):
                pyautogui.press("volumemute")
                speak("Volume muted")

            elif "open camera" in query:
                speak("Opening camera sir")
                subp.run('start microsoft.windows.camera:', shell=True)

            elif "schedule" in query:
                schedule()

            elif "open notepad" in query:
                speak("Opening Notepad for you sir")
                notepad_path = "C:\\Windows\\System32\\notepad.exe"
                os.startfile(notepad_path)

            elif "open discord " in query:
                speak("Opening Discord for you sir")
                discord_path = "C:\\Users\\Harshit Deva\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc"
                os.startfile(discord_path)

            elif "open valorant" in query:
                speak("Opening valorant for you sir")
                valorant_path = "C:\\Riot Games\\Riot Client"
                os.startfile(valorant_path)

            elif "open spotify" in query:
                speak("Opening Spotify for you sir")
                spotify_uri = "spotify://"
                subprocess.Popen(['start', spotify_uri], shell=True)

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(
                    f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "close notepad" in query:
                closeApp("notepad")
            elif "close discord" in query:
                closeApp("discord")
            elif "close valorant" in query:
                closeApp("valorant")
            elif "close spotify" in query:
                closeApp("spotify")

            elif "wikipedia" in query:
                speak("what do you want to search on wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

            elif 'give me news' in query:
                speak(f"I am reading out the latest headline of today,sir")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(), sep='\n')

            elif 'weather' in query:
                ip_address = find_my_ip()
                speak("tell me the name of your city")
                city = input("Enter name of your city")
                speak(f"Getting weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline', 'plot summary not available')
                    speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                          f"The plot summary of movie is {plot}")

                    print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                          f"The plot summary of movie is {plot}")

            elif "calculate" in query:
                app_id = "2PRJAP-VG875PXLG8"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("I couldn't find that . Please try again")

            elif 'what is' in query or 'who is' in query or 'which is' in query:
                app_id = "K23496-Q98UUKETVG"
                client = wolframalpha.Client(app_id)
                try:

                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                            query.lower().index('which is') if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind + 2:]
                        result = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer is " + ans)
                        print("The answer is " + ans)
                    else:
                        speak("I couldn't find that. Please try again.")
                except StopIteration:
                    speak("I couldn't find that. Please try again.")

            elif "send message on whatsapp" in query:
                send_msg_wa()

