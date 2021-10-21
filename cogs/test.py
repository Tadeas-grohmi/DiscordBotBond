# Created by Tada at 6.5.2021
import discord
import time
import random
import datetime
import nacl
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import youtube_dl
import requests
import json
import os
import pymongo
from pymongo import MongoClient
import certifi
import PIL
from PIL import Image
from io import BytesIO
from discord.ext import commands
from utils.tajne import Mongo

mango_url = Mongo()
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["test"] 

class test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command()
    async def graf(self, ctx, jakej=None):
        if jakej == "casino":
            await casino()
            await ctx.send(file=discord.File("./yt-dl/casino.png"))
        if jakej == "commandy":
            await commandy()
            await ctx.send(file=discord.File("./yt-dl/commandy.png"))
        else:
            await ctx.send("casino, commandy!")

    @graf.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Nejsi owner..")
            
            
            








def setup(client):
    client.add_cog(test(client))
