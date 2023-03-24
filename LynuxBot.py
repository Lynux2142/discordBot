from os import getenv
import logging
from datetime import datetime
import discord
import json

BOT_TOKEN = getenv("BOT_TOKEN")
LOG_CHANNEL_INFO_FILE = "log_channel_info.json"

logger = logging.getLogger("discord.client")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

try:
    with open(LOG_CHANNEL_INFO_FILE, "r") as f:
        log_channel_info = json.load(f)
except:
    log_channel_info = {}

user_info = {}

@client.event
async def on_ready():
    now = datetime.now().replace(microsecond=0)
    for guild in client.guilds:
        for channel in guild.voice_channels:
            for member in channel.members:
                user_info[member.id] = now

@client.event
async def on_voice_state_update(member, before, after):
    channel_log = (
        client.get_guild(member.guild.id).system_channel
        if not str(member.guild.id) in log_channel_info
        else client.get_channel(log_channel_info[str(member.guild.id)])
    )

    now = datetime.now().replace(microsecond=0)
    message = ""

    if before.channel != after.channel:
        if not before.channel:
            message = f"{member} has connected to {after.channel.name}"
            user_info[member.id] = now
        elif not after.channel:
            message = f"{member} has disconnected to the server ({now - user_info[member.id]})"
            del user_info[member.id]
        else:
            message = f"{member} has left {before.channel.name} to join {after.channel.name}"
    logger.info(message)
    await channel_log.send(message)

@client.event
async def on_message(message):
    if message.content.startswith("!time"):
        now = datetime.now().replace(microsecond=0)
        reply_message = ""
        if message.mentions:
            for member in message.mentions:
                if member.id in user_info:
                    reply_message += f"{member} is connected since {now - user_info[member.id]}\n"
                    continue
                reply_message += f"{member} is not connected to a voice channel\n"
            reply_message = reply_message[:-1]
        else:
            reply_message = (
                str(now - user_info[message.author.id])
                if message.author.id in user_info
                else "You are not connected to a voice channel"
            )
        logger.info(reply_message)
        await message.reply(reply_message, mention_author=False)
    elif message.content.startswith("!setlogchannel"):
        channel_id = message.content.split(" ")[1]
        new_channel = client.get_channel(int(channel_id))
        if new_channel:
            log_channel_info[str(message.author.guild.id)] = new_channel.id
            with open(LOG_CHANNEL_INFO_FILE, "w") as f:
                f.write(json.dumps(log_channel_info))
            logger.info(f"The log channel has set to {new_channel.id}")
            await message.reply(f"Log channel has set to {new_channel.name}")
        else:
            await message.reply(f"Incorrect channel id ({channel_id})")

client.run(BOT_TOKEN)
