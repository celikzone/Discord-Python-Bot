import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import math
import aiohttp
import io
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import json

class Lvl(commands.Cog, name='leveling'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('data/main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
            val = (message.guild.id, message.author.id, 2, 0)
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
            result1 = cursor.fetchone()
            exp = int(result1[1])
            sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
            val = (exp + 2, str(message.guild.id), str(message.author.id))
            cursor.execute(sql, val)
            db.commit()

            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
            result2 = cursor.fetchone()

            xp_start = int(result2[1])
            lvl_start = int(result2[2])
            xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
            if xp_end < xp_start:
                desc=f'🎉 {message.author.mention} seviye atladı! O artık {lvl_start + 1}. seviye! 🎉'
                embed = discord.Embed(color=0x406da2)
                embed.add_field(name='**Seviye Atladı**', value=desc)
                embed.timestamp = datetime.datetime.utcnow()
                await message.channel.send(embed=embed)
                #await message.channel.send(f'🎉 {message.author.mention} seviye atladı! O artık {lvl_start + 1}. seviye! 🎉')
                sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")
                val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (0, str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

    """@commands.command()
    async def rankold(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('data/main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('That user is not yet ranked.')
            else:
                await ctx.send(f'{user.name} is currently level {str(result[2])} and has {str(result[1])} XP')
            cursor.close()
            db.close()
        elif user is None:
            db = sqlite3.connect('data/main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('That user is not yet ranked.')
            else:
                await ctx.send(f'{ctx.message.author.name} is currently level {str(result[2])} and has {str(result[1])} XP')
            cursor.close()
            db.close()"""

    @commands.command(pass_context=True)
    async def seviye(self, ctx, user:discord.User=None):
        if user is None:
            main = sqlite3.connect('data/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT exp, lvl FROM levels WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                img = Image.open("data/rank.png") #Replace infoimgimg.png with your background image.
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("data/Quotable.otf", 35) #Make sure you insert a valid font from your folder.
                font1 = ImageFont.truetype("data/Quotable.otf", 24) #Make sure you insert a valid font from your folder.
                #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(ctx.author.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((156, 156)), (50, 60))

                draw.text((242, 100), "0", (255, 255, 255), font=font)
                draw.text((242, 180), "0", (255, 255, 255), font=font)
                draw.text((50,220), f"{ctx.author.name}", (255, 255, 255), font=font1)
                draw.text((50,240), f"#{ctx.author.discriminator}", (255, 255, 255), font=font1)
                img.save('data/infoimg2.png') #Change Leveling/infoimg2.png if needed.
                ffile = discord.File("data/infoimg2.png")
                await ctx.send(file=ffile)
            elif result is not None:
                img = Image.open("data/rank.png") #Replace infoimgimg.png with your background image.
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("data/Quotable.otf", 35) #Make sure you insert a valid font from your folder.
                font1 = ImageFont.truetype("data/Quotable.otf", 24) #Make sure you insert a valid font from your folder.
                #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(ctx.author.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((156, 156)), (50, 60))

                draw.text((242, 100), f"{str(result[1])}", (255, 255, 255), font=font)
                draw.text((242, 180), f"{str(result[0])}", (255, 255, 255), font=font)
                draw.text((50,220), f"{ctx.author.name}", (255, 255, 255), font=font1)
                draw.text((50,240), f"#{ctx.author.discriminator}", (255, 255, 255), font=font1)
                img.save('data/infoimg2.png') #Change Leveling/infoimg2.png if needed.
                ffile = discord.File("data/infoimg2.png")
                await ctx.send(file=ffile)
            cursor.close()
            main.close()
        else:
            main = sqlite3.connect('data/main.sqlite')
            cursor = main.cursor()
            cursor.execute(f"SELECT exp, lvl FROM levels WHERE guild_id = '{ctx.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                img = Image.open("data/rank.png") #Replace infoimgimg.png with your background image.
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("data/Quotable.otf", 35) #Make sure you insert a valid font from your folder.
                font1 = ImageFont.truetype("data/Quotable.otf", 24) #Make sure you insert a valid font from your folder.
                #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(user.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((156, 156)), (50, 60))

                draw.text((242, 100), "0", (255, 255, 255), font=font)
                draw.text((242, 180), "0", (255, 255, 255), font=font)
                draw.text((50,220), f"{user.name}", (255, 255, 255), font=font1)
                draw.text((50,240), f"#{user.discriminator}", (255, 255, 255), font=font1)
                img.save('data/infoimg2.png') #Change Leveling/infoimg2.png if needed.
                ffile = discord.File("data/infoimg2.png")
                await ctx.send(file=ffile)
            elif result is not None:
                img = Image.open("data/rank.png") #Replace infoimgimg.png with your background image.
                draw = ImageDraw.Draw(img) 
                font = ImageFont.truetype("data/Quotable.otf", 35) #Make sure you insert a valid font from your folder.
                font1 = ImageFont.truetype("data/Quotable.otf", 24) #Make sure you insert a valid font from your folder.
                #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(user.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((156, 156)), (50, 60))

                draw.text((242, 100), f"{str(result[1])}", (255, 255, 255), font=font)
                draw.text((242, 180), f"{str(result[0])}", (255, 255, 255), font=font)
                draw.text((50,220), f"{user.name}", (255, 255, 255), font=font1)
                draw.text((50,240), f"#{user.discriminator}", (255, 255, 255), font=font1)
                img.save('data/infoimg2.png') #Change Leveling/infoimg2.png if needed.
                ffile = discord.File("data/infoimg2.png")
                await ctx.send(file=ffile)
            cursor.close()
            main.close()
        
    @commands.command(pass_context=True)
    async def lidertablosu(self, ctx):
        main = sqlite3.connect('data/main.sqlite')
        cursor = main.cursor()
        cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.guild.id}' ORDER BY lvl DESC, exp DESC")
        result = cursor.fetchall()
        desc = ''
        v = 1
        for result in result:
            if v > 5:
                break

            if result[0] == None:
                continue
            
            user = self.bot.get_user(int(result[0]))
            lvl = result[2]
            desc += f'**{str(user)}** *[Seviye {lvl}]*\n'
            v += 1
            
        embed = discord.Embed(color=0x406da2)
        embed.add_field(name='**Lider Tablosu**', value=desc)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/705387235079356417/707253386189340672/gold-cup.jpg')
        embed.set_footer(text=f'{ctx.message.guild}', icon_url=f'{ctx.message.guild.icon_url}')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Lvl(bot))
    print('Leveling is loaded.')