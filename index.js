const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const fs = require('fs');
const app = express();

require("dotenv").config();

// Change this to your desired environment setup
const PORT = 5051;
const CORS_ORIGIN = '*';


// Middleware
app.use(cors());
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', CORS_ORIGIN);
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    next();
  });
app.use(express.json());

app.use((req, res, next) => {
    console.log(`Incoming request: ${req.method} ${req.url}`);
    next();
});

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

    const command = 'python3 script/lush.py m';

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

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});