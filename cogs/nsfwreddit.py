# Created by Tada at 15.5.2021
import discord
import time
import random
import datetime
import requests
from discord.ext import commands
from utils.utils import zapis

class nsfwreddit(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["Hentai"])
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.is_nsfw()
    async def hentai(self, ctx):
        chn= ctx.message.channel
        async with chn.typing():
            odpoved = requests.get("https://meme-api.herokuapp.com/gimme/hentai")
            p = odpoved.json()
            pp = p["url"]
            jmeno = p["title"]

            em = discord.Embed(color=0xff00e1)
            em.set_author(name=jmeno, url=pp)
            em.set_footer(text=f"Trochu toho hentai porna {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            em.set_image(url=pp)
            await ctx.send(embed=em)
        await zapis("hentai")
        
    @commands.command(aliases=["Lolhentai"])
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.is_nsfw()
    async def lolhentai(self, ctx):
        chn= ctx.message.channel
        async with chn.typing():
            odpoved = requests.get("https://meme-api.herokuapp.com/gimme/Rule34LoL")
            p = odpoved.json()
            pp = p["url"]
            jmeno = p["title"]

            em = discord.Embed(color=0xff00e1)
            em.set_author(name=jmeno, url=pp)
            em.set_footer(text=f"Lol hentai pro {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            em.set_image(url=pp)
            await ctx.send(embed=em)
        await zapis("lolhentai")
        
    @commands.command(aliases=["Valohentai"])
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.is_nsfw()
    async def valohentai(self, ctx):
        chn= ctx.message.channel
        async with chn.typing():
            odpoved = requests.get("https://meme-api.herokuapp.com/gimme/valorantrule34")
            p = odpoved.json()
            pp = p["url"]
            jmeno = p["title"]

            em = discord.Embed(color=0xff00e1)
            em.set_author(name=jmeno, url=pp)
            em.set_footer(text=f"Valorant hentai pro {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            em.set_image(url=pp)
            await ctx.send(embed=em)
        await zapis("valohentai")
        
    @commands.command(aliases=["Overhentai"])
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.is_nsfw()
    async def overhentai(self, ctx):
        chn= ctx.message.channel
        async with chn.typing():
            odpoved = requests.get("https://meme-api.herokuapp.com/gimme/OverwatchNSFW")
            p = odpoved.json()
            pp = p["url"]
            jmeno = p["title"]

            em = discord.Embed(color=0xff00e1)
            em.set_author(name=jmeno, url=pp)
            em.set_footer(text=f"Valorant hentai pro {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            em.set_image(url=pp)
            await ctx.send(embed=em)
        await zapis("overhentai")
        
    @hentai.error
    @valohentai.error
    @lolhentai.error
    @overhentai.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            zprava = ("Klídek ty honiči " + ctx.author.mention + " command použij znova za {:.1f}".format(error.retry_after))
            await ctx.send(zprava)
        elif isinstance(error, commands.NSFWChannelRequired):
            zprava = ("Tohle si přesuň do NSFW kanálů :kissing_heart:")
            await ctx.send(zprava)

def setup(client):
    client.add_cog(nsfwreddit(client))
