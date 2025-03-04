const express = require("express");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 5050;

app.use(express.json());
app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.urlencoded({ extended: true }));

// Route to start Selenium script
app.post("/start-script", (req, res) => {
    const pythonProcess = spawn("python3", ["script.py"], { stdio: "pipe" });

    pythonProcess.stdout.on("data", (data) => console.log(`Python: ${data}`));
    pythonProcess.stderr.on("data", (data) => console.error(`Python Error: ${data}`));

    res.json({ message: "Script started, waiting for user input." });
});

app.post("/submit-phone", (req, res) => {
    fs.writeFileSync("phone.txt", req.body.phone);
    res.json({ message: "Phone number received. Please enter OTP." });
});

// Route to accept OTP from user
app.post("/submit-otp", (req, res) => {
    fs.writeFileSync("otp.txt", req.body.otp);
    res.json({ message: "OTP received. Logging in..." });
});

// Route to download the Excel file
app.get("/download/:filename", (req, res) => {
    const filePath = path.join(__dirname, "Results", req.params.filename);
    if (fs.existsSync(filePath)) {
        res.download(filePath);
    } else {
        res.status(404).json({ error: "File not found" });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
