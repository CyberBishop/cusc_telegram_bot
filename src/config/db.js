const dotenv = require("dotenv");
const mongoose = require("mongoose");

dotenv.config();
const CONNECTION_STRING = process.env.CONNECTION_STRING;

// connect to mongodb
mongoose.set("strictQuery", true);

mongoose
	.connect(CONNECTION_STRING, {
		useNewUrlParser: true,
		useUnifiedTopology: true,
	})
	.then(() => {
		console.log("Connected to MongoDB");
	})
	.catch((err) => {
		console.log("Error connecting to MongoDB", err);
	});

// export the mongoose object
module.exports = { mongoose };
