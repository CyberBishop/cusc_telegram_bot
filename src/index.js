require("./config/db");

const {
	insertNewUser,
	getIds,
	changeMediaId,
	getMediaId,
} = require("./controllers/db");

const { spawn } = require("child_process");
const TelegramBot = require("node-telegram-bot-api");
const BOT_TOKEN = process.env.TOKEN;

let bot = new TelegramBot(BOT_TOKEN, {
	polling: true,
});

bot.on("message", async (msg) => {
	// Start message
	if (msg.text === "/start") {
		// Regular user
		getIds().then((ids) => {
			if (ids.includes(msg.from.id.toString())) {
				bot.sendMessage(
					msg.chat.id,
					(start_message_text = `Hi there \!\!\! 👋\n\nI'm CUSC bot 🤖, the official bot of the CU Student Council.\n\nI'm here to give you first hand information and news concerning student life on campus 🏫.\n\nYou can also connect with the student council through the official Instagram page: https://www.instagram.com/studentcouncil_cu/\n\nStay tuned\!\!\! 💥
				`)
				);
			} else {
				insertNewUser(msg.from.id, msg.chat.type);
				bot.sendMessage(
					msg.chat.id,
					(start_message_text = `Hi there \!\!\! 👋\n\nI'm CUSC bot 🤖, the official bot of the CU Student Council.\n\nI'm here to give you first hand information and news concerning student life on campus 🏫.\n\nYou can also connect with the student council through the official Instagram page: https://www.instagram.com/studentcouncil_cu/\n\nStay tuned\!\!\! 💥`)
				);
			}
		});
		return;
	}
});

// insertNewUser("123456788", "supergroup");
// getIds({ chat_type: "supergroup" });
// changeMediaId("123456789", "welcome");
// getMediaId("welcome");
