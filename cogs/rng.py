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

from discord.ext import commands


class gamble(commands.Cog):

    def __init__(self, client):
        self.client = client




    @commands.command()
    async def mince(self, ctx):
        cislo = random.randint(0, 1)
        zprava = "Hlava" if cislo == 1 else "Orel"
        barva = random.randint(0, 0xffffff)
        embed = discord.Embed(title="Hod mincí", description=f"**Mince dopadla na: {zprava}**", colour=barva)
        embed.set_thumbnail(url="https://st2.depositphotos.com/5624298/11071/i/600/depositphotos_110715036-stock-photo-hand-tossing-a-euro-coin.jpg")
        embed.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        await ctx.send(embed=embed)


    @commands.command()
    async def rng(self, ctx, konec: int = 100):
        rng= random.randrange(1, konec)
        barva = random.randint(0, 0xffffff)
        embed = discord.Embed(title="**RNG**", description=f"**Vybírám random číslo od 1 do {konec}** \n **Tvé je: {rng}**", colour=barva)
        embed.set_thumbnail(url="https://images.squarespace-cdn.com/content/v1/5d66e96e2d579f000145f966/1569874042442-LHN4KRFSU9CFEFT28C7R/ke17ZwdGBToddI8pDm48kDHPSfPanjkWqhH6pl6g5ph7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0mwONMR1ELp49Lyc52iWr5dNb1QJw9casjKdtTg1_-y4jz4ptJBmI9gQmbjSQnNGng/rng.jpg?format=1000w")
        embed.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(gamble(client))