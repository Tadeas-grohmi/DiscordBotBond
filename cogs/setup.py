# Created by Tada at 13.5.2021
import asyncio

import discord
import time
import random
import datetime
from discord.ext import commands


class start(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def helpsetup(self, ctx):
        embed = discord.Embed(colour=0x0091ff,title="Co všechno chceš udělat?", description="**fullsetup**- udělá welcome a bye roomku, slouží k uvítaní nových lidí\n **rolesetup**- vytvoří pouze roli BondAdmin, která slouží k různým příkazům")
        embed.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        await ctx.send(embed=embed, delete_after=120)

    @commands.command()
    @commands.cooldown(1, 99999999999999999999999999999999999999999999999999999999999999*99999999999999999999999999999999999999999999999999, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def fullsetup(self, ctx):
        await ctx.send("Právě probíhá set up bota!")
        await asyncio.sleep(1)

        guild = ctx.guild
        prava = {guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=True), guild.me: discord.PermissionOverwrite(send_messages=True)}
        await guild.create_text_channel("welcome", topic= "Kanál na přivítání nových lidí", overwrites=prava)
        await guild.create_text_channel("bye", topic="Kanál kde se ukáže jaká pepega to leavnula!", overwrites=prava)
        await guild.create_role(name="BondAdmin", colour=discord.Colour(0x0091ff))

        await ctx.send("Setup proběhl bez problémů!")
        await asyncio.sleep(0.5)
        embed = discord.Embed(colour=0x0091ff,title="Co k čemu je?", description="**welcome** roomka slouží k uvítání nových lidí na server\n **bye** roomka slouží k rozloučení se s lidma co odešli\n **BondAdmin** role slouží k ovládání commandů jako:\ntempmute, mute, serverstatus, zmenaprefixu")
        embed.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.add_field(name="To je ode mě vše :smile:", value="ted už jen napiš !!pomoc a uvidíš co všechno umím :smile: ",inline=False)
        await ctx.send(embed=embed, delete_after=120)

    @commands.command()
    @commands.cooldown(1, 99999999999999999999999999999999999999999999999999999999999999*99999999999999999999999999999999999999999999999999, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def rolesetup(self, ctx):
        await ctx.send("Právě probíhá set up bota!")
        await asyncio.sleep(1)

        guild = ctx.guild
        await guild.create_role(name="BondAdmin", colour=discord.Colour(0x0091ff))

        await ctx.send("Setup proběhl bez problémů!")
        await asyncio.sleep(0.5)
        embed = discord.Embed(colour=0x0091ff,title="Co k čemu je?", description="**BondAdmin** role slouží k ovládání commandů jako:\ntempmute, mute, serverstatus, zmenaprefixu\n Kdybys chtěl/a dodatečně uvítací kanál, stačí vytvořit kanál se jménem **welcome** a **bye**\n Kdyžtak je to v adminhelp")
        embed.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.add_field(name="To je ode mě vše :smile:", value="ted už jen napiš !!pomoc a uvidíš co všechno umím :smile: ",inline=False)
        await ctx.send(embed=embed, delete_after=120)




    @fullsetup.error
    @rolesetup.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            print("Lmao setup")
            await ctx.send("Tohle můžeš jenom jednou..")

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Tohle může jenom admin!")



def setup(client):
    client.add_cog(start(client))
