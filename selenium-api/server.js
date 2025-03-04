const express = require("express");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = process.env.PORT || 5050;

const cors = require("cors");
app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

let userPhone = "";
let otpCode = "";

// Route to start Selenium script
app.post("/start-script", (req, res) => {
    const pythonProcess = spawn("python3", ["../main.py"]);

    pythonProcess.stdout.on("data", (data) => {
        console.log(`Python Output: ${data}`);
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Error: ${data}`);
    });

    pythonProcess.on("close", (code) => {
        console.log(`Python script finished with code ${code}`);
    });

    res.json({ message: "Script started, waiting for user input." });
});

// Route to accept phone number from user
app.post("/submit-phone", (req, res) => {
    userPhone = req.body.phone;
    fs.writeFileSync("phone.txt", userPhone);
    res.json({ message: "Phone number received. Please enter OTP next." });
});

// Route to accept OTP from user
app.post("/submit-otp", (req, res) => {
    otpCode = req.body.otp;
    fs.writeFileSync("otp.txt", otpCode);
    res.json({ message: "OTP received. Logging in..." });
});

// Route to download the Excel file
app.get("/download/:filename", (req, res) => {
    const filePath = path.join(__dirname, "..", "Results", req.params.filename);
    console.log(filePath)
    if (fs.existsSync(filePath)) {
        res.download(filePath);
    } else {
        res.status(404).json({ error: "File not found", filePath: filePath });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
