# bot.py
import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.command(name='join', help='The Bot joines the voice channel you are currently in')
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='The Bot leaves the voice channel it is currently in')
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()

@bot.command()
async def play(ctx, file):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    voice = get(bot.voice_clients, guild=ctx.guild)

    voice.play(discord.FFmpegPCMAudio(file), after=lambda e: print(f"{file} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    file_name = file.rsplit("-", 2)
    await ctx.send(f"Playing: {file_name[0]}")

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
        await ctx.send("The bot was not playing anything before this. Use play_song command")
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='boop', help='boop')
async def boop(ctx):
    response = 'boop'
    await ctx.send(response)

bot.run(TOKEN)