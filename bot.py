import asyncio
import functools
import itertools
import math
import random
import discord

from random import randrange
from discord import utils
from async_timeout import timeout
from discord.ext import commands

bot = commands.Bot('tt.')
bot.remove_command("help")

###Corona Komutları İçin Gerekenler###
from discord.ext.commands import Bot
from discord import Game, Embed
import requests


###Korona Komutları Başlangıç###
BASE_PATH = "https://corona.lmao.ninja"
ENDPOINTS = {
    "total": "/v2/all",
    "countries": "/v2/countries"
}

def find_country(countries, name):
    for i in range(len(countries)):
        if countries[i]["country"].lower() == name.lower():
            return countries[i]


@bot.command(name="covid19-dünya")
async def total(ctx):
    res = requests.get(BASE_PATH+ENDPOINTS["total"])
    if res.status_code != 200:
        print("İşlem başarısız {0}{1}".format(BASE_PATH, ENDPOINTS))

    json = res.json()
    embed = Embed(title="Covid-19 Dünya İstatistikleri", type="rich").add_field(name="Toplam Vaka", value=json["cases"]).add_field(
        name="Toplam Ölüm", value=json["deaths"]).add_field(name="Toplam İyileşen", value=json["recovered"])
    await ctx.channel.send(embed=embed)


@bot.command(name="covid19-ülke")
async def country(ctx, arg):
    res = requests.get(BASE_PATH+ENDPOINTS["countries"])
    if res.status_code != 200:
        print("İşlem başarısız {0}{1}".format(BASE_PATH, ENDPOINTS))
        msg = "Üzgünüm, şu anda veri sağlayamıyorum."
        await ctx.channel.send(msg)
        pass

    json = res.json()
    country = find_country(json, arg)
    if (country is None):
        msg = "Ülke adını yanlış girdiniz: **{0}**. Lütfen ülkelerin İngilizce isimlerini girin. **Örnek: Turkey**".format(
            arg)
        await ctx.channel.send(msg)
        pass

    embed = Embed(title="Covid-19 {0} İstatistikleri".format(country["country"]), type="rich").add_field(
        name="Toplam Vaka", value=country["cases"]).add_field(name="Toplam Ölüm", value=country["deaths"]).add_field(name="Toplam İyileşen", value=country["recovered"]).add_field(
            name="Bugünkü Vaka", value=country["todayCases"]).add_field(name="Bugünkü Ölüm", value=country["todayDeaths"]).add_field(name="Yoğun Bakım", value=country["critical"])
    await ctx.channel.send(embed=embed)

###Korona Komutları Bitiş###

@bot.command()
async def ping(ctx):
	msg = f"Ping `{round(bot.latency * 1000)}ms`"
	embed = discord.Embed(title="Taluy Bot", description=msg, color=discord.Color.purple())
	await ctx.send(embed=embed)
        
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('t.yardım'))
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

    extensions = ['cogs.mod', 'cogs.fun', 'cogs.general', 'cogs.music', 'cogs.ticket', 'cogs.owner', 'cogs.leveling', 'cogs.giveaway']

    if __name__ == '__main__':
        for ext in extensions:
            bot.load_extension(ext)

bot.run('your_secret_code')