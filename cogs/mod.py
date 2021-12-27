import asyncio
import functools
import itertools
import math
import random
import discord
import datetime
import psutil
import platform

from discord.utils import get
from random import randrange
from discord import utils
from discord.ext import commands

ROLE = "Yeni Üye"

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_datetime_timestamp(self, t: datetime.datetime):
        """
        formats a datetime.datetime object as a string
        used for properly displaying discord.Member.joined_at
        """

        # format minutes
        if t.minute < 10:
            minute = "0{0}".format(t.minute)
        else:
            minute = t.minute

        return "{0}/{1}/{2} @ {3}:{4}".format(t.day, t.month, t.year, t.hour, minute)

    @commands.Cog.listener()
    async def on_member_join(self, member):

        embed = discord.Embed(colour = discord.Colour.green(), description=f"Sunucumuza hoşgeldin! Bizim {len(list(member.guild.members))}. üyemizsin.")
        embed.add_field(name="Kullanıcı Adı", value=member.name)
        embed.add_field(name="Kod", value=member.discriminator)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Kayıt Tarihi", value=self.format_datetime_timestamp(member.created_at))
        embed.add_field(name="Sunucuya Giriş", value=self.format_datetime_timestamp(member.joined_at))
        embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')

        channel = discord.utils.get(member.guild.channels, name='hoşgeldiniz')

        await channel.send(embed=embed)
        role = get(member.guild.roles, name=ROLE)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        embed = discord.Embed(colour = discord.Colour.red(), description=f"Aramızdan ayrıldı, güle güle.")
        embed.add_field(name="Kullanıcı Adı", value=member.name)
        embed.add_field(name="Kod", value=member.discriminator)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Kayıt Tarihi", value=self.format_datetime_timestamp(member.created_at))
        embed.add_field(name="Sunucuya Giriş", value=self.format_datetime_timestamp(member.joined_at))
        embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')

        channel = discord.utils.get(member.guild.channels, name='hoşgeldiniz')

        await channel.send(embed=embed)
        

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'🔨 {member.mention} adlı kullanıcı banlandı!')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'🔨 {user.mention} adlı kullanıcının banı kaldırıldı!')
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None):
        await member.kick()
        await ctx.send(f'🔨 {member.mention} adlı üye kicklendi!')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    #read_message_history=True
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_messages=True)
    async def temizle(self, ctx, amount=1):
        amount=amount + 1
        await ctx.channel.purge(limit=amount)
        botMesaji=await ctx.send('👌 **{}** adet mesaj silindi!'.format(amount-1))
        await asyncio.sleep(3)
        await botMesaji.delete()

    @temizle.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['yavaşmod'])
    async def slowmode(self, ctx, seconds: int=0):
        if seconds > 120:
            msg = '⛔ **120** saniyeden daha fazla yavaş mod ekleyemezsiniz.'
            return await ctx.send(msg, delete_after = 10)
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            msg = 'Yavaş mod **kaldırıldı**.'
            await ctx.send(msg, delete_after = 10)
            
        else:
            if seconds == 1:
                numofsecs = "saniye"
            else:    
                numofsecs = "saniye"
            await ctx.channel.edit(slowmode_delay=seconds)
            msg = (f'Kanal yavaş mod gecikmesi **{seconds}** {numofsecs} ayarlandı.\nKapatmak için **t.yavaşmod** yazın.')
            await ctx.send(msg, delete_after = 35)

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)


    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def rolver(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.top_role > user.top_role or ctx.author == ctx.guild.owner:
            await user.add_roles(role)
            msg = (f"**{user.mention}** adlı üyeye **`{role}`** rolü verildi.")
            await ctx.send(msg, delete_after = 15)

    @rolver.error
    async def rolver_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def rolal(self, ctx, user : discord.Member, *, role : discord.Role):
        if ctx.author.top_role >= user.top_role or ctx.author == ctx.guild.owner:
            await user.remove_roles(role)
            msg = (f"**`{role}`** rolü **{user.mention}** adlı üyeden kaldırıldı.")
            await ctx.send(msg, delete_after = 15)

    @rolal.error
    async def rolal_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def mute(self, ctx, user: discord.Member, time: int=15):
        '''Mute a member in the guild'''
        secs = time * 60
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=False)
        await ctx.send(f"{user.mention} adlı üye {time} dakika susturuldu.")
        await asyncio.sleep(secs)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        await ctx.send(f'{user.mention} adlı üyenin susturulması kaldırıldı.')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unmute(self, ctx, user: discord.Member):
        '''Unmute a member in the guild'''
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        await ctx.send(f'{user.mention} adlı üyenin susturulması kaldırıldı.')

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    @commands.command()
    async def kim(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
            
        embed=discord.Embed(title="Etiketlediğin Kişi Kim?")
        embed.set_author(name=member, icon_url=member.avatar_url)
        embed.set_image(url=member.avatar_url)
        embed.add_field(name="Kullanıcı Adı", value=member.name)
        embed.add_field(name="Kod", value=member.discriminator)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Kayıt Tarihi", value=self.format_datetime_timestamp(member.created_at))
        if member.joined_at is not None:
            embed.add_field(name="Sunucuya Giriş", value=self.format_datetime_timestamp(member.joined_at))
        else:
            embed.add_field(name="Sunucuya Giriş", value="Bilinmiyor")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def sunucubilgi(self, ctx):
        guild = ctx.guild
        roles = [role.name for role in guild.roles]
        embed = discord.Embed(title="Sunucu Bilgisi", colour=discord.Color.blurple())
        embed.add_field(name="İsim", value=guild.name)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Sahip", value=f"{guild.owner.name}#{guild.owner.discriminator}")
        embed.add_field(name="Sunucu Oluşturma Tarihi", value=guild.created_at.replace(microsecond=0))
        embed.add_field(name="Kanallar", value=str(len(guild.text_channels) + len(guild.voice_channels)))
        embed.add_field(name="Üyeler", value=guild.member_count)
        embed.add_field(name="Roller", value=str(len(roles)))
        if guild.icon:
            embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    @sunucubilgi.error
    async def sunucubilgi_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Bunu yapmaya yetkiniz yok!", delete_after=15)

    @commands.command()
    @commands.cooldown(rate = 2,per=300,type =  commands.BucketType.user)
    async def öneri(self,ctx,*,msg):
        """
        Gives any feedback about bot. Cooldown: 5 min
        For example, reporting bot, new idea/suggestions.
        A quicker way to get hold of owner without joining server.
        Sooner or later, bot may(not) contact you via PMS about status of your requests.
        Only able to make feedback once a five minute.
        """
        await ctx.message.delete()
        embed = discord.Embed()
        embed.set_author(name = ctx.message.author,icon_url=ctx.message.author.avatar_url or ctx.message.author.default_avatar_url)
        embed.add_field(name = "Sahibi",value = "**ID**:{0.id}".format(ctx.message))
        embed.add_field(name = "Sunucu",value = "**İsim**:{0.guild.name}\n**ID**:{0.guild.id}\n**Kanal**:{0.channel.name} - {0.channel.id}".format(ctx.message))
        embed.add_field(name = "Öneri",value = msg)

        channel = self.bot.get_channel(706913733951094884)
        await channel.send(embed=embed)
        await ctx.send(u"\U0001F44C"+", Değerli öneriniz için teşekkürler. \nEn kısa zamanda bu isteğiniz ile ilgileneceğiz.", delete_after=7)

    @commands.command(name="duyuru")
    @commands.has_permissions(manage_messages=True)
    async def announcement(self, ctx, *, message):
        await ctx.message.delete()

        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)

        embed.set_author(name="Duyuru!", icon_url=f'{ctx.guild.icon_url}')

        embed.add_field(name=f"Yayınlayan {ctx.message.author}", value=str(message))

        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(mod(bot))