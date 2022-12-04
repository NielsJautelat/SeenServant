# Unseen Servant written by Niels Jautelat
import os
import random
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

#A variable to help break a recursive loop
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

#This command will make the bot join the voice channel that you are currently in
@bot.command(name='join', help='The Bot joines the voice channel you are currently in')
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

#This command will make the bot leave the voice channel
@bot.command(name='leave', help='The Bot leaves the voice channel it is currently in')
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()

#This command will make the bot play a specific local mp3 file, based on the relative path to the file
@bot.command(name='play', help='The Bot plays a specific mp3 file \'!play song.mp3\'')
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

#These commands make the Bot play a random rotation of mp3 files from specific folder/directory
@bot.command(name='BattleMusic', help='Plays a random rotation of mp3 files in your BattleMusic folder/directory')
async def BattleMusic(ctx):
    stoploop(ctx)
    await playcollection(ctx, 'BattleMusic')
@bot.command(name='CalmMusic', help='Plays a random rotation of mp3 files in your CalmMusic folder/directory')
async def CalmMusic(ctx):
    stoploop(ctx)
    await playcollection(ctx, 'CalmMusic')
@bot.command(name='SuspensefulMusic', help='Plays a random rotation of mp3 files in your SuspensefulMusic folder/directory')
async def SuspensefulMusic(ctx):
    stoploop(ctx)
    await playcollection(ctx, 'SuspensefulMusic')
@bot.command(name='TavernMusic', help='Plays a random rotation of mp3 files in your TavernMusic folder/directory')
async def TavernMusic(ctx):
    stoploop(ctx)
    await playcollection(ctx, 'TavernMusic')


#This function will make the bot play a collection of mp3 files from a specific folder/directory randomly ad nauseam
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

    def playnext(voice):
        global loopbreak
        if loopbreak:
            loopbreak = False
            print("In Break")
            return
        try:
            currentsong = random.choice(songs)
            voice.play(discord.FFmpegPCMAudio(folder + "/" + currentsong), after=lambda e: playnext(voice))
            print(f"Now playing: {folder}/{currentsong}")
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            voice.is_playing()
        except:
            print("Error")
    
    global loopbreak
    if channel and not voice.is_playing() and not loopbreak:
        try:
            currentsong = random.choice(songs)
            voice.play(discord.FFmpegPCMAudio(folder + "/" + currentsong), after=lambda e: playnext(voice))
            print(f"Now playing: {folder}/{currentsong}")
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            voice.is_playing()
        except:
            print("Error")

#This function will stop the playlist
def stoploop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        global loopbreak
        loopbreak = True
        voice_client.stop()

#This command pauses the song
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
#This command resumes the paused song
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this.")

#This command skips the current song
@bot.command(name='skip', help='Stops the song')
async def skip(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

#This command stops the playlist
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    stoploop(ctx)

#This hidden command is there to download music from YouTube onto your computer so that you can put the mp3 files into the respective folders/directories
@bot.command(hidden=True)
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

#boop
@bot.command(name='boop', help='boop')
async def boop(ctx):
    response = 'boop'
    await ctx.send(response)

#And finally we are running the bot with this command
bot.run(TOKEN)