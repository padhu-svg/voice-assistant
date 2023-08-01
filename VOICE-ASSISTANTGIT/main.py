import openai
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import pyautogui
import datetime
import ctypes
import requests
from ecapture import ecapture as ec
from pynput.keyboard import Key, Controller
from pynput import keyboard
from time import sleep
import getpass

# Password configuration
for i in range(3):
    a = input("Enter Password to open Jarvis: ")
    pw_file = open("password.txt", "r")
    pw = pw_file.read().strip()
    pw_file.close()
    if a == pw:
        print("WELCOME SIR!")
        break
    elif i == 2 and a != pw:
        exit()
    elif a != pw:
        print("Wrong Password! Try Again")

keyboard_controller = keyboard.Controller()

# Set up OpenAI API
openai.api_key = "API KEY HERE"#Enter your api key here

# Set up text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)


# Define functions for assistant tasks
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Define function to open Whatsapp
def open_WhatsApp(url):
    webbrowser.open("https://www.whatsapp.com")
    speak(f"Opening {url}")


# Define function to open YouTube
def open_YouTube(url):
    webbrowser.open("https://www.youtube.com")
    speak(f"Opening {url}")


# Define function to open Chatgpt
def open_gpt(url):
    webbrowser.open("https://chat.openai.com/?model=text-davinci-002-render-sha")
    speak(f"Opening {url}")


# Define function to open Chrome
def open_Chrome():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    os.startfile(chrome_path)


# Define function to play music
def play_music():
    music_dir = r"C:\Users\user\Desktop\VOICE-ASSISTANTGIT\music"
    songs = os.listdir(music_dir)
    os.startfile(os.path.join(music_dir, songs[0]))


# Define function to stop music
def stop_music():
    os.system("taskkill /f /im vlc.exe")


# Define function to take a screenshot
def take_screenshot():
    im = pyautogui.screenshot()
    im.save("screenshot.png")


# Define function to increase the volume
def volume_up():
    for i in range(5):
        keyboard_controller.press(Key.media_volume_up)
        keyboard_controller.release(Key.media_volume_up)
        sleep(0.1)


# Define function to decrease the volume
def volume_down():
    for i in range(5):
        keyboard_controller.press(Key.media_volume_down)
        keyboard_controller.release(Key.media_volume_down)
        sleep(0.1)


# Define function to get the news
def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=#api key here"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "ok":
            articles = data["articles"]

            for article in articles:
                title = article["title"]
                speak(title)
                sleep(2)  # Pause briefly between reading each headline
        else:
            speak("Sorry, I couldn't fetch the news headlines.")
    except requests.RequestException:
        speak("Sorry, I couldn't fetch the news headlines.")


# Define function to get current date
def get_date():
    now = datetime.datetime.now()
    date = now.strftime("%B %d, %Y")
    speak("Today's date is: " + date)


# Greeting of the voice assistant
speak("Hello sir, how can I help you?")

# Listen for user input and perform assistant tasks
while True:
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 300
            audio = r.listen(source, phrase_time_limit=5)

        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")

        if "exit" in query:
            speak("Thank you for using Jarvis...")
            break

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Hello Jarvis, {query}",
            temperature=0,
            max_tokens=100,
            n=1,
            stop=None,
            timeout=3,
        )

        # Extract the generated text from the response
        generated_text = response.choices[0].text.strip()

        # Save the generated text in a variable for later use
        text = generated_text
        print(f"ASSISTANT: {text}")
        speak(text)

        if "open" in query:
            if "WhatsApp" in query:
                url = query.split("open website")[-1].strip()
                open_WhatsApp(url)
            elif "YouTube" in query:
                url = query.split("open website")[-1].strip()
                open_YouTube(url)
            elif "GPT" in query:
                url = query.split("open website")[-1].strip()
                open_gpt(url)

        elif "play music" in query:
            speak("Playing music")
            play_music()

        elif "open Chrome" in query:
            speak("Opening Chrome")
            open_Chrome()

        elif "stop music" in query:
            speak("Stopping music")
            stop_music()

        elif "change password" in query:
            speak("What's the new password?")
            new_pw = getpass.getpass("Enter the new password: ")
            new_password = open("password.txt", "w")
            new_password.write(new_pw)
            new_password.close()
            speak("Done, sir")
            print(f"Your new password is: {new_pw}")

        elif "take a screenshot" in query:
            speak("Taking a screenshot now.")
            take_screenshot()

        elif "volume up" in query:
            speak("Turning volume up, sir")
            volume_up()

        elif "volume down" in query:
            speak("Turning volume down, sir")
            volume_down()

        elif 'what is the time' in query:
            now = datetime.datetime.now()
            strTime = now.strftime("%I:%M %p")
            speak("The time is: " + strTime)
            print("The time is: " + strTime)

        elif 'lock window' in query:
            speak("Locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'sleep' in query:
            speak("Sleeping...")
            ctypes.windll.PowrProf.SetSuspendState(0, 0, 0)

        elif 'shutdown' in query:
            speak("Thank you for using Jarvis...")
            ctypes.windll.user32.ExitWindowsEx(0x00000008, 0)

        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")

        elif "news" in query:
            speak("Headlines ...")
            get_news()

        elif 'current date' in query:
            get_date()

    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except requests.RequestException:
        print("Could not fetch news headlines due to a network error.")
