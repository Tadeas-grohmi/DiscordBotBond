from discord.ext import commands
from discord.ext import tasks
import time
import discord
import random


class status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.status_zmena.start()
        print("Status zapnut")


    @tasks.loop(seconds=10)
    async def status_zmena(self):
        statuses = ["Použij !! nebo $", f"Jsem na {len(self.bot.guilds)} serverech", f"Mám {len(self.bot.users)} uživatelů"]
        #urls = ["https://www.youtube.com/watch?v=blN4xe3y430&t=29s", "https://www.youtube.com/watch?v=s8umOD72H0E","https://www.youtube.com/watch?v=RV6aLIQgmYg", "https://www.youtube.com/watch?v=hQDv_y1BWl8&t=10s"]
        status = random.choice(statuses)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(status))

    @commands.command()
    async def statuson(self):
        try:
            self.status_zmena.start()
        except:
            self.status_zmena.stop()
            time.sleep(1)
            self.status_zmena.start()


def setup(client):
    client.add_cog(status(client))
