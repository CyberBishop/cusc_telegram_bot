require("./config/db");

const {
	insertNewUser,
	getIds,
	changeMediaId,
	getMediaId,
} = require("./controllers/db");

// insertNewUser("123456789", "private");
getIds();
