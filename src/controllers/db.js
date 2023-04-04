const BotUser = require("../models/BotUser");
const Image = require("../models/Image");

const insertNewUser = async (id, chatType) => {
	try {
		await BotUser.create({ _id: id.toString(), chat_type: chatType });
	} catch (err) {
		console.error(err);
	}
};

const getIds = async () => {
	console.log("Getting all user IDs");

	const userIds = await BotUser.find();
	if (!userIds || userIds.length === 0) {
		console.log("No IDs exist");
		return "No IDs exist";
	}
	console.log(userIds);
	return userIds.map((user) => user._id);
};

const changeMediaId = async (id, type) => {
	try {
		await Image.findOneAndUpdate(
			{ _id: type },
			{ $set: { image_id: id } },
			{ upsert: true }
		);
		console.log("Successfully updated");
	} catch (err) {
		console.error(err);
	}
};

const getMediaId = async (type) => {
	const image = await Image.findOne({ _id: type });
	return image ? image.image_id.toString() : "";
};

module.exports = {
	insertNewUser,
	getIds,
	changeMediaId,
	getMediaId,
};
