import logging
import json
from datetime import datetime
import discord

logger = logging.getLogger("discord.client")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

try:
    with open("config.json", "r") as f:
        config = json.load(f)
        assert "BOT_TOKEN" in config, "BOT_TOKEN must be present in config.json"
        assert "CHANNEL_ID" in config, "CHANNEL_ID must be present in config.json"
except IOError:
    print(f"IOError: config.json is missing")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

userInfo = {}

@client.event
async def on_ready():
    now = datetime.now().replace(microsecond=0)
    for guild in client.guilds:
        for channel in guild.voice_channels:
            for member in channel.members:
                userInfo[member.id] = now

@client.event
async def on_voice_state_update(member, before, after):
    now = datetime.now().replace(microsecond=0)
    channelLog = client.get_channel(int(config["CHANNEL_ID"]))
    message = ""

    if before.channel != after.channel:
        if not before.channel:
            message = f"{member} has connected to {after.channel.name}"
            userInfo[member.id] = now
        elif not after.channel:
            message = f"{member} has disconnected to the server ({now - userInfo[member.id]})"
            del userInfo[member.id]
        else:
            message = f"{member} has left {before.channel.name} to join {after.channel.name}"
    logger.info(message)
    await channelLog.send(message)

@client.event
async def on_message(message):
    if message.content.startswith("!time"):
        now = datetime.now().replace(microsecond=0)
        reply_message = ""
        if message.mentions:
            for member in message.mentions:
                if member.id in userInfo:
                    reply_message += f"{member} is connected since {now - userInfo[member.id]}\n"
                    continue
                reply_message += f"{member} is not connected to a voice channel\n"
            reply_message = reply_message[:-1]
        else:
            reply_message = (
                str(now - userInfo[message.author.id])
                if message.author.id in userInfo
                else "You are not connected to a voice channel"
            )
        logger.info(reply_message)
        await message.reply(reply_message, mention_author=False)

client.run(config["BOT_TOKEN"])
