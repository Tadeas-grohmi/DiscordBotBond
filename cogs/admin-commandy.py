# Created by Tada at 15.5.2021
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
from utils.tajne import Mongo

mango_url = Mongo()
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["vitej_room"]
db2 = cluster["Prefixy"]

class admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Smaz", "smaž", "Smaž"])
    @commands.has_role("BondAdmin")
    async def smaz(self, ctx,limit: int = 1):
        if 0 < limit <=100:
            with ctx.channel.typing():
                gif = await ctx.send("https://tenor.com/view/get-this-shit-out-club-penguin-mop-just-let-me-get-rid-of-the-shit-post-above-gif-17264103")
                await asyncio.sleep(0.7)
                await ctx.channel.purge(limit=limit+2, after=datetime.datetime.utcnow()-datetime.timedelta(days=14))
                await asyncio.sleep(0.5)
                await gif.delete()
                await ctx.send(f"Smazáno {limit} zpráv!", delete_after= 3)
        else:
            await ctx.send("Limit zpráv na smazání je 100!")

    @commands.command()
    @commands.has_role("BondAdmin")
    async def ssmaz(self, ctx,limit: int = 1):
        if 0 < limit <=100:
            await ctx.channel.purge(limit=limit+1, after=datetime.datetime.utcnow()-datetime.timedelta(days=14))
        else:
            await ctx.send("Limit zpráv na smazání je 100!")
    
    
    @commands.command(alaises=["changeprefix", "zmenaprefixu"])
    @commands.has_permissions(administrator=True)
    async def zmenaprefixu(self, ctx, prefix=None):
        if prefix == None:
            prefix = ["!!", "$"]

        collection2 = db2["prefixy"]
        data = collection2.find_one({"_id": ctx.guild.id})
        post = {"$set": {"prefix": prefix}}
        collection2.update_one(data, post)
        pre = data["prefix"]
        await ctx.send(f"Prefix byl změnen z **{pre}** na **{prefix}**")
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def vitej(self, ctx, kanal: discord.TextChannel = None):
        jmeno = ctx.guild.id
        collection = db["vitej_data"]
        data = collection.find_one({"_id": jmeno})
        if kanal == None:
            await ctx.send("Napiš v jakým kanálu chceš posílat oznámení!")
            return
        if data == None:
            kanal = kanal.id
            guild = ctx.guild.id
            jmeno = ctx.guild.name
            post = {"_id": guild,"jmeno serveru": jmeno, "vitej_kanal": kanal, "vitej_stav": "On", "bye_kanal": kanal, "bye_stav": "On"}
            collection.insert_one(post)
            await ctx.send("Kanál pro oznámení udělán!")
        else:
            kanal_update = kanal.id
            guild = ctx.guild.id
            data = collection.find_one({"_id": guild})
            prace = {"$set": {"vitej_kanal": kanal_update}}
            collection.update_one(data, prace)
            await ctx.send(f"Přivítací kanál změněn na {kanal.name}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def bye(self, ctx, kanal: discord.TextChannel = None):
        jmeno = ctx.guild.id
        collection = db["vitej_data"]
        data = collection.find_one({"_id": jmeno})
        if kanal == None:
            await ctx.send("Napiš v jakým kanálu chceš posílat oznámení!")
            return
        if data == None:
            kanal = kanal.id
            guild = ctx.guild.id
            jmeno = ctx.guild.name
            post = {"_id": guild,"jmeno serveru": jmeno, "vitej_kanal": kanal, "vitej_stav": "On", "bye_kanal": kanal, "bye_stav": "On"}
            collection.insert_one(post)
            await ctx.send("Kanál pro oznámení udělán!")
        else:
            kanal_update = kanal.id
            guild = ctx.guild.id
            data = collection.find_one({"_id": guild})
            post = {"$set": {"bye_kanal": kanal_update}}
            collection.update_one(data, post)
            await ctx.send(f"Bye kanál změněn na {kanal.name}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def vitej_off(self, ctx):
        guild = ctx.guild.id
        collection = db["vitej_data"]
        data = collection.find_one({"_id": guild})
        prace = {"$set": {"vitej_stav": "Off"}}
        if (data["vitej_stav"]) == "Off":
            await ctx.send("Přivítání už je vyplé", delete_after=5)
        else:
            collection.update_one(data, prace)
            await ctx.send(f"Přivítání je vyplé")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def vitej_on(self, ctx):
        guild = ctx.guild.id
        collection = db["vitej_data"]
        data = collection.find_one({"_id": guild})
        prace = {"$set": {"vitej_stav": "On"}}
        kanal = data["vitej_kanal"]
        test = self.client.get_channel(kanal)
        if (data["vitej_stav"]) == "On":
            await ctx.send("Přivítání už je zaplé", delete_after=5)
        else:
            collection.update_one(data, prace)
            await ctx.send(f"Přivítání je zaplé v kanálu {test}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def bye_off(self, ctx):
        guild = ctx.guild.id
        collection = db["vitej_data"]
        data = collection.find_one({"_id": guild})
        prace = {"$set": {"bye_stav": "Off"}}
        if (data["bye_stav"]) == "Off":
            await ctx.send("Přivítání už je vyplé", delete_after=5)
        else:
            collection.update_one(data, prace)
            await ctx.send(f"Přivítání je vyplé")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def bye_on(self, ctx):
        guild = ctx.guild.id
        collection = db["vitej_data"]
        data = collection.find_one({"_id": guild})
        prace = {"$set": {"bye_stav": "On"}}
        kanal = data["bye_kanal"]
        test = self.client.get_channel(kanal)
        if (data["bye_stav"]) == "On":
            await ctx.send("Přivítání už je zaplé", delete_after=5)
        else:
            collection.update_one(data, prace)
            await ctx.send(f"Přivítání je zaplé v kanálu {test}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def vitej_delete(self, ctx):
        guild = ctx.guild.id
        collection = db["vitej_data"]
        data = collection.find_one({"_id": guild})
        collection.delete_one(data)
        await ctx.send(f"Databáze pro kanály pro server {ctx.guild.name} je smazána!")

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["vs"])
    async def vitej_status(self, ctx):
        jmeno = ctx.guild.id
        collection = db["vitej_data"]
        data = collection.find_one({"_id": jmeno})

        vitej_stav = data["vitej_stav"]
        vitej_kanal = data["vitej_kanal"]
        bye_stav = data["bye_stav"]
        bye_kanal = data["bye_kanal"]

        vitej = self.client.get_channel(vitej_kanal)
        byee = self.client.get_channel(bye_kanal)

        embed = discord.Embed(title="", color=0xc800ff)
        embed.add_field(name="Přivítací kanál je:", value=f"**{vitej}**", inline=False)
        embed.add_field(name="Přivítání je:", value=f"{vitej_stav}", inline=False)
        embed.add_field(name="Rozloučení je v kanálu:", value=f"**{byee}**", inline=False)
        embed.add_field(name="Rozloučení je:", value=f"{bye_stav}", inline=False)
        embed.set_author(name="Oznámení", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.set_footer(text="S pozdravem Bond <33", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        await ctx.channel.send(embed=embed, delete_after=25)


    @ssmaz.error
    @smaz.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.channel.send("Musíš mít roli BondAdmin!!", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Zadej číslo!")
    
    @vitej.error
    @vitej_delete.error
    @vitej_status.error
    @vitej_on.error
    @vitej_off.error
    @bye.error
    @bye_on.error
    @bye_off.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Na tohle má práva jen admin!")
    
    @zmenaprefixu.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Na změnu prefixu má práva jen Admin!!")
    
    
def setup(client):
    client.add_cog(admin(client))
