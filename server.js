
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const app = express();

app.use(cors());
app.use(express.json());

const residentRoutes = require("./routes/Residentroutes");

app.use("/api/residents", residentRoutes);

// Test API
app.get("/", (req, res) => {
    res.send("Smart Hostel Backend is Running!");
});

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI)
.then(() => {
    console.log("MongoDB Connected Successfully!");
})
.catch((err) => {
    console.log("MongoDB Error:", err.message);
});

// Start server
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
