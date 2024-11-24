import os
import psutil
import pyttsx3
import requests
import scope
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
import config
import subprocess
import wolframalpha
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import datetime
from datetime import datetime
import smtplib
from email.message import EmailMessage


EMAIL = ""
PASSWORD = ""

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 140)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine


import speech_recognition as sr


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        return "None"

    return query.lower()

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def cal_day():

    return datetime.now().strftime("%A")

def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def search_on_google(query):
    kit.search(query)

def schedule():
    day = cal_day().lower()
    speak("Boss, today's schedule is:")

    week = {
        "monday": (
            "From 9:30 to 10:30, you have 'Introduction to Python Lab'. "
            "From 10:30 to 11:30, another 'Introduction to Python Lab' class. "
            "From 11:30 to 12:30, it's 'Introduction to Python Theory 'class . "
            "You have lunch from 12:30 to 1:30. "
            "After lunch, from 1:30 to 2:30, you have 'Free Hour'. "
            "From 2:30 to 3:30, you have Computer Network class."
        ),
        "tuesday": (
            "From 9:30 to 10:30, you have 'Introduction to Python'. "
            "From 10:30 to 11:30, you have 'Holistic Education and Development'. "
            "From 11:30 to 12:30, it's 'French'. "
            "You have lunch from 12:30 to 1:30. "
            "After lunch, from 1:30 to 2:30, you have 'Financial Accounting'. "
            "From 2:30 to 3:30, you have 'Mobile Applications'."
        ),
        "wednesday": (
            "From 9:30 to 10:30, you have 'Computer Networks'. "
            "From 10:30 to 11:30, it's 'French'. "
            "From 11:30 to 12:30, you have 'Financial Accounting'. "
            "You have lunch from 12:30 to 1:30. "
            "From 1:30 to 2:30, you have 'Mobile Applications'. "
            "From 2:30 to 3:30, you have 'Computer Networks'."
        ),
        "thursday": (
            "From 9:30 to 10:30, you have 'Computer Networks'. "
            "From 10:30 to 11:30, 'Operating System'. "
            "From 11:30 to 12:30, 'Financial Accounting'. "
            "You have lunch from 12:30 to 1:30. "
            "From 1:30 to 2:30, 'Operating System'. "
            "From 2:30 to 3:30, you have free time."
        ),
        "friday": (
            "From 9:30 to 10:30, you have 'Operating System'. "
            "From 10:30 to 11:30, 'Mobile Applications'. "
            "From 11:30 to 12:30, 'Financial Accounting'. "
            "You have lunch from 12:30 to 1:30. "
            "From 1:30 to 2:30, you have 'Mobile Applications'. "
            "From 2:30 to 3:30, you have free time."
        ),
        "saturday": (
            "From 9:00 to 10:00, you have 'Mobile Applications'. "
            "From 10:00 to 11:00, another 'Mobile Applications' class. "
            "From 11:00 to 1:00, you have free time."
        ),
        "sunday": "Boss, today is a holiday. Enjoy your break!"
    }

    if day in week:
        speak(week[day])
    else:
        speak("I'm sorry, I couldn't find the schedule for today.")  # Handle unexpected days



def youtube(video):
    kit.playonyt(video)


def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False


def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey"
                          f"=3776f83839a24f96953e78a24e5aff2e").json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]


def weather_forecast(city):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=b1459704e802304d352432c6f7a3e813").json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temp}°C", f"{feels_like}°C"

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=60:
        speak("Boss we have enough charging to continue our python evaluation")
    elif percentage>=40:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging otherwise recording should be off...")

