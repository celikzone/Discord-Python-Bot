import asyncio
import functools
import itertools
import math
import random
import discord
import aiohttp
from datetime import datetime

from random import randrange, choice, randint
from discord import utils
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, ctx):
        return
        

    @commands.command(pass_context=True, aliases=['seç'])
    async def choose(self, ctx, *, choices: str):
        """Choose randomly from the options you give. [p]choose this | that"""
        await ctx.send('Seçimim: ``{}``'.format(random.choice(choices.split("-"))))

    @commands.command(aliases=['piyango'])
    @commands.cooldown(rate=2, per=30.0, type=commands.BucketType.user)
    async def lottery(self, ctx, *, guesses):
        '''Enter the lottery and see if you win!'''
        author = ctx.author
        numbers = []
        for x in range(3):
            numbers.append(random.randint(1, 5))

        mesaj = ('Sayılarınız **1 ile 5** arasında, **3 adet** ve arasında **boşluk** olmalıdır. **`Örnek: t.piyango 2 3 5`**')
        split = guesses.split(' ')
        if len(split) != 3:
            return await ctx.send(mesaj, delete_after = 25)

        string_numbers = [str(i) for i in numbers]
        if split[0] == string_numbers[0] and split[1] == string_numbers[1] and split[2] == string_numbers[2]:
            await ctx.send(f'{author.mention} Kazandın! Piyangoyu kazandığınız için tebrikler. 🎉')
        else:
            await ctx.send(f"{author.mention} Bir dahaki sefere... Piyangoyu kaybeden onlarca kişiden birisin...\nNumaralar şunlardı: `{', '.join(string_numbers)}` 😢")

    @lottery.error
    async def lottery_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command()
    async def yazıtura(self, ctx):
        choices = ["**Yazı**", "**Tura**"]
        rancoin = random.choice(choices)
        await ctx.send('🔄 {} geldi!'.format(rancoin))

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def kazıkazan(self, ctx, *args):

        if int(args[0]) > 1:
            await ctx.send('Tek seferde 1\'den fazla kullanamazsınız!')
        else:
            await ctx.send('Kartınız kazınıyor...')
            await asyncio.sleep(2)
            for i in range(int(args[0])):
                unbox_chance = random.random()
                if unbox_chance <= .00001:
                    await ctx.send(f"{ctx.message.author.mention} 💰 1.000.000 TL")
                elif unbox_chance < .0001:
                    await ctx.send(f"{ctx.message.author.mention} 💰 500.000 TL")
                elif unbox_chance < .0002:
                    await ctx.send(f"{ctx.message.author.mention} 💰 250.000 TL")
                elif unbox_chance < .006:
                    await ctx.send(f"{ctx.message.author.mention} 💰 100.000 TL")
                elif unbox_chance < .008:
                    await ctx.send(f"{ctx.message.author.mention} 💰 50.000 TL")
                elif unbox_chance < .01:
                    await ctx.send(f"{ctx.message.author.mention} 💰 20.000 TL")
                elif unbox_chance < .03:
                    await ctx.send(f"{ctx.message.author.mention} 💰 12.000 TL")
                elif unbox_chance < .05:
                    await ctx.send(f"{ctx.message.author.mention} 💰 2.500 TL")
                elif unbox_chance < .07:
                    await ctx.send(f"{ctx.message.author.mention} 💰 1.000 TL")
                elif unbox_chance < .09:
                    await ctx.send(f"{ctx.message.author.mention} 💰 500 TL")
                elif unbox_chance < .1:
                    await ctx.send(f"{ctx.message.author.mention} 💰 100 TL")
                elif unbox_chance < .2:
                    await ctx.send(f"{ctx.message.author.mention} 💰 10 TL")
                else:
                    await ctx.send(f"{ctx.message.author.mention} 💰 1 TL")

    @kazıkazan.error
    async def kazıkazan_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command()
    async def zarat(self, ctx):
	    await ctx.send(f"{ctx.message.author.mention}: [**{randrange(1, 7)}**][**{randrange(1, 7)}**] attın!")

    @commands.command()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def tokatla(self, ctx, *, member: discord.Member = None):
	    if member is None:
		    embed = discord.Embed(color=discord.Color.purple(), title="Tokatlanacak kimse yok! 🙄", description="Tokatlamak için birisini etiketlemelisin.")
		    embed.set_thumbnail(url="https://i.imgur.com/6YToyEF.png")
		    await ctx.send(embed=embed)
	    elif member.id == ctx.message.author.id:
		    embed = discord.Embed(title="Kendini mi? 🤔", description="Seni tokatlayamam çünkü sen benim arkadaşımsın.", color=discord.Color.purple())
		    embed.set_image(url="http://4.bp.blogspot.com/-FL6mKTZOk94/UBb_9EuAYNI/AAAAAAAAOco/JWsTlyInMeQ/s400/Jean+Reno.gif")
		    await ctx.send(embed=embed)
	    else:
		    embed = discord.Embed(title="Tokatlandı!", description=f"**{ctx.author} tokatladı {member}**", color=discord.Color.purple())
		    embed.set_image(url="https://thumbs.gfycat.com/RepentantInbornGoldenmantledgroundsquirrel-size_restricted.gif")
		    await ctx.send(embed=embed)

    @tokatla.error
    async def tokatla_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command()
    async def ters(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"↪️ {t_rev}")

    @commands.command(aliases=['slot'])
    @commands.cooldown(rate=1, per=15.0, type=commands.BucketType.user)
    async def slotmch(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.message.author.mention}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} Hepsi eşleşti, kazandın! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} İki tane eşleşti, kazandın! 🎉")
        else:
            await ctx.send(f"{slotmachine} Eşleşme yok, kaybettin! 😢")

    @slotmch.error
    async def slot_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)
        
        else:
            raise error

    @commands.command()
    async def sarıl(self, ctx, *, member: discord.Member = None):
	    if member is None:
		    await ctx.send(f"{ctx.message.author.mention} kendi kendine sarıldı! 💝")
	    elif member.id == ctx.message.author.id:
		    await ctx.send(f"{ctx.message.author.mention} birbirlerine sarıldılar çünkü yalnızlar! 👬")
	    else:
		    await ctx.send(f"{ctx.message.author.mention} sana kocaman sarıldı! {member.mention} 💝")

    @commands.command(name='doğruluk')
    async def doğruluk(self, ctx, *, msg):
        '''You gotta tell me a question and I will answer it if it is True or False.'''

        cha = random.choice(['%100 Haklısın',
                             'Şimdi söylemesem daha iyi',
                             'Dışarıdan iyi görünüyor',
                             'Hayır',
                             'Pek iyi görünmüyor',
                             'Çok şüpheli',
                             'Yanıtım hayır',
                             'Biraz belirsiz, tekrar dene',
                             'Evet, elbette',
                             'Belirtiler olduğu yönünde',
                             'Kesinlikle öyle',
                             'Konsantre ol ve öyle sor',
                             'Büyük ihtimalle',
                             'İşaretler eveti gösteriyor',
                             'Buna güvenebilirsiniz',
                             '👍',
                             '👎'])
        embed = discord.Embed(title='Doğruluk Makinesi', description=f'Soru: {msg} \n Cevap: {cha}', color=0x550a8a)
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['keko'])
    async def drunkify(self, ctx, *, s):
        lst = [str.upper, str.lower]
        newText = await commands.clean_content().convert(ctx, ''.join(random.choice(lst)(c) for c in s))
        if len(newText) <= 380:
            await ctx.send(newText)
        else:
            try:
                await ctx.author.send(newText)
                await ctx.send(f"{ctx.author.mention} Yazı çok uzun, sana özel mesaj olarak gönderdim! :mailbox_with_mail:")
            except Exception:
                await ctx.send(f"{ctx.author.mention} Bir sorun var, lütfen daha sonra deneyin.")

    @commands.command(name='yüz')
    @commands.guild_only()
    async def lenny(self, ctx):
        faces = (
            "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "( ͡~ ͜ʖ ͡°)", "( ͡ʘ ͜ʖ ͡ʘ)", "( ͡o ͜ʖ ͡o)", "(° ͜ʖ °)", "( ‾ʖ̫‾)",
            "( ಠ ͜ʖಠ)",
            "( ͡° ʖ̯ ͡°)", "( ͡ಥ ͜ʖ ͡ಥ)", "༼  ͡° ͜ʖ ͡° ༽", "(▀̿Ĺ̯▀̿ ̿)", "( ✧≖ ͜ʖ≖)", "(ง ͠° ͟ل͜ ͡°)ง",
            "(͡ ͡° ͜ つ ͡͡°) ",
            "[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅])", "(✿❦ ͜ʖ ❦)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡° ͜ʖ ͡°)╭∩╮",
            "(╯ ͠° ͟ʖ ͡°)╯┻━┻)", "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)", "ಠ_ಠ")
        await ctx.send(content=f"{random.choice(faces)}")

    @commands.command(name="fbi", help="FBI, OPEN UP!", usage="<@user>")
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def swat(self, ctx, member: discord.Member):
        await ctx.send(f"FBI **{member.name}** adlı üyeye gönderiliyor, lütfen bekleyin...")
        await asyncio.sleep(1)
        embed = discord.Embed(title=None,
                              description="Polis departmanı yasaklı sitelere girdiğinizi tespit etti!",
                              color=discord.Color.green(), timestamp=datetime.utcnow())
        embed.set_image(url="https://media.tenor.com/images/a1912e38f72c5df9050d931853fafddb/tenor.gif")
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        #embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(content=None, embed=embed)

    @swat.error
    async def swat_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command(name="uçantekme", usage="<@user>")
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def dropkick(self, ctx, member: discord.Member):
        embed = discord.Embed(title=None,
                              description=f"**{member.name}** uçan tekme yedi!",
                              color=discord.Color.green(), timestamp=datetime.utcnow())
        embed.set_image(url="https://media.giphy.com/media/mFulmRSjkW9by/source.gif")
        #embed.set_image(url="https://media.giphy.com/media/YD0sJDzEgueXK/source.gif")
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(content=None, embed=embed)

    @dropkick.error
    async def dropkick_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command(name="öldür", usage="<@user>")
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def kill(self, ctx, member: discord.Member):
        random_int = random.randint(1, 1000)
        if member == ctx.author:
            if 1 <= random_int <= 500:
                embed = discord.Embed(title=None,
                                      description=f"İntihar ettin!",
                                      color=discord.Color.green(), timestamp=datetime.utcnow())
                embed.set_image(url="https://media1.tenor.com/images/1547113c4d7cbfe1b6d41b4211edf096/tenor.gif")
                embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                return await ctx.send(content=None, embed=embed)
            else:
                embed = discord.Embed(title=None,
                                      description=f"Kendini öldürmeye çalıştın!",
                                      color=discord.Color.green(), timestamp=datetime.utcnow())
                embed.set_image(url="https://media1.tenor.com/images/e349f19d4c0f48abf4a8cdfceb3bf151/tenor.gif")
                embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                return await ctx.send(content=None, embed=embed)

        if 1 <= random_int <= 500:
            embed = discord.Embed(title=None,
                                  description=f"**{member.name}** adlı üyeyi öldürmeye çalıştın ama saldırıdan kaçmayı başardı!",
                                  color=discord.Color.green(), timestamp=datetime.utcnow())
            embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(content=None, embed=embed)
        else:
            embed = discord.Embed(title=None,
                                  description=f"**{member.name}** adlı üye **{ctx.author.name}** tarafından öldürüldü!",
                                  color=discord.Color.green(), timestamp=datetime.utcnow())
            embed.set_image(url="https://media.giphy.com/media/jaDfrTlGwiMX6/source.gif")
            embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(content=None, embed=embed)

    @kill.error
    async def kill_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command(name="vpn")
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def vpn(self, ctx):
        countries = ("Rusya", "Kuzey Kore", "Almanya", "Çin", "Kanada", "Ukrayna")
        country = random.choice(countries)
        message = await ctx.send(content=f"VPN için **{country}** ülkesine bağlanılıyor.")
        await asyncio.sleep(1)
        await message.edit(content=f"Güvenli sunucuya bağlanılıyor **{country}** .")
        await asyncio.sleep(1)
        await message.edit(content=f"Güvenli sunucuya bağlanılıyor **{country}** ..")
        await asyncio.sleep(1)
        await message.edit(content=f"Güvenli sunucuya bağlanılıyor **{country}** ...")
        await asyncio.sleep(1)
        await message.edit(content=f"Güvenli sunucuya bağlanılıyor **{country}** ....")
        await asyncio.sleep(1)
        await message.edit(content=f"Güvenli sunucuya bağlanılıyor **{country}** .....")
        await asyncio.sleep(1)
        await ctx.send(content="Bağlandı!")

    @vpn.error
    async def vpn_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command(name="hack")
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def hack(self, ctx):
        gifs = ("https://media.giphy.com/media/YQitE4YNQNahy/source.gif",
                "https://media.giphy.com/media/eCqFYAVjjDksg/source.gif")
        embed = discord.Embed(title=None,
                              description=None,
                              color=discord.Color.green(), timestamp=datetime.utcnow())
        embed.set_image(url=random.choice(gifs))
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(content=None, embed=embed)

    @hack.error
    async def hack_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command(name='espri')
    @commands.cooldown(rate=1, per=15.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def espri(self, ctx):
        espri = (
            "i run each teen me?\n-i run each team.", "Uzun lafın kısası\n-U.L.", "Seven unutmaz oğlum.\n-Eight unutur.", "Yangın dolabını açarsan nolur?\n-Yang gelir kapatır.", "Sen kamyonu al.\n-Leonardo da vinci.", "Bill Gates neden grip olmuş?\n-Windows açık kalmış da ondan…", "Volkswagen Passat\n-Bencil oynama.",
            "Çekyata niye çekyat denir?\n-Çünkü itotur diyemeyiz.",
            "Pişmemiş burgere ne denir?\n-Hamburger.", "Terazi ile diş macunu arasındaki fark nedir?\n-Biri tartar öbürü anti tartar.", "En çok eşek yavrusu nerede olur?\n-Spa merkezinde.", "Neden Fransızlar?\n-Fran'ı bilmem ama ben sızlamam.", "Tesla Mars'ta restoran açmış?\n-Herşey güzel ama atmosfer pek yok.",
            "Blade'in karısı Blade için hangi şarkıyı söylemiş?\n-Bileydim senin için ağlar mıydım? Bileydiiim bileydim...")
        await ctx.send(content=f"{random.choice(espri)}")

    @espri.error
    async def espri_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command(name="boks")
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    @commands.guild_only()
    async def box(self, ctx):
        random_int = random.randint(1, 8000)
        if 1 <= random_int <= 8000:
            embed = discord.Embed(title=None,
                                    description=f"Boks Makinesi",
                                    color=discord.Color.green(), timestamp=datetime.utcnow())
            embed.set_image(url="https://media.giphy.com/media/l2JhDTLBnmolcdYGI/giphy.gif")
            embed.add_field(name='Skor', value=(random_int))
            embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            return await ctx.send(content=None, embed=embed)

    @box.error
    async def box_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command(name='1vs1')
    @commands.cooldown(rate=1, per=180.0, type=commands.BucketType.user)
    async def fight(self, ctx, user: discord.User):
        battleAnnounce = discord.Embed(title="" + ctx.author.display_name + " tarafından " + user.display_name + "  adlı kullanıcıya meydan okundu!",
                                       description="**Kazanan kim olacak?**", color=discord.Color.blurple())
        battleAnnounce.set_thumbnail(url="https://assets.faceit-cdn.net/hubs/avatar/1a0c85d3-4eca-43ec-b877-e4db5647adb6_1551279832161.jpg")
        await ctx.send(embed=battleAnnounce)
        if ctx.author == user:
            await ctx.send(embed=discord.Embed(color=discord.Color.blurple(), description="**" + user.display_name + "** " + choice(["talihsiz bir kaza sonucu...",
                                                                                                                                                   "kendisine sapladığı bıçak sebebiyle...",
                                                                                                                                                   "yediği dayak yüzünden...",
                                                                                                                                                   "kaynamış kazana düşerek...",
                                                                                                                                                   "C4 patlayıcı ile oynarken...",
                                                                                                                                                   "kendini kaybetti ve..."])))
            return

        p1_hp = 20
        p2_hp = 20
        await ctx.send(embed=discord.Embed(title="" + ctx.author.display_name + ": " + str(p1_hp) + "  ❤️ <|> " + user.display_name + ": " + str(p2_hp) + " ❤️", color=discord.Color.blurple()))
        while p1_hp > 0 and p2_hp > 0:
            await asyncio.sleep(2.5)
            p2_hp -= randint(2, 12) # Player 1's turn
            p1_hp -= randint(5, 12) # Player 2's turn
            if ctx.author.id == 639498607632056321:
                p2_hp -= 7
            if user.id == 639498607632056321:
                p1_hp -= 7

            if p2_hp < 0:
                p2_hp = 0

            if p1_hp < 0:
                p1_hp = 0

            if p2_hp <= 0:
                p2_hp = 0
                if p1_hp <= 0:
                    p1_hp = 1
                await ctx.send(embed=discord.Embed(title="" + ctx.author.display_name + ": " + str(p1_hp) + "  ❤️ <|> " + user.display_name + ": " + str(p2_hp) + " ❤️", color=discord.Color.blurple()))
                win = discord.Embed(title="Muhteşem **" + ctx.author.display_name + " **tarafından **" + user.display_name + "** adlı kullanıcı bozguna uğratıldı!", color=discord.Color.blurple())
                win.set_thumbnail(url=str(ctx.author.avatar_url))
                await ctx.send(embed=win)
            elif p1_hp <= 0:
                p1_hp = 0
                if p2_hp <= 0:
                    p2_hp = 1
                await ctx.send(embed=discord.Embed(title="" + ctx.author.display_name + ": " + str(p1_hp) + "  ❤️ <|> " + user.display_name + ": " + str(p2_hp) + " ❤️", color=discord.Color.blurple()))
                win = discord.Embed(title="Muhteşem **" + user.display_name + " **tarafından **" + ctx.author.display_name + "** adlı kullanıcı bozguna uğratıldı!", color=discord.Color.blurple())
                win.set_thumbnail(url=str(user.avatar_url))
                await ctx.send(embed=win)
            else:
                await ctx.send(embed=discord.Embed(title="" + ctx.author.display_name + ": " + str(p1_hp) + "  ❤️ <|> " + user.display_name + ": " + str(p2_hp) + " ❤️", color=discord.Color.blurple()))

    @fight.error
    async def fight_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command()
    @commands.cooldown(rate=1, per=15.0, type=commands.BucketType.user)
    async def tkm(self, ctx, choice: str = ""):
        """Play a game of rock paper scissors."""
        options = {
            "t": "taş",
            "k": "kağıt",
            "m": "makas"
        }

        if choice == "":
            embed = discord.Embed(title='Lütfen birini seçin: taş, kağıt, makas',
                                  color=discord.Color.red())
            m = await ctx.channel.send(embed=embed)

            def validate(m_):
                return m_.author == ctx.author and m_.channel == ctx.channel

            try:
                choice = await ctx.bot.wait_for('message', check=validate,
                                                timeout=60)
                choice = choice.content
            except asyncio.TimeoutError:
                return await m.delete()

        player = choice.lower()

        bot = random.choice(list(options.values()))

        if player == bot:
            color = discord.Color.dark_grey()
            message = "Berabere!"
        elif player == "taş":
            if bot == "kağıt":
                color = discord.Color.red()
                message = f"Kaybettin! {bot} sardı {player}"
            else:
                color = discord.Color.green()
                message = f"Kazandın! {player} ezdi {bot}"
        elif player == "kağıt":
            if bot == "makas":
                color = discord.Color.red()
                message = f"Kaybettin! {bot} kesti {player}"
            else:
                color = discord.Color.green()
                message = f"Kazandın! {player} sardı {bot}"
        elif player == "makas":
            if bot == "taş":
                color = discord.Color.red()
                message = f"Kaybettin! {bot} ezdi {player}"
            else:
                color = discord.Color.green()
                message = f"Kazandın! {player} kesti {bot}"

        embed = discord.Embed(title=message,
                              color=color)
        await ctx.channel.send(embed=embed)

    @tkm.error
    async def tkm_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command()
    @commands.cooldown(rate=1, per=600.0, type=commands.BucketType.user)
    async def ascii(self, ctx, *, text):
        """Turn text into fancy ascii art."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://artii.herokuapp.com/make?text={text}") as response:
                content = await response.text()

        await ctx.send(f"```\n{content}\n```")

    @ascii.error
    async def ascii_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command()
    @commands.cooldown(rate=1, per=1800.0, type=commands.BucketType.user)
    async def mayıntarlası(self, ctx):
        field00 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field01 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field02 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field03 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field04 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field05 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field06 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field07 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field08 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        field10 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field11 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field12 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field13 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field14 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field15 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field16 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field17 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field18 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        field20 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field21 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field22 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field23 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field24 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field25 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field26 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field27 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field28 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        field30 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field31 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field32 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field33 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field34 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field35 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field36 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field37 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field38 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        field40 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field41 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field42 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field43 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field44 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field45 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field46 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field47 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field48 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        field50 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field51 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field52 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field53 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field54 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field55 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field56 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field57 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field58 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        field60 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field61 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field62 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field63 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field64 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field65 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field66 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field67 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field68 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        field70 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field71 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field72 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field73 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field74 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field75 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field76 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field77 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field78 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        field80 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field81 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field82 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field83 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field84 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field85 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field86 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field87 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])
        field88 = random.choice(['1️⃣', '2️⃣', '3️⃣', '💥'])

        minesweeper = f"""
        || {field00} || || {field10} || || {field20} || || {field30} || || {field40} || || {field50} || || {field60} || || {field70} || || {field80} ||
        || {field01} || || {field11} || || {field21} || || {field31} || || {field41} || || {field51} || || {field61} || || {field71} || || {field81} ||
        || {field02} || || {field12} || || {field22} || || {field32} || || {field42} || || {field52} || || {field62} || || {field72} || || {field82} ||
        || {field03} || || {field13} || || {field23} || || {field33} || || {field43} || || {field53} || || {field63} || || {field73} || || {field83} ||
        || {field04} || || {field14} || || {field24} || || {field34} || || {field44} || || {field54} || || {field64} || || {field74} || || {field84} ||
        || {field05} || || {field15} || || {field25} || || {field35} || || {field45} || || {field55} || || {field65} || || {field75} || || {field85} ||
        || {field06} || || {field16} || || {field26} || || {field36} || || {field46} || || {field56} || || {field66} || || {field76} || || {field86} ||
        || {field07} || || {field17} || || {field27} || || {field37} || || {field47} || || {field57} || || {field67} || || {field77} || || {field87} ||
        || {field08} || || {field18} || || {field28} || || {field38} || || {field48} || || {field58} || || {field68} || || {field78} || || {field88} ||
        """

        await ctx.send(f'{minesweeper}')

    @mayıntarlası.error
    async def mayıntarlası_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    


def setup(bot):
    bot.add_cog(Fun(bot))
