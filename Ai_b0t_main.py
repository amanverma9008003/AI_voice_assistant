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

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

# GPT setup
openai.api_key = "YOUR_OPENAI_API_KEY"

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
    if "chrome" in app_name:
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif "notepad" in app_name:
        os.system("notepad")
    else:
        speak("App not configured.")

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
        song = listen()
        pywhatkit.playonyt(song)
    elif "joke" in command:
        speak(pyjokes.get_joke())
    elif "weather" in command:
        speak("Which city?")
        city = listen()
        speak(get_weather(city))
    elif "open" in command:
        open_app(command)
    elif "wikipedia" in command:
        query = command.replace("wikipedia", "")
        speak(search_wiki(query))
    elif "timer" in command:
        speak("For how many seconds?")
        try:
            seconds = int(listen())
            set_timer(seconds)
        except:
            speak("I didn't get the time.")
    elif "exit" in command or "bye" in command:
        speak("Goodbye! Call me anytime.")
        exit()
    else:
        response = ask_gpt(command)
        speak(response)

def main():
    speak("Hello! I am your AI voice assistant.")
    while True:
        command = listen()
        if command:
            handle_command(command)

if __name__ == "__main__":
    main()

# Note : Replace

'''            🧠 Key Functionalities
Your AI voice assistant, can perform various tasks using voice commands. Here are some of the key functionalities 
    Feature	                        Command Example

🕐 Time	                          “What's the time?”
🤖 GPT-powered reply	          “How are you feeling today?”
🌦️ Weather	                       “What's the weather in Delhi?”
🎵 Play music on YouTube	      “Play Believer on YouTube”
🤣 Joke	                          “Tell me a joke”
📚 Wikipedia summary	          “Tell me about Python from Wikipedia”
⏰ Set a timer	                 “Set timer for 10 seconds”
🖥️ Open apps	                   “Open Chrome” or “Open Notepad”
📴 Exit	                          “Exit” or “Bye”'''