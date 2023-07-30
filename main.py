import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import openai
import requests
from config import apikey
import datetime as dt

openai.api_key = apikey

def getSong(query):
    # li =
    query.replace(' ','%20')
    print(query)
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q":query,"type":"tracks","offset":"1","limit":"1","numberOfTopResults":"10"}

    headers = {
        "X-RapidAPI-Key": "99db78a117mshf10d54a13f695fep172c0fjsn5044db8fc6e7",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    res = response.json()
    print(res["tracks"]["items"][0]["data"]["id"])
    id = res["tracks"]["items"][0]["data"]["id"]
    webbrowser.open(f"https://open.spotify.com/track/{id}")


chatStr = ""
def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\n Wednesday: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai_ans(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    with open(f"OpenAI/{prompt}.txt","w") as f:
        f.write(response["choices"][0]["text"])




def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeSong():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"Song name: {query}")
            prompt = query
            getSong(prompt)
        except Exception as e:
            print("I can't hear you boss!!")
        
def takeCmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User Said: {query}")
            prompt = query
            return query
        except Exception as e:
            print("I can't hear you boss!!")
            return "I can't hear you boss!!"



sites = ["youtube", "google", "instagram", "wikipedia",'git', "github","gmail"]
stop_keywords = ["stop","close","shutup","exit","quit"]




say("Hi Boss, How can I help you today?")
while True:
    print("Listening.....")
    query = takeCmd()
    recognized_site = None
    recognized_song = None
    for site in sites:
        if f"open {site}" in query.lower():
            recognized_site = site
            break


    if recognized_site:
        say(f"Opening {recognized_site} boss...")
        webbrowser.open(f"https://www.{recognized_site}.com/")
    elif "the time" in query.lower():
        say(f"Time is {dt.datetime.now().strftime('%H:%M:%S')} boss...")
    elif any(keyword in query.lower() for keyword in stop_keywords):
        say("Ok Boss, I am Leaving")
        break
    elif "open brave" in query.lower():
        say("Opening Brave Boss...")
        os.startfile("C:\Program Files\BraveSoftware\Brave-Browser\Application\\brave")
    elif "open anime" in query.lower():
        say("Opening Anime Stuff Boss...")
        os.startfile("E:\Anime Stuff")
    elif "open mini projects" in query.lower():
        os.startfile("D:\Mini Projects");
    elif "using ai" in query.lower():
        ai_ans(query)
    elif 'reset chat' in query.lower():
        chatStr = ""
    elif "on spotify" in query.lower():
        # getSong(query)
        say("Sure which song you want to play...")
        songName = takeSong()
    else:
        print("Chatting")
        chat(query)
# https://open.spotify.com/track/4W4fNrZYkobj539TOWsLO2?si=005b45ad5a524826