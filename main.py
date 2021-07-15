import os
import youtube_dl
from discord.ext import commands
import discord 
import asyncio
from keep_alive import keep_alive

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


client = commands.Bot(command_prefix='--')


@client.event
async def on_ready():
  print("here we goooo")

@client.command(pass_context=True)
async def join(ctx):
  ch = ctx.message.author.voice.channel
  await ch.connect()

@client.command(pass_context=True)
async def microaggression(ctx):
  
  url = 'https://www.youtube.com/watch?v=834d-fhL9OM&ab_channel=MemeFountain'
  server = ctx.message.guild
  voice_channel = server.voice_client

  async with ctx.typing():
    player = await YTDLSource.from_url(url)
    voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
  await ctx.send('Did just hear someone use a microaggression')


  #player = await voice_client.create_ytdl_player(url)
  #player.start()


@client.command(pass_context=True)
async def pqp(ctx):
  
  url = 'https://www.myinstants.com/instant/bolsonaro-palavroes-32791/?utm_source=copy&utm_medium=share'
  server = ctx.message.guild
  voice_channel = server.voice_client

  async with ctx.typing():
    player = await YTDLSource.from_url(url)
    voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
  await ctx.send('pqp hein')

  #player = await voice_client.create_ytdl_player(url)
  #player.start()

keep_alive()
client.run(os.environ['TOKEN'])





