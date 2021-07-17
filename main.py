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


@client.command(pass_context=True)
async def pqp(ctx):
  
  url = 'https://www.myinstants.com/instant/bolsonaro-palavroes-32791/?utm_source=copy&utm_medium=share'
  server = ctx.message.guild
  voice_channel = server.voice_client

  async with ctx.typing():
    player = await YTDLSource.from_url(url)
    voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
  await ctx.send('pqp hein')



@client.command(pass_context=True)
async def sucky(ctx):
  
  url = 'https://www.myinstants.com/instant/sucky-sucky-5-dolla-78201/?utm_source=copy&utm_medium=share'
  server = ctx.message.guild
  voice_channel = server.voice_client

  async with ctx.typing():
    player = await YTDLSource.from_url(url)
    voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
  await ctx.send('sucky sucky')


@client.command(pass_context=True)
async def radio_guedes(ctx):
  
  url = 'https://stream-ar.planetradio.co.uk/absoluteclassicrockhigh.aac?direct=true&listenerid=undefined&aw_0_1st.bauer_listenerid=undefined&amsparams=playerid:BMUK_html5;skey:1626468207;&aw_0_1st.playerid=BMUK_html5&aw_0_1st.skey=1626468207&aw_0_1st.bauer_loggedin=false&awparams=loggedin:false;&aw_0_req.userConsentV2=CPJc1m0PJc1m0AGABCENBjCsAP_AAAAAAAKIHANf_X_fb3_D-_59_9t0eY1f9_7_v-0zjgeds-8Nyd_X_L8X_2M7vB36pq4KuR4Eu3LBAQdlHOHcTQmQ6IkVqTPsbk2Mr7NKJ7PEmlMbe2dYGH9_n9XT_ZKY79_____7__-_____77f__-__3_v59UgEAAACQyAyABQAIYATABHACkAGWANSAfYB-AEYAI4AUsAq4BWwDeAJiATYAtEBbAC8wGBAMPAZEAzkBngDPhgAkAbQA8ACxAHVAR6Ak4BdAC8gGhCIDwAVgBDACkAGQAMsAagA2QB-AEAAIwAUsAp4BVwDWAHVAPkAhsBDoCLwEiAJsATsApEBcgDAgGEgMPAZOAzkBnwgAIAbwBdADQgG6BIKoACAAFwAUABUADIAHIAPABAACIAGAAMgAaAA8gCGAIoATAAnwBVAFYALAAbwA5gB6AEIAIaARABEgCOgEsAS4AmgBSgC3AGGAMgAZcA1ADVAGyAO8AewA-IB9gH6AQCAi4CMAEaAI4ASkAoIBSwCngFXALmAX4AxQBrADaAG4AN4AegA-QCGwEOgIvASIAmIBMoCbAE7AKHAUiApoBYoC0AFsALkAXeAvMBgQDBgGEgMNAYeAyIBkgDJwGXAM5AZ8A0gBp0DWANZCAIIAHAAeAH8ARQAkQBmgDaAHOAQMAg4BPwChgGiAOqAh8BHoCVgE2gLCAXQAuoBdoC8gGIAMWAZCAyMBoQDRgGlANTAbcA3QNAlACsAFwAQwApABkADLAGoANkAfgBAACCgEYAKWAU8Aq8BaAFpANYAbwA6oB8gENgIdARUAi8BIgCbAE7AKRAXIAwIBhIDDwGMAMnAZyAzwBnwYAOAbIA6gC6AF9AMjAaEA3QVAdAAoAEMAJgAXABHACkAGWANQAfgBGACOAFLAKvAWgBaQDeAJBATEAmwBTYC2AFyALzAYEAw8BkQDOQGeAM-AbkKAEgDaAHgAQUA6oCPQF0AL6AaEA14dBlAAXABQAFQAMgAcgA-AEAAIgAXQAwADIAGgAPAAfQBDAEUAJgAT4AqgCsAFgALgAXwAxABmADeAHMAPQAhABDQCIAIkAR0AlgCYAE1AKMApQBYgC3gGEAYYAyABlADRAGoANkAb4A7wB7QD7AP0Af4BA4CLAIwARyAlICVAFBAKeAVcAsUBaAFpALmAXUAvIBfgDFAG0ANxAdMB1AD0AIbAQ6AiIBFQCLwEggJEASoAmwBOwChwFNAKsAWKAtCBbAFsgLgAXIAu0Bd4C8wGDAMJAYaAw8BiQDGAGPAMkAZOAyoBlwDOQGfANEgaQBpIDSwGnANYAbGOAiAAIgAcAB4AFwAcgA_ADIAGgAP4AigBIgCzAGWAM0AbQA5wB3AEAAILAQcBCACIgE2gJ8An4BSwCoAF6AMCAZkA1gBvADjgHSAOqAeQA-QCEAEPgI9gSsBK4CYoEyATKAm0BQoCkAFJgKYAVMAqoBWwCuwFlALUAXFAugC6gF9AMCAYgAxYBkIDLwGhQNFA0YBpQDTQGpgNeAbSA2wBtxCB6AAsACgAGQARAAuABiAEMAJgAVQAuABfADEAGYAN4AegBHACkAFiAMIAZQA1ABvgDvgH2AfgA_wCMAEcAJSAUEAoYBTwCrwFoAWkAuYBfgDFAG0AOoAegBIICRAEqAJsAU0AsUBaMC2ALaAXAAuQBdoDDwGJAMiAZOAzkBngDPgGiANJAaWA4AgAlAAQAD8ANAAfwBIgDLAG0AOcAeABBQCfAFLALEAZkA3gB1QDtgIfAR6Ak4BK4CYgE2gKFAUgApMBWwC6AF5AL6AYEA0IBooDSgGpgNsAbcSgcgAIAAWABQADIAHAARQAwADEAHgARAAmABVAC4AF8AMQAZgA2gCEAENAIgAiQBHQCjAKUAW4AwgBlADVAGyAO8AfgBGACOAEnAKeAVeAtAC0gF1AMUAbgA6gB8gEOgIqAReAkQBNgCxQFsALtAXmAw8BkQDJwGcgM8AZ8A0gBrADgCQB0ABwAFwAQgA5ADIAJEAXIAywBqADaAHcAQAAnwBUADMgG8AOqAfYBHoCVgE2gKTAWUAugBfQDFgGhANKAbkUgkAALgAoACoAGQAOQAfACAAEUAMAAyABoADyAIYAigBMACeAFIAKoAWAAvgBiADMAHMAQgAhoBEAETAKMApQBYgC3AGEAMoAaIA1QBsgDvgH2AfoBFgCMAEcAJSAUEAoYBVwCtgFzALyAbQA3AB6AEOgIvASIAk4BNgCdgFDgK2AWKAtgBcAC5AF2gLzAYaAw8BjADIgGSAMnAZcAzkBngDPoGkAaTA1gDWQGxlAGgAFwAQgA5AB-AFYAMgAbQBHACRAFyAMsAagA1wBtADnAHcAPAAgABFQCRAE2AJ3AT4BPwClgFiALqAYoA3gB1QDtgHkAP-Aj0BMQCZQE2gKQAUwAqYBXYC0AF0ALyAX0AwIBiwDQgGiANKAabA1IDUwGvA.YAAAAAAAAAAA&aw_0_1st.bauer_dmp=%5B%22533114%22%2C%22594434%22%2C%22596148%22%2C%22628965%22%2C%22629665%22%2C%22650698%22%5D&aw_0_1st.octave_dmp=%5B%22533114%22%2C%22594434%22%2C%22596148%22%2C%22628965%22%2C%22629665%22%2C%22650698%22%5D'
  channel = ctx.message.author.voice.channel
  global pl
  try:
    pl = await channel.connect()
  except:
    pass
  pl.play(discord.FFmpegPCMAudio(url))
  await ctx.send('s2')

@client.command(pass_context=True)
async def stop_radio_guedes(ctx):
  
  pl.stop()

keep_alive()
client.run(os.environ['TOKEN'])





