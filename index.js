const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const fs = require('fs');
const app = express();

require("dotenv").config();

const PORT = process.env.PORT || 5051;

// Middleware
app.use(cors({origin: process.env.CORS_ORIGIN}));
app.use(express.json());

const runShellCommand = (commandString) => new Promise((resolve, reject) => {

	exec(commandString, (err, stdout, stdin) => {
		if (err) {
			console.error(stderr.toString());
			return reject(err);
		}
		return resolve(stdout.toString());
	});
});

// Routes
app.post('/recommend', async (req, res) => {
    const userPreferences = req.body;
    
    fs.writeFileSync('script/in/in.json', JSON.stringify(userPreferences));

    const command = 'python3 script/lush.py';

    console.log("Executing Python script");
    runShellCommand(command).then( () => {
        const output = JSON.parse(fs.readFileSync('script/out/out.json', 'utf-8'));

        console.log("Sending response");
        res.json(output);
    }) .catch((err) => {
        console.error(`Error executing script: ${err}`);
        return res.status(500).json({ error: "Internal Server Error" });
    })
}
);

const server = app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
server.timeout = 100000;