const express = require("express");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 5050;
const originUrl = process.env.CORS_ORIGIN || "http://localhost:5173"

app.use(express.json());
app.use(cors({ origin:  originUrl}));
app.use(express.urlencoded({ extended: true }));

const DATA_DIR = "/app/data";
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// app.post("/start-script", (req, res) => {
//     console.log("🚀 Starting Selenium script...");

//     const pythonProcess = spawn("python3", ["script.py"], { stdio: "pipe" });

//     pythonProcess.stdout.on("data", (data) => console.log(`Python: ${data.toString()}`));
//     pythonProcess.stderr.on("data", (data) => console.error(`Python Error: ${data.toString()}`));

//     pythonProcess.on("close", (code) => {
//         console.log(`Python script exited with code ${code}`);
//     });

//     res.json({ message: "Script started, waiting for user input." });
// });

app.post("/start-script", (req, res) => {
    console.log("🚀 Received request to start Selenium script...");

    const pythonProcess = spawn("python3", ["/app/script.py"], { stdio: "inherit" });

    pythonProcess.on("close", (code) => {
        console.log(`✅ Python script exited with code ${code}`);
    });

    res.json({ message: "Script started, check logs for updates." });
});

app.post("/submit-phone", (req, res) => {
    if (!req.body.phone) return res.status(400).json({ error: "Phone number is required" });

    fs.writeFileSync(`${DATA_DIR}/phone.txt`, req.body.phone);
    res.json({ message: "Phone number received. Please enter OTP." });
});

app.post("/submit-otp", (req, res) => {
    if (!req.body.otp) return res.status(400).json({ error: "OTP is required" });

    fs.writeFileSync(`${DATA_DIR}/otp.txt`, req.body.otp);
    res.json({ message: "OTP received. Logging in..." });
});

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
