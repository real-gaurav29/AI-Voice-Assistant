import speech_recognition as sr    #pip install speechrecognition
import webbrowser    #provides a simple, high-level interface to display web-based documents to users
import pyttsx3    #text to speech package
from musicLibrar import music
import requests
from google import genai
import os


recognizer = sr.Recognizer()    #sr.Recognizer() - recognize speech and store in recognizer
#initialize pyttsx(text to speech)
# newsapi = "ENTER_YOUR_API_KEY_HERE"
NEWS_API_KEY = "ENTER_YOUR_NEWS_API_KEY_HERE" 
GEMINI_API_KEY = "ENTER_YOUR_GEMINI_API_KEY_HERE"

def speak(text):   #function which takes a text and speak
    engine = pyttsx3.init()    
    engine.say(text) #say that (text)
    engine.runAndWait() #run and wait don't quit

def ai_command(text):
    try:
        # 1. Ensure the API key is correct
        client = genai.Client(api_key="GEMINI_API_KEY")
        
        system_prompt = "You are Jarvis, a witty and helpful AI assistant for Gaurav. Keep your responses concise and conversational."
        
        # 2. Use the full model path

        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=f"{system_prompt}\n\nUser: {text}"
        )
        
        # 3. Use .text but add a fallback just in case
        if response.text:
            return response.text
        else:
            return "I understood you, but I don't have a verbal response."

    except Exception as e:
        # This will print the REAL error in your terminal (e.g., Invalid API Key, Quota Exceeded, etc.)
        print(f"Gemini Error: {e}") 
        return "I'm having trouble connecting to my brain right now."

def processCommand(c):
    if "open google"  in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook"  in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin"  in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube"  in c.lower():
        webbrowser.open("https://youtube.com")
    elif "gmail"  in c.lower():
        webbrowser.open("https://gmail.com")
    elif "chatgpt"  in c.lower() or "chat gpt" in c.lower():
        webbrowser.open("https://chatgpt.com")
    elif "gemini"  in c.lower():
        webbrowser.open("https://gemini.google.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=NEWS_API_KEY")
        if r.status_code == 200:
            data = r.json() #perse the json response

            # extract the article and speak the headlines
            for article in data.get("articles", []):
                speak(article.get("title"))
        else:
            print("Error:", r.status_code)

    else: #Let gemini handel the request

        output = ai_command(c)
        print(output)
        speak(output)
        

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        #Listen for the wake word "Jarvis"
        #Obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=4, phrase_time_limit=3) #listen function has 2 parameter oe is timeout for how long should you listen

            word = r.recognize_google(audio)

            if "hello jarvis" in word.lower():
                speak("Hello Gaurav, how can I help you?") 
                
                while True: 
                    try:
                        with sr.Microphone() as source:
                            print("Jarvis Active... (Say 'Abort' to stop)")
                            r.adjust_for_ambient_noise(source, duration=0.5)
                            # Longer limit so you can ask Gemini complex questions
                            audio = r.listen(source, timeout=5, phrase_time_limit=8)
                            command = r.recognize_google(audio).lower()
                            
                            print(f"Gaurav: {command}")

                            if "gaurav" in command or "gaurab" in command:
                                input = "gaurav is a hero, with a VERY STRONG MINDSET and he loves learning and using AI and building things"
                                speak(input)

                            # THE ABORT LOGIC
                            elif "abort" in command or "stop" in command or "exit" in command:
                                speak("Understood. Exiting conversation mode.")
                                break # This breaks the INNER loop and goes back to waiting for "Hello Jarvis"

                            # If not aborting, process the command normally
                            processCommand(command)

                    except sr.UnknownValueError:
                        # If he doesn't hear anything, he just waits for you to speak again
                        continue 
                    except Exception as e:
                        print(f"Error: {e}")
                        break 
                # --- END CONVERSATION MODE ---
                    

        except Exception as e:
            print("Sory couldn't hear you")

