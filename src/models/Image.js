const mongoose = require("mongoose");

const imageSchema = new mongoose.Schema({
	_id: {
		type: String,
		required: true,
	},
	image_id: {
		type: Number,
		required: true,
		default: 0,
	},
});

const Image = mongoose.model("Image", imageSchema);

module.exports = Image;
