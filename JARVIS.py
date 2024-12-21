import random 
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
import cv2
import wikipedia
import webbrowser
import pywhatkit as kit
import time
import smtplib
import sys
import pyautogui
import instaloader
import numpy as np
from translate import Translator
import threading
from playsound import playsound
from googletrans import Translator

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the desired voice

# Text-to-speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Voice-to-text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except sr.WaitTimeoutError:
            speak("You didn't say anything. Please try again.")
        except sr.UnknownValueError:
            speak("I couldn't understand. Please say that again.")
        except sr.RequestError:
            speak("Check your internet connection.")
    return "none"

# Wish command
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if hour >= 0 and hour < 12:
        speak(f"Good Morning! It's {tt}")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon! It's {tt}")
    else:
        speak(f"Good Evening! It's {tt}")
    speak("I am JARVIS. How can I help you today?")

# Send email
def sendEmail(to, subject, content):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login('anurag.23bai11240@vitbhopal.ac.in', 'Anurag@vitb')  # Add your credentials
        message = f"Subject: {subject}\n\n{content}"
        server.sendmail("anurag.23bai11240@vitbhopal.ac.in", to, message)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak(f"Failed to send email. {e}")

# Google Search
def google_search(query):
    try:
        speak("Searching Google...")
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        speak("Here are the search results.")
    except Exception as e:
        speak("Could not complete Google search.")

# Weather Forecast
def weather_forecast(city):
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    try:
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
        response = requests.get(complete_url)
        weather_data = response.json()

        if weather_data["cod"] != "404":
            main = weather_data["main"]
            weather_desc = weather_data["weather"][0]["description"]
            temp = main["temp"]
            humidity = main["humidity"]

            speak(f"The current temperature in {city} is {temp}°C with {weather_desc}. Humidity is {humidity}%.")
        else:
            speak("City not found. Please try again.")
    except Exception as e:
        speak("Could not fetch weather details. Check your internet connection.")

def search_website():
    websites = {
    "Google": "https://www.google.com",
    "Youtube": "https://www.youtube.com",
    "Facebook": "https://www.facebook.com",
    "Twitter": "https://www.twitter.com",
    "Instagram": "https://www.instagram.com",
    "Linkedin": "https://www.linkedin.com",
    "Github": "https://www.github.com",
    "Reddit": "https://www.reddit.com",
    "Amazon": "https://www.amazon.com",
    "Netflix": "https://www.netflix.com",
    "Bhopal": "https://vtop.vitbhopal.ac.in/vtop/open/page",
}
    while True:
        site_name = takecommand()
        if site_name == "none":
            continue  # Retry listening
        elif site_name in websites:
            webbrowser.open(websites[site_name])
            speak(f"Opening {site_name}...")
            break
        else:
            speak("Sorry, I couldn't find that website in my list. Please try again.")

def search_live_location():
    while True:
        location = takecommand()
        if location == "none":
            continue  # Retry listening
        else:
            speak(f"Searching for the live location of {location}.")
            webbrowser.open(f"https://www.google.com/maps/search/{location}")
            break

def tell_news():
    try:
        speak("Fetching the latest news...")
        query = "latest news"
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url)
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = soup.find_all("h3", limit=5)  # Adjust number of headlines to fetch
            for i, headline in enumerate(headlines, start=1):
                speak(f"Headline {i}: {headline.get_text()}")
        else:
            speak("Unable to fetch news. Please check your internet connection.")
    except Exception as e:
        speak(f"An error occurred while fetching news: {e}")
import wikipedia
import webbrowser

# Function to search Wikipedia and open the page
def search_wikipedia():
    speak("What should I search on Wikipedia?")
    search_query = takecommand().lower()
    if search_query == "none":
        speak("I couldn't hear anything. Please try again.")
        return

    try:
        # Perform the Wikipedia search
        speak("Searching Wikipedia...")
        summary = wikipedia.summary(search_query, sentences=5)
        speak(f"According to Wikipedia: {summary}")

        # Open the Wikipedia page
        wiki_page_url = wikipedia.page(search_query).url
        webbrowser.open(wiki_page_url)
        speak("I've opened the Wikipedia page in your browser.")
    except wikipedia.DisambiguationError as e:
        speak("There are multiple results for this query. Please be more specific.")
    except wikipedia.PageError:
        speak("I couldn't find a Wikipedia page for this query. Please try again.")
    except Exception as e:
        speak("Sorry, I couldn't complete the Wikipedia search. Please check your internet connection.")
 
def translate_to_indian_language():
    translator = Translator()
    speak("Please tell me the text you want to translate.")
    text_to_translate = takecommand().lower()
    if text_to_translate == "none":
        speak("I couldn't hear anything. Please try again.")
        return

    speak("Into which Indian language should I translate it?")
    target_language = takecommand().lower()

    # Mapping of Indian languages to their codes
    indian_language_codes = {
        "hindi": "hi",
        "bengali": "bn",
        "tamil": "ta",
        "telugu": "te",
        "kannada": "kn",
        "malayalam": "ml",
        "marathi": "mr",
        "gujarati": "gu",
        "punjabi": "pa",
        "urdu": "ur",
        "assamese": "as",
        "odia": "or"
    }

    if target_language in indian_language_codes:
        try:
            translation = translator.translate(text_to_translate, dest=indian_language_codes[target_language])
            translated_text = translation.text
            speak(f"The translation in {target_language} is: {translated_text}")
        except Exception as e:
            speak("Sorry, I couldn't translate the text. Please check your internet connection.")
    else:
        speak("I currently support only Indian languages. Please try again.")
