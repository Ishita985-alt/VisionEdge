# VisionEdge AI Surveillance Studio

A modern **Computer Vision** and **Edge AI Surveillance System** developed as part of the **Python Development Internship at Axlero Solutions**.

VisionEdge is designed to provide intelligent real-time surveillance using computer vision techniques such as object detection, face recognition, event logging, recording, and automated alert generation.

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

---

# 📁 Project Structure

    VisionEdge/
    │
    ├── Images/
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
    │
    ├── scripts/
    │   ├── build_engine.py
    │   └── export_onnx.py
    │
    ├── streams/
    │
    ├── main.py
    ├── README.md
    └── .gitignore

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

---

# 🧪 Camera Manager Validation

The Camera Manager was successfully tested using a physical camera.

### Test Result

    VisionEdge Camera Manager Test

    [✓] Camera started successfully
    [✓] Resolution: 1280x720
    [✓] Camera window opened
    [✓] Press Q inside the camera window to stop
    [✓] Press ESC inside the camera window to stop
    [INFO] Stop key pressed.
    [✓] Camera released
    [✓] Camera test completed

The successful test confirms that the Camera Manager can initialize the camera, capture frames, configure the camera resolution, process the camera session, and release the camera resources correctly.

---

# 🚧 Upcoming Backend Development

The following modules will be implemented progressively:

- Frame Processing Pipeline
- YOLO Inference Integration
- Video Recording Module
- Snapshot Module
- SQLite Database Integration
- Event Logging
- Alert Management
- Dashboard Integration
- Integration with other VisionEdge modules

---

# 📅 Development Timeline

| Day | Development Area | Status |
|-----|------------------|--------|
| Day 1 | Backend Initialization & Configuration | ✅ Completed |
| Day 2 | Camera Manager & Frame Capture | ✅ Completed |
| Day 3 | Frame Processing Pipeline | 🚧 Upcoming |
| Day 4 | Database & Event Logging | 🚧 Upcoming |
| Day 5 | Recording & Snapshot Management | 🚧 Upcoming |
| Day 6 | Alert Management & Backend Integration | 🚧 Upcoming |
| Day 7 | Testing, Integration & Final Review | 🚧 Upcoming |

> **Note:** The development timeline may be adjusted based on team discussions, module dependencies, and internship deliverables.

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

> **Note:** Work distribution and module assignments are currently in progress. Individual responsibilities will be updated as development progresses.

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

**Project Version:** `0.2.0`

### ✅ Completed Modules

- Project Structure
- Backend Initialization
- Configuration System
- Camera Manager
- Camera Frame Capture
- Camera Testing

### 🚧 Modules Under Development

- Frame Processing Pipeline
- AI Inference
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

# 🔗 Repository

### Team Repository

https://github.com/Ishita985-alt/VisionEdge

### Backend Development Repository

https://github.com/Ravikumar07-Byte/VisionEdge-Backend

> The team repository is used for collaborative development. The backend repository is maintained separately to preserve the backend development history and contributions.

---

# 📄 License

This project is developed as part of the **Python Development Internship at Axlero Solutions** for educational, learning, and demonstration purposes.

---

# ⭐ Acknowledgements

Special thanks to **Axlero Solutions** for providing the internship opportunity and project guidance, and to all contributors collaborating on the development of VisionEdge AI Surveillance Studio.