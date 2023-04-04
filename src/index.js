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
			if (ids.includes(msg.from.id.toString()) == "private") {
				bot.sendMessage(msg.chat.id, "Welcome back!");
			} else {
				insertNewUser(msg.from.id, msg.chat.type);
				bot.sendMessage(msg.chat.id, "Welcome to the bot!");
			}
		});
		return;
	}
});

// insertNewUser("123456788", "supergroup");
// getIds({ chat_type: "supergroup" });
// changeMediaId("123456789", "welcome");
// getMediaId("welcome");
