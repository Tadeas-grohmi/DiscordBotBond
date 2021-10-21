import discord
import random
import datetime
import os
import requests
from utils.utils import zapis
import asyncio
from discord.ext import commands

class reddit(commands.Cog):
    
    def __init__(self, client):
        self.client = client


    @commands.command(aliases= ["Duklock", "duklok", "Duklok"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def duklock(self, ctx):
        channel = ctx.message.channel
        async with channel.typing():
            odpoved = requests.get("https://meme-api.herokuapp.com/gimme/Duklock")
            p = odpoved.json()
            pp = p["url"]
            jmeno = p["title"]

            em = discord.Embed(color=0xfff700, title=jmeno)
            em.set_footer(text=f"Duklock ty kokos {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            em.set_image(url=pp)
            await ctx.send(embed=em)
        await zapis("ducklock")
        
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def haha(self, ctx):
        chn = ctx.message.channel
        async with chn.typing():
            odpoved = requests.get("https://meme-api.herokuapp.com/gimme/Darkhumorrage")
            p = odpoved.json()
            pp = p["url"]
            jmeno = p["title"]

            em = discord.Embed(color=0x000000, title=jmeno)
            em.set_footer(text=f"Tak se jdem zasmát {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            em.set_image(url=pp)
            await ctx.send(embed=em)
        await zapis("haha")
        
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def down(self, ctx):
        chn = ctx.message.channel
        async with chn.typing():
            odpoved = requests.get("https://meme-api.herokuapp.com/gimme/EvilBender47")
            p = odpoved.json()
            pp = p["url"]
            jmeno = p["title"]

            em = discord.Embed(color=0xffc800, title=jmeno)
            em.set_footer(text=f"Downův sindrom pro {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png",)
            em.set_image(url=pp)
            await ctx.send(embed=em)
        await zapis("down")
        
    @commands.command(aliases= ["peecko", "Porno", "porno"])
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.is_nsfw()
    async def pecko(self, ctx):
        chn= ctx.message.channel
        async with chn.typing():
            odpoved = requests.get("https://meme-api.herokuapp.com/gimme/nsfw")
            p = odpoved.json()
            pp = p["url"]
            jmeno = p["title"]

            em = discord.Embed(color=0xff0059, title=jmeno)
            em.set_footer(text=f"Pohoň si {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            em.set_image(url=pp)
            await ctx.send(embed=em)
        await zapis("pecko")
        


    @duklock.error
    @haha.error
    @down.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            zprava = ("Klídek ty koště " + ctx.author.mention + " command použij znova za {:.1f}".format(error.retry_after))
            await ctx.send(zprava)

    @pecko.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            zprava = ("Klídek ty honiči " + ctx.author.mention + " command použij znova za {:.1f}".format(error.retry_after))
            await ctx.send(zprava)
        elif isinstance(error, commands.NSFWChannelRequired):
            zprava = ("Tohle si přesuň do NSFW kanálů :kissing_heart:")
            await ctx.send(zprava)


def setup(client):
    client.add_cog(reddit(client))