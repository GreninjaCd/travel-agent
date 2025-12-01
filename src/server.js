require("dotenv").config();
const express = require("express");
const { callPythonAgent } = require("./agentClient");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

app.post("/api/travel", async (req, res) => {
  try {
    const request = req.body;
    const result = await callPythonAgent(request);
    res.json({ success: true, data: result });
  } catch (error) {
    console.error("Error calling Python agent:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Express server listening on port ${PORT}`);
});
