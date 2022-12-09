# UnseenServant

This is my own private DiscordMusic Bot.
You are free to use it, noncommercially yourself, as long as you don't claim it as your own work.
A credit or mention would be nice, but being honest is enough

## How to set it up

First, you got to set up an Application and a Bot in your Discord Developer Portal. Then, you reset your Bot Token. It will be reaveled only once so make sure to copy it somewhere. After that, in the UnseenServant directory, create a file called ".env" and add the line 'DISCORD_TOKEN=XXXXX' where XXXXX is the Token of your Bot.

Finally, if you are on Windows run 'start.bat' and you are good to go. The bot is running and will continue to do so, until you close the terminal/cmd or until someone types "!shutdown" in a text channel that the Bot can see.

Or, if you aren't using Windows or you want to do in manually, install the requirements by opening your terminal/cmd in the project directory and running the command 'pip install -r requirements.txt'. Then you can start the bot with 'python bot.py'.

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

This command downloads a video from YouTube in a mp3 format, so that you can place it in one of the folders.

### !shutdown

This commmand shuts the bot down.
