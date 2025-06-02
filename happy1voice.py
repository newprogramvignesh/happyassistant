import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import datetime
import time
import psutil  # For battery status
import pyautogui  # For screenshots
import random

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # 1 for female, 0 for male voice

paused = False  # Pause flag


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def take_command():
    """Listen and recognize voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything, please try again.")
        except sr.UnknownValueError:
            speak("I didn't understand that, please repeat.")
        except sr.RequestError:
            speak("Sorry, speech recognition is unavailable right now.")
        return "none"


def open_application(path, app_name):
    """Open local applications if available."""
    if os.path.exists(path):
        speak(f"Opening {app_name}")
        os.startfile(path)
    else:
        speak(f"{app_name} is not installed or the path is incorrect.")


def get_time():
    """Get current time."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")


def get_date():
    """Get current date."""
    today_date = datetime.datetime.today().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {today_date}")


def get_battery_status():
    """Get battery percentage."""
    battery = psutil.sensors_battery()
    if battery:
        percentage = battery.percent
        speak(f"The battery is currently at {percentage} percent.")
    else:
        speak("Unable to retrieve battery status.")


def take_screenshot():
    """Capture a screenshot and save it."""
    filename = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot().save(filename)
    speak("Screenshot taken and saved.")


def search_google(query):
    """Search Google."""
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching Google for {query}.")


def search_youtube(query):
    """Search YouTube."""
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    speak(f"Searching YouTube for {query}.")


def tell_joke():
    """Fetch a random joke."""
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "I told my computer I needed a break, and now it won’t stop sending me error messages!",
        "Why do Java developers wear glasses? Because they don’t see sharp!"
    ]
    joke = random.choice(jokes)
    speak(joke)

if __name__ == "__main__":
    speak("Happy Assistance activated.")
    speak("How can I help you?")

    while True:
        query = take_command()

        if query == "none":
            continue  # Ignore unrecognized speech

        if "stop" in query:
            paused = True
            speak("Pausing assistance. Say 'start' to resume.")
            time.sleep(10) 
            continue
            

        if paused:
            if "start" in query:
                paused = False
                speak("Resuming assistance. How can I help you?")
            continue  # Skip processing while paused

        elif "who are you" in query:
            speak("I am Happy, developed by VIGANESH KANNA.")        #Origin details

        elif "open" in query:
            websites = {
                "youtube": "https://www.youtube.com",
                "google": "https://www.google.com",
                "github": "https://www.github.com",
                "spotify": "https://www.spotify.com"
            }
            for site in websites:
                if site in query:
                    speak(f"Opening {site}")
                    webbrowser.open(websites[site])

        elif "play music" in query:
            speak("Opening Spotify for music.")
            webbrowser.open("https://www.spotify.com")

        elif "open whatsapp" in query:
            open_application("C:\\Users\\jaspr\\AppData\\Local\\WhatsApp\\WhatsApp.exe", "WhatsApp")

        elif "open local disk" in query:
            disks = {"c": "C://", "d": "D://", "e": "E://"}
            for disk in disks:
                if disk in query:
                    speak(f"Opening local disk {disk.upper()}")
                    webbrowser.open(disks[disk])

        elif "tell me the time" in query:
            get_time()

        elif "tell me the date" in query:
            get_date()

        elif "check battery status" in query:
            get_battery_status()

        elif "take a screenshot" in query:
            take_screenshot()

        elif "search google for" in query:
            search_google(query.replace("search google for", "").strip())

        elif "search youtube for" in query:
            search_youtube(query.replace("search youtube for", "").strip())

        elif "tell me a joke" in query:
            tell_joke()

        elif "exit" in query or "sleep" in query:
            speak("Goodbye!")
            break

        speak("I'm ready for your next command.") 

