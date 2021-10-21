# Created by Tada at 5.5.2021
import asyncio

import discord
import time
import random
import datetime

from utils.cas import time_since
from discord.ext import commands

vibes = open("./files/vibes.txt").readlines()
vibegif = open("./files/vibegif.txt").readlines()

class pomoc(commands.Cog):

    def __init__(self, client):
        self.client = client

    player = {}


    @commands.command(aliases=["Pomoc", "Help", "help"])
    async def pomoc(self, ctx):
        first_run = True
        while True:
            if first_run:
                page1 = discord.Embed(title="Základní prefix je !! a $",
                                      description="\n**Základní příkazy:**"
                                                  " \n prefix- ukáže prefix na serveru :man_shrugging:"
                                                  " \n pp- změří vaše pele :eggplant:"
                                                  " \n gay <kdo>- prostě je to gay :rainbow_flag:"
                                                  " \n vtip/joke- řekne random vtip(vtip-česky, joke-anglicky) :joy: "
                                                  " \n idc- když někdo poslal nějakou kravinu :sunglasses:"
                                                  " \n kdoje <@...> - Informace o dané osobě :face_with_monocle:"
                                                  " \n admin- ukáže admin příkazy :crown:"
                                      , color=0x007bff)
                page1.set_author(name="Příkazy pro Bonda", url="https://www.youtube.com/watch?v=esX7SFtEjHg",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page1.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page1.set_thumbnail(url="https://cdn.discordapp.com/attachments/586526210469789717/839401032719138816/8850_peepoHappyLove.png")

                first_run = False
                msg = await ctx.send(embed=page1)
                reactmoji = ["🤖", "😂", "🎧", "📖", "🎰","🤏", "❌"]
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
            elif '🤖' in str(res.emoji):
                await msg.remove_reaction("🤖", user)
                await msg.edit(embed=page1, delete_after=60)

            elif '😂' in str(res.emoji):
                page2 = discord.Embed(title="**Příkazy pro reddit**",
                                      description=
                                          " \n haha- post černýho humoru :grimacing:"
                                          " \n duklock- post z dušanova redditu :rofl:"
                                          " \n down- pošle post z bendrova dead redditu :zany_face:"
                                          " \n nsfw- trochu NSFW příkazů :underage: "
                                      , color=0x007bff)
                page2.set_author(name="Příkazy pro Bonda", url="https://www.youtube.com/watch?v=esX7SFtEjHg",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page2.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page2.set_thumbnail(url="https://cdn.discordapp.com/attachments/586526210469789717/839401032719138816/8850_peepoHappyLove.png")
                await msg.remove_reaction("😂", user)
                await msg.edit(embed=page2, delete_after=60)

            elif '🎧' in str(res.emoji):
                page3 = discord.Embed(title="**Všechny příkazy spojený s hudbou**",
                                      description=
                                          " \n**Hudba:**"
                                          " \n napoj- napojí se do voicu :robot:"
                                          " \n hraj- pustí song z jména nebo url :musical_note:"
                                          " \n pauza/pokracuj- zastaví song, pokračuje dál v songu"
                                          " \n skip- skipne song v frontě"
                                          " \n stop- stopne hudbu, aby jste si mohli pustit další :mute:"
                                          " \n volume- změní volume :sound:"
                                          " \n padej- odpojí kamaráda z vc :mute:"
                                          " \n fronta- ukáže frontu"
                                          " \n loop- zapne/vypne loop právě hrané songu"
                                          " \n np- úkáže co právě hraju"
                                          "\n**Rádio:**"
                                          " \n evropa2- pustí evropu 2 :headphones:"
                                          " \n kiss- pustí kiss :notes:"
                                          " \n beat- pustí radio beat :notes:"
                                      , color=0x007bff)
                page3.set_author(name="Příkazy pro Bonda", url="https://www.youtube.com/watch?v=esX7SFtEjHg",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page3.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page3.set_thumbnail(url="https://cdn.discordapp.com/attachments/586526210469789717/839401032719138816/8850_peepoHappyLove.png")
                await msg.remove_reaction("🎧", user)
                await msg.edit(embed=page3, delete_after=60)

            elif '📖' in str(res.emoji):

                page4 = discord.Embed(title="**Ostatní příkazy**",
                                      description=
                                          "\n**Počasí:** "
                                          " \n počasí <město> - ukáže jaký je počasí :beach:"
                                          " \n fullpočasí <město> - tryhard verze počasí :satellite_orbital:"
                                          " \n **Chatbot**"
                                          " \n chatbot - ukáže v jakém kanále je nastaven"
                                          " \n chatbot_setup <kanál> - setup chatbota do daného kanálu"
                                          " \n chatbot_delete - smaže/ vypne chatbota"
                                          "\n**Ostatní:**"
                                          " \n mince- hodí mincí :coin:"
                                          " \n rng (číslo)- random číslo (základní číslo je 100) :infinity: "
                                          " \n report <problém> - pošlě report o nějakém problému"
                                      , color=0x007bff)
                page4.set_author(name="Příkazy pro Bonda", url="https://www.youtube.com/watch?v=esX7SFtEjHg",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page4.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page4.set_thumbnail(url="https://cdn.discordapp.com/attachments/586526210469789717/839401032719138816/8850_peepoHappyLove.png")
                await msg.remove_reaction("📖", user)
                await msg.edit(embed=page4, delete_after=60)
                
            elif '🎰' in str(res.emoji):

                page4 = discord.Embed(title="**Příkazy na casino**",
                                      description=
                                          " \n peníze- ukáže váš účet "
                                          " \n vybrat <kolik> - vybere peníze"
                                          " \n vlozit <kolik> - vloží peníze"
                                          " \n dát <komu> - dá dané osobě peníze"
                                          " \n prace - jdem pracovat!"
                                          " \n kurva - no, prostě taková malá službička"
                                          " \n sloty <sázka> - zatočí automatem"
                                          " \n kostka <sázka> <číslo> - "
                                          " \n doublekostka <sázka> <číslo>- "
                                          " \n ruleta <sázka> <barva> <číslo>- "
                                      , color=0x007bff)
                page4.set_author(name="Příkazy pro Bonda", url="https://www.youtube.com/watch?v=esX7SFtEjHg",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page4.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                page4.set_thumbnail(url="https://cdn.discordapp.com/attachments/586526210469789717/839401032719138816/8850_peepoHappyLove.png")
                await msg.remove_reaction("🎰", user)
                await msg.edit(embed=page4, delete_after=60)

            elif '🤏' in str(res.emoji):
                zkratky = discord.Embed(title="Všechny zkratky ke příkazům:",
                                      description="\n**Základní příkazy:**"
                                                  " \n pp- PP, pele, PELE, perko"
                                                  " \n idc- IDC"
                                                  " \n serverstatus- stats, Stats, Sstats"
                                                  " \n kdoje <@...> - Kdoje"
                                                  "\n**Reddit:**"
                                                  " \n duklock- Duklock, duklok, Duklok"
                                                  "\n**Rádio:**"
                                                  " \n evropa2- e2, E2"
                                                  " \n kiss- Kiss"
                                                  " \n beat- Beat, BigBeat"
                                                  "\n**Hudba:**"
                                                  " \n hraj- Streamuj"
                                                  "\n**Počasí:** "
                                                  " \n počasí <město> - pocasi"
                                                  " \n fullpočasí <město> - fullpocasi"
                                      , color=0x007bff)
                zkratky.set_author(name="Příkazy pro Bonda", url="https://www.youtube.com/watch?v=esX7SFtEjHg",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                zkratky.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                zkratky.set_thumbnail(url="https://media1.tenor.com/images/67164b3656353e10806740c021b37cf6/tenor.gif")
                await msg.remove_reaction("🤏", user)
                await msg.edit(embed=zkratky, delete_after=60)

            elif '❌' in str(res.emoji):
                cs = discord.Embed(title="Tak se měj hezky <33"
                                      , color=0x007bff)
                cs.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
                await msg.remove_reaction("❌", user)
                await msg.edit(embed=cs, delete_after=1)

    @commands.command(aliases=["Admin"])
    @commands.has_permissions(administrator=True)
    async def admin(self, ctx):
        embed = discord.Embed(title="Admin příkazy:",
                              description=" \n **Tyto příkazy :arrow_down: můžou použít jen admini!**"
                                          " \n zmenaprefixu- změní prefix dle vaší libosti"
                                          " \n zakladniprefix- změní zpět prefix na !! a $"
                                          " \n vitej <kanál>- zde budete dostávat oznámení o nových lidí"
                                          " \n bye <kanál>- zde budete dostávat oznámení o lidech, co to leavnuli"
                                          " \n vitej on/off- no vypnutí a zapnutí oznámení.."
                                          " \n bye on/off- no vypnutí a zapnutí oznámení.."
                                          " \n **Na tyto příkazy :arrow_down:  je potřeba role BondAdmin!**"
                                          " \n smaz <číslo>- smaže vámi zadaný počet zpráv"
                                          " \n tempmute- in progres..."
                                          " \n mute- in progress..."
                                          " \n unmute- in progress..."
                                          " \n inv- in progress..."
                                          ,color=0x007bff)
        embed.set_author(name="Příkazy pro Bonda", url="https://www.youtube.com/watch?v=esX7SFtEjHg",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/essentials-volume-3/128/crown-512.png")
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["NSFW"])
    @commands.is_nsfw()
    async def nsfw(self, ctx):
        embed = discord.Embed(title="NSFW příkazy:",
                              description=" \n pecko- klasické porno :underage:"
                                          " \n hentai- hentai :underage:"
                                          " \n lolhentai- lolko hentai :underage:"
                                          " \n valohentai- valorant hentai :underage:"
                                          " \n overhentai- overwatch hentai :underage:"
                                          ,color=0x007bff)
        embed.set_author(name="Příkazy pro Bonda", url="https://www.youtube.com/watch?v=esX7SFtEjHg",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.set_footer(text="S pozdravem Bond <33",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Pornhub-logo.svg/1280px-Pornhub-logo.svg.png")
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["vlist", "vibe", "Vibe", "Vibelist"])
    async def vibelist(self, ctx):
        embed = discord.Embed(title="Best 24/7 streamy <3", color=0xc800ff)
        embed.add_field(name="24/7 HipHop", value="https://www.youtube.com/watch?v=5qap5aO4i9A", inline=False)
        embed.add_field(name="24/7 Chill/programing", value="https://www.youtube.com/watch?v=esX7SFtEjHg", inline=False)
        embed.add_field(name="24/7 House/Chill", value="https://www.youtube.com/watch?v=I83XWCSBgSc", inline=False)
        embed.set_author(name="Příkazy pro Bonda", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.set_footer(text="S pozdravem Bond <33", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.set_thumbnail(url=random.choice(vibes))
        await ctx.channel.send(embed=embed, delete_after=25)

    @commands.command(aliases= ["Sstatus", "Sstats", "Statistiky", "stats", "Stats"])
    async def serverstatus(self, ctx, *args):
        guild = ctx.guild
        no_voice_channels = len(guild.voice_channels)
        no_text_channels = len(guild.text_channels)
        role = len(guild.roles)
        emoji = len(guild.emojis)
        created = time_since(ctx.guild.created_at, precision="hodinami")
        embed = discord.Embed(description="**Status serveru**:",
                              colour=discord.Colour.dark_purple())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        emoji_string = ""
        for e in guild.emojis:
            if e.is_usable():
                emoji_string += str(e)
        embed.add_field(name="Jméno serveru:", value=guild.name, inline=True)
        embed.add_field(name="Založení serveru:", value="Před " + created, inline=False)
        embed.add_field(name="Custom emoji:",
                        value=emoji or "Žádne custom emoji :((", inline=False)
        embed.add_field(name="Voice kanály:", value=f"{no_voice_channels}", inline=True)
        embed.add_field(name="Textové kanály:", value=f"{no_text_channels}", inline=True)
        embed.add_field(name="AFK kanály:", value=guild.afk_channel, inline=True)
        embed.add_field(name="Počet lidí na serveru:", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Počet rolí na serveru:", value=f"{role}", inline=True)
        #embed.set_author(name=self.client.user.name)
        cas = datetime.datetime.now()
        embed.set_footer(text=f"Pro: {ctx.author.name}" + cas.strftime("%H:%M:%S"), icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=["Kdoje"])
    async def kdoje(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author

        embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                                  title=f"Info o: {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Pro: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        embed.add_field(name="Přezdívka:", value=member.display_name, inline=False)
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Účet vytvořen v:", value=member.created_at.strftime("%a, %d %b %Y %H:%M:%S"),inline=False)
        embed.add_field(name="Na server se připojil:", value=member.joined_at.strftime("%a, %d %b %Y %H:%M:%S"),inline=False)
        embed.add_field(name="Role:", value="".join([role.mention for role in member.roles[1:]]))
        embed.add_field(name="Nejvyšší role:", value=member.top_role.mention, inline=False)
        await ctx.send(embed=embed)



    @admin.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send("Nemáš na to práva ty koště- musíš mít právo na banovaní!")

    @nsfw.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            zprava = ("Tohle si přesuň do NSFW kanálů :kissing_heart:")
            await ctx.send(zprava)


def setup(client):
    client.add_cog(pomoc(client))