def closeApp(command):
    if "notepad" in command:
        speak("Closing Notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "discord" in command:
        speak("Closing Discord")
        os.system('taskkill /f /im Discord.exe')
    elif "valorant" in command:
        speak("Closing Valorant")
        os.system('taskkill /f /im RiotClientServices.exe')
    elif "spotify" in command:
        speak("Closing Spotify")
        os.system('taskkill /f /im Spotify.exe')

        import smtplib
        from email.message import EmailMessage

def room_service_request():
            speak("Please tell me what you'd like to order for room service.")


            order = take_command()

            speak(f"You've ordered: {order}. Confirming your order now.")


            with open("room_service_log.txt", "a") as log_file:
                log_file.write(f"Room Service Order: {order} - {datetime.now()}\n")


            send_room_service_email(order)

def send_room_service_email(order):
            try:
                EMAIL = ""  # Your hotel email
                PASSWORD = ""
                STAFF_EMAIL = ""  # Kitchen or staff emai

                msg = EmailMessage()
                msg.set_content(f"New Room Service Order: {order}\nPlease prepare it as soon as possible.")

                msg['Subject'] = 'New Room Service Order'
                msg['From'] = EMAIL
                msg['To'] = STAFF_EMAIL

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(EMAIL, PASSWORD)
                    server.send_message(msg)

                speak("Your order has been placed successfully and the staff has been notified.")
            except Exception as e:
                speak("Sorry, there was an issue placing your order. Please try again later.")
                print(f"Error sending email: {e}")



rooms = {
    '101': 'available',
    '102': 'booked',
    '103': 'available',
    '104': 'booked',
    '105': 'available'
}


def check_room_availability():
    """Check if a room is available."""
    speak("Please provide the room number you want to check.")
    room_number = take_command()

    if room_number in rooms:
        if rooms[room_number] == 'available':
            speak(f"Room {room_number} is available for booking.")
        else:
            speak(f"Room {room_number} is already booked.")
    else:
        speak(f"Room {room_number} does not exist. Please check the number and try again.")


def book_room():
    """Book an available room."""
    speak("Which room would you like to book?")
    room_number = take_command()

    if room_number in rooms:
        if rooms[room_number] == 'available':
            rooms[room_number] = 'booked'
            speak(f"Room {room_number} has been successfully booked for you.")
        else:
            speak(f"Sorry, Room {room_number} is already booked.")
    else:
        speak(f"Room {room_number} does not exist.")


import os


def remember_this(query):
    """Remembers the given message."""
    rememberMessage = query.replace("remember that", "").replace("jarvis", "")
    speak(f"You told me to remember that {rememberMessage}")

    with open("Remember.txt", "a") as remember:
        remember.write(rememberMessage + "\n")


def recall_memory():
    """Recalls the remembered messages."""
    if os.path.exists("Remember.txt"):
        with open("Remember.txt", "r") as remember:
            memories = remember.read()
            if memories.strip():  # Check if the file is not empty
                speak("You told me to remember the following: " + memories)
            else:
                speak("You haven't told me to remember anything yet.")
    else:
        speak("You haven't told me to remember anything yet.")


def send_msg_wa():
    speak("Who do you want to send the message to, sir?")


    recipient = take_command().lower()
    print(f"Recognized recipient: {recipient}")


    if "Name" in recipient:
        speak("What is the message, sir?")


        message = take_command().lower()
        print(f"Recognized message: {message}")


        now = datetime.now()
        hour = now.hour
        minute = now.minute + 1

        # Send the message using the contact's phone numbe
        kit.sendwhatmsg("Receivers number", message, hour, minute)  # Replace with the correct phone number in Receivers number

        speak("Message sent successfully.")
    else:
        speak("Sorry, I don't have that contact saved.")


def process_wolfram_query(query):
    app_id = "K23496-Q98UUKETVG"
    client = wolframalpha.Client(app_id)

    try:
        # Clean and extract the main query text
        if 'what is' in query.lower():
            main_query = query.lower().split('what is', 1)[1].strip()
        elif 'who is' in query.lower():
            main_query = query.lower().split('who is', 1)[1].strip()
        elif 'which is' in query.lower():
            main_query = query.lower().split('which is', 1)[1].strip()
        else:
            speak("Sorry, I didn't understand the question.")
            return


        result = client.query(main_query)


        try:
            ans = next(result.results).text
            speak(f"The answer is {ans}")
            print(f"The answer is: {ans}")
        except StopIteration:
            speak("I couldn't find the answer to that. Please try again.")

    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")



