import json

def openweather():
    tajne = json.load(open("utils/info/tajne.json"))
    api_key = tajne["OPENWEATHERAPI-KLIC"]
    return api_key

def ChatBot():
    tajne = json.load(open("utils/info/tajne.json"))
    chatbot_klic = tajne["CHATBOT-KLIC"]
    return chatbot_klic

def Lyrics():
    tajne = json.load(open("utils/info/tajne.json"))
    Lyrics_klic = tajne["LYRICS_KLIC"]
    return Lyrics_klic

def Mongo():
    tajne = json.load(open("utils/info/tajne.json"))
    mongo_url = tajne["MONGO-URL"]
    return mongo_url