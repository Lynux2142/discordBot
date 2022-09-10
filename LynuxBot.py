import os
import sys
import discord
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

userInfo = {}

@client.event
async def on_ready():
	sys.stdout.write(f'We have logged in as {client.user}')
	now = datetime.now().replace(microsecond = 0)
	for guild in client.guilds:
		for channel in guild.voice_channels:
			for member in channel.members:
				userInfo[member.id] = now

@client.event
async def on_voice_state_update(member, before, after):
	now = datetime.now().replace(microsecond = 0)
	channelLog = client.get_channel(int(os.getenv('CHANNEL_LOG_ID')))

	if not(before.channel):
		message = f'[{now.strftime("%d/%m/%Y, %H:%M:%S")}] INFO: {member} has connected to {after.channel.name}\n'
		userInfo[member.id] = now
	elif not(after.channel):
		message = f'[{now.strftime("%d/%m/%Y, %H:%M:%S")}] INFO: {member} has disconnected to the server ({now - userInfo[member.id]})\n'
		del userInfo[member.id]
	else:
		message = f'[{now.strftime("%d/%m/%Y, %H:%M:%S")}] INFO: {member} has left {before.channel.name} to join {after.channel.name}\n'
	await channelLog.send(message)
	sys.stdout.write(message)

@client.event
async def on_message(message):
	if (message.channel.id == int(os.getenv('CHANNEL_LOG_ID'))):
		if (message.content.startswith('!time')):
			now = datetime.now().replace(microsecond = 0)
			if (message.mentions):
				reply_message = ""
				for member in message.mentions:
					if member.id in userInfo:
						reply_message += f'{member.name}#{member.discriminator} is connected since {now - userInfo[member.id]}\n'
						continue
					reply_message += f'{member.name}#{member.discriminator} is not connected to the server\n'
				await message.reply(reply_message, mention_author = False)
				sys.stdout.write(f'[{now.strftime("%d/%m/%Y, %H:%M:%S")}] INFO: {message.author.name} asked for some members time\n')
			else:
				reply_message = now - userInfo[message.author.id]
				await message.reply(reply_message, mention_author = False)
				sys.stdout.write(f'[{now.strftime("%d/%m/%Y, %H:%M:%S")}] INFO: {message.author.name} asked for his time\n')

client.run(os.getenv('BOT_TOKEN'))
