# Seen Servant written by Niels Jautelat
import os
import random
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from static_ffmpeg import run

print("Initalizing...")

# A variable to help break a recursive loop
# Needed when you want to change or stop the music when a collection plays
loopbreak = False

# Loading the .env file, containing your personal and secret Discord Token
# You should have a file called '.env' in the same directory that contains the line:
# DISCORD_TOKEN=XXXXX, where the XXXXX is the Bot Token from your Developer Portal
print("Loading the \'.env\' file...")
try:
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
except Exception as e:
    print("ERROR: No file \'.env\' containing the token was found")
    print(e)
    exit()

# Loads ffmpeg
# So the bot can decode mp3 files and play them
print("Loading FFMPEG...")
try:
    ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
except Exception as e:
    print("ERROR: FFMPEG failed to load")
    print(e)
    exit()

# Saves the directory path for future reference
# Needed, as there are instances where the current working directory isn't this directory and
# then the bot is confused, where the music has gone
print("Finding the directory...")
try:
    directoryPath = os.path.dirname(__file__)
except Exception as e:
    print("ERROR: Directory not found")
    print(e)
    exit()

# This means the bot is allowed to do anything.
# Not ideal for an unknown Bot, but since it runs on your local maschine and you can check the source code this is fine.
print("Loading intents...")
try:
    intents = discord.Intents.all()
except Exception as e:
    print("ERROR: Intents could not be initalized")
    print(e)
    exit()

# This initializes the bot and defines the way to interact with the bot as '!command'
# In the case, that you want to change the prefix, change the exclamation mark to whatever your heart desires.
print("Initializing Bot...")
try:
    bot = commands.Bot(command_prefix='!', intents=intents)
except Exception as e:
    print("ERROR: Bot could not be started")
    print(e)
    exit()


# When it is ready to receive commands it will say that it is ready.
@bot.event
async def on_ready():
    print("The Bot is ready")
    print("Awaiting commands...")

# This command will make the bot join the voice channel that you are currently in.
# Internally this will call the join_InternalFunction function.
@bot.command(name='join', help='The Bot joines the voice channel you are currently in')
async def join(ctx):
    print("Bot Command: join from User {}".format(ctx.message.author))
    await join_InternalFunction(ctx, True)

# This internal function will make the bot join the voice channel that you are currently in.
# If you aren't in one, it will be very upset at you.
# In case you restarted the bot, while it was in a voice channel, it won't realize that it still is in one.
async def join_InternalFunction(ctx, showMessage):
    print("Internal Function: join from User {}".format(ctx.message.author))
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return

    target_channel = ctx.message.author.voice.channel

    # Check if the bot is already connected to a voice channel in the guild
    for vc in bot.voice_clients:
        if vc.guild == ctx.guild:
            # If the bot is in the same channel as the user, do nothing
            if vc.channel == target_channel:
                if showMessage:
                    await ctx.send("The bot is already in your voice channel.")
                return
            # If the bot is in a different channel, disconnect and then connect to the new channel
            else:
                await vc.disconnect()

    try:
        await target_channel.connect()
    except Exception as e:
        print("Error: could not join voice channel of {}".format(ctx.message.author.name))
        await ctx.send("The bot failed to join the voice channel")
        print(e)
        return

    try:
        await ctx.guild.change_voice_state(channel=target_channel, self_mute=False, self_deaf=True)
    except Exception as e:
        print("ERROR: Failed to deafen the bot")
        await ctx.send("The bot failed to deafen itself. Sorry for the inconvenience. You can always try the deafen command at a later point. Also don't trust any bot that isn't deafend.")
        print(e)

# This command will make the bot leave the voice channel it is in.
# If it isn't in a voice channel, the bot will be very disappointed in you.
@bot.command(name='leave', help='The Bot leaves the voice channel it is currently in')
async def leave(ctx):
    print("Bot Command: leave from User {}".format(ctx.message.author))
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel. (Or maybe it rebooted, while it was in a voice channel, in that case it will leave shortly)")
    except Exception as e:
        print("Error could not leave voice channel")
        await ctx.send("The bot failed to leave its voice channel.")
        print(e)
        return

