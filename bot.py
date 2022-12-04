# Unseen Servant written by Niels Jautelat
import os
import random
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

loopbreak = False


#Loading the .env file, containing your personal and secret Discord Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#This means the bot is allowed to do anything. Not ideal for an unknown Bot, but since it runs on your local maschine and you can check the source code this is fine
intents = discord.Intents.all()

#This initializes the bot and defines the way to interact with the bot as '!command'
bot = commands.Bot(command_prefix='!', intents=intents)





#When it is ready to receive commands it will say that it is ready
@bot.event
async def on_ready():
    print("Bot is ready")






#This command will make the bot join the voice channel
@bot.command(name='join', help='The Bot joines the voice channel you are currently in')
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

#This command will make the bot leave the voice channel
@bot.command(name='leave', help='The Bot leaves the voice channel it is currently in')
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()





#This command will make the bot play a specific local file
@bot.command()
async def play(ctx, file):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    voice.play(discord.FFmpegPCMAudio(file), after=lambda e: print(f"{file} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    file_name = file.rsplit("-", 2)
    await ctx.send(f"Playing: {file_name[0]}")





@bot.command()
async def BattleMusic(ctx):
    #await stop(ctx)
    await playcollection(ctx, 'BattleMusic')
@bot.command()
async def CalmMusic(ctx):
    #await stop(ctx)
    await playcollection(ctx, 'CalmMusic')
@bot.command()
async def SuspensefulMusic(ctx):
    #await stop(ctx)
    await playcollection(ctx, 'SuspensefulMusic')
@bot.command()
async def TavernMusic(ctx):
    #await stop(ctx)
    await playcollection(ctx, 'TavernMusic')


#This command will make the bot play a collection of files randomly ad nauseam 
@bot.command()
async def playcollection(ctx, folder):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    folder_name = folder.rsplit("-", 2)
    await ctx.send(f"Playing: {folder_name[0]}")

    songs = []
    for file in os.listdir(folder):
        if file.endswith(".mp3"):
            songs.append(file)

    async def playnext(voice):
        global loopbreak
        if loopbreak:
            loopbreak = False
            print("In Break")
            return
        try:
            currentsong = random.choice(songs)
            voice.play(discord.FFmpegPCMAudio(folder + "/" + currentsong), after=lambda e: playnext(voice))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            voice.is_playing()
        except:
            print("Error")
    
    global loopbreak
    if channel and not voice.is_playing() and not loopbreak:
        print("Next Song")
        try:
            currentsong = random.choice(songs)
            voice.play(discord.FFmpegPCMAudio(folder + "/" + currentsong), after=lambda e: playnext(voice))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            voice.is_playing()
        except:
            print("Error")
    


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this.")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
        #if voice_client.is_playing():
           # global loopbreak
            #loopbreak = True
            #await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")





@bot.command(name='download')
async def download(ctx, url):
    await ctx.send("Getting your music")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await ctx.send("Finished Download")





@bot.command(name='boop', help='boop')
async def boop(ctx):
    response = 'boop'
    await ctx.send(response)





bot.run(TOKEN)