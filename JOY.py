"""
########################
" Voice Assistant - Joy"
########################


This is a pet project which was created for fun activities and getting assistance with daily needs of a user. It is
inspired from a fictional Artificially Intelligent assistant " JARVIS" in the movie "IRONMAN". This program is
essentially a prompt or request based retrieval system which recognizes speech and fulfils the request.

Some cool things that you can do are the following:

1. Ask name : " Who are you?", " What is your name?"
2. Play videos on youtube by command: " Could you play?"
3. Ask meaning on Wikipedia: " What do you mean by?, " What is the meaning of?"
4. Chatterbot inclusion - Talk anything you want with Joy
5. Ask meaning of a word( Pydictionary) : " Meaning of"
6. Ask temperature (Yahoo Weather): : " Temperature Outside"
7. Ask cureent news: "What's in news", "Give me some news", "What's happening around the world"]
8. Greet : " Thank you"
"""


import speech_recognition as sr
import webbrowser
import os
import urllib.request
import urllib.parse
import re
import wikipedia
import random
import sys
import msvcrt
import pafy
import vlc

from PyDictionary import PyDictionary


from chatterbot import ChatBot


chatbot = ChatBot(
    'Joy',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    #trainer='chatterbot.trainers.chatterbot.corpus.english',
     logic_adapters = [
         "chatterbot.logic.BestMatch",
         #"chatterbot.logic.MathematicalEvaluation",
         #"chatterbot.logic.TimeLogicAdapter"
]
)

# Train based on the english corpus
chatbot.train("chatterbot.corpus.english")

# Get a response to an input statement
#print(chatbot.get_response("What is your name?"))


from weather import Weather
weather = Weather()

from wikiapi import WikiApi
wiki = WikiApi()

dictionary = PyDictionary()


# Lookup WOEID via http://weather.yahoo.com. # Use this code alternatively to use Yahoo WOEID for your city to
#lookup = weather.lookup(560743)             # to get weather conditions for your city
#condition = lookup.condition()

location = weather.lookup_by_location('st. louis') # Enter your city name before running the script
condition = location.condition()



def speak(arg):
    import pyttsx3
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 40)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(arg)
    engine.say("   ")
    engine.runAndWait()

query = ' '

