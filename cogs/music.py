import math
import re

import discord
import lavalink
from discord.ext import commands

url_rx = re.compile('https?:\\/\\/(?:www\\.)?.+')  # noqa: W605


class Music(commands.Cog):
    """Music Time"""

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('localhost', 2333, 'cool61pass', 'eu', 'TaluyBot')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voice channel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(aliases=['oynat'])
    async def play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Bir şey bulunamadı!')

        embed = discord.Embed(color=discord.Color.blurple())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = '🎵 Playlist Eklendi'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = '🎵 Şarkı Eklendi'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['sar'])
    async def seek(self, ctx, *, seconds: int):
        """ Seeks to a given position in a track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)

        await ctx.send(f'Şarkı bu süreye alındı: **{lavalink.utils.format_time(track_time)}**')

    @commands.command(aliases=['geç'])
    async def skip(self, ctx):
        """ Skips the current track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Hiçbir şey çalmıyor.')

        await player.skip()
        await ctx.send('⏭ | Şarkı geçildi.')

    @commands.command(aliases=['dur'])
    async def stop(self, ctx):
        """ Stops the player and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Hiçbir şey çalmıyor.')

        player.queue.clear()
        await player.stop()
        await ctx.send('⏹ | Şarkı durduruldu.')

    @commands.command(aliases=['çalanşarkı'])
    async def now(self, ctx):
        """ Shows some stats about the currently playing song. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.current:
            return await ctx.send('Hiçbir şey çalmıyor.')

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 ÇALAN ŞARKI'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(color=discord.Color.blurple(),
                              title='Şimdi Çalan', description=song)
        await ctx.send(embed=embed)

    @commands.command(aliases=['liste'])
    async def queue(self, ctx, page: int = 1):
        """ Shows the player's queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('Listede şarkı yok.')

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=discord.Color.blurple(),
                              description=f'**{len(player.queue)} Şarkı**\n\n{queue_list}')
        embed.set_footer(text=f'Gösterilen sayfa {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['dd'])
    async def pause(self, ctx):
        """ Pauses/Resumes the current track. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Hiçbir şey çalmıyor.')

        if player.paused:
            await player.set_pause(False)
            await ctx.send('⏯ | Devam Ediyor')
        else:
            await player.set_pause(True)
            await ctx.send('⏯ | Durduruldu')

    @commands.command(aliases=['ses'])
    async def volume(self, ctx, volume):
        """ Changes the player's volume (0-1000). """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        try:
            volume = int(volume)
        except:
            volume = int(volume[:-1])

        if not volume:
            return await ctx.send(f'🔈 | %{player.volume}')

        await player.set_volume(volume)  # Values are automatically capped between, or equal to 0-1000.
        await ctx.send(f'🔈 | Ses %{player.volume} seviyesine getirildi.')

    @commands.command(aliases=['karıştır'])
    async def shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Hiçbir şey çalmıyor.')

        player.shuffle = not player.shuffle
        await ctx.send('🔀 | Karıştırma ' + ('aktif' if player.shuffle else 'pasif'))

    @commands.command(aliases=['tekrar'])
    async def repeat(self, ctx):
        """ Repeats the current song until the command is invoked again. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Hiçbir şey çalmıyor.')

        player.repeat = not player.repeat
        await ctx.send('🔁 | Tekrar ' + ('aktif' if player.repeat else 'pasif'))

    @commands.command(aliases=['kaldır'])
    async def remove(self, ctx, index: int):
        """ Removes an item from the player's queue with the given index. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('Listede şarkı yok.')

        if index > len(player.queue) or index < 1:
            return await ctx.send(f'Girilen değer 1 ve {len(player.queue)} **arasında** olmalıdır.')

        removed = player.queue.pop(index - 1)  # Account for 0-index.

        await ctx.send(f'**{removed.title}** adlı şarkı listeden kaldırıldı.')

    @commands.command(aliases=['ara'])
    async def find(self, ctx, *, query):
        """ Lists the first 10 search results from a given query. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Hiçbir şey bulunamadı.')

        tracks = results['tracks'][:10]  # First 10 results

        o = ''
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            o += f'`{index}.` [{track_title}]({track_uri})\n'

        embed = discord.Embed(color=discord.Color.blurple(), description=o)
        await ctx.send(embed=embed)

    @commands.command(aliases=['git'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Bağlı değilim.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('Aynı ses kanalında değiliz!')

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | Bağlantı kesildi.')

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voice channel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.

        should_connect = ctx.command.name in ('play')  # Add commands that require joining voice to work.

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Lütfen herhangi bir ses kanalına bağlanın.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Bağlı değil.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('Şarkı çalabilmek için `BAĞLANMA` ve `KONUŞMA` izinlerine sahip olmalıyım.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('Benimle aynı ses kanalında olmalısın.')


def setup(bot):
    """ Initialize music module """
    bot.add_cog(Music(bot))