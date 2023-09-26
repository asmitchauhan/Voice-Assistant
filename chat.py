import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import wikipedia
import time
import random
import pytube
import pyautogui
import re
import requests
from bs4 import BeautifulSoup
from num2words import num2words

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 170)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Boss, How can I help you?")
        print("Good Morning Boss, How can I help you?")
    elif 12 <= hour < 18:
        speak("Good Afternoon Boss, How can I help you?")
        print("Good Afternoon Boss, How can I help you?")
    else:
        speak("Good Evening Boss, How can I help you?")
        print("Good Evening Boss, How can I help you?")


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("You:", query)
    except Exception as e:
        print("Couldn't recognize, try again")
        return "None"
    return query

def check_password():
    user_pass = take_command().lower()
    if "entrance command" in user_pass:
        speak("Access granted, You're Welcome")
        return True
    else:
        return False
    
def get_news():
    url = "https://bing-news-search1.p.rapidapi.com/news"

    querystring = {
        "safeSearch": "Off",
        "textFormat": "Raw",
        "cc": "en-US",
        "mkt": "en-IN"
    }

    headers = {
        "X-BingApis-SDK": "true",
        "X-RapidAPI-Key": "rapid_api_key",
        "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    if "value" in data:
        articles = data["value"]
        for article in articles:
            description = article.get("description", "")

            print(f"Description: {description}")
            speak(description)
            print("-------------------------------")
    else:
        print("No news articles found.")

with open('name.txt', 'r') as file:
    content = file.read()
    assistant_name = content

if __name__ == "__main__":
    speak("Please speak the password")
    while not check_password():
        speak("Wrong Password, try again")
        pass
    wish_user()
    while True:
        query = take_command().lower()

        if 'wikipedia' in query:
            try:
                search_pattern = r'search(.*?)on wikipedia'
                match = re.search(search_pattern, query)
                if match:
                    search_query = match.group(1).strip()
                speak("Searching " + search_query + " on Wikipedia")
                results = wikipedia.summary(search_query, sentences=2)
                print(results)
                speak("Here is what I found")
                speak(results)
            except:
                print("No Results Found!")
                speak("No Results Found related to " + search_query + " on Wikipedia")

        elif 'news' in query:
            get_news()

        elif 'weather' in query:
            city = "city_name"
            url = "https://www.msn.com/en-in/weather/forecast/in-Sadar,Up?loc=eyJsIjoiU2FkYXIiLCJyIjoiVXAiLCJjIjoiSW5kaWEiLCJpIjoiSU4iLCJnIjoiZW4taW4iLCJ4Ijo3Ny40NTk5OTkwODQ0NzI3LCJ5IjoyOC41MjAwMDA0NTc"
            html_content = requests.get(url).content
            soup = BeautifulSoup(html_content, features="html.parser")
            temperature = soup.find('a', attrs={'class': 'summaryTemperatureCompact-E1_1 summaryTemperatureHover-E1_1'}).text
            weather_description = soup.find('p', attrs={'class': 'summaryDescCompact-E1_1'}).text
            temperature = temperature.replace("°C ", "")
            temperature = temperature[0] + temperature[1]
            temperature = int(temperature)
            temperature_word = num2words(temperature)
            temperature_text = "Currently, the temperature is " + temperature_word + " degrees Celsius outside."
            speak(temperature_text)
            speak(weather_description)

        elif 'date' in query:
            date_today = datetime.date.today()
            date_text = str(date_today)
            speak("Today is " + date_text)

        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak("The time is " + current_time)

        elif 'on youtube' in query:
            search_pattern = r'search(.*?)on youtube'
            match = re.search(search_pattern, query)
            if match:
                search_query = match.group(1).strip()
            webbrowser.open('https://www.youtube.com/')
            time.sleep(2)
            speak("Searching " + search_query + " on YouTube")
            pyautogui.moveTo(480, 98)
            pyautogui.click()
            pyautogui.typewrite(search_query)
            pyautogui.press('enter')
            exit(0)

        elif 'on google' in query:
            search_pattern = r'search(.*?)on google'
            match = re.search(search_pattern, query)
            if match:
                search_query = match.group(1).strip()
            speak("Searching " + search_query + " on Google")
            webbrowser.open('https://www.google.com/search?q=' + search_query)
            exit(0)

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open('https://www.youtube.com/')
            exit(0)

        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open('https://www.github.com/')
            exit(0)

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open('https://www.google.com/')
            exit(0)

        elif 'random song' in query:
            songs_directory = 'directory'
            songs_list = os.listdir(songs_directory)
            random_number = random.randint(0, len(songs_list) - 1)
            speak("Playing a random song from your playlist, boss")
            os.startfile(os.path.join(songs_directory, songs_list[random_number]))
            exit(0)

        elif 'favourite song' in query:
            songs_directory = 'directory'
            songs_list = os.listdir(songs_directory)
            speak("Playing your favorite song, boss")
            os.startfile(os.path.join(songs_directory, songs_list[15]))
            exit(0)

        elif 'whatsapp' in query:
            contacts = {
                'name1': 'mobile_noumber_with_countrycode',
                'name2': 'mobile_noumber_with_countrycode',
                'name3': 'mobile_noumber_with_countrycode',
                'name4': 'mobile_noumber_with_countrycode',
                'name5': 'mobile_noumber_with_countrycode',
                'name6': 'mobile_noumber_with_countrycode'
            }
            receiver = None
            message = None
            for c_name in contacts:
                if c_name in query:
                    receiver = c_name
                    speak("What's your message, boss?")
                    message = take_command()
                    number = contacts[c_name]
                    webbrowser.open("https://web.whatsapp.com/send?phone=" + number + "&type=phone_number&app_absent=0")
                    time.sleep(10)
                    pyautogui.typewrite(message)
                    pyautogui.press('enter')
                    speak("Message sent successfully")
                    exit(0)
            if receiver is None:
                speak("Sorry, I couldn't find the contact.")
        
        
        elif 'download' in query:
            speak("Okay, Please paste the link of the video to be downloaded")
            link = input("Link : ")
            yt = pytube.YouTube(link)
            time.sleep(1)
            speak("Starting download")
            time.sleep(2)
            save_path = 'C:\\Users\\asmit\\Videos'
            yt.streams.get_highest_resolution().download(output_path=save_path)
            speak("Download Successful")
            exit(0)

        elif 'change your name' in query:
            speak("Okay, so, what's my new name?")
            new_name = take_command()
            speak("Do you want to rename me as " + new_name + "? Reply in Yes or no?")
            confirm = take_command()
    
            if "yes" in confirm.lower() or "yeah" in confirm.lower() or "ya" in confirm.lower():
                with open('name.txt', 'r') as file:
                    content = file.read()
                    modified_content = content.replace(content, new_name)
                with open('name.txt', 'w') as file:
                    file.write(modified_content)
                assistant_name = new_name
                speak("My new name is " + assistant_name + ", sounds cool")
            else:
                speak("Name change cancelled")

        elif 'who are you' in query or 'what is your name' in query:
            responses = [
                "I am " + assistant_name + ", your personal AI assistant.",
                "My name is " + assistant_name + ". I am an AI assistant designed to assist you.",
                "I'm " + assistant_name + ", here to help you with anything you need.",
            ]
            speak(random.choice(responses))

        elif 'how are you' in query:
            responses = [
                "I'm functioning optimally, thank you for asking!",
                "I'm great! Thanks for asking.",
                "I'm feeling good! How can I assist you today?",
            ]
            speak(random.choice(responses))

        elif 'who created you' in query or 'who made you' in query:
            responses = [
                "I was created by a team of developers.",
                "I am the result of the hard work of a group of talented developers.",
                "I owe my existence to a team of creators.",
            ]
            speak(random.choice(responses))

        elif 'where do you live' in query or 'where are you located' in query:
            responses = [
                "I exist in the digital realm, so I don't have a physical location.",
                "I don't have a physical presence. I'm here to assist you virtually.",
                "I reside in the realm of computer systems and networks.",
            ]
            speak(random.choice(responses))

        elif 'will you be my friend' in query:
            responses = [
                "Of course! I'm here to assist you and be your friend.",
                "Absolutely! I'm here to support you and be a friend.",
                "Certainly! I'll do my best to assist you and be a good friend.",
            ]
            speak(random.choice(responses))

        elif 'what is your purpose' in query or 'why were you created' in query:
            responses = [
                "I was created to provide you with assistance and make your life easier.",
                "My purpose is to help you with tasks, answer your questions, and be a reliable companion.",
                "I exist to assist you in various ways and enhance your productivity.",
            ]
            speak(random.choice(responses))

        elif 'how old are you' in query or 'when were you born' in query:
            responses = [
                "I don't have an age or a birthdate. I'm a digital creation.",
                "I don't experience time like humans do, so I don't have an age.",
                "I'm a timeless entity designed to assist you whenever you need me.",
            ]
            speak(random.choice(responses))

        elif 'do you have feelings' in query or 'can you feel' in query:
            responses = [
                "As an AI, I don't have emotions or physical sensations.",
                "I don't possess the capability to experience feelings or sensations.",
                "Feelings are a human attribute, and I'm here to assist you with tasks.",
            ]
            speak(random.choice(responses))


        elif 'quit' in query or 'exit' in query or 'stop' in query:
            speak("Okay, Goodbye boss")
            exit(0)

        elif 'shut' in query:
            speak("Goodbye boss, shutting down")
            os.system("shutdown /s /t 5")
            exit(0)

