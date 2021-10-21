from pymongo import MongoClient
import certifi
import discord
import matplotlib.pyplot as plt

mango_url = "mongodb+srv://Bond:Drago00914*@disbotbond.xo3fb.mongodb.net/test"
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["Zaznamy"]

collection = db["zaznamy"]
data = collection.find_one({"_id": "Zaznamy"})
penize = data["penize"]
zebrat = data["zebrat"]
pocasi = data["pocasi"]
fullpocasi = data["fullpocasi"]
hentai = data["hentai"]
kurva = data["kurva"]
prace = data["prace"]
sloty = data["sloty"]
vlozit = data["vlozit"]
kostka = data["kostka"]
vybrat = data["vybrat"]
dat = data["dat"]
okrast = data["okrast"]
padej = data["padej"]
e2 = data["evropa2"]
beat = data["beat"]
emoji = data["emoji"]

async def casino():
    x = [penize, zebrat, prace, kurva, sloty, kostka, vlozit, vybrat, dat, okrast]
    casino = ["Peníze", "Žebrat", "Práce", "Kurva", "Sloty", "Kostka", "Vložit", "Vybrat", "Dát", "Okrást"]
    plt.figure(figsize=(8, 5))
    plt.bar(casino, x)
    plt.title("Používání commandů")
    plt.savefig("./yt-dl/casino.png")

async def commandy():
    y = [e2, beat, padej, pocasi, fullpocasi, emoji]
    commandy = ["Evropa 2", "Beat", "Padej", "Počasí", "Fullpočasí", "Emoji"]
    plt.figure(figsize=(8, 5))
    plt.bar(commandy, y)
    plt.title("Používání commandů")
    plt.savefig("./yt-dl/commandy.png")
