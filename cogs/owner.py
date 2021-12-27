from discord.ext import commands
import discord

import asyncio
import time
import os
import pprint
import dbl
import psutil
import platform


class Owner(commands.Cog, command_attrs={"hidden": True}):
    """Commands that can only be performed by the bot owner"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxNDUzNzcxMDk0NTY5NzgxNiIsImJvdCI6dHJ1ZSwiaWF0IjoxNTg4NTExNjAxfQ.34y-kV8IYSYpc8FTDhTe2oMQDMv_ZrJ0kHuAoV1s5Ac' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    def bot_owner(self, ctx):
	    return ctx.author.id == 295475608169873411

    @commands.command()
    @commands.check(bot_owner)
    async def reloaddHZ4Ja9xJf(self, ctx, *, cog=None):
        """Reload one or all of MAT's cogs"""

        try:
            if cog is None:
                for extension in self.bot.extensions.keys():
                    self.bot.reload_extension(extension)
                await ctx.send(f"Bütün eklentiler yeniden yüklendi", delete_after=5.0)
            else:
                self.bot.reload_extension("cogs." + cog.lower())
                await ctx.send(f"Yeniden yüklendi `{cog.capitalize()}`", delete_after=5.0)
        except:
            await ctx.send("Hatalı eklenti adı.", delete_after=5.0)

        await ctx.message.delete()

    @commands.command()
    @commands.check(bot_owner)
    async def unloadjv9pzTlBG2(self, ctx, cogname: str):
        try:
            cog = "cogs." + cogname
            self.bot.unload_extension(cog)
            await ctx.send(f"{cogname} commands disabled")
            print(f"{cogname} commands disabled")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")

    @commands.command()
    @commands.check(bot_owner)
    async def botstatszEH9J9Q7em(self, ctx):
        await ctx.message.delete()
        servers = list(self.bot.guilds)
        users = list(self.bot.users)
        embed = discord.Embed(title=f"{self.bot.user.name} İstatikleri", colour=discord.Color.blurple())
        embed.add_field(name="Sahip", value="zolhh#9942")
        embed.add_field(name="CPU Kullanımı", value=f"%{psutil.cpu_percent()}")
        embed.add_field(name="RAM Kullanımı", value=f"%{psutil.virtual_memory().percent}")
        embed.add_field(name="Sunucu Sayısı", value=f"{str(len(servers))}")
        embed.add_field(name="Kullanıcı Sayısı", value=f"{str(len(users))}")
        embed.add_field(name="Python Version", value=platform.python_version())
        embed.add_field(name="discord.py Version", value=discord.__version__)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(
            text=f"discord.py ❤ kullanarak oluşturuldu.", icon_url="https://www.python.org/static/opengraph-icon-200x200.png",
        )
        await ctx.send(embed=embed)

    

def setup(bot):
    bot.add_cog(Owner(bot))