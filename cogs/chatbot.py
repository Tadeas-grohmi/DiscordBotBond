import discord
from discord.ext import commands
from pymongo import MongoClient
import certifi
from prsaw import RandomStuff
from utils.tajne import ChatBot

api_key = ChatBot()
mango_url = "mongodb+srv://Bond:Drago00914*@disbotbond.xo3fb.mongodb.net/test"
cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
db = cluster["chatbot"]

rs = RandomStuff(async_mode=True, api_key=api_key, dev_name="Tadeas", ai_language="cs", bot_name="Bondik")

class chatbot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            jmeno = message.guild.id
            collection = db["chatbot_guild_id"]
            data = collection.find_one({"_id": jmeno})
            kanal_data = data["kanal"]
            if data == None:
                return
            kanal = self.client.get_channel(kanal_data)
            if message.channel != kanal:
                return
            else:
                try:
                    if message.author.bot:
                        return
                    if message.channel == kanal:
                        reply = await rs.get_ai_response(message.content)
                        odpoved = reply[0]['message']
                        await message.reply(odpoved)
                except:
                    await message.reply("Ups něco se podělalo, zkus znova napsat(V angličtině nejlépe)")
        except:
            return
        await self.client.process_commands(message)

    @commands.has_permissions(manage_channels=True)
    @commands.command(aliases=["Chatbot_setup"])
    async def chatbot_setup(self, ctx, kanal: discord.TextChannel = None):
        jmeno = ctx.guild.id
        collection = db["chatbot_guild_id"]
        data = collection.find_one({"_id": jmeno})
        if kanal == None:
            await ctx.send("Napiš v jakým kanálu chceš chatbota")
            return
        if data == None:
            kanal_novy = kanal.id
            post = {"_id": jmeno, "kanal": kanal_novy, "guild_jmeno": ctx.guild.name}
            collection.insert_one(post)
            await ctx.send(f"Chatbot je nastaven na kanal **{kanal.name}**")
        else:
            kanal_update = kanal.id
            post = {"$set": {"kanal": kanal_update}}
            collection.update_one(data, post)
            await ctx.send(f"Chatbot je nově nastaven na kanal **{kanal.name}**")

    @commands.command(aliases=["Chatbot"])
    async def chatbot(self, ctx):
        jmeno = ctx.guild.id
        collection = db["chatbot_guild_id"]
        data = collection.find_one({"_id": jmeno})
        try:
            kanal = data["kanal"]
            jmeno = self.client.get_channel(kanal)
            await ctx.send(f"Chatbot je nastaven v kanálu **{jmeno}**")
        except:
            await ctx.send(f"Chatbot není nastaven (pro nastavení použijte chatbot_setup)")

    @commands.has_permissions(manage_channels= True)
    @commands.command(aliases=["Chatbot_delete"])
    async def chatbot_delete(self, ctx):
        jmeno = ctx.guild.id
        collection = db["chatbot_guild_id"]
        try:
            data = collection.find_one({"_id": jmeno})
            collection.delete_one(data)
            await ctx.send(f"Chatbot kanál je smazán z {ctx.guild.name}")
        except:
            await ctx.send(f"Chatbot není nastaven (pro nastavení použijte chatbot_setup)")

    @chatbot_setup.error
    @chatbot_delete.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Na tohle musíš mít alespon práva na upravení kanálů")

def setup(client):
    client.add_cog(chatbot(client))