def activate_speech():

        while(1):

            try:
                new = 2
                # Record Audio
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Say something!")
                    audio = r.listen(source)
                    tag = r.recognize_google(audio)

                # Speech recognition using Google Speech Recognition
                try:
                    # for testing purposes, we're just using the default API key
                    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                    # instead of `r.recognize_google(audio)`
                    print("You said: " + r.recognize_google(audio))
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                str_greet_list = ["who are you","what is your name"]
                str_thank_list = ["thank you"]
                str1 = "what do you mean by "
                str2 = "what is"
                str3 = "could you play"
                str4 = "who is"
                str5 = "what is the meaning of"
                str6 = "meaning of"
                str7 = "temperature outside"
                str_how_list = ["how are you", "how are you today", "how are you doing today", "what's up", "what's going on"]
                str_love_list = ["i love you", "you are so sexy", "your voice is so beautiful"]
                str_news_list = ["what's in news", "give me some news", "what's happening around the world"]
                if tag.upper() in (name.upper() for name in str_thank_list):
                    speak(" You're welcome")
                elif tag.upper() in (name.upper() for name in str_greet_list):
                    speak("My name is joy, i am your personal voice assistant, ready to assist to you, now, go on and ask me something")
                elif str1 in tag:
                    query = tag.split("by", 1)[1]
                    print(query)
                    results = wiki.find(query)
                    article = wiki.get_article(results[0])
                    a = article.summary
                    result = re.sub(r'\([^()]*\)', '', a)
                    result = re.sub(r'\[.*?\]', '', result)
                    print(result)
                    from nltk.tokenize import sent_tokenize, word_tokenize
                    x = sent_tokenize(result)
                    y = ''.join(x[0:1])
                    print(result)
                    speak(result)
                elif str2 in tag:
                    query = tag.split("is", 1)[1]
                    print(query)
                    results = wiki.find(query)
                    article = wiki.get_article(results[0])
                    a = article.summary
                    result = re.sub(r'\([^()]*\)', '', a)
                    result = re.sub(r'\[.*?\]', '', result)
                    from nltk.tokenize import sent_tokenize, word_tokenize
                    x = sent_tokenize(result)
                    y = ''.join(x[0:2])
                    print(y)
                    speak(y)

                elif str3.upper() in tag.upper():
                    #query = ' '.join(tag.split(' ')[1:])   # Use this if you have to say just "play"
                    query = tag.split("play", 1)[1]
                    print(query)
                    query_string = urllib.parse.urlencode({"search_query": query})
                    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

                    # The next line to play the video song on youtube
                    webbrowser.open("http://www.youtube.com/watch?v=" + search_results[0])

                    # The following four lines allow you to play youtube video on VLC player
                    # url = "http://www.youtube.com/watch?v=" + search_results[0]
                    # vlc_path = "C:\Program Files (x86)\VideoLAN\VLC"
                    # os.chdir(vlc_path)
                    # os.system(f"vlc {url}")
                elif str4 in tag:
                    query = tag.split("is", 1)[1]
                    print(query)
                    results = wiki.find(query)
                    article = wiki.get_article(results[0])
                    a1 = article.summary
                    result1 = re.sub(r'\([^()]*\)', '', a1)
                    result1 = re.sub(r'\[.*?\]', '', result1)
                    from nltk.tokenize import sent_tokenize, word_tokenize
                    x1 = sent_tokenize(result1)
                    y1 = ''.join(x1[0:2])
                    print(y1)
                    speak(y1)
                elif str5 in tag:
                    query = tag.split("of", 1)[1]
                    print(query)
                    results = wiki.find(query)
                    article = wiki.get_article(results[0])
                    a = article.summary
                    result = re.sub(r'\([^()]*\)', '', a)
                    result = re.sub(r'\[.*?\]', '', result)
                    print(result)
                    speak(result)
                elif tag.upper() in (name.upper() for name in str_love_list):
                    str_love_reply = ["Stop it, no really stop it",
                                      " I am so sorry, I already have a boyfriend, and his name is Jarvis",
                                      " Better luck next time"]
                    speak(random.choice(str_love_reply))
                elif tag.upper() in (name.upper() for name in str_how_list):
                    str_how_reply = ["I am fine honey, how are you?",
                                     "I am good, thanks for asking",
                                     "I am good, how about you?", " I am good, how can I help you today"]
                    speak(random.choice(str_how_reply))
                elif str6 in tag:
                    try:
                        query = tag.split("of", 1)[1]
                        if query != '':
                            print(dictionary.meaning(query))
                            speak(dictionary.meaning(query))
                            speak("Do you want to learn some similar words like " + query)
                            with sr.Microphone() as source:
                                r = sr.Recognizer()
                                print("Say something!")
                                syn = r.listen(source)
                                synf = (r.recognize_google(syn))
                                print(synf)
                                if  synf == "yes":
                                    print(dictionary.synonym(query))
                                    speak(" Some of the synonyms are")
                                    speak(dictionary.synonym(query))
                                else:
                                    speak("Thankyou for your time")
                                print(dictionary.antonym(query))
                        elif query == ' ':
                            speak("Could you please repeat that again?")

                    except:
                        speak("I am sorry, could you please repeat that again?")

                elif str7 in tag:

                    f = int(condition['temp'])
                    temp_c = round((f - 32) * .5556)
                    speak("It is " + condition['text'] + " with a temperature of "+ str(temp_c)+ " degree celsius")
                elif tag.upper() in (name.upper() for name in str_news_list):
                    print("Alright, do you want to get news from India or the US?")
                    speak("Alright, do you want to get news from India or the US")
                    with sr.Microphone() as source:
                        r = sr.Recognizer()
                        print("Say something!")
                        audio = r.listen(source)
                        place = r.recognize_google(audio)
                        print(place)
                        if place == "India":
                            url = ('https://newsapi.org/v2/top-headlines?'
                                   'sources=the-times-of-india&'
                                   'apiKey=fd3422eb98d846e0b288ee8601299b13')
                            import requests
                            response = requests.get(url)
                            data = response.json()
                            title_list = data['articles']
                            for title in title_list:
                                titlenow = title['title']
                                titlesplit = titlenow.split('-')[0]
                                split = titlesplit.split('|')[0]
                                print(split)
                                speak(split)
                        elif tag =="us" |  tag =="the us":
                            url = ('https://newsapi.org/v2/top-headlines?'
                                   'sources=cnn&'
                                   'apiKey=fd3422eb98d846e0b288ee8601299b13')
                            import requests
                            response = requests.get(url)
                            data = response.json()
                            title_list = data['articles']
                            for title in title_list:
                                titlenow = title['title']
                                titlesplit = titlenow.split('-')[0]
                                split = titlesplit.split('|')[0]
                                print(split)
                                speak(split)


                # else :
                #     speak(chatbot.get_response(tag))

            except:
                print("Say something dear!!")


activate_speech()

