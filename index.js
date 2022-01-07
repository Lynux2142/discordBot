const { Client, Intents } = require('discord.js');
const SERVERID = '601320582579224586';
const DEFAULTCHANNELID = '772435316858552350';

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_VOICE_STATES] });

const timestampToTimeFormat = (timestamp, username) => {
	const duration = new Date(timestamp ? timestamp : 0);
	console.log(username);
	console.log('---------------------');
	console.log(timestamp);
	console.log(duration.toISOString().substr(11, 8));
	console.log('---------------------');
	const splitDuration = duration.toISOString().substr(11, 8).split(':');
	const strDuration = `${splitDuration[0]}h ${splitDuration[1]}mn ${splitDuration[2]}sec`;
	return (strDuration);
};

client.on('voiceStateUpdate', (oldMember, newMember) => {
	client.users.fetch(newMember.id).then(user => {
		const oldChannel = client.channels.cache.get(oldMember.channelId);
		const newChannel = client.channels.cache.get(newMember.channelId);
		if (oldChannel != newChannel) {
			if (oldChannel) {
				const upTime = timestampToTimeFormat(Math.round(Date.now() - user.connexionTimestamp), user.username);
				client.channels.cache.get(DEFAULTCHANNELID).send(`${user.username} has left ${oldChannel.name} (${upTime})`);
			}
			if (newChannel) {
				client.channels.cache.get(DEFAULTCHANNELID).send(`${user.username} has joined ${newChannel.name}`);
				user.connexionTimestamp = Date.now();
			}
		}
	});
});

client.login(process.env.BOT_TOKEN);
