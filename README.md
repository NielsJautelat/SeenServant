# UnseenServant

This is my own private DiscordMusic Bot.
You are free to use it, noncommercially yourself, as long as you don't claim it as your own work.
A credit or mention would be nice, but being honest is enough

## How to set it up

In the folder with the bot.py file, create a file called ".env". This file will be empty with the exception of the line: "DISCORD_TOKEN=XXXXX", where XXXXX is the Token you get in your Discord Developer Account.

Then you will put "ffmpeg.exe", "ffplay.exe" and "ffprobe.exe" into the same folder.
You can get them here: https://www.gyan.dev/ffmpeg/builds/

To be honest, you only need one or two of those, but I put all three in and am to lazy to check wich one I am actually using.

## How to use it

Once you have set it up, you can let the python script run.
Maybe install the dependencies that it whines about and you are of.

To play a song use the "!play" command. It uses a relative filepath as an argument.
To play "song.mp3" in the same folder, you would use "!play song.mp3".
