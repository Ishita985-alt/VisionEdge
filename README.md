# VisionEdge AI Surveillance Studio

A modern **Computer Vision** and **Edge AI Surveillance System** developed as part of the **Python Development Internship at Axlero Solutions**.

VisionEdge is designed to provide intelligent real-time surveillance using computer vision techniques such as object detection, face recognition, event logging, recording, and automated alert generation.

The project follows a modular architecture so that camera management, frame processing, AI inference, recording, database logging, alerts, and dashboard components can be developed and integrated independently.

---

# 🚀 Features

- 🎥 Live camera feed
- 🖥️ Modern desktop dashboard
- 🤖 Real-time object detection using **Ultralytics YOLO**
- 👤 Face recognition with known-face matching
- 🎬 Video recording
- 📸 Snapshot capture
- 🚨 Intelligent alert generation
- 🗄️ SQLite-based event logging
- ⚙️ Modular backend architecture
- 🔧 Configurable application settings
- 📂 Organized project structure for collaborative development

---

# 📁 Project Structure

```text
VisionEdge/
│
├── Images/
│   └── .gitkeep
│
├── backend/
│   ├── app.py
│   ├── config.py
│   └── requirements.txt
│
├── decoder/
│   ├── video_decoder.py
│   └── test_camera.py
│
├── inference/
│   └── trt_inference.py
│
├── models/
│   └── .gitkeep
│
├── output/
│   ├── database/
│   ├── logs/
│   ├── recordings/
│   └── snapshots/
│
├── processing/
│   ├── frame_processor.py
│   └── test_frame_processor.py
│
├── scripts/
│   ├── build_engine.py
│   └── export_onnx.py
│
├── streams/
│   └── .gitkeep
│
├── main.py
├── README.md
└── .gitignore
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python 3.x |
| Computer Vision | OpenCV |
| AI Framework | Ultralytics YOLO |
| Numerical Computing | NumPy |
| Image Processing | Pillow |
| Database | SQLite |
| Version Control | Git & GitHub |

---

# 📌 Backend Development Progress

## ✅ Completed

### Day 1 – Backend Initialization

- Backend project initialization
- Configuration management system
- Automatic project directory creation
- Backend startup system
- Project folder organization
- Dependency management
- Python project configuration
- Git ignore configuration

### Day 2 – Camera Manager

- Camera Manager implementation using OpenCV
- Camera initialization and startup
- Camera resolution configuration
- Camera availability checking
- Real-time frame capture
- Camera start and stop functionality
- Camera resource cleanup
- Frame capture error handling
- Camera operation logging
- Camera testing module
- Successful camera testing at 1280×720 resolution
- Keyboard-controlled shutdown using Q/ESC

### Day 3 – Frame Processing Pipeline

- Created modular `processing` package
- Implemented `FrameProcessor`
- Added frame validation
- Added invalid-frame handling
- Added frame resizing functionality
- Added basic frame preprocessing
- Added processing error handling
- Added frame processing logging
- Added `test_frame_processor.py`
- Tested 1280×720 input frame processing
- Validated 640×640 processed output
- Tested handling of invalid/empty frames
- Prepared the processing layer for future YOLO/inference integration

---

# 🧪 Camera Manager Validation

The Camera Manager was tested successfully using a physical camera.

### Test Result

```text
[✓] Camera started successfully
[✓] Resolution: 1280x720
[✓] Camera window opened
[INFO] Stop key pressed.
[✓] Camera released
[✓] Camera test completed
```

The test confirmed successful camera initialization, frame capture, camera control, and resource cleanup.

---

# 🧪 Frame Processor Validation

The Frame Processor was tested using a simulated OpenCV frame.

### Test Result

```text
# VisionEdge Frame Processor Test

[✓] Test frame created
[✓] Original resolution: 1280x720
[✓] Frame validation successful
[✓] Processed resolution: 640x640
[✓] Frame processing completed
[✓] Day 3 Frame Processor test successful

# Invalid Frame Test