# This command will make the bot play a specific local mp3 file, based on the relative path to the file.
# i.e. '!play song.mp3'
# If a file is already playing, it will stop that it will stop the previous playback.
# If the bot isn't in a voice channel or a different one, it will first try to get to your voice channel.
@bot.command(name='play', help='The Bot plays a specific mp3 file \'!play song.mp3\'')
async def play(ctx, file):
    print("Bot Command: play from User {}".format(ctx.message.author))
    stoploop(ctx)
    await join_InternalFunction(ctx, False)
    try:
        voice_client = get(bot.voice_clients, guild=ctx.guild)
    except Exception as e:
        print("Error: Failed to interface with my voice")
        await ctx.send("The bot failed to find its own voice.")
        print(e)
        return

    try:
        voice_client.play(discord.FFmpegPCMAudio(directoryPath + '\\' + file, executable=ffmpeg), after=lambda e: print(f"{file} has finished playing"))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = 0.07

        file_name = file.rsplit("-", 2)
        await ctx.send(f"Playing: {file_name[0]}")
    except Exception as e:
        print("ERROR: Failed to play audio file")
        await ctx.send(f"The bot failed to play {file}. Are you sure you have spelled it correctly and is at its proper place?")
        print(e)
        return

# These commands make the Bot play a random rotation of mp3 files from specific folder/directory.
# i.e. randomly playing the audio files in the BattleMusic/CalmMusic/SuspensefulMusic/TavernMusic directory.
@bot.command(name='BattleMusic', help='Plays mp3 files randomly from the BattleMusic folder')
async def BattleMusic(ctx):
    print("Bot Command: BattleMusic from User {}".format(ctx.message.author))
    await playcollection(ctx, 'BattleMusic')

@bot.command(name='CalmMusic', help='Plays mp3 files randomly from the CalmMusic folder')
async def CalmMusic(ctx):
    print("Bot Command: CalmMusic from User {}".format(ctx.message.author))
    await playcollection(ctx, 'CalmMusic')

@bot.command(name='SuspensefulMusic', help='Plays mp3 files randomly from the SuspensefulMusic folder')
async def SuspensefulMusic(ctx):
    print("Bot Command: SuspensefulMusic from User {}".format(ctx.message.author))
    await playcollection(ctx, 'SuspensefulMusic')

@bot.command(name='TavernMusic', help='Plays mp3 files randomly from the TavernMusic folder')
async def TavernMusic(ctx):
    print("Bot Command: TavernMusic from User {}".format(ctx.message.author))
    await playcollection(ctx, 'TavernMusic')


# This function will make the bot play all the mp3 files in a specific directory randomly and ad nauseam.
# The function is only called internally by the commands for specific directories, above.
# If a file is already playing, it will stop that it will stop the previous playback.
# If the bot isn't in a voice channel or a different one, it will first try to get to your voice channel.
# If the directory is empty or doesn't exist, the bot will just be silenced.
async def playcollection(ctx, folder):
    print("Internal Function: playcollection")
    stoploop(ctx)
    await join_InternalFunction(ctx, False)
    try:
        voice_client = get(bot.voice_clients, guild=ctx.guild)
    except Exception as e:
        print("Error: Failed to interface with my voice")
        await ctx.send("The bot failed to find its own voice.")
        print(e)
        return

    folder_name = folder.rsplit("-", 2)

    if not os.path.exists(directoryPath + '\\' + folder):
        await ctx.send(f"No folder called {folder_name[0]} was found in the directory, check logs for searched directoy")
        print("The path " + directoryPath + '\\' + folder + " does not exist")
        return

    songs = []
    for file in os.listdir(directoryPath + '\\' + folder):
        if file.endswith(".mp3"):
            songs.append(file)

    if songs.count == 0:
        await ctx.send(f"No mp3 files were found in the {folder_name[0]} folder")
        return
    else:
        await ctx.send(f"Playing: {folder_name[0]}")
    
    global loopbreak
    loopbreak = False
    
    def playnext(voice_client):
        print("Internal Function: playnext")
        global loopbreak
        if loopbreak:
            loopbreak = False
            print("In Break")
            return
        
        currentsong = random.choice(songs)
        try:
            voice_client.play(discord.FFmpegPCMAudio(directoryPath + '\\' + folder + "/" + currentsong, executable=ffmpeg), after=lambda e: playnext(voice_client))
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
            voice_client.source.volume = 0.07

            print(f"Now playing: {folder}/{currentsong}")
        except Exception as e:
            print("ERROR: Failed to play audio file")
            print(e)
            return
    
    if voice_client and not voice_client.is_playing():        
        currentsong = random.choice(songs)
        try:
            voice_client.play(discord.FFmpegPCMAudio(directoryPath + '\\' + folder + "/" + currentsong, executable=ffmpeg), after=lambda e: playnext(voice_client))
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
            voice_client.source.volume = 0.07

            print(f"Now playing: {folder}/{currentsong}")
        except Exception as e:
            print("ERROR: Failed to play audio file")
            print(e)
            return

