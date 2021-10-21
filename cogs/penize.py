# Created by Tada at 1.9.2021
import discord
import random
import datetime
from pymongo import MongoClient
import certifi
import asyncio
from discord.ext import commands
from utils.utils import zapis
from utils.tajne import Mongo

mango_url = Mongo()
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["DiscordCasinoPenize"]


class penize(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["Penize", "peníze", "Peníze"])
    async def penize(self, ctx, koho: discord.Member = None):
        if koho == None:
            koho = ctx.author
            if not koho.bot:
                jmeno = str(ctx.guild.id)
                collection = db[jmeno]
                data = collection.find_one({"_id": koho.id})
                if data is None:
                    id = koho.id
                    post = {"_id": id, "cash": 250, "banka": 450, "jmeno": koho.display_name}
                    collection.insert_one(post)
                    await ctx.channel.send('Právě jsi vytvořil ůčet, hůrá :partying_face:!')
                else:
                    penezenka_cislo = (data["cash"])
                    banka_cislo = (data["banka"])
                    celk = banka_cislo + penezenka_cislo
                    embed = discord.Embed(title=f"Peníze pana {koho.display_name}",
                                          description=f"**Peněženka :money_with_wings::** {penezenka_cislo}$"
                                                      f"\n**Banka :moneybag::** {banka_cislo}$"
                                                      f"\n**Dohromady :bank::** {celk}$",
                                          timestamp=ctx.message.created_at, colour=discord.Colour.random())
                    embed.set_footer(text=f"Pro: {ctx.author}")
                    await ctx.send(embed=embed)
            else:
                await ctx.send("Boti nemůžou gamblit...")
        else:
            if not koho.bot:
                jmeno = str(ctx.guild.id)
                collection = db[jmeno]
                data = collection.find_one({"_id": koho.id})
                if data is None:
                    id = koho.id
                    post = {"_id": id, "cash": 250, "banka": 450, "jmeno": koho.display_name}
                    collection.insert_one(post)
                    await ctx.channel.send('Právě jsi vytvořil ůčet, hůrá :partying_face:!')
                else:
                    penezenka_cislo = (data["cash"])
                    banka_cislo = (data["banka"])
                    celk = banka_cislo + penezenka_cislo
                    embed = discord.Embed(title=f"Peníze pana {koho.display_name}",
                                          description=f"\n**Banka :moneybag::** {banka_cislo}$"
                                                      f"\n**Dohromady :bank::** {celk}$",
                                          timestamp=ctx.message.created_at, colour=discord.Colour.random())
                    embed.set_footer(text=f"Pro: {ctx.author}")
                    await ctx.send(embed=embed)
            else:
                await ctx.send("Boti nemůžou gamblit...")
        await zapis("penize")

    @commands.command(aliases=["Vlozit", "vložit", "Vložit"])
    async def vlozit(self, ctx, kolik=0):
        if kolik == None:
            await ctx.send("Napiš kolik chceš vybrat ty koště!")
            return
        member = ctx.author
        jmeno = str(ctx.guild.id)
        collection = db[jmeno]
        data = collection.find_one({"_id": member.id})
        if kolik < 1:
            await ctx.send("Minimun na vložení je 1!")
            return
        if kolik > (data["cash"]):
            await ctx.send("Nemáš dostatek peněz ty pepego!")
            return
        else:
            collection.update(data, {"$inc": {
                "banka": kolik,
                "cash": -kolik,
            }})
            await ctx.send(f"{ctx.author.mention} vložil sis {kolik}$")
        await zapis("vlozit")

    @commands.command(aliases=["Vybrat", "výběr", "Výběr"])
    async def vybrat(self, ctx, kolik: int):
        if kolik == None:
            await ctx.send("Napiš kolik chceš vybrat ty koště!")
            return
        member = ctx.author
        jmeno = str(ctx.guild.id)
        collection = db[jmeno]
        data = collection.find_one({"_id": member.id})
        if kolik < 1:
            await ctx.send("Minimun na výběr je 1!")
            return
        if kolik > int(data["banka"]):
            await ctx.send("Nemáš tolik peněz ty peepgo!")
            return
        else:
            collection.update(data, {"$inc": {
                "banka": -kolik,
                "cash": kolik,
            }})
            await ctx.send(f"{ctx.author.mention} vybral sis {kolik}$")
        await zapis("vybrat")

    @commands.command(aliases=["Dat", "Dát", "dát"])
    async def dat(self, ctx, komu: discord.Member = None, *, kolik: int = None):
        if komu == None:
            komu = ctx.author

        if not komu.bot:
            if kolik == None:
                await ctx.send("Napiš kolik chceš dát ty koště!")
                return
            if komu == ctx.author:
                await ctx.send("Proč bys dával sám sobě peníze když už je máš?")
                return
            posilac = ctx.author
            jmeno = str(ctx.guild.id)
            collection = db[jmeno]
            data_odeslani = collection.find_one({"_id": posilac.id})
            data_prijem = collection.find_one({"_id": komu.id})
            if kolik < 1:
                await ctx.send("Minimun na darování je 1!")
                return
            if kolik > int(data_odeslani["cash"]):
                await ctx.send("Nemáš dostatek peněz ty pepego!")
                return
            else:
                collection.update_many(data_prijem, {"$inc": {
                    "cash": kolik,
                }})
                collection.update_many(data_odeslani, {"$inc": {
                    "cash": -kolik,
                }})
                await ctx.send(f"Dal jsi {komu.mention} {kolik}$")
        else:
            await ctx.send("Botům nemůžeš dát peníze")
        await zapis("dat")

    @commands.command(aliases=["Prevod", "Převod", "převod"])
    async def prevod(self, ctx, komu: discord.Member = None, *, kolik: int = None):
        if komu == None:
            komu = ctx.author
        if not komu.bot:
            if kolik == None:
                await ctx.send("Napiš kolik chceš dát ty koště!")
                return
            if komu == ctx.author:
                await ctx.send("Proč bys převáděl sám sobě peníze když už je máš?")
                return
            posilac = ctx.author
            jmeno = str(ctx.guild.id)
            collection = db[jmeno]
            data_odeslani = collection.find_one({"_id": posilac.id})
            data_prijem = collection.find_one({"_id": komu.id})
            if kolik < 1:
                await ctx.send("Minimun na poslání je 1!")
                return
            if kolik > int(data_odeslani["banka"]):
                await ctx.send("Nemáš dostatek peněz ty pepego!")
                return
            else:
                collection.update_many(data_prijem, {"$inc": {
                    "banka": kolik,
                }})
                collection.update_many(data_odeslani, {"$inc": {
                    "banka": -kolik,
                }})
                await ctx.send(f"Poslal jsi {komu.mention} {kolik}$")
        else:
            await ctx.send("Botům nemůžeš poslat peníze")
        await zapis("dat")

    @commands.command(aliases=["Prace", "Práce", "práce"])
    @commands.cooldown(1, 28800, commands.BucketType.member)
    async def prace(self, ctx):
        datum = datetime.datetime.today().strftime("%A")
        datum = datum.lower()
        if datum == "saturday":
            await ctx.send("V sobotu se odpočívá ty koště!")
            await ctx.command.reset_cooldown(ctx)
            return
        if datum == "sunday":
            await ctx.send("V neděli se už vůbec nechodí do práce!!")
            await ctx.command.reset_cooldown(ctx)
            return
        else:
            jmeno = str(ctx.guild.id)
            collection = db[jmeno]
            member = ctx.author
            data = collection.find_one({"_id": member.id})

            msg1 = await ctx.send ("Jdeš do práce")
            msg = await ctx.send("🏭..........🏃.🏡")
            await asyncio.sleep(0.1)
            await msg.edit(content="🏭..........🏃.🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭.........🏃..🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭........🏃...🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭.......🏃....🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭......🏃.....🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭.....🏃......🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭....🏃.......🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭...🏃........🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭..🏃.........🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭.🏃..........🏡")
            await asyncio.sleep(0.25)
            await msg.edit(content="🏭🏃...........🏡")
            await msg1.delete()
            
            reakce = ["⛏", "⚒", "🔨", "⚔", "📱", "💻"]
            prace_emoji = random.choice(reakce)

            await msg.edit(content=f"Už jsi v práci, klikni na {prace_emoji}  aby sis odpracoval svoji část")

            suffleemoji = random.shuffle(reakce)
            for emoji in reakce:
                await msg.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == prace_emoji
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)
            except asyncio.TimeoutError:
                platba = random.randint(150, 350)
                platba_kolik = {"$inc": {"cash": -platba}}
                collection.update_one(data, platba_kolik)
                await ctx.send(f"Máš smůlu, nestihl si šichtu!\n Musíš zaplatit {platba} jako kompenzaci")
                await msg.delete()
            else:
                prace_vydelek = random.randint(120, 650)
                prace = {"$inc": {"cash": prace_vydelek}}
                collection.update_one(data, prace)
                await ctx.send(f"Odpracoval sis svojí část a vydělal sis {prace_vydelek}\nPro dnešek máš padla {ctx.author.mention}!")
                await msg.delete()
        await zapis("prace")

    @commands.command(aliases=["Zebrat", "Žebrat", "žebrat"])
    @commands.cooldown(1, 43200, commands.BucketType.member)
    async def zebrat(self, ctx):
        jmeno = str(ctx.guild.id)
        collection = db[jmeno]
        member = ctx.author
        data = collection.find_one({"_id": member.id})

        msg1 = await ctx.send("Jdeš žebrat")
        msg = await ctx.send("🗑️..........🏃.🌉")
        await asyncio.sleep(0.15)
        await msg.edit(content="🗑️..........🏃.🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️.........🏃..🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️........🏃...🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️.......🏃....🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️......🏃.....🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️.....🏃......🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️....🏃.......🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️...🏃........🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️..🏃.........🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️.🏃..........🌉")
        await asyncio.sleep(0.25)
        await msg.edit(content="🗑️🏃...........🌉")
        await msg1.delete()
        await msg.delete()

        vydelek = random.randrange(25, 200)
        await ctx.send(f"Hezky {ctx.author.mention} vyžebral sis {vydelek}$")
        vydel = {"$inc": {"cash": vydelek}}
        collection.update_one(data, vydel)
        await zapis("zebrat")

    @commands.command(aliases=["Kurva", "slapka", "Slapka"])
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def kurva(self, ctx):
        member = ctx.author
        jmeno = str(ctx.guild.id)
        collection = db[jmeno]
        data = collection.find_one({"_id": member.id})

        spatna_list = ["Tak ty neschopná, radši běž makat do mekáče 🤬",
                       "Ty seš prkno teda, co to jako mělo být? sex to teda nebyl :unamused:",
                       "Tak to bylo teda pěkně špatný.. :persevere:",
                       "S tebou už radši nechci nic mít ty prasečí ksichte :middle_finger:"]
        dobra_list = ["Dobře jsi mi ho vykouřila :smiling_face_with_3_hearts:", "No tyjo to byl teda sex :zany_face: ",
                      "Takhle dobrej vrz už jsem dlouho neměl :hot_face:", "Tak to teda byla honička :smirk: "]
        dobra = random.choice(dobra_list)
        spatna = random.choice(spatna_list)

        kurva = random.randint(1, 100)
        if kurva > 30:
            vyhra = random.randint(20, 300)
            sloty = {"$inc": {"cash": vyhra}}
            collection.update_one(data, sloty)
            kurva = discord.Embed(title=f"{dobra}", description=f"Tím ode mě získáváš **{vyhra}$**", colour=0xff00ae)
            kurva.set_thumbnail(
                url="https://d3b4rd8qvu76va.cloudfront.net/484/531/515/1940003029-1rn044k-hnnof659see7na0/original/maxresdefault.jpg")
            kurva.set_footer(text=f"Kurvička pro: {ctx.author.name}",
                             icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            msg = await ctx.send(embed=kurva)
        else:
            prohra = random.randint(50, 450)
            sloty = {"$inc": {"cash": -prohra}}
            collection.update_one(data, sloty)
            kurva = discord.Embed(title=f"{spatna}", description=f"Za to musíš zaplatit **{prohra}$** jako kompenzaci",
                                  colour=0xff00ae)
            kurva.set_thumbnail(
                url="https://d3b4rd8qvu76va.cloudfront.net/484/531/515/1940003029-1rn044k-hnnof659see7na0/original/maxresdefault.jpg")
            kurva.set_footer(text=f"Kurvička pro: {ctx.author.name}",
                             icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")
            msg = await ctx.send(embed=kurva)
        await zapis("kurva")

    @commands.command(aliases=["Okrast", "Okrást", "okrást"])
    @commands.cooldown(1, 43200, commands.BucketType.member)
    async def okrast(self, ctx, koho: discord.Member = None):
        if not koho.bot:
            if koho == ctx.author:
                await ctx.send("Proč kradl sam sebe?")
                return

            posilac = ctx.author
            jmeno = str(ctx.guild.id)
            collection = db[jmeno]
            data_zlodej = collection.find_one({"_id": posilac.id})
            data_ojebany = collection.find_one({"_id": koho.id})

            if int(data_ojebany["cash"]) < 250:
                await ctx.send(f"Bohužel {koho.display_name} je moc chudej :(")
                await ctx.command.reset_cooldown(ctx)
                return
            else:
                sance = random.randint(1, 100)
                if sance > 69:
                    kolik_ma = int(data_ojebany["cash"])
                    kolik_okrast = round(kolik_ma / 3)
                    collection.update_many(data_zlodej, {"$inc": {
                        "cash": kolik_okrast,
                    }})
                    collection.update_many(data_ojebany, {"$inc": {
                        "cash": -kolik_okrast,
                    }})
                    await ctx.send(
                        f"Hezky, měl jsi štěstí a policie tě nechytla, {koho.display_name} si okradl o {kolik_okrast}$")
                else:
                    pokuta = random.randint(250, 1000)
                    collection.update_many(data_zlodej, {"$inc": {
                        "cash": -pokuta,
                    }})
                    await ctx.send(f"Ale ne, chytla tě policie a musíš zaplatit {pokuta}$ jako kauci!")
        else:
            await ctx.send("Botům nemůžeš krást peníze")
        await zapis("okrast")

    @vybrat.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Peníze se počítaj v číslech a ne písmenech degeš...")

    @dat.error
    @prevod.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Ale komu to chceš poslat napiš!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Peníze se počítaj v číslech a ne písmenech degeš...")

    @zebrat.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            zprava = (
                        ctx.author.mention + f"žebrat můžeš znova za  {str(datetime.timedelta(seconds=int(error.retry_after)))}")
            await ctx.send(zprava)

    @kurva.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            zprava = (
                        ctx.author.mention + "Klid sakra, dej mi trochu času na odpočinek, na další kolo půjdem za {:.0f}s".format(
                    error.retry_after))
            await ctx.send(zprava)

    @okrast.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cas = str(datetime.timedelta(seconds=int(error.retry_after)))
            zprava = (ctx.author.mention + f"žebrat můžeš znova za  {cas}")
            await ctx.send(zprava)

    @prace.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cas = str(datetime.timedelta(seconds=int(error.retry_after)))
            zprava = (ctx.author.mention + f"Do práce můžeš znova až za {cas}")
            await ctx.send(zprava)

def setup(client):
    client.add_cog(penize(client))