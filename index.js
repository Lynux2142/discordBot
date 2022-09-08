const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
	intents: [
		GatewayIntentBits.Guilds,
		GatewayIntentBits.GuildMessages,
		GatewayIntentBits.MessageContent,
		GatewayIntentBits.GuildVoiceStates
	]
});

const timestampToTimeFormat = (timestamp, username) => {
	const duration = new Date(timestamp ? Date.now() - timestamp : 0);
	const currentDate = new Date().toLocaleString();
	const splitDuration = duration.toISOString().substr(11, 8).split(':');
	const strDuration = `${splitDuration[0]}h ${splitDuration[1]}mn ${splitDuration[2]}sec`;
	return (strDuration);
};

client.on('messageCreate', message => {
	const regex = new RegExp('^!time');
	if (regex.test(message.content)) {
		const currentDate = new Date().toLocaleString();
		if (message.mentions.users.size === 0) {
			console.log(`[${currentDate}] INFO: ${message.author.username} ask for his timestamp`);
			if (message.author.connexionTimestamp) {
				message.reply(timestampToTimeFormat(Math.round(message.author.connexionTimestamp), message.author.username));
			} else {
				message.reply('You are currently not connected to a voice room');
			}
		} else {
			message.mentions.users.map(user => {
				console.log(`[${currentDate}] INFO: ${message.author.username} ask for ${user.username} timestamp`);
				if (user.connexionTimestamp) {
					message.reply(`${user.username} is connected since ${timestampToTimeFormat(Math.round(user.connexionTimestamp), user.username)}`);
				} else {
					message.reply(`${user.username} are currently not connected to a voice room`);
				}
			});
		}
	}
});

client.on('voiceStateUpdate', (oldMember, newMember) => {
	client.users.fetch(newMember.id).then(user => {
		const oldChannel = client.channels.cache.get(oldMember.channelId);
		const newChannel = client.channels.cache.get(newMember.channelId);
		if (oldChannel != newChannel) {
			const currentDate = new Date().toLocaleString();
			if (oldChannel && newChannel) {
				console.log(`[${currentDate}] INFO: ${user.username} has change channel`);
				const upTime = timestampToTimeFormat(Math.round(user.connexionTimestamp), user.username);
				client.channels.cache.get(process.env.CHANNEL_LOG_ID).send(`${user.username} has left ${oldChannel.name} to join ${newChannel.name}`);
			}
			if (oldChannel && !newChannel) {
				console.log(`[${currentDate}] INFO: ${user.username} has disconnected from the server`);
				const upTime = timestampToTimeFormat(Math.round(user.connexionTimestamp), user.username);
				client.channels.cache.get(process.env.CHANNEL_LOG_ID).send(`${user.username} has disconnected from the server (${upTime})`);
				delete user.connexionTimestamp;
			}
			if (!oldChannel && newChannel) {
				console.log(`[${currentDate}] INFO: ${user.username} has connected to the server`);
				client.channels.cache.get(process.env.CHANNEL_LOG_ID).send(`${user.username} has connected to ${newChannel.name}`);
				user.connexionTimestamp = Date.now();
			}
		}
	});
});

client.login(process.env.BOT_TOKEN);
