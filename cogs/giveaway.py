import asyncio
import functools
import itertools
import math
import random
import discord
from discord.ext import commands
import datetime

bot = commands.Bot('tt.')

class Giveaway(commands.Cog):
    def __init__(self, ctx):
        return

    @commands.command()
    async def çekiliş(self, ctx, item, amount: int):
        #check = "🎉"
        await ctx.message.delete()
        if amount <= 10:

            first_embed = discord.Embed(
               title="🎉 Çekiliş 🎉", color=discord.Color.blurple()
            )
            first_embed.add_field(name="Hediye", value=item, inline=True)
            first_embed.add_field(name="Kalan Süre", value=amount, inline=True)
            first_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
            msg = await ctx.send("Çekiliş Başladı!", embed=first_embed)
            await msg.add_reaction("🎉")

            for i in range(amount):
                await asyncio.sleep(1)
                new_embed = discord.Embed(
                title="🎉 Çekiliş 🎉", color=discord.Color.blurple())
                new_embed.add_field(name="Hediye", value=item, inline=True)
                new_embed.add_field(name="Kalan Süre", value=(str(amount - i)), inline=True)
                new_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
                await msg.edit(embed=new_embed)

            msg = await msg.channel.fetch_message(msg.id)

            for reaction in msg.reactions:
                users = await reaction.users().flatten()
            winner = random.choice(users)

            for i in range(amount):
                await asyncio.sleep(1)
                new2_embed = discord.Embed(
                title="🎉 Çekiliş 🎉", color=discord.Color.blurple())
                new2_embed.add_field(name="Sonuçlar", value="@{} adlı üye çekilişi kazandı!".format(winner), inline=True)
                new2_embed.add_field(name="Hediye", value=item, inline=False)
                new2_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
                await msg.edit(embed=new2_embed)
        elif amount < 60:

            first_embed = discord.Embed(
               title="🎉 Çekiliş 🎉", color=discord.Color.blurple()
            )
            first_embed.add_field(name="Hediye", value=item, inline=True)
            first_embed.add_field(name="Çekiliş Süresi", value=(str(amount)) + " Saniye", inline=True)
            first_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
            msg = await ctx.send("Çekiliş Başladı!", embed=first_embed)
            await msg.add_reaction("🎉")

            msg = await msg.channel.fetch_message(msg.id)

            for reaction in msg.reactions:
                users = await reaction.users().flatten()
            winner = random.choice(users)

            for i in range(amount):
                await asyncio.sleep(amount)
                new2_embed = discord.Embed(
                title="🎉 Çekiliş 🎉", color=discord.Color.blurple())
                new2_embed.add_field(name="Sonuçlar", value="@{} adlı üye çekilişi kazandı!".format(winner), inline=True)
                new2_embed.add_field(name="Hediye", value=item, inline=False)
                new2_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
                await msg.edit(embed=new2_embed)

        elif 60 <= amount < 3540:

            first_embed = discord.Embed(
               title="🎉 Çekiliş 🎉", color=discord.Color.blurple()
            )
            first_embed.add_field(name="Hediye", value=item, inline=True)
            first_embed.add_field(name="Çekiliş Süresi", value=(str(round(amount/60))) + " Dakika", inline=True)
            first_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
            msg = await ctx.send("Çekiliş Başladı!", embed=first_embed)
            await msg.add_reaction("🎉")

            msg = await msg.channel.fetch_message(msg.id)

            for reaction in msg.reactions:
                users = await reaction.users().flatten()
            winner = random.choice(users)

            for i in range(amount):
                await asyncio.sleep(amount)
                new2_embed = discord.Embed(
                title="🎉 Çekiliş 🎉", color=discord.Color.blurple())
                new2_embed.add_field(name="Sonuçlar", value="@{} adlı üye çekilişi kazandı!".format(winner), inline=True)
                new2_embed.add_field(name="Hediye", value=item, inline=False)
                new2_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
                await msg.edit(embed=new2_embed)
        elif 4000 <= amount < 86400:

            first_embed = discord.Embed(
               title="🎉 Çekiliş 🎉", color=discord.Color.blurple()
            )
            first_embed.add_field(name="Hediye", value=item, inline=True)
            first_embed.add_field(name="Çekiliş Süresi", value=(str(round(amount/3600))) + " Saat", inline=True)
            first_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
            msg = await ctx.send("Çekiliş Başladı!", embed=first_embed)
            await msg.add_reaction("🎉")

            msg = await msg.channel.fetch_message(msg.id)

            for reaction in msg.reactions:
                users = await reaction.users().flatten()
            winner = random.choice(users)

            for i in range(amount):
                await asyncio.sleep(amount)
                new2_embed = discord.Embed(
                title="🎉 Çekiliş 🎉", color=discord.Color.blurple())
                new2_embed.add_field(name="Sonuçlar", value="@{} adlı üye çekilişi kazandı!".format(winner), inline=True)
                new2_embed.add_field(name="Hediye", value=item, inline=False)
                new2_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
                await msg.edit(embed=new2_embed)
        else:
            first_embed = discord.Embed(
               title="🎉 Çekiliş 🎉", color=discord.Color.blurple()
            )
            first_embed.add_field(name="Hediye", value=item, inline=True)
            first_embed.add_field(name="Çekiliş Süresi", value=(str(round(amount/86400))) + " Gün", inline=True)
            first_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
            msg = await ctx.send("Çekiliş Başladı!", embed=first_embed)
            await msg.add_reaction("🎉")

            msg = await msg.channel.fetch_message(msg.id)

            for reaction in msg.reactions:
                users = await reaction.users().flatten()
            winner = random.choice(users)

            for i in range(amount):
                await asyncio.sleep(amount)
                new2_embed = discord.Embed(
                title="🎉 Çekiliş 🎉", color=discord.Color.blurple())
                new2_embed.add_field(name="Sonuçlar", value="@{} adlı üye çekilişi kazandı!".format(winner), inline=True)
                new2_embed.add_field(name="Hediye", value=item, inline=False)
                new2_embed.set_footer(text=f'{ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
                await msg.edit(embed=new2_embed)
    

def setup(bot):
    bot.add_cog(Giveaway(bot))