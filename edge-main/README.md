# VisionEdge AI Surveillance Studio

A polished computer vision and edge-computing project with a live dashboard UI for object detection, face recognition, recording, snapshots, and alerting.

## Features
- Live camera feed with a modern desktop dashboard
- Object detection using Ultralytics YOLO
- Face recognition mode with known-face matching
- Recording to video files
- Snapshot capture and alert integration
- SQLite-based event logging

## Run
```bash
cd /Users/india/Desktop/1
source .venv/bin/activate
python gui.py
```

## Optional alert setup
Set these environment variables before sending alerts:
```bash
export SENDER_EMAIL="you@example.com"
export APP_PASSWORD="your-app-password"
export RECEIVER_EMAIL="destination@example.com"
```
