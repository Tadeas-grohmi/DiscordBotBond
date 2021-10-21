
import discord
import time
import random
import datetime
import requests
from utils.utils import zapis
from discord.ext import commands

from utils.tajne import openweather

api_key = openweather()

base_url = "http://api.openweathermap.org/data/2.5/weather?"
metricke = "&units=metric"

class pocasi(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases= ["Pocasi", "počasí", "Počasí"])
    async def pocasi(self, ctx, *, city: str):
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + metricke
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        if x["cod"] != "404":
            async with channel.typing():
                y = x["main"]
                current_temperature = y["temp"]
                #current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_humidity = y["humidity"]
                feellike = y["feels_like"]
                z = x["weather"]
                c = x["wind"]
                windspeed = c["speed"]
                weather_description = z[0]["description"]
                embed = discord.Embed(title=f"Počasí v {city_name}",
                                      color=0x0062ff,
                                      timestamp=ctx.message.created_at, )
                embed.add_field(name=":white_sun_cloud: Obloha:", value=f"**{weather_description}**", inline=False)
                embed.add_field(name=":thermometer: Teplota:", value=f"**{current_temperature:.0f}**°C", inline=False)
                embed.add_field(name=":eyeglasses: Pocitová teplota:", value=f"**{feellike:.0f}°C**", inline=False)
                embed.add_field(name=":dash: Rychlost větru:", value=f"**{windspeed:.1f}m/s**", inline=False)
                embed.add_field(name=":droplet: Vlhkost:", value=f"**{current_humidity}%**", inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                embed.set_footer(text=f"Pro: {ctx.author.name}", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")

            await channel.send(embed=embed)
        else:
            await channel.send("Město nenalezeno.")
        await zapis("pocasi")
        
    @commands.command(aliases= ["FullPocasi", "fullpočasí", "fullPočasí"])
    async def fullpocasi(self, ctx, *, city: str):
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + metricke
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        if x["cod"] != "404":
            async with channel.typing():
                y = x["main"]
                current_temperature = y["temp"]
                #current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                maxtemp = y["temp_max"]
                mintemp = y["temp_min"]
                feellike = y["feels_like"]
                z = x["weather"]
                weather_description = z[0]["description"]
                c = x["wind"]
                windspeed = c["speed"]
                smer = c["deg"]
                v = x["coord"]
                lon = v["lon"]
                lat = v["lat"]
                b = x["sys"]
                vychod = b["sunrise"]
                zapad = b["sunset"]
                vychodprepocet = time.strftime("%H:%M", time.localtime(int(vychod)))
                zapadprepocet = time.strftime("%H:%M", time.localtime(int(zapad)))
                rychlostprepocet = round((windspeed) * 3.6, 1)

                embed = discord.Embed(title=f"Počasí v {city_name}",
                                      color=0x0062ff,
                                      timestamp=ctx.message.created_at,)
                embed.add_field(name=":cloud: Obloha:", value=f"Stav mraků: {weather_description}", inline=False)
                embed.add_field(name=":thermometer: Teplota:", value=f"Teplota: {current_temperature:.1f}°C\n Pocitová teplota: {feellike:.1f}°C\n Max teplota: {maxtemp:.1f}°C\n Min teplota: {mintemp:.1f}°C", inline=False)
                #embed.add_field(name="Pocitová teplota(C):", value=f"**{feellike}°C**", inline=False)
                #embed.add_field(name="Max teplota(C):", value=f"**{maxtemp}°C**", inline=False)
                #embed.add_field(name="Min teplota(C):", value=f"**{mintemp}°C**", inline=False)
                #embed.add_field(name="Vlhkost(%):", value=f"**{current_humidity}%**", inline=False)
                #embed.add_field(name="Atmosférický tlak(hPa):", value=f"**{current_pressure}hPa**", inline=False)
                embed.add_field(name=":dash: Vítr:", value=f"Rychlost větru(m/s): {windspeed:.1f}m/s\n Rychlost větru(Km/h): {rychlostprepocet:.1f}Km/h\n Směr větru: {smer}°", inline=False)
                embed.add_field(name=":droplet: Stav vzduchu:", value=f"Vlhkost: {current_humidity}%\n Atmosférický tlak: {current_pressure}hPa", inline=False)
                #embed.add_field(name="Rychlost větru(m/s):", value=f"**{windspeed}m/s**", inline=False)
                #embed.add_field(name="Směr větru(°):", value=f"**{smer}°**", inline=False)
                #embed.add_field(name="Souřadnice(Z. výška):", value=f"**{lat}°**", inline=False)
                #embed.add_field(name="Souřadnice (Z. šířka):", value=f"**{lon}°**", inline=False)
                embed.add_field(name=":white_sun_small_cloud: Slunce:", value=f"Východ slunce v: {vychodprepocet}\n Západ slunce v: {zapadprepocet}")
                embed.add_field(name=":earth_africa: Souřadnice", value=f"Z. výška: {lat}°\n Z. šířka: {lon}°", inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                embed.set_footer(text=f"Pro: {ctx.author.name}", icon_url="https://cdn.discordapp.com/attachments/586526210469789717/839401432272207891/BondPFP.png")


            await channel.send(embed=embed)
        else:
            await channel.send("Město nenalezeno.")
        await zapis("fullpocasi")
        
    @pocasi.error
    @fullpocasi.error
    async def on_message_error(self, ctx, error):
        await ctx.send("Napiš jaký město!")






def setup(client):
    client.add_cog(pocasi(client))