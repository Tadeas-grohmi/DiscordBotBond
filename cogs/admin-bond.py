# Created by Tada at 13.5.2021
import discord
import time
import random
import datetime
from discord.ext import commands
import json
from pymongo import MongoClient
import certifi
import asyncio
from utils.tajne import Mongo

mango_url = Mongo()
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["reporty"]

class adminbota(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        await ctx.channel.send(extension + " Cog reloadnut!")
        cas = datetime.datetime.now()
        print(cas.strftime("%H:%M:%S") + " " + "reload" + " " + extension + "-cog")


    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        await ctx.channel.send(extension + " Cog loadnut!")
        cas = datetime.datetime.now()
        print(cas.strftime("%H:%M:%S") + " " + "loadnul" + " " + extension + "-cog")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        await ctx.channel.send(extension + " Cog unloadnut!")
        cas = datetime.datetime.now()
        print(cas.strftime("%H:%M:%S") + " " + "loadnul" + " " + extension + "-cog")
    
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def report(self, ctx,*, report:str):
        collection = db["ReportyDB"]
        kanal = self.client.get_channel(845572031252267008)
        cas = datetime.datetime.now()

        reportem = discord.Embed(title=f"Report od {ctx.author.name} z serveru {ctx.guild.name}", description=f"Report: **{report}**", colour=discord.Colour.blue())
        reportem.add_field(name=f"Id:",value=f"{ctx.author.id}")
        reportem.set_thumbnail(url=ctx.message.author.avatar_url)
        reportem.add_field(name="Čas:", value=cas.strftime("%H:%M:%S"))
        reportem.add_field(name="Den:", value=cas.strftime("%d %b %Y"))
        reportem.add_field(name="Databáze:", value="Ano")
        embed = await kanal.send(embed=reportem)


        kdo = ctx.author.name
        server = ctx.guild.name
        cas1 = cas.strftime("%H:%M:%S")
        datum = cas.strftime("%d %b %Y")
        
        rep = await ctx.send("Report úspěšně poslán!")
        msg = await ctx.send("Chceš ho zálohovat do databáze?")
        
        reactmoji = ["✔", "❌"]
        for react in reactmoji:
            await msg.add_reaction(react)

        def check_react(reaction, user):
            if reaction.message.id != msg.id:
                return False
            if user != ctx.message.author:
                return False
            if str(reaction.emoji) not in reactmoji:
                return False
            return True

        try:
            res, user = await self.client.wait_for('reaction_add', check=check_react)
        except asyncio.TimeoutError:
            return await msg.clear_reactions()

        if user != ctx.message.author:
            pass
        elif '✔' in str(res.emoji):
            await msg.remove_reaction("✔", user)
            post = {"Jméno": kdo, "Server": server, "Čas": cas1, "Datum": datum, "Report": report}
            collection.insert_one(post)
            rep1 = await ctx.send("Report úspěšně zálohován!")
            await asyncio.sleep(5)
            await rep1.delete()
            await rep.delete()
            await msg.delete()
            reportem1 = discord.Embed(title=f"Report od {ctx.author.name} z serveru {ctx.guild.name}",
                                     description=f"Report: **{report}**", colour=discord.Colour.blue())
            reportem1.add_field(name=f"Id:", value=f"{ctx.author.id}")
            reportem1.set_thumbnail(url=ctx.message.author.avatar_url)
            reportem1.add_field(name="Čas:", value=cas.strftime("%H:%M:%S"))
            reportem1.add_field(name="Den:", value=cas.strftime("%d %b %Y"))
            reportem1.add_field(name="Databáze:", value="Ano")
            await embed.edit(embed=reportem1)

        elif '❌' in str(res.emoji):
            await msg.remove_reaction("❌", user)
            ne = await ctx.send("Záloha neproběhla!")
            await msg.delete()
            await rep.delete()
            await ne.delete()
            reportem2 = discord.Embed(title=f"Report od {ctx.author.name} z serveru {ctx.guild.name}",
                                     description=f"Report: **{report}**", colour=discord.Colour.blue())
            reportem2.add_field(name=f"Id:", value=f"{ctx.author.id}")
            reportem2.set_thumbnail(url=ctx.message.author.avatar_url)
            reportem2.add_field(name="Čas:", value=cas.strftime("%H:%M:%S"))
            reportem2.add_field(name="Den:", value=cas.strftime("%d %b %Y"))
            reportem2.add_field(name="Databáze:", value="Ne")
            await embed.edit(embed=reportem2)

    @commands.command()
    @commands.is_owner()
    async def reportdm(self, ctx, koho:discord.Member= None, *, zprava:str):
        if koho == None:
            await ctx.send("Napiš komu ty koště!")
            return
        else:
            dm = discord.Embed(title=f"Máš tu odpověď na tvůj report od: {ctx.author.name}", description=f"Odpověď: **{zprava}**",colour=discord.Colour.random())
            dm.set_footer(text=f"Snad to pomohlo, Bond <3",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            dm.set_author(name="Report odpověď" ,icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await koho.send(embed=dm)
            await ctx.send(f"Odpověď pro {koho.display_name} úspěšně odeslána!")

    @reload.error
    @load.error
    @unload.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.channel.send("Co to zkoušíš?!")

    @reportdm.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Nejsi owner..")

    @report.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            zprava = ("Klídek ty koště " + ctx.author.mention + " report můžeš poslat až za {:.0f}s".format(error.retry_after))
            await ctx.send(zprava)

def setup(client):
    client.add_cog(adminbota(client))
