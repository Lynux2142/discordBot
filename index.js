const { Client, Intents } = require('discord.js');
const { token } = require('./config.json');
const allIntents = new Intents(32767);
const SERVERID = '601320582579224586';
const DEFAULTCHANNELID = '772435316858552350';

const client = new Client({ intents: allIntents });

client.on('voiceStateUpdate', (oldMember, newMember) => {
	client.users.fetch(newMember.id).then(user => {
		const oldChannel = client.channels.cache.get(oldMember.channelId);
		const newChannel = client.channels.cache.get(newMember.channelId);
		if (oldChannel) {
			client.channels.cache.get(DEFAULTCHANNELID).send(`${user.username} has left ${oldChannel.name}`);
		}
		if (newChannel) {
			client.channels.cache.get(DEFAULTCHANNELID).send(`${user.username} has joined ${newChannel.name}`);
		}
	});
});

client.login(token);
