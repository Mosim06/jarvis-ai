import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit
import pyjokes
import os
import pyautogui
import json
import importlib
from openai import OpenAI

# ================== SETUP ==================
client = OpenAI(api_key="YOUR_NEW_API_KEY_HERE")

engine = pyttsx3.init()
recognizer = sr.Recognizer()

PLUGIN_FOLDER = "plugins"

# ================== LOAD PLUGINS ==================
def load_plugins():
    plugins = {}

    if not os.path.exists(PLUGIN_FOLDER):
        os.makedirs(PLUGIN_FOLDER)

    for file in os.listdir(PLUGIN_FOLDER):
        if file.endswith(".py"):
            name = file[:-3]
            try:
                module = importlib.import_module(f"{PLUGIN_FOLDER}.{name}")
                plugins[name] = module
            except Exception as e:
                print(f"Error loading plugin {name}:", e)

    return plugins

# ================== SPEAK ==================
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ================== LISTEN ==================
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return ""

# ================== MEMORY ==================
def remember(key, value):
    try:
        with open("memory.json", "r") as file:
            data = json.load(file)
    except:
        data = {}

    data[key] = value

    with open("memory.json", "w") as file:
        json.dump(data, file)

def recall(key):
    try:
        with open("memory.json", "r") as file:
            data = json.load(file)
            return data.get(key, "I don't remember that.")
    except:
        return "Memory is empty."

# ================== AI ==================
def ask_ai(question):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"You are Jarvis, a smart personal assistant.\nUser: {question}"
        )
        return response.output_text
    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I am having trouble connecting right now."

# ================== SYSTEM CONTROL ==================
def open_notepad():
    os.system("notepad")

def open_browser():
    os.system("start chrome")

def shutdown_pc():
    os.system("shutdown /s /t 5")

def type_text(text):
    pyautogui.write(text)

# ================== WISH ==================
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour < 12:
        speak("Good Morning")
    elif hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("Hello, I am Jarvis. How can I help you?")

# ================== WAKE WORD ==================
def wait_for_wake_word():
    speak("Say Jarvis to wake me up")

    while True:
        text = listen()

        if "jarvis" in text:
            speak("Yes, I am listening")
            break

# ================== MAIN LOGIC ==================
def run_jarvis():

    # 🔥 LOAD PLUGINS (STEP 2)
    plugins = load_plugins()

    while True:

        command = listen()

        if command == "":
            continue

        # 🔥 RUN PLUGINS (STEP 3)
        for name, module in plugins.items():
            try:
                if hasattr(module, "run"):
                    if name.replace("_", " ") in command:
                        module.run()
                        break
            except Exception as e:
                print(f"Plugin error ({name}):", e)

        # ---------- BASIC ----------
        if "time" in command:
            time = datetime.datetime.now().strftime('%H:%M')
            speak("The time is " + time)

        elif "who is" in command:
            person = command.replace("who is", "")
            try:
                info = wikipedia.summary(person, 2)
                speak(info)
            except:
                speak("Sorry, I couldn't find information.")

        elif "joke" in command:
            speak(pyjokes.get_joke())

        # ---------- WEB ----------
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")

        elif "open google" in command:
            webbrowser.open("https://google.com")

        elif "search" in command:
            search = command.replace("search", "")
            pywhatkit.search(search)
            speak("Searching for " + search)

        elif "play" in command:
            song = command.replace("play", "")
            speak("Playing " + song)
            pywhatkit.playonyt(song)

        # ---------- SYSTEM ----------
        elif "open notepad" in command:
            open_notepad()

        elif "open browser" in command:
            open_browser()

        elif "shutdown" in command:
            speak("Shutting down system")
            shutdown_pc()

        elif "type" in command:
            text = command.replace("type", "")
            type_text(text)

        # ---------- MEMORY ----------
        elif "remember" in command:
            speak("What should I remember?")
            key = listen()
            speak("What is the value?")
            value = listen()
            remember(key, value)
            speak("I remembered that")

        elif "recall" in command:
            speak("What should I recall?")
            key = listen()
            speak(recall(key))

        # ---------- EXIT ----------
        elif "stop" in command or "exit" in command:
            speak("Goodbye")
            break

        # ---------- AI ----------
        else:
            answer = ask_ai(command)
            speak(answer)

# ================== START ==================
if __name__ == "__main__":
    wish()
    wait_for_wake_word()
    run_jarvis()
