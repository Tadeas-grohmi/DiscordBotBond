# Created by Tada at 8.5.2021
import discord
import time
import random
import datetime
import nacl
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import youtube_dl
from pymongo import MongoClient
import certifi
from discord.ext import commands

mango_url = "mongodb+srv://Bond:Drago00914*@disbotbond.xo3fb.mongodb.net/test"
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["vitej_room"]

class eventy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            jmeno = member.guild.id
            collection = db["vitej_data"]
            data = collection.find_one({"_id": jmeno})
            if (data["vitej_stav"]) == "On":
                kanal = data["vitej_kanal"]
                channel = self.client.get_channel(kanal)
                if channel:
                    embed = discord.Embed(description=member.mention + "Se připojil :partying_face:"
                                                      "\n**Pravidla:**"
                                                      "\n Nechovej se jak debil :rofl: \nPoužívej příkazy pro boty :robot:\nNespamuj jak degeš :face_with_symbols_over_mouth: \nNSFW matroš posílej do NSFW roomek :underage: \nA hlavně se bav :smile:",
                                          color=0x0011ff)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_author(name=member.name, icon_url=member.avatar_url)
                    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await channel.send(embed=embed)
            else:
                pass
        except:
            pass


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            jmeno = member.guild.id
            collection = db["vitej_data"]
            data = collection.find_one({"_id": jmeno})
            if (data["bye_stav"]) == "On":
                kanal = data["bye_kanal"]
                channel = self.client.get_channel(kanal)
                if channel:
                    embed = discord.Embed(description=member.mention + "Nás opustil :confused: "
                                                      "\nBudeš nám určitě chybět",color=0x000000)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_author(name=member.name, icon_url=member.avatar_url)
                    #embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await channel.send(embed=embed)
            else:
                pass
        except:
            pass




def setup(client):
    client.add_cog(eventy(client))
