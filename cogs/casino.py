# Created by Tada at 20.5.2021
import discord
import time
import random
import datetime
from pymongo import MongoClient
import certifi
import asyncio
from utils.ruleta.ruleta_barvy import ruleta_barva_passer
from discord.ext import commands
from utils.utils import zapis
from utils.tajne import Mongo

mango_url = Mongo()
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["DiscordCasinoPenize"]


class casino(commands.Cog):

    def __init__(self, client):
        self.client = client

    """ 
    Samotné casino zde 
    """

    @commands.command(aliases=["Sloty", "Slot", "slot"])
    @commands.cooldown(1, 4, commands.BucketType.member)
    async def sloty(self, ctx, sazka:int = None):
        member = ctx.author
        jmeno = str(ctx.guild.id)
        collection = db[jmeno]
        data = collection.find_one({"_id": member.id})

        if sazka == None:
            await ctx.send("Musíš napsat kolik chceš vsadit!")
            return
        if sazka < 25:
            await ctx.send("Minimální částka je 25$!")
            return
        else:
            if sazka > int(data["cash"]):
                await ctx.send("Nemáš tolik peněz")
                return
            if sazka < 0:
                await ctx.send("Sázka musí být větší než 0")
                return

        final = []
        for i in range(3):
            a = random.choice(["🍇", "👑", "🎟", "💎", "7️⃣", "❤", "🍒", "🍓"])
            final.append(a)

        embed1 = discord.Embed(title=f"Roztáčím automat {ctx.author.name}", description="Hodně štestí!!",colour=discord.Colour.random())
        embed1.set_thumbnail(url="https://image.freepik.com/free-vector/slot-machine-poster_1284-18890.jpg")
        embed1.set_footer(text=f"Pro: {ctx.author.name}", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        msg = await ctx.send(embed=embed1)
        await asyncio.sleep(1.3)
        emoji1 = final[0]
        emoji2 = final[1]
        emoji3= final[2]
        if final[0] == final[1] == final[2]:
            vyhra = sazka * 8
            sloty = {"$inc": {"cash": vyhra}}
            collection.update_one(data, sloty)
            cash = int(data["cash"]) + vyhra
            slotembed = discord.Embed(title=f"{ctx.author.name} Tady je tvoje hra", colour=discord.Colour.random())
            slotembed.add_field(name="Tvoje sloty jsou:", value=f">{emoji1}<  >{emoji2}<  >{emoji3}<")
            slotembed.add_field(name=f"Hezky pěkně {ctx.author.name} vyhrál jsi mega vyhru {vyhra}$", value=f"Nyní máš v šrajtofli {cash}$", inline=False)
            slotembed.set_thumbnail(url="https://image.freepik.com/free-vector/slot-machine-poster_1284-18890.jpg")
            slotembed.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=slotembed)

        elif final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
            vyhra = sazka * 3 - sazka
            sloty = {"$inc": {"cash": vyhra}}
            collection.update_one(data, sloty)
            cash1 = int(data["cash"]) + vyhra
            slotembed = discord.Embed(title=f"{ctx.author.name} Tady je tvoje hra", colour=discord.Colour.random())
            slotembed.add_field(name="Tvoje sloty jsou:", value=f">{emoji1}<  >{emoji2}<  >{emoji3}<")
            slotembed.add_field(name=f"Hezky pěkně {ctx.author.name} vyhrál jsi {vyhra}", value=f"Nyní máš v šrajtofli {cash1}$", inline=False)
            slotembed.set_thumbnail(url="https://image.freepik.com/free-vector/slot-machine-poster_1284-18890.jpg")
            slotembed.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=slotembed)
        else:
            sloty = {"$inc": {"cash": -sazka}}
            collection.update_one(data, sloty)
            cash2 = int(data["cash"]) - sazka
            slotembed = discord.Embed(title=f"{ctx.author.name} Tady je tvoje hra", colour=discord.Colour.random())
            slotembed.add_field(name="Tvoje sloty jsou:", value=f">{emoji1}<  >{emoji2}<  >{emoji3}<")
            slotembed.add_field(name=f"Bohužel si prohrál {sazka}", value=f"Haha ted máš jenom {cash2}$ v šrajtofli", inline=False)
            slotembed.set_thumbnail(url="https://image.freepik.com/free-vector/slot-machine-poster_1284-18890.jpg")
            slotembed.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=slotembed)
        await zapis("sloty")
        
    @commands.command(aliases=["Kostka", "Kostky", "kostky"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def kostka(self, ctx, sazka:int=None, cislo:int=None):
        member = ctx.author
        jmeno = str(ctx.guild.id)
        collection = db[jmeno]
        data = collection.find_one({"_id": member.id})
        if sazka == None:
            await ctx.send("Musíš napsat kolik chceš vsadit!")
            return
        if sazka < 25:
            await ctx.send("Minimální částka je 25$!")
            return
        if cislo == None:
            await ctx.send("Napiš na jaký číslo chceš vsadit!")
            return
        if cislo > 6:
            await ctx.send("Maximálně se může hodit 6!")
            return
        else:
            if sazka > int(data["cash"]):
                await ctx.send("Nemáš tolik peněz")
                return
            if sazka < 0:
                await ctx.send("Sázka musí být větší než 0")
                return
            if cislo < 0:
                await ctx.send("Číslo musí být větší než 0!")
                return
        kostka = discord.Embed(title=f"Hazím kostkou {ctx.author.name}", colour=0xff0000)
        kostka.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1024px-Two_red_dice_01.svg.png")
        kostka.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        msg = await ctx.send(embed=kostka)
        await asyncio.sleep(1)
        cislo_bot= random.randint(1,6)
        if cislo_bot == cislo:
            vyhra = sazka*5
            kostka = {"$inc": {"cash": vyhra}}
            collection.update_one(data, kostka)
            kostka = discord.Embed(title="Hod kostkou", description=f"**Tvoje číslo: {cislo}**\n **Můj hod: {cislo_bot}**\n Hezky {ctx.author.name} trefil ses \n Vyhráváš {vyhra}$", colour=0xff0000)
            kostka.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1024px-Two_red_dice_01.svg.png")
            kostka.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=kostka)
        else:
            kostka = {"$inc": {"cash": -sazka}}
            collection.update_one(data, kostka)
            kostka = discord.Embed(title="Hod kostkou", description=f"**Tvoje číslo: {cislo}**\n **Můj hod: {cislo_bot}**\n Bohužel {ctx.author.name} netrefil ses \n Seš o {sazka}$ lehčí", colour=0xff0000)
            kostka.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1024px-Two_red_dice_01.svg.png")
            kostka.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=kostka)
        await zapis("kostka")

    @commands.command(aliases=["Doublekostka", "Dvojhod"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def doublekostka(self, ctx, sazka:int=None, cislo:int=None):
        member = ctx.author
        jmeno = str(ctx.guild.id)
        collection = db[jmeno]
        data = collection.find_one({"_id": member.id})
        if sazka == None:
            await ctx.send("Musíš napsat kolik chceš vsadit!")
            return
        if sazka < 10:
            await ctx.send("Minimální částka je 10$!")
            return
        if cislo == None:
            await ctx.send("Napiš na jaký číslo chceš vsadit!")
            return
        if cislo > 12:
            await ctx.send("Maximálně se může hodit 6!")
            return
        else:
            if sazka > int(data["cash"]):
                await ctx.send("Nemáš tolik peněz")
                return
            if sazka < 0:
                await ctx.send("Sázka musí být větší než 0")
                return
            if cislo < 0:
                await ctx.send("Číslo musí být větší než 0!")
                return

        doublekostka = discord.Embed(title="Woooouuu máme tu double hod", description=f"Tak si jdem pořádně zahrát {ctx.author.name}\nHazím kostku..", colour=0xff0000)
        doublekostka.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1024px-Two_red_dice_01.svg.png")
        doublekostka.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        msg = await ctx.send(embed=doublekostka)
        await asyncio.sleep(1)
        hod1= random.randint(1,6)
        hod2 = random.randint(1,6)
        bot_celk = hod1 + hod2
        if cislo == bot_celk:
            vyhra = sazka*20
            doublekostka = {"$inc": {"cash": vyhra}}
            collection.update_one(data, doublekostka)
            doublekostka = discord.Embed(title="A kostka dopadla",description=f"A výsledky jsou:", colour=0xff0000)
            doublekostka.add_field(name=f"Tvoje číslo je:", value=f"{cislo}", inline=False)
            doublekostka.add_field(name="Můj první hod:", value=f"{hod1}", inline=True)
            doublekostka.add_field(name="Můj druhý hod:", value=f"{hod2}", inline=True)
            doublekostka.add_field(name="Můj celkový počet tedy je:", value=f"{bot_celk}", inline=True)
            doublekostka.add_field(name=f"no nekecej {ctx.author.name} ty jsi vyhrál :partying_face: ", value=f"Užívej svojí výhru v hodnotě {vyhra}$", inline=True)
            doublekostka.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1024px-Two_red_dice_01.svg.png")
            doublekostka.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=doublekostka)
        else:
            doublekostka = {"$inc": {"cash": -sazka}}
            collection.update_one(data, doublekostka)
            doublekostka = discord.Embed(title="A kostka dopadla",description=f"A výsledky jsou:", colour=0xff0000)
            doublekostka.add_field(name=f"Tvoje číslo je:", value=f"{cislo}", inline=False)
            doublekostka.add_field(name="Můj první hod:", value=f"{hod1}", inline=True)
            doublekostka.add_field(name="Můj druhý hod:", value=f"{hod2}", inline=True)
            doublekostka.add_field(name="Můj celkový počet tedy je:", value=f"{bot_celk}", inline=True)
            doublekostka.add_field(name=f"Bohužel jsi nic nevyhrál, zkus to příště", value=f"A taky si přišel o {sazka}$", inline=True)
            doublekostka.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Two_red_dice_01.svg/1024px-Two_red_dice_01.svg.png")
            doublekostka.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=doublekostka)
        await zapis("doublekostka")

    @commands.command(aliases=["Ruleta"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def ruleta(self, ctx,sazka:int=None, barva:ruleta_barva_passer=None , cislo:int=None):
        member = ctx.author
        jmeno = str(ctx.guild.id)
        collection = db[jmeno]
        data = collection.find_one({"_id": member.id})
        if sazka == None:
            await ctx.send("Musíš napsat kolik chceš vsadit!")
            return
        if cislo == None:
            await ctx.send("Zadej na jaký číslo chceš vsadit!")
            return
        if sazka < 10:
            await ctx.send("Minimální částka je 10$!")
            return
        if cislo > 36:
            await ctx.send("Maximální číslo je 36!")
            return
        if cislo < 1:
            await ctx.send("Číslo musí být větší než 0!")
            return
        else:
            if sazka > int(data["cash"]):
                await ctx.send("Nemáš tolik peněz")
                return
            if sazka < 0:
                await ctx.send("Sázka musí být větší než 0")
                return

        ruleta = discord.Embed(title=f"Roztáčím ruletu {ctx.author.name}", colour=0xff0240)
        ruleta.set_thumbnail(url="https://www.sazka.cz/SazkaWeb/media/content/Online%20hry/French%20Roulette/french_roulette-350x280@2x.jpg?ext=.jpg")
        ruleta.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
        msg = await ctx.send(embed=ruleta)
        await asyncio.sleep(1)

        hrac_barva = barva.choice
        cislo_barva = random.randint(0, 1)
        barva_bota = "cerna" if cislo_barva == 1 else "cervena"
        cislo_bota = random.randint(1, 36)

        if cislo == cislo_bota and hrac_barva == barva_bota:
            vyhra = sazka*25
            ruleta = {"$inc": {"cash": vyhra}}
            collection.update_one(data, ruleta)

            ruleta = discord.Embed(title=f"A ruleta se dotočila {ctx.author.name}\nA výsledky jsou", colour=0xff0240)
            ruleta.add_field(name=f"Vsadil sis na:", value=f"{hrac_barva}", inline=True)
            ruleta.add_field(name=f"A vsadil sis na:", value=f"{cislo}", inline=True)
            ruleta.add_field(name=f"A vsadil jsi:", value=f"{sazka}$", inline=True)
            ruleta.add_field(name="A padla:", value=f"{barva_bota}", inline=True)
            ruleta.add_field(name="A číslo je:", value=f"{cislo_bota}", inline=True)
            ruleta.add_field(name="JACKPOT :partying_face:", value=f"Vyhrál jsi na číslo a na barvu zároven", inline=True)
            ruleta.add_field(name="Tvá šrajtofle je o:", value=f"**{vyhra}$** težší",inline=True)
            ruleta.set_thumbnail(url="https://www.sazka.cz/SazkaWeb/media/content/Online%20hry/French%20Roulette/french_roulette-350x280@2x.jpg?ext=.jpg")
            ruleta.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=ruleta)

        elif barva_bota == hrac_barva:
            vyhra = sazka*2 -sazka

            ruleta = discord.Embed(title=f"A ruleta se dotočila {ctx.author.name}\nA výsledky jsou", colour=0xff0240)
            ruleta.add_field(name=f"Vsadil sis na:", value=f"{hrac_barva}", inline=True)
            ruleta.add_field(name=f"A vsadil sis na:", value=f"{cislo}", inline=True)
            ruleta.add_field(name=f"A vsadil jsi:", value=f"{sazka}$", inline=True)
            ruleta.add_field(name="A padla:", value=f"{barva_bota}", inline=True)
            ruleta.add_field(name="A číslo je:", value=f"{cislo_bota}", inline=True)
            ruleta.add_field(name="Hezky", value=f"Vyhrál jsi jenom na barvu", inline=True)
            ruleta.add_field(name="Tvá šrajtofle je o:", value=f"**{vyhra}$** težší",inline=True)
            ruleta.set_thumbnail(url="https://www.sazka.cz/SazkaWeb/media/content/Online%20hry/French%20Roulette/french_roulette-350x280@2x.jpg?ext=.jpg")
            ruleta.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=ruleta)

        elif cislo == cislo_bota:
            vyhra = sazka*4 -sazka
            ruleta = {"$inc": {"cash": vyhra}}
            collection.update_one(data, ruleta)

            ruleta = discord.Embed(title=f"A ruleta se dotočila {ctx.author.name}\nA výsledky jsou", colour=0xff0240)
            ruleta.add_field(name=f"Vsadil sis na:", value=f"{hrac_barva}", inline=True)
            ruleta.add_field(name=f"A vsadil sis na:", value=f"{cislo}", inline=True)
            ruleta.add_field(name=f"A vsadil jsi:", value=f"{sazka}$", inline=True)
            ruleta.add_field(name="A padla:", value=f"{barva_bota}", inline=True)
            ruleta.add_field(name="A číslo je:", value=f"{cislo_bota}", inline=True)
            ruleta.add_field(name="Hezky", value=f"Vyhrál jsi jenom na číslo", inline=True)
            ruleta.add_field(name="Tvá šrajtofle je o:", value=f"**{vyhra}$** težší",inline=True)
            ruleta.set_thumbnail(url="https://www.sazka.cz/SazkaWeb/media/content/Online%20hry/French%20Roulette/french_roulette-350x280@2x.jpg?ext=.jpg")
            ruleta.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=ruleta)

        else:
            ruleta = {"$inc": {"cash": -sazka}}
            collection.update_one(data, ruleta)

            ruleta = discord.Embed(title=f"A ruleta se dotočila {ctx.author.name}\nA výsledky jsou", colour=0xff0240)
            ruleta.add_field(name=f"Vsadil sis na:", value=f"{hrac_barva}", inline=True)
            ruleta.add_field(name=f"A vsadil sis na:", value=f"{cislo}", inline=True)
            ruleta.add_field(name=f"A vsadil jsi:", value=f"{sazka}$", inline=True)
            ruleta.add_field(name="A padla:", value=f"{barva_bota}", inline=True)
            ruleta.add_field(name="A číslo je:", value=f"{cislo_bota}", inline=True)
            ruleta.add_field(name="Bohužel nic nepadlo", value=f"Prohrál jsi vše", inline=True)
            ruleta.add_field(name="Tvá šrajtofle je o:", value=f"**{sazka}$** lehčí",inline=True)
            ruleta.set_thumbnail(url="https://www.sazka.cz/SazkaWeb/media/content/Online%20hry/French%20Roulette/french_roulette-350x280@2x.jpg?ext=.jpg")
            ruleta.set_footer(text=f"Pro: {ctx.author.name}",icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            await msg.edit(embed=ruleta)
            await zapis("ruleta")
            
            
    @commands.command()
    async def board(self, ctx):
        jmeno = str(ctx.guild.id)
        baze = db[jmeno]
        cash = baze.find().sort("cash", -1)
        banka = baze.find().sort("banka", -1)
        i = 1
        b = 1
        embed = discord.Embed(title="Leaderboard peněz:", colour=discord.colour.Colour.gold())
        embed.set_footer(text=f"Pro: {ctx.author}")
        embed.add_field(name="Peníze v peněžence:", value="-------------------------")
        for l in cash:
            try:
                penize = l["cash"]
                jmeno = ctx.guild.get_member(l["_id"])
                embed.add_field(name=f"{b}: {jmeno.name}", value=f"Prachy v peněžence: {penize}$",inline=False)
                b += 1
            except:
                pass
            if b == 11:
                break
        embed.add_field(name="Peníze v bance:", value="-------------------------", inline=False)
        for x in banka:
            try:
                temp = ctx.guild.get_member(x["_id"])
                banka = x["banka"]
                embed.add_field(name=f"{i}: {temp.name}", value=f"Prachy v bance: {banka}$", inline=False)
                i += 1
            except:
                pass;
            if i == 11:
                break
        await ctx.send(embed=embed)

    @ruleta.error
    @sloty.error
    @kostka.error
    @doublekostka.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            zprava = ("Klídek ty koště " + ctx.author.mention + " command použij znova za {:.1f}".format(error.retry_after))
            await ctx.send(zprava)
    
    @kostka.error
    @doublekostka.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Asi si to napsal blbě, zkus to ještě jednou- kostka <sazka> <cislo>")

    @ruleta.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Asi si to napsal blbě, zkus to ještě jednou- ruelta <sázka> <barva (černáxčervená)> <číslo na ruletě>")

def setup(client):
    client.add_cog(casino(client))
