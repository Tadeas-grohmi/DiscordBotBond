# Created by ${USER} at ${DATE}
import discord
import time
import random
import datetime
import nacl
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import youtube_dl
from utils.utils import zapis
from discord.ext import commands

player = {}

class radio(commands.Cog):

    def __init__(self, client,):
        self.client = client

    @commands.command(aliases=['E2', 'e2'])
    async def evropa2(self, ctx, url: str = 'http://20873.live.streamtheworld.com/EVROPA2.mp3'):
        try:
            channel = ctx.message.author.voice.channel
            global player
            try:
                player.play(FFmpegPCMAudio('http://ice.actve.net/fm-evropa2-128'))
                player.source = discord.PCMVolumeTransformer(player.source)
                player.source.volume = 1.1
                await ctx.send("Evropa 2 puštěna!")
            except:
                player = await channel.connect()
                player.play(FFmpegPCMAudio('http://ice.actve.net/fm-evropa2-128'))
                player.source = discord.PCMVolumeTransformer(player.source)
                player.source.volume = 1.1
                await ctx.send("Evropa 2 puštěna!")
        except:
            await ctx.send("Musis byt ve vc")
        await zapis("evropa2")
        
    @commands.command(aliases=['Beat', 'BigBeat'])
    async def beat(self, ctx, url: str = 'http://icecast2.play.cz/radiobeat128.mp3'):
        channel = ctx.message.author.voice.channel
        global player
        try:
            player.play(FFmpegPCMAudio('http://icecast2.play.cz/radiobeat128.mp3'))
            player.source = discord.PCMVolumeTransformer(player.source)
            player.source.volume = 1.0
        except:
            player = await channel.connect()
            player.play(FFmpegPCMAudio('http://icecast2.play.cz/radiobeat128.mp3'))
            player.source = discord.PCMVolumeTransformer(player.source)
            player.source.volume = 1.0
        await zapis("beat")
        
    @commands.command(aliases=['kis', 'kiss'])
    async def Kiss(self, ctx, url: str = 'http://icecast4.play.cz/kiss128.mp3'):
        channel = ctx.message.author.voice.channel
        global player
        try:
            player.play(FFmpegPCMAudio('http://icecast4.play.cz/kiss128.mp3'))
            player.source = discord.PCMVolumeTransformer(player.source)
            player.source.volume = 1.0
        except:
            player = await channel.connect()
            player.play(FFmpegPCMAudio('http://icecast4.play.cz/kiss128.mp3'))
            player.source = discord.PCMVolumeTransformer(player.source)
            player.source.volume = 1.0
        await zapis("kiss")
    
    @commands.command(aliases=["Stop"])
    async def stop(self, ctx):
        try:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            voice.stop()
            await ctx.send("Stopnuto 🔇")
        except:
            await ctx.send("Není co stopnout 😥")

    
    @Kiss.error
    @beat.error
    async def on_command_error(self, ctx, error):
        print("idk nejakej error, snad to jede dal xD-radio")

def setup(client):
    client.add_cog(radio(client))