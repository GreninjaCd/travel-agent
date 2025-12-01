"""
DEPRECATED: This was the original FastAPI entrypoint. Now using Express (Node.js) with agent_cli.py wrapper.
Kept for reference only.
"""
from fastapi import FastAPI

app = FastAPI(title="Travel Agent Demo (Deprecated)")

@app.get("/health")
def health_check():
    return {"status": "ok", "note": "Use Node.js server instead"}
