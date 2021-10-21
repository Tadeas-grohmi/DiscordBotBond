# Created by ${USER} at ${DATE}
import discord
import time
import random
import datetime
from discord.ext import commands
import asyncio
from utils.utils import Pag
from utils.utils import clean_code
import contextlib
import textwrap
from traceback import format_exception
import io

class kod(commands.Cog):

    def __init__(self, client,):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def kod(self, ctx, *, kod):
        kod = clean_code(kod)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.client,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n {textwrap.indent(kod,'     ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pager = Pag(
            timeout=100,
            entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```py\n",
            suffix="```"
        )

        await pager.start(ctx)
        
    @kod.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.channel.send("Bohužel, tenhle command může použít jen pár lidí...")


def setup(client):
    client.add_cog(kod(client))