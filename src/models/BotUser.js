const mongoose = require("mongoose");

const botUserSchema = new mongoose.Schema({
	_id: {
		type: String,
		required: true,
	},
	chat_type: {
		type: String,
		required: true,
	},
});

module.exports = mongoose.model("BotUser", botUserSchema);
