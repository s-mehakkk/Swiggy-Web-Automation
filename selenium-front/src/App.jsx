import './App.css'
import React, { useState } from "react";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5050";

function App() {
    const [phone, setPhone] = useState("");
    const [otp, setOtp] = useState("");
    const [status, setStatus] = useState("");
    const [fileReady, setFileReady] = useState(false);
    const [filename, setFilename] = useState("");

    const startScript = async () => {
        try {
            setStatus("Starting script...");
            await axios.post(`${API_BASE_URL}/start-script`);
            setStatus("Script started. Please enter phone number.");
        } catch (error) {
            setStatus("Error starting script.");
        }
    };

    const submitPhone = async () => {
        if (!phone) return setStatus("Please enter a phone number.");
        try {
            setStatus("Sending phone number...");
            await axios.post(`${API_BASE_URL}/submit-phone`, { phone });
            setStatus("Phone number submitted. Please enter OTP.");
        } catch (error) {
            setStatus("Error submitting phone number.");
        }
    };

    const submitOtp = async () => {
        if (!otp) return setStatus("Please enter the OTP.");
        try {
            setStatus("Sending OTP...");
            await axios.post(`${API_BASE_URL}/submit-otp`, { otp });
            setStatus("OTP submitted. Processing data...");
            
            // Assuming Excel file will be ready after script execution
            setTimeout(() => {
                setFileReady(true);
                setFilename("HouseOfWok_data.xlsx");  // Change based on output filename
                setStatus("Data extracted! Click to download.");
            }, 15000); // Adjust time as per script execution time
        } catch (error) {
            setStatus("Error submitting OTP.");
        }
    };

    const downloadFile = () => {
      window.open(`${API_BASE_URL}/download/${filename}`, "_blank");
    };

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>Swiggy Automation</h1>

            <button onClick={startScript} style={{ marginBottom: "20px" }}>
                Start Script
            </button>

            <div>
                <input
                    type="text"
                    placeholder="Enter Phone Number"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                />
                <button onClick={submitPhone}>Submit Phone</button>
            </div>

            <div style={{ marginTop: "20px" }}>
                <input
                    type="text"
                    placeholder="Enter OTP"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                />
                <button onClick={submitOtp}>Submit OTP</button>
            </div>

            {fileReady && (
                <div style={{ marginTop: "20px" }}>
                    <button onClick={downloadFile}>Download Excel File</button>
                </div>
            )}

            <p style={{ marginTop: "20px", fontWeight: "bold" }}>{status}</p>
        </div>
    );
}

export default App;