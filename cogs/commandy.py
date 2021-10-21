import discord
import random
import datetime
import os
import requests
import asyncio
import time
import json
import PIL
from PIL import Image
from io import BytesIO
from discord.ext import commands
import wikipedia
import pyqrcode
import png
from utils.utils import zapis
import requests
import lyricsgenius
from utils.utils import Pag
from utils.tajne import Lyrics

lyrics_api = Lyrics()

test = open("./files/Test.txt").readlines()
pp = open("./files/pp.txt").readlines()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class commandy(commands.Cog):

    def __init__(self, client):
        self.client = client

    player = {}

    @commands.command(pass_context=True)
    async def hita(self, ctx):
        await ctx.channel.send("Sieg heil :fist_tone4: " + ctx.author.mention)
        embed = discord.Embed(title="Adolf je nej", url="https://www.youtube.com/watch?v=rcVb6l4TpHw",
                              description="Všichni ho máme rádi <333", color=0x0088ff)
        embed.set_thumbnail(url="https://i0.wp.com/www.pixer.cz/wp-content/uploads/2015/07/Hitler04.jpg?ssl=1")
        embed.set_footer(text="tady je jeho sexy pic <3")
        embed.set_image(url=random.choice(test))
        time.sleep(0.5)
        await ctx.channel.send(embed=embed)
        #await ctx.channel.send(random.choice(test))
        cas = datetime.datetime.now()
        print(str(ctx.message.author) + " " + f"{bcolors.OKBLUE}Použil híťu a zahailoval si{bcolors.ENDC}" + " " + "čas:" + " " + cas.strftime("%H:%M:%S"))

    @commands.command(aliases=["IDC"])
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def idc(self, ctx):
        chn = ctx.channel
        await ctx.message.delete()
        embed = discord.Embed(title="ALE OPRAVDU TO NIKOHO NEZAJÍMÁ", url="https://www.youtube.com/watch?v=R0mKjKdyJvE",
                              description="POCHOP TO", color=0x1eff00)
        embed.set_author(name="NO ONE CARES", url="https://www.youtube.com/watch?v=R0mKjKdyJvE")
        embed.set_footer(text="just kys pls")
        await chn.send("https://cdn.discordapp.com/attachments/586526210469789717/838335535944564756/Editor40.mp4")
        # await ctx.channel.send(embed=embed)

    @commands.command(aliases=["pp", "pepe", "PELE", "PP", "perko"])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def pele(self, ctx, koho: discord.Member=None):
        if koho == None:
            koho = ctx.author

        if koho.id == 506874709607186432:
            await ctx.channel.send("Takový máš pele " + koho.mention)
            await ctx.channel.send("8=================================================D")
        else:
            await ctx.channel.send("Takový máš pele " + koho.mention)
            await ctx.channel.send(random.choice(pp))
        await zapis("pp")
        
    @commands.command()
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def cas(self, ctx):
        cas = datetime.datetime.now()
        await ctx.channel.send(cas.strftime("%Y-%m-%d %H:%M:%S"))

    @commands.command()
    @commands.cooldown(6, 10, commands.BucketType.user)
    async def mama(self, ctx, member: discord.Member = None):
        with open("./files/jokes.json") as joke_file:
            jokes = json.load(joke_file)
        random_category = random.choice(list(jokes.keys()))
        insult = random.choice(list(jokes[random_category]))
        if member is not None:
            print("za 1 dostal " + member.name)
            await ctx.send("%s Tady máš šmejde: %s " % (member.name, insult))
        else:
            print("Hehe " + ctx.message.author.name + " se sám vyroastil")
            await ctx.send("%s jeden pro tebe: %s " % (ctx.message.author.name, insult))

    @commands.command()
    @commands.cooldown(6, 8, commands.BucketType.user)
    async def vtip(self, ctx):
        odpoved = requests.get("https://v2.jokeapi.dev/joke/Any?lang=cs")
        h = odpoved.json()

        if h["type"] == "single":
            j = h["joke"]
            await ctx.send(j)

        if h["type"] == "twopart":
            s = h["setup"]
            d = h["delivery"]
            await ctx.send(s)
            await asyncio.sleep(1)
            await ctx.send(d)

    @commands.command()
    @commands.cooldown(6, 8, commands.BucketType.user)
    async def joke(self, ctx):
        odpoved = requests.get("https://v2.jokeapi.dev/joke/Any?lang=en")
        h = odpoved.json()

        if h["type"] == "single":
            j = h["joke"]
            await ctx.send(j)

        if h["type"] == "twopart":
            s = h["setup"]
            d = h["delivery"]
            await ctx.send(s)
            await asyncio.sleep(1)
            await ctx.send(d)
        await zapis("joke")
        
    @commands.command()
    async def hitler(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        hitler = Image.open("./files/hitler.jpg")
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((160,187))
        hitler.paste(pfp, (50,35))
        hitler.save("./yt-dl/hitler.jpeg")
        await ctx.send(file= discord.File("./yt-dl/hitler.jpeg"))
        await zapis("hitler")

    @commands.command()
    async def gay(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        gay = Image.open("./files/gay.jpg")
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((180,180))
        gay.paste(pfp, (225,165))
        gay.save("./yt-dl/gay.jpg")
        await ctx.send(file= discord.File("./yt-dl/gay.jpg"))
        await zapis("gay")
        
    @commands.command()
    async def emoji(self, ctx, *, text):
        chn = ctx.channel
        await ctx.message.delete()
        emoji = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {'0': 'zero', '1':'one','2':'two',
                           '3':'three', '4':'four', '5':'five',
                           '6':'six', '7':'seven', '8':'eight', '9':'nine'}
                emoji.append(f":{num2emo.get(s)}:")
            elif s.isalpha():
                emoji.append(f":regional_indicator_{s}:")
            else:
                emoji.append(s)
        await ctx.send(" ".join(emoji))
        await zapis("emoji")
        
    @commands.command(aliases=["Wiki"])
    async def wiki(self, ctx,*,co):
        def wiki_celek(self, arg):
            jazyk = 'cz'
            wikipedia.set_lang(jazyk)
            definition = wikipedia.summary(arg,sentences=3,chars=1000)
            return definition
        wiki_embed = discord.Embed(title="**Definice z wiki:**",description=wiki_celek(self, co), color=discord.Colour.random())
        wiki_embed.set_footer(text=f"Pro: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        await ctx.send(embed=wiki_embed)
        await zapis("wiki")
        
    @commands.command(aliases=["Qr", "QR", "qrkod", "Qrkod", "QRkod", "qrcode"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def qr(self,ctx,*, url: str= None):
        if url == None:
            await ctx.send("Chybí url adresa, nebo je tahle vadná.", delete_after=4)
            return
        chn = ctx.channel
        await ctx.message.delete()
        obr = pyqrcode.create(url)
        obr.svg("./yt-dl/qrcode.svg", scale=8)
        obr.png("./yt-dl/qrcode.png", scale=6)
        soubor = discord.File("./yt-dl/qrcode.png")
        await ctx.send(file=soubor, content=f"QR kod zde {ctx.author.mention} :")
        await zapis("qr")
        
    @commands.command(aliases=["Bypass"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def bypass(self, ctx, arg):
        r = requests.get('https://bypass.bot.nu/bypass2?url=' + arg)
        a = ('%' + r.text)
        chunks = a.split(',')
        dest = chunks[1]
        stripped = dest.split('"')
        embed = discord.Embed()
        embed.set_footer(text=f"Pro: {ctx.author.name}")
        embed.set_thumbnail(url="https://media3.giphy.com/media/XEVH1nBDsw14qk9POU/giphy.gif")
        # https://thumbs.gfycat.com/PlainHonestAzurevase-size_restricted.gif
        embed.add_field(name="Bypassnuty link zde:", value=stripped[3], inline=False)
        await ctx.send(embed=embed)
        await zapis("linkvertise-bypass")
        
    @commands.command(aliases=["Text", "lyrics", "Lyrics"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def text(self, ctx, *, song=None):
        genius = lyricsgenius.Genius(lyrics_api)
        artist = genius.search(search_term=song)
        idk = artist["hits"]
        dale = idk[0]
        ll = dale["result"]
        id = ll["id"]
        song = genius.lyrics(song_id=id)
        song.strip()
        jmeno = ll["full_title"]
        pager = Pag(
            timeout=200,
            entries=[song[i: i + 2000] for i in range(0, len(song), 2000)],
            length=1,
            prefix="\n",
            suffix="\n"
        )
        await ctx.send(f"Lyrics pro songu: **{jmeno}**")
        await pager.start(ctx)

    @cas.error
    @pele.error
    @mama.error
    @idc.error
    @joke.error
    @vtip.error
    @qr.error
    @bypass.error
    @text.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            zprava = ("Klídek ty koště " + ctx.author.mention + " command použij znova za {:.1f}".format(error.retry_after))
            await ctx.send(zprava)

def setup(client):
    client.add_cog(commandy(client))