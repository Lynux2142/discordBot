import os
from datetime import datetime
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

userInfo = {}

@client.event
async def on_ready():
	now = datetime.now().replace(microsecond = 0)
	for guild in client.guilds:
		for channel in guild.voice_channels:
			for member in channel.members:
				userInfo[member.id] = now

@client.event
async def on_voice_state_update(member, before, after):
	now = datetime.now().replace(microsecond = 0)
	channelLog = client.get_channel(int(os.getenv('CHANNEL_LOG_ID')))
	message = ""

	if before.channel != after.channel:
		if not before.channel:
			message = f'[{now.strftime("%d/%m/%Y %H:%M:%S")}] {member} has connected to {after.channel.name}\n'
			userInfo[member.id] = now
		elif not after.channel:
			message = f'[{now.strftime("%d/%m/%Y %H:%M:%S")}] {member} has disconnected to the server ({now - userInfo[member.id]})\n'
			del userInfo[member.id]
		else:
			message = f'[{now.strftime("%d/%m/%Y %H:%M:%S")}] {member} has left {before.channel.name} to join {after.channel.name}\n'
	await channelLog.send(message)

@client.event
async def on_message(message):
	if message.content.startswith('!time'):
		now = datetime.now().replace(microsecond = 0)
		if message.mentions:
			reply_message = ""
			for member in message.mentions:
				if member.id in userInfo:
					reply_message += f'{member} is connected since {now - userInfo[member.id]}\n'
					continue
				reply_message += f'{member} is not connected to the server\n'
			await message.reply(reply_message, mention_author = False)
			return
		await message.reply(now - userInfo[message.author.id], mention_author = False)

client.run(os.getenv('BOT_TOKEN'))
