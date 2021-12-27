import asyncio
import functools
import itertools
import math
import random
import discord

from random import randrange
from discord import utils
from discord.ext import commands

bot = commands.Bot('t.')

class general(commands.Cog):
    def __init__(self, ctx):
        return

    @commands.command()
    @commands.cooldown(rate=2, per=180.0, type=commands.BucketType.user)
    async def anket(self, ctx, *, pollInfo):
        emb = (discord.Embed(description=pollInfo, colour=0x7a28a3))
        emb.set_author(name=f"{ctx.message.author} Anketi", icon_url="https://lh3.googleusercontent.com/7ITYJK1YP86NRQqnWEATFWdvcGZ6qmPauJqIEEN7Cw48DZk9ghmEz_bJR2ccRw8aWQA=w300")
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        try:
            pollMessage = await ctx.send(embed=emb)
            await pollMessage.add_reaction("\N{THUMBS UP SIGN}")
            await pollMessage.add_reaction("\N{THUMBS DOWN SIGN}")
        except Exception as e:
            await ctx.send(f"Bir sorun var, ankete emoji ekleyemiyorum. Emoji eklemek için yetkimi kontrol et! ```py\n{e}```")

    @anket.error
    async def anketerror(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_roles:
                await ctx.reinvoke()
            else:
                msg = '🕛 Bu komutun kullanımı sınırlıdır, lütfen **{:.2f}** saniye içinde tekrar deneyin.'.format(error.retry_after)
                await ctx.send(msg, delete_after = 5)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
        show_avatar = discord.Embed(

            color = discord.Color.purple()        
    )
        show_avatar.set_image(url='{}'.format(member.avatar_url))
        await ctx.send(embed=show_avatar)

    @commands.command()
    async def yardım(self, ctx):

        embed=discord.Embed(title="Komut Grupları", colour=discord.Color.purple(), description='•t.yardım-genel > Genel komutları gönderir.\n•t.yardım-müzik > Müzik komutlarını gönderir.\n•t.yardım-eğlence > Eğlence komutlarını gönderir.\n•t.yardım-mod > Yetkili komutlarını gösterir.\n•t.yardım-ticket > Destek sistemi komutlarını gösterir.\n•t.yardım-seviye > Seviye sistemi komutlarını gösterir.\n•t.yardım-oto > Otomatik rol ve otomatik hoşgeldin mesajı hakkında bilgi verir.\n•t.yardım-bot > Bot yapımcısı ve destek sunucusu hakkında bilgi verir.\n\nNot: Özel mesajlarınız açık olmalıdır.')

        await ctx.send(embed=embed)

    @commands.command(name='yardım-genel')
    async def yardımgenel(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author

        embed = discord.Embed(title="📄 Genel Komutlar - Taluy Bot", colour=discord.Color.purple(),
            description="`t.avatar` Etiketlediğiniz kişinin avatarını gösterir.\n`t.kim` Etiketlediğiniz kişinin bilgilerini gösterir.\n`t.davet` Botu sunucunuza davet edebileceğiniz bir link gönderir.\n`t.anket` Anket düzenlemenizi sağlar.\n`t.oyver` Bota oy verebileceğiniz link gönderir.\n`t.öneri` Öneri mesajınızı bot geliştiricisine ulaştırır. `Örnek: t.öneri Bota şu...`\n`t.covid19-dünya` Dünyadaki Covid-19 vaka sayısını gösterir.\n`t.covid19-ülke` Ülkedeki Covid-19 vaka sayısını gösterir. `Örnek: t.covid19-ülke Turkey`")

        await ctx.send(f'Genel komutlar **özel mesaj** olarak gönderilmiştir. {ctx.message.author.mention}', delete_after=5)
        await author.send(embed=embed)

    @commands.command(name='yardım-müzik')
    async def yardımmusic(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author

        embed = discord.Embed(title="🎧 Müzik Komutları - Taluy Bot", colour=discord.Color.purple(),
            description="`t.oynat [ŞARKI ADI/LİNK]` İstediğiniz şarkıyı çalmanızı sağlar.\n`t.dur` Şarkıyı kapatır ve listeyi temizler.\n`t.sar` Şarkıyı **saniye** cinsinden belirttiğiniz zaman kadar ileri sarar.\n`t.geç` Şu an çalan şarkıyı geçebilirsiniz.\n`t.çalanşarkı` Şu an çalan şarkıyı görüntüleyebilirsiniz.\n`t.liste` Çalacak olan şarkıların listesini görebilirsiniz.\n`t.ses [1-100]` Çalan şarkının ses düzeyini ayarlayabilirsiniz.\n`t.dd` İlk yazdığınızda şarkıyı duraklatır tekrar yazdığınızda devam ettirir.\n`t.karıştır` Listedeki şarkıları karıştırır.\n`t.tekrar` Çalan şarkıyı tekrar eder. Tekrar yazarsanız tekrar sonlanır.\n`t.kaldır` Listeden numarası girilen şarkıyı kaldırır.\n`t.ara` YouTube üzerinden, girdiğiniz şarkıyı arar ve 10 sonuç listeler.\n`t.git` Botu kanaldan gönerir ve listeyi temizler.")

        await ctx.send(f'Müzik komutları **özel mesaj** olarak gönderilmiştir. {ctx.message.author.mention}', delete_after=5)
        await author.send(embed=embed)

    @commands.command(name='yardım-eğlence')
    async def yardımfun(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author

        embed = discord.Embed(title="🤪 Eğlence Komutları - Taluy Bot", colour=discord.Color.purple(),
            description="`t.yazıtura` Yazı tura atmanızı sağlar.\n`t.tkm` Taş, kağıt, makas oyunu oynarsınız.\n`t.kazıkazan 1` Kazı kazan oynamanızı sağlar.\n`t.zarat` Zar atmanızı sağlar.\n`t.1vs1` Etiketlediğiniz kişiyle düello yaparsınız.\n`t.doğruluk` Cevabı EVET ya da HAYIR olan bir soru sorun!\n`t.tokatla` Etiketlediğiniz kişiyi tokatlamanızı sağlar.\n`t.sarıl` Etiketlediğiniz kişiye sarılmanızı sağlar.\n`t.slot` Slot oyunu oynamanızı sağlar.\n`t.ters` Yazınızı tersten yazıp gönderir.\n`t.piyango` Piyango oynamanızı sağlar. **`Örnek: t.piyango 1 5 5`** \n`t.seç` Araya - koyarak bota seçtireceğiniz şıkları yazın.\n`t.keko` Yazdığınız yazıyı büyük küçük harflerle yazar.\n`t.yüz` Rastgele yüz karakterleri atar.\n`t.fbi` Etiketlediğiniz kişiye FBI yollar.\n`t.uçantekme` Etiketlediğiniz kişiye uçan tekme atarsınız.\n`t.öldür` Etiketlediğiniz kişiye suikast düzenlersiniz.\n`t.vpn` VPN bağlanma komutunu çalıştırır.\n`t.hack` Hacker gifi atar.\n`t.espri` Soğuk espri yapar.\n`t.boks` Boks makinesine vurursunuz.\n`t.ascii` Yazdığınız yazıyı ascii formatına dönüştürür.")

        await ctx.send(f'Eğlence komutları **özel mesaj** olarak gönderilmiştir. {ctx.message.author.mention}', delete_after=5)
        await author.send(embed=embed)

    @commands.command(name='yardım-mod')
    async def yardımmod(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author

        embed = discord.Embed(title="🔨 Moderasyon Komutları - Taluy Bot", colour=discord.Color.purple(),
            description="`t.ban` Etiketlediğiniz kullanıcıyı banlarsınız.\n`t.unban` Ban kaldırmanızı sağlar. `Örnek: t.unban Taluy#4934`\n`t.kick` Etiketlediğiniz kişiyi sunucudan atmanızı sağlar.\n`t.mute` Etiketlediğiniz kişiyi susturmanızı sağlar.\n`t.unmute` Etiketlediğiniz kişinin susturmasını kaldırır.\n`t.yavaşmod [1-120]` Kanala yazma süresini belirttiğiniz saniye kadar geciktirir.\n`t.temizle [1-500]` Belirttiğiniz kadar mesajı kanaldan siler.\n`t.rolal @kullanıcıadı [ROL ADI]` Belirttiğiniz rolü kullanıcıdan alır.\n`t.rolver @kullanıcıadı [ROL ADI]` Belirttiğiniz rolü kullanıcıya verir.\n`t.sunucubilgi` Sunucu hakkında bilgi verir.")

        await ctx.send(f'Yetkili komutları **özel mesaj** olarak gönderilmiştir. {ctx.message.author.mention}', delete_after=5)
        await author.send(embed=embed)

    @commands.command(name='yardım-ticket')
    async def yardımticket(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author

        embed = discord.Embed(title="🎟️ Destek Sistemi Komutları - Taluy Bot", colour=discord.Color.purple(),
            description="`t.destek` Destek talebi oluşturur.\n`t.kapat` Destek talebinizi kapatır.\n`t.erişimekle` Destek taleplerine erişebilecek rollerin ID'sini ekleyebilirsiniz.\n`t.erişimkaldır` Destek taleplerine erişimini keseceğinz rollerin ID'sini ekleyebilirsiniz.\n\n```Örnek:\nt.erişimekle 156165156114561\nt.erişimkaldır 156165156114561```")

        await ctx.send(f'Ticket komutları **özel mesaj** olarak gönderilmiştir. {ctx.message.author.mention}', delete_after=5)
        await author.send(embed=embed)

    @commands.command(name='yardım-seviye')
    async def yardımseviye(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author

        embed = discord.Embed(title="⭐ Seviye Komutları - Taluy Bot", colour=discord.Color.purple(),
            description="`t.seviye` Sizin veya etiketlediğiniz kişinin seviyesini gösterir.\n`t.lidertablosu` Sunucudaki en yüksek seviyeye sahip 5 kişiyi gösterir.")

        await ctx.send(f'Seviye komutları **özel mesaj** olarak gönderilmiştir. {ctx.message.author.mention}', delete_after=5)
        await author.send(embed=embed)

    @commands.command(name='yardım-oto')
    async def yardımoto(self, ctx):
        await ctx.message.delete()
        author = ctx.message.author

        embed = discord.Embed(title="💡 Otomatik Sunucu Komutları - Taluy Bot", colour=discord.Color.purple(),
            description="```Otomatik Hoşgeldin Mesajı\nSistemin çalışması için sunucunuzda ismi 'hoşgeldiniz' olan bir yazı kanalı oluşturun. Ardından sistem otomatik olarak çalışacaktır.```\n```Otomatik Rol Verme\nSistemin çalışması için tek yapmanız gereken 'Yeni Üye' adında bir rol oluşturmak. Ardından sistem otomatik olarak çalışacaktır.``` ")

        await ctx.send(f'Otomatik sunucu komutları **özel mesaj** olarak gönderilmiştir. {ctx.message.author.mention}', delete_after=5)
        await author.send(embed=embed)

    @commands.command(name='yardım-bot')
    async def yardımbot(self, ctx):
        embed = discord.Embed(title="Yardım mı lazım?", description="Taluy Bot destek sunucusu ve geliştiricisi iletişim bilgileri.", colour=discord.Color.blurple(), url="https://discord.gg/Cw9Dqu3")

        embed.add_field(name="Geliştirici", value="<@295475608169873411>")
        embed.add_field(name="Destek Sunucusu", value="https://discord.gg/Cw9Dqu3")

        await ctx.send(embed=embed)

    @commands.command()
    async def oyver(self, ctx):
        oylink = "https://top.gg/bot/614537710945697816/vote"
        embed = discord.Embed(title="Oy Ver", colour=discord.Color.purple(), description=f"**[Buraya]({oylink})** tıklayarak bota her 12 saatte bir oy verebilirsin!")
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def davet(self, ctx):
        davetlink = "https://discordapp.com/oauth2/authorize?client_id=614537710945697816&scope=bot&permissions=8"
        embed = discord.Embed(title="Sunucuna Ekle", colour=discord.Color.purple(), description=f"**[Buraya]({davetlink})** tıklayarak Taluy Bot'u sunucunuza ekleyebilirsiniz!")
        embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(general(bot))