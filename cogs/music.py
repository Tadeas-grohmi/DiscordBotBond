import discord
from discord.ext import commands
import DiscordUtils

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'yt-dl/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f'```ini\nSong: {data["title"]} přidán do fronty.\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer():
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                if self in self._cog.players.values():
                    return self.destroy(self._guild)
                return

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'Error.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f"Právě hraju: **{source.title}**")
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Test_Music(commands.Cog):

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            for entry in self.players[guild.id].queue._queue:
                if isinstance(entry, YTDLSource):
                    entry.cleanup()
            self.players[guild.id].queue._queue.clear()
        except KeyError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send("Špatný voice kanál, zkus jiný")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        return player

    @commands.command(aliases=["Napoj", "pripoj", "Pripoj"])
    async def napoj(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel("Nemám se ke komu připojit, nebo se tam nemůžu připojit")
        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Přesouvání do: <{channel}> se nepovedlo.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Připojování do: <{channel}> se nepovedlo.')
        await ctx.send(f'Připojen do: **{channel}**', delete_after=20)

    @commands.command(aliases=["hraj", "Hraj", "p", "P", "h", "H"])
    async def play(self, ctx, *, search: str):
        try:
            await ctx.trigger_typing()
            vc = ctx.voice_client
            if not vc:
                await ctx.invoke(self.napoj)
            player = self.get_player(ctx)
            # If download is False, source will be a dict which will be used later to regather the stream.
            # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
            await player.queue.put(source)
        except:
            await ctx.send("Video je 18+ a tudíž ho nemůžu pustit :(") 

    @commands.command(aliases=["Pauza"])
    async def pauza(self, ctx):
        vc = ctx.voice_client
        co = vc.source.title
        if not vc or not vc.is_playing():
            return await ctx.send('Nemám co bych zapauzoval!', delete_after=20)
        elif vc.is_paused():
            return
        vc.pause()
        await ctx.send(f"**{co}** zapauzováno")

    @commands.command(aliases=["Pokracuj"])
    async def pokracuj(self, ctx):
        vc = ctx.voice_client
        co = vc.source.title
        if not vc or not vc.is_connected():
            return await ctx.send("Nemám co bych zapauzoval!", delete_after=20)
        elif not vc.is_paused():
            return
        vc.resume()
        await ctx.send(f"hraju dál: **{co}**")

    @commands.command(aliases=["Skip", "Pass", "pass"])
    async def skip(self, ctx):
        vc = ctx.voice_client
        jmeno = vc.source.title
        player = self.get_player(ctx)
        if not vc or not vc.is_connected():
            return await ctx.send("Nemám co skipnout!", delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return
        vc.stop()
        player.np = await ctx.send(f"Song: **{jmeno}** přeskočen", delete_after=15)

    @commands.command(aliases=["q","Fronta", "Q"])
    async def fronta(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send("Nejsem ve voicu", delete_after=20)
        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send("Nejsou zde další songy ve frontě")
        upcoming = list(itertools.islice(player.queue._queue, 0, 25))
        fmt = '\n'.join(f'**{_["title"]}**' for _ in upcoming)
        embed = discord.Embed(title=f'Songy ve frontě: {len(upcoming)}', description=fmt, colour=discord.Colour.random())
        await ctx.send(embed=embed)

    @commands.command(aliases=["np","NP", "prave_hraje"])
    async def now_playing(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send("Nejsem ve voicu", delete_after=20)
        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send("Nic nehraju")
        try:
            await player.np.delete()
        except discord.HTTPException:
            pass
        player.np = await ctx.send(f"Právě hraju: **{vc.source.title}**")

    @commands.command(aliases=["Volume", "v", "V"])
    async def volume(self, ctx, *, vol: float):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send("Nejsem ve voicu", delete_after=20)
        if not 0 < vol < 101:
            return await ctx.send("Napiš hodnotu od 1 do 100")
        player = self.get_player(ctx)
        if vc.source:
            vc.source.volume = vol / 100
        player.volume = vol / 100
        await ctx.send(f"Volume změněno na: **{vol}%**")

    @commands.command(aliases=["S"])
    async def stopik(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send("Nic nehraju", delete_after=20)
        await self.cleanup(ctx.guild)
        await ctx.send("Stopnuto")

    @pauza.error
    @volume.error
    @pokracuj.error
    @pauza.error
    @skip.error
    @fronta.error
    async def on_command_error(self, ctx, error):
        await ctx.send("To bych ještě musel něco hrát...")

    @play.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Ale napiš jaké video chceš pustit?")


def setup(bot):
    bot.add_cog(Test_Music(bot))
