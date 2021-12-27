import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import asyncio

bot = commands.Bot('tt.')
keys = []

class ticket(commands.Cog):
    def __init__(self, ctx):
        return

    @commands.command(pass_context=True)
    async def destek(self, ctx, *, args = None):

        if args == None:
            message_content = "Lütfen yardım almak istediğiniz konuyu açıklayın."
    
        else:
            message_content = "".join(args)

        with open("data/ticket.json") as f:
            data = json.load(f)

        ticket_number = int(data["ticket-counter"])
        ticket_number += 1

        ticket_channel = await ctx.guild.create_text_channel("destek-{}".format(ticket_number))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

        for role_id in data["valid-roles"]:
            role = ctx.guild.get_role(role_id)

            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

        em = discord.Embed(title="Yeni Destek Talebi {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)

        await ticket_channel.send(embed=em)
        await ticket_channel.send(f'{ctx.message.author.mention}')

        pinged_msg_content = ""
        non_mentionable_roles = []

        if data["pinged-roles"] != []:

            for role_id in data["pinged-roles"]:
                role = ctx.guild.get_role(role_id)

                pinged_msg_content += role.mention
                pinged_msg_content += " "

                if role.mentionable:
                    pass
                else:
                    await role.edit(mentionable=True)
                    non_mentionable_roles.append(role)
        
            await ticket_channel.send(pinged_msg_content)

            for role in non_mentionable_roles:
                await role.edit(mentionable=False)
    
        data["ticket-channel-ids"].append(ticket_channel.id)

        data["ticket-counter"] = int(ticket_number)
        with open("data/ticket.json", 'w') as f:
            json.dump(data, f)
    
        #created_em = discord.Embed(title="Taluy Destek Sistemi", description="Destek talebiniz başarıyla oluşturuldu **" + ctx.author.display_name + "** {}".format(ticket_channel.mention), color=0x00a8ff)
    
        #await ctx.send(embed=created_em, delete_after=5)
        await ctx.message.delete()

    @commands.command()
    async def kapat(self, ctx):
        with open('data/ticket.json') as f:
            data = json.load(f)

        if ctx.channel.id in data["ticket-channel-ids"]:

            channel_id = ctx.channel.id

            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data/ticket.json', 'w') as f:
                json.dump(data, f)

    @commands.command()
    async def erişimekle(self, ctx, role_id=None):

        with open('data/ticket.json') as f:
            data = json.load(f)
    
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
    
        if valid_user or ctx.author.guild_permissions.administrator:
            role_id = int(role_id)

            if role_id not in data["valid-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    with open("data/ticket.json") as f:
                        data = json.load(f)

                    data["valid-roles"].append(role_id)

                    with open('data/ticket.json', 'w') as f:
                        json.dump(data, f)
                
                    em = discord.Embed(title="Taluy Destek Sistemi", description="`{}` rolünü başarıyla destek sistemine erişmesi için eklediniz.".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(title="Taluy Destek Sistemi", description="Girdiğiniz ID herhangi bir rol ile eşleşmiyor. Lütfen doğru ID girin.")
                    await ctx.send(embed=em)
        
            else:
                em = discord.Embed(title="Taluy Destek Sistemi", description="Bu role zaten erişim yetkisi verilmiş!", color=0x00a8ff)
                await ctx.send(embed=em)
    
        else:
            em = discord.Embed(title="Taluy Destek Sistemi", description="Üzgünüm, komutu çalıştırmak için yetkiniz yok.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.command()
    async def erişimkaldır(self, ctx, role_id=None):
        with open('data/ticket.json') as f:
            data = json.load(f)
    
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)

                with open("data/ticket.json") as f:
                    data = json.load(f)

                valid_roles = data["valid-roles"]

                if role_id in valid_roles:
                    index = valid_roles.index(role_id)

                    del valid_roles[index]

                    data["valid-roles"] = valid_roles

                    with open('data/ticket.json', 'w') as f:
                        json.dump(data, f)

                    em = discord.Embed(title="Taluy Destek Sistemi", description="`{}` rolünün destek sistemine erişimini başarıyla kestiniz.".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)
            
                else:
                
                    em = discord.Embed(title="Taluy Destek Sistemi", description="Bu rolün zaten destek sistemine erişimi yok!", color=0x00a8ff)
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Taluy Destek Sistemi", description="Girdiğiniz ID herhangi bir rol ile eşleşmiyor. Lütfen doğru ID girin.")
                await ctx.send(embed=em)
    
        else:
            em = discord.Embed(title="Taluy Destek Sistemi", description="Üzgünüm, komutu çalıştırmak için yetkiniz yok.", color=0x00a8ff)
            await ctx.send(embed=em)

    """@commands.command()
    async def bildirimrolüekle(self, ctx, role_id=None):

        with open('data.json') as f:
            data = json.load(f)
    
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
    
        if valid_user or ctx.author.guild_permissions.administrator:

            role_id = int(role_id)

            if role_id not in data["pinged-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    with open("data.json") as f:
                        data = json.load(f)

                    data["pinged-roles"].append(role_id)

                    with open('data.json', 'w') as f:
                        json.dump(data, f)

                    em = discord.Embed(title="Taluy Destek Sistemi", description="`{}` rolünü yeni destek talebi oluşturulduğunda bildirim alması için başarıyla eklediniz!".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(title="Taluy Destek Sistemi", description="Girdiğiniz ID herhangi bir rol ile eşleşmiyor. Lütfen doğru ID girin.")
                    await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title="Taluy Destek Sistemi", description="Bu rol zaten destek talepleri oluşturulduğunda bildirim alıyor!", color=0x00a8ff)
                await ctx.send(embed=em)
    
        else:
            em = discord.Embed(title="Taluy Destek Sistemi", description="Üzgünüm, komutu çalıştırmak için yetkiniz yok.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.command()
    async def bildirimrölükaldır(self, ctx, role_id=None):

        with open('data.json') as f:
            data = json.load(f)
    
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
    
        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                pinged_roles = data["pinged-roles"]

                if role_id in pinged_roles:
                    index = pinged_roles.index(role_id)

                    del pinged_roles[index]

                    data["pinged-roles"] = pinged_roles

                    with open('data.json', 'w') as f:
                        json.dump(data, f)

                    em = discord.Embed(title="Taluy Destek Sistemi", description="`{}` rolünü yeni destek talebi oluşturulduğunda bildirim almaması için başarıyla listeden kaldırdınız!".format(role.name), color=0x00a8ff)
                    await ctx.send(embed=em)
            
                else:
                    em = discord.Embed(title="Taluy Destek Sistemi", description="Bu rol zaten destek talebi oluşturulduğunda bildirim almıyor!", color=0x00a8ff)
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Taluy Destek Sistemi", description="Girdiğiniz ID herhangi bir rol ile eşleşmiyor. Lütfen doğru ID girin.")
                await ctx.send(embed=em)
    
        else:
            em = discord.Embed(title="Taluy Destek Sistemi", description="Üzgünüm, komutu çalıştırmak için yetkiniz yok.", color=0x00a8ff)
            await ctx.send(embed=em)"""        

def setup(bot):
    bot.add_cog(ticket(bot))