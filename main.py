import discord
import time
import random
import datetime
from discord.ext import commands
import asyncio
import os.path
import json
from pymongo import MongoClient
import certifi
from utils.tajne import Mongo

mango_url = Mongo()
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["DiscordCasinoPenize"]
db2 = cluster["Prefixy"]

def get_prefix(client, message):
    collection2 = db2["prefixy"]
    data = collection2.find_one({"_id": message.guild.id})
    prefix = data["prefix"]
    return prefix

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')
tajne = json.load(open("./utils/info/tajne.json"))
token = tajne["TOKEN"]

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print('Zapínám {0.user}'.format(bot))
    time.sleep(2)
    print('Jsem zapnut a připojen za {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping je {round(bot.latency * 1000)}ms')


@bot.event
async def on_guild_join(guild):
    collection2 = db2["prefixy"]
    ID = str(guild.id)
    collection3 = db[ID]

    await guild.create_role(name="BondAdmin", colour=discord.Colour(0x0091ff))

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(title="Děkuji moc za pozvání na tenhle ůžasný server :smile:",description="Napiš !!help a zjisti co všechno umím :wink:\nA automaticky jsem vytvořil roli BondAdmin, pro další info !!admin\n Předem se omlouvám za jakékoliv chyby (kdyžtak napiš !!report <problém>) :sweat_smile: \n snažim se je co nejrychleji odstranit :smile: ",colour=0x0091ff)
            embed.set_thumbnail(url="https://media1.tenor.com/images/6c5f3a53057472f80f1de27ebb9e85e6/tenor.gif")
            embed.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await channel.send(embed=embed, delete_after=120)
        break

    try:
        jmeno = str(guild.id)
        db.create_collection(jmeno)
    except:
        pass
    
    try:
        post = {"_id": guild.id, "prefix": ["!!", "$"]}
        collection2.insert_one(post)
    except:
        pass
    time.sleep(5)
    try:
        for member in guild.members:
            if member.bot == False:
                try:
                    id = member.id
                    post = {"_id": id, "cash": 250, "banka": 450, "jmeno": member.name}
                    collection3.insert_one(post)
                    time.sleep(0.8)
                except:
                    pass
    except:
        pass

@bot.command()
async def prefix(ctx):
    collection2 = db2["prefixy"]
    data = collection2.find_one({"_id": ctx.guild.id})
    prefix = data["prefix"]
    await ctx.channel.send(f"Můj prefix na tomto serveru je {prefix}")


#TOKEN zde dik
bot.run(token)
