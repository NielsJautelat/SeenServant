# UnseenServant

This is my own private DiscordMusic Bot.
You are free to use it, noncommercially yourself, as long as you don't claim it as your own work.
A credit or mention would be nice, but being honest is enough

## How to set it up

In the folder with the bot.py file, create a file called ".env". This file will be empty with the exception of the line: "DISCORD_TOKEN=XXXXX", where XXXXX is the Token you get in your Discord Developer Account.

Then you will put "ffmpeg.exe", "ffplay.exe" and "ffprobe.exe" into the same folder.
You can get them here: <https://www.gyan.dev/ffmpeg/builds/>

To be honest, you only need one or two of those, but I put all three in and am to lazy to check wich one I am actually using.

Once you have set it up, you can let the python script run.
Maybe install the dependencies that it whines about and you are of.

## Commands

### !help

This command list all commands available (except the download command)

### !join

When the bot is online you can use this command to summon it into your voice channel. (optional)

### !BattleMusic

This command plays all the mp3 files in your BattleMusic folder randomly and ad nauseam.

### !CalmMusic

This command plays all the mp3 files in your CalmMusic folder randomly and ad nauseam.

### !SuspensefulMusic

This command plays all the mp3 files in your SuspensefulMusic folder randomly and ad nauseam.

### !TavernMusic

This command plays all the mp3 files in your TavernMusic folder randomly and ad nauseam.

### !pause

This command pauses the current song.

### !resume

This command resumes the paused song.

### !skip

This command skips the current song and chooses a new random song from the folder (might be the same song).

### !stop

This command stops the current song and prevents more songs from playing.

### !leave

This command makes the bot leave the voice channel.

### !boop

boop

### !download

This command downloads a video from YouTube in a mp3 format, so that you can place it in one of the folders