import cv2

# Function to open the camera and capture a photo with spacebar
def open_camera_and_capture_photo():
    try:
        cap = cv2.VideoCapture(0)  # Open the default camera
        speak("Opening the camera. Press the spacebar to capture the photo or 'Q' to quit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                speak("Failed to access the camera.")
                break

            cv2.imshow("Camera", frame)
            
            # Wait for user input: spacebar to capture, 'Q' to quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Spacebar to capture
                photo_filename = "captured_photo.jpg"
                cv2.imwrite(photo_filename, frame)
                speak(f"Photo captured and saved as {photo_filename}.")
                break
            elif key == ord('q'):  # 'Q' to quit
                speak("Exiting the camera.")
                break

        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        speak(f"An error occurred while accessing the camera. {e}")

    except Exception as e:
        speak(f"An error occurred while capturing the photo. {e}")
def play_alarm_ringtone():
    ringtone_path = "alarm ringtone.mp3"  # Path to your ringtone file
    try:
        speak("Time to wake up! Your alarm is ringing.")
        playsound(ringtone_path)  # Play the ringtone
    except Exception as e:
        speak(f"Could not play the alarm sound. {e}")


# Function to set an alarm
def set_alarm(alarm_time):
    speak(f"Alarm set for {alarm_time}.")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            play_alarm_ringtone()
            break
        time.sleep(1)
def stop_alarm():
    global alarm_running
    if alarm_running:
        alarm_running = False
        speak("The alarm has been stopped.")
    else:
        speak("No alarm is currently running.")
# Main Program
if __name__ == "__main__":
    query = takecommand().lower()
    if "wake up jarvis" in query:
        wish()
    
    while True:
        query = takecommand().lower()

        # Open Notepad
        if "open notepad" in query:
            os.startfile("C:\\Windows\\System32\\notepad.exe")

        # Open Command Prompt
        elif "open command prompt" in query:
            os.system("start cmd")

        elif "search live location" in query:
             search_live_location()
        elif "tell news" in query or "news" in query:
            tell_news()
        elif "translate" in query:
            translate_to_indian_language()


        elif "set alarm" in query:
            speak("Please tell me the time to set the alarm in HH:MM format.")
            alarm_time = takecommand().lower()
            try:
                datetime.datetime.strptime(alarm_time, "%H:%M")  # Validate the time format
                alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time,))
                alarm_thread.start()  # Run alarm in a separate thread
            except ValueError:
                speak("The time format is invalid. Please try again.")
        elif "stop alarm" in query:
            stop_alarm()

        # Wikipedia search for specific topics
        elif "wikipedia" in query:
            search_wikipedia()



        elif "search websites" in query:
            search_website()


        elif "send message" in query:
            try:
                phone_number = "+917477058602"  # Replace with the recipient's phone number
                message = "This is a testing protocol"
                kit.sendwhatmsg_instantly(phone_number, message)  # Send message instantly
                speak("Message has been sent successfully!")
            
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this message.")

        # Open Camera
        elif "open camera" in query or "click a photo" in query:
              open_camera_and_capture_photo()

        elif 'volume up' in query:
            pyautogui.press("volumeup")

        elif 'volume down' in query:
            pyautogui.press("volumedown")

        elif 'volume mute' in query or 'mute' in query:
            pyautogui.press("volumemute")

        elif "open mobile camera" in query:
            import urllib.request
            import cv2 #pip install opencv-python import numpy as np #pip install numpy import time
            URL = "http://192.168.43.170:8080/shot.jpg"
            while True:
                img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
                img = cv2. imdecode(img_arr, -1)
                cv2. imshow( 'IPWebcam', img)
                q = cv2.waitKey (1)
                if q == ord("q"):
                    break
            
            cv2.destroyAllWindows ()

        # Open YouTube
        elif "open youtube" in query:
            webbrowser.open("youtube.com")

         # Play music
        elif "play music" in query:
                music_dir=r"C:\Users\dubey\Downloads\music"
                songs=os.listdir(music_dir)
                rd=random.choice(songs)
                file_path = os.path.join(music_dir, rd)
                os.startfile(file_path)

        # Open Google
        elif "open google" in query:
            speak("What should I search?")
            search_query = takecommand().lower()
            google_search(search_query)

        # Send Email
        elif "send email" in query:
            try:
                speak("What should be the subject?")
                subject = takecommand().lower()
                speak("What is the content of the email?")
                content = takecommand().lower()
                sendEmail("recipient-anurag.23bai11240@vitbhopal.ac.in", subject, content)
            except Exception as e:
                speak(f"Unable to send email. {e}")

        # Weather Forecast
        elif "weather" in query:
            speak("Please tell me the city name.")
            city = takecommand().lower()
            weather_forecast(city)

        # Take Screenshot
        elif "take screenshot" in query:
            speak("What should I name the screenshot file?")
            name = takecommand().lower()
            time.sleep(2)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot saved successfully.")

        # Exit Program
        elif "no thanks" in query or "exit" in query:
            speak("Thanks for using me. Have a great day!")
            sys.exit()

        elif "close application" in query:
            speak("Closing application.")
            sys.exit()

        else:
            speak("Do you need any other help?") 