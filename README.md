# UnseenServant

This is my own private DiscordMusic Bot.
You are free to use it, noncommercially yourself, as long as you don't claim it as your own work.
A credit or mention would be nice, but being honest is enough

## How to set it up

First you got to set up an Application and a Bot in your Discord Developer Portal. Then you reset your Bot Token. It will be reaveled only once, so make sure to copy it somewhere. Then open the file called ".env" and change the 'XXXXX' in the file to your Token.

After that run setup.bat and you are good to go. (Or install the requirements, by opening navigating into the directory using your terminal/cmd and running the command 'pip install -r requirements.txt')

Run bot.py and your bot is running as long as you keep the terminal/cmd open. (Sometimes the working directory is not the same as the folder with 'bot.py' in it. Don't know why, but opening the folder in VS Code and then running it, works every time)

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
