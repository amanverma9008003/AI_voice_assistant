import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pyjokes
import os
import requests
import wikipedia
import pywhatkit
import openai
import time
import threading
import tkinter as tk
from tkinter import scrolledtext

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# GPT setup
openai.api_key = "YOUR_OPENAI_API_KEY"

wake_word = "jarvis"

# GUI Setup
class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS Assistant")
        self.root.geometry("500x400")
        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12))
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_window.config(state='disabled')
        self.insert_text("JARVIS: Hello! I am your AI voice assistant. Say 'Hey Jarvis' to start.\n")

    def insert_text(self, text):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, text + "\n")
        self.chat_window.see(tk.END)
        self.chat_window.config(state='disabled')

def speak(text):
    print(f"JARVIS: {text}")
    gui.insert_text(f"JARVIS: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking: {e}")


def listen_background():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
    stop_listening = recognizer.listen_in_background(mic, lambda r, a: callback(r, a, recognizer))
    return stop_listening


def callback(recognizer, audio, r):
    try:
        command = recognizer.recognize_google(audio).lower()
        if wake_word in command:
            speak("Yes? I'm listening.")
            gui.insert_text(f"You: {command}")
            handle_command(command.replace(wake_word, "").strip())
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        speak("Network error.")


def ask_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a funny AI assistant with a sarcastic tone."},
                {"role": "user", "content": question}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "Sorry, I couldn't think of a good response."


def get_weather(city):
    api_key = "YOUR_OPENWEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        data = requests.get(url).json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"It's {temp}°C in {city} with {desc}."
    except:
        return "I couldn't fetch the weather."


def open_app(app_name):
    try:
        if "chrome" in app_name:
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        elif "notepad" in app_name:
            os.system("notepad")
        else:
            speak("App not configured.")
    except Exception as e:
        speak("Couldn't open the application.")


def search_wiki(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except:
        return "I couldn't find that on Wikipedia."


def set_timer(seconds):
    speak(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    speak("Time's up!")


def handle_command(command):
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif "youtube" in command:
        speak("What should I play?")
        song = listen_single()
        pywhatkit.playonyt(song)
    elif "joke" in command:
        speak(pyjokes.get_joke())
    elif "weather" in command:
        speak("Which city?")
        city = listen_single()
        speak(get_weather(city))
    elif "open" in command:
        open_app(command)
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "")
        speak(search_wiki(query))
    elif "timer" in command:
        speak("For how many seconds?")
        try:
            seconds = int(listen_single())
            set_timer(seconds)
        except:
            speak("I didn't get the time.")
    elif "exit" in command or "bye" in command:
        speak("Goodbye! Call me anytime.")
        root.quit()
    else:
        response = ask_gpt(command)
        speak(response)


def listen_single():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except:
        return ""


def main():
    listen_background()
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    gui = AssistantGUI(root)
    main()