# This function will stop the playback of audio files.
# It additionally sets a flag so that the bot doesn't simply go to the next song, but also stops picking the next random song.
def stoploop(ctx):
    print("Internal Function: stoploop")
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        global loopbreak
        loopbreak = True
        voice_client.stop()

# This command pauses the voice client and intern the playback of the audio file.
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    print("Bot Command: pause from User {}".format(ctx.message.author))
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        try:
            voice_client.pause()
        except Exception as e:
            print("ERROR: Failed to pause playback")
            await ctx.send("The bot failed to pause the playback... I don't know what happens now...")
            print(e)
            return
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
# This command resumes the voice client and intern the playback of the audio file.
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    print("Bot Command: resume from User {}".format(ctx.message.author))
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_paused():
        try:
            voice_client.resume()
        except Exception as e:
            print("ERROR: Failed to resume playback")
            await ctx.send("The bot failed to resume the playback. Maybe you could try using the stop command and then start playback again.")
            print(e)
            return
    else:
        await ctx.send("The bot was not playing anything before this.")

# This command skips the current audio file, by stopping the voice client.
# It doesn't however set a flag to stop the next song.
# Therefore the bot only sees that the audio file finished playing aand will serve up the next one.
@bot.command(name='skip', help='Skips the song')
async def skip(ctx):
    print("Bot Command: skip from User {}".format(ctx.message.author))
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        try:
            voice_client.stop()
        except Exception as e:
            print("ERROR: Failed to skip the current audio file")
            await ctx.send("The bot failed to skip the current adio file.")
            print(e)
            return
    else:
        await ctx.send("The bot is not playing anything at the moment.")

# This command stops the playback entirely, by envocing the stoploop function.
# This will both stop the current song and signal to the bot that it shouldn't select a new one.
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    try:
        print("Bot Command: stop from User {}".format(ctx.message.author))
        stoploop(ctx)
    except Exception as e:
        print("ERROR: Failed to stop the playback")
        await ctx.send("The bot failed to stop the playback. Don't worry about it, was probably just the wind.")
        print(e)
        return

# This hidden command is there to download music from YouTube onto your computer, in a mp3 format.
# You can use it to get the audio files that you want to play with your bot.
# If you want the audio file to be played as a collection, move the song to the appropriate directory.
@bot.command(hidden=True)
async def download(ctx, url):
    print("Bot Command: download from User {}".format(ctx.message.author))
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

# boop
@bot.command(name='boop', help='boop')
async def boop(ctx):
    print("Bot Command: boop from User {}".format(ctx.message.author))
    response = 'boop'
    await ctx.send(response)

# This commands deafens the bot in the voice channel
@bot.command(name='deafen', help='This commands deafens the bot in the voice channel')
async def deafen(ctx):
    try:
        voice_client = get(bot.voice_clients, guild=ctx.guild)
    except Exception as e:
        print("ERROR: Failed to interface with my voice")
        await ctx.send("The bot failed to find its own voice.")
        print(e)
        return
    try:
        await ctx.guild.change_voice_state(channel=voice_client.channel, self_mute=False, self_deaf=True)
    except Exception as e:
        print("ERROR: Failed to deafen the bot")
        await ctx.send("The bot failed to deafen itself.")
        print(e)
        return

#This comand just prints out a short info message
@bot.command(name='info', help='info')
async def info(ctx):
    await ctx.send(f"HI, \nI am the Seen Servant.\n(I used to be unseen, but then they discovered me... Also there were other bots named Unseen Servant, so I changed my name to the Seen Servant)\nA bot developed as a utility for online D&D and other TTRPGs.\nI am still very unfinished and am actively worked on by my creator Niels Jautelat.")

# This hidden command shuts the bot down. 
@bot.command(hidden=True)
async def shutdown(ctx):
    print("Bot Command: Shutting Down from User {}".format(ctx.message.author))
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await leave(ctx)
    exit()

# This will starts the bot.
# When it is ready to receive commands it will tell you so.
bot.run(TOKEN)