[✓] Invalid frame handled correctly
```

The test confirmed that the Frame Processor can validate incoming frames, resize valid frames, process frames successfully, and safely handle invalid input.

---

# 🔄 Current Backend Flow

The current backend processing flow is:

```text
Camera
   │
   ▼
Camera Manager
   │
   │ Raw OpenCV Frame
   ▼
Frame Processor
   │
   ├── Frame Validation
   ├── Frame Preprocessing
   └── Frame Resizing
   │
   ▼
Processed Frame
   │
   ▼
Future YOLO / Inference Module
```

The Frame Processor is intentionally kept separate from the AI inference module so that the modules can be developed independently and integrated later.

---

# 🚧 Upcoming Backend Development

The following modules are planned for subsequent development:

- YOLO Inference Integration
- Video Recording Module
- Snapshot Module
- SQLite Database Integration
- Event Logging
- Alert Management
- Dashboard Integration
- Backend Integration with other VisionEdge modules

---

# 📅 Development Timeline

| Day | Development Area | Status |
|-----|------------------|--------|
| Day 1 | Backend Initialization & Configuration | ✅ Completed |
| Day 2 | Camera Manager & Frame Capture | ✅ Completed |
| Day 3 | Frame Processing Pipeline | ✅ Completed |
| Day 4 | Database & Event Logging | 🚧 Upcoming |
| Day 5 | Recording & Snapshot Management | 🚧 Upcoming |
| Day 6 | Alert Management & Backend Integration | 🚧 Upcoming |
| Day 7 | Testing, Integration & Final Review | 🚧 Upcoming |

> **Note:** The timeline may be adjusted based on team discussions, module dependencies, and internship deliverables.

---

# 📚 Internship Information

| Field | Details |
|-------|---------|
| Organization | Axlero Solutions |
| Internship | Python Development Internship |
| Project | VisionEdge AI Surveillance Studio |
| Domain | Computer Vision & Edge AI |

---

# 👥 Team Members

This project is being developed collaboratively as part of the **Python Development Internship at Axlero Solutions**.

| Sl. No. | Team Member |
|---------|-------------|
| 1 | Ishita Bhariya |
| 2 | Shri Abishek M K |
| 3 | Bairi Saivardhan |
| 4 | Saifuddin |
| 5 | Ravikumar S |
| 6 | Anthati Venkatesh |

> **Note:** Work distribution and module assignments are being finalized collaboratively.

---

# 👥 Contributors

| Contributor | Current Status |
|-------------|----------------|
| Ishita Bhariya | Repository Owner |
| Anthati Venkatesh | Team Member |
| Shri Abishek M K | Team Member |
| Bairi Saivardhan | Team Member |
| Saifuddin | Team Member |
| Ravikumar S (@Ravikumar07-Byte) | Backend Development & Repository Contributor |

---

# 📊 Current Status

**Project Version:** `0.3.0`

### ✅ Completed Modules

- Project Structure
- Backend Initialization
- Configuration System
- Camera Manager
- Camera Frame Capture
- Camera Testing
- Frame Processor
- Frame Validation
- Frame Resizing
- Frame Processing Testing

### 🚧 Modules Under Development

- YOLO / AI Inference Integration
- Database Integration
- Recording System
- Snapshot System
- Alert Management
- Dashboard Integration
- Backend Integration with Other Modules

---

# 🔮 Future Enhancements

- Multi-camera support
- GPU acceleration
- Advanced face recognition
- Email and Telegram notifications
- Cloud synchronization
- Web-based dashboard
- User authentication and authorization
- REST API integration
- Docker containerization
- Performance monitoring and analytics

---

# 🔗 Repositories

### Team Repository

https://github.com/Ishita985-alt/VisionEdge

### Backend Development Repository

https://github.com/Ravikumar07-Byte/VisionEdge-Backend

The team repository is used for collaborative project development. The backend development repository maintains the backend development history and contributions.

---

# 📄 License

This project is developed as part of the **Python Development Internship at Axlero Solutions** for educational, learning, and demonstration purposes.

---

# ⭐ Acknowledgements

Special thanks to **Axlero Solutions** for providing the internship opportunity and project guidance, and to all contributors collaborating on the development of VisionEdge AI Surveillance Studio.