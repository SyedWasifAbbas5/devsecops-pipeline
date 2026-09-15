from datetime import datetime, timezone
import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "devsecops-pipeline")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.get("/")
def home():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "message": "DevSecOps pipeline is running",
        "hostname": socket.gethostname()
    })

@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.get("/ready")
def ready():
    return jsonify({
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.get("/api/v1/status")
def status():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
