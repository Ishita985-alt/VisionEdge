# VisionEdge AI Surveillance Studio

A modern **Computer Vision** and **Edge AI Surveillance System** developed as part of the **Python Development Internship at Axlero Solutions**.

VisionEdge is designed to provide intelligent real-time surveillance using computer vision techniques such as object detection, face recognition, event logging, recording, and automated alert generation.

The project follows a modular architecture so that camera management, frame processing, AI inference, database logging, recording, alerts, and dashboard components can be developed and integrated independently.

---

# 🚀 Features

- Live camera feed
- Modern desktop dashboard
- Real-time object detection using **Ultralytics YOLO**
- Face recognition with known-face matching
- Video recording
- Snapshot capture
- Intelligent alert generation
- SQLite-based event logging
- Modular backend architecture
- Configurable application settings
- Organized project structure for collaborative development

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
│   ├── requirements.txt
│   │
│   └── database/
│       ├── database_manager.py
│       └── test_database.py
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

# Technology Stack

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

# Backend Development Progress

## Day 1 – Backend Initialization

Completed the initial backend project setup.

- Backend project initialization
- Configuration management system
- Automatic project directory creation
- Backend startup system
- Project folder organization
- Dependency management
- Python project configuration
- Git ignore configuration

Status: Completed

---

## Day 2 – Camera Manager

Implemented the Camera Manager using OpenCV.

- Camera initialization and startup
- Camera availability checking
- Camera resolution configuration
- Real-time frame capture
- Camera start and stop functionality
- Camera resource cleanup
- Frame capture error handling
- Camera operation logging
- Camera testing module
- Successful camera testing at 1280x720 resolution
- Q and ESC keyboard controls for safely stopping the camera

Status: Completed

---

## Day 3 – Frame Processing Pipeline

Implemented the Frame Processing Pipeline as an independent backend module.

- Created the `processing` module
- Implemented `FrameProcessor`
- Added frame validation
- Added invalid and empty frame handling
- Added frame resizing
- Added basic frame preprocessing
- Added processing error handling
- Added frame processing logging
- Created `test_frame_processor.py`
- Tested a 1280x720 input frame
- Successfully processed the frame to 640x640
- Tested invalid frame handling
- Prepared the processing layer for future AI inference integration

Status: Completed

---

## Day 4 – SQLite Database and Event Logging

Implemented the SQLite Database Manager for storing VisionEdge surveillance events.
## Day 5 — Video Recording Module

Implemented the VisionEdge video recording module using OpenCV.

- Created `VideoRecorder` class for video recording.
- Added video writer initialization with configurable FPS and codec.
- Added frame writing and frame-size handling.
- Added recording start and stop functionality.
- Added recording state management.
- Added resource cleanup and error handling.
- Created `test_video_recorder.py` to validate recording functionality.
- Verified successful generation of `test_recording.mp4`.
- Added invalid-frame validation and testing.

## Day 6 — Camera & Video Recording Integration

Integrated the video recording module with the VisionEdge backend `CameraManager`.

- Integrated `VideoRecorder` into `CameraManager`.
- Automatically starts recording when the camera starts.
- Records processed camera frames during live operation.
- Stops and releases the recorder when the camera stops.
- Added `CameraManager` resource cleanup for the video recorder.
- Created `backend/test_recording_integration.py`.
- Tested camera startup, YOLO frame processing, video recording, and camera shutdown.
- Successfully processed camera frames and generated `visionedge_recording.mp4`.
- Verified that recording becomes inactive after the camera stops.
### Database Manager

- Created the `backend/database` module
- Implemented `DatabaseManager`
- Added SQLite database initialization
- Added automatic database directory creation
- Added database connection management
- Added events table creation
- Added surveillance event insertion
- Added event retrieval
- Added database error handling
- Added database operation logging
- Added support for configurable database paths

### Event Structure

The events table contains:

| Field | Description |
|-------|-------------|
| id | Unique event identifier |
| timestamp | Event creation time |
| camera_id | Camera associated with the event |
| event_type | Type of surveillance event |
| description | Description of the event |
| severity | Event severity level |

### Database Location

The SQLite database is automatically created at:

```text
output/database/visionedge.db
```

### Database Testing

The Database Manager was successfully tested for:

- Database initialization
- Events table creation
- Event insertion
- Event retrieval
- Database logging
- SQLite connection handling

### Test Result

```text
# VisionEdge Database Manager Test

[✓] Database initialized successfully
[✓] Events table created successfully
[✓] Event inserted successfully: ID 1
[✓] Retrieved 1 event(s)

ID: 1
Camera: camera_0
Type: motion_detected
Severity: INFO

[✓] Day 4 Database Manager test completed successfully
```

Status: Completed

---

# Current Backend Flow

The current backend architecture is:

```text
Camera
   |
   v
Camera Manager
   |
   | Raw OpenCV Frame
   v
Frame Processor
   |
   | Validation
   | Preprocessing
   | Resizing
   v
Processed Frame
   |
   v
Future AI / YOLO Inference
   |
   v
Surveillance Event
   |
   v
Database Manager
   |
   v
SQLite Database
```

The individual modules are kept independent so that they can be integrated progressively without creating unnecessary dependencies between team members' work.

---

# Backend Modules Completed

The following backend components have been completed:

- Backend Initialization
- Configuration Management
- Camera Manager
- Camera Frame Capture
- Camera Testing
- Frame Processor
- Frame Validation
- Frame Resizing
- Frame Processing Testing
- SQLite Database Manager
- Event Table
- Event Insertion
- Event Retrieval
- Database Testing

---

# Upcoming Backend Development

The following modules are planned for subsequent development:

- YOLO Inference Integration
- Video Recording Module
- Snapshot Module
- Event Logging Integration
- Alert Management
- Dashboard Integration
- Backend Integration with Other VisionEdge Modules
- End-to-end system testing

---

# Development Timeline

|Day	Development Area	Status
Day 1	Backend Initialization and Configuration	Completed
Day 2	Camera Manager and Frame Capture	Completed
Day 3	Frame Processing Pipeline	Completed
Day 4	SQLite Database and Event Logging	Completed
Day 5	Video Recording Module	Completed
Day 6	Camera & Video Recording Integration	Completed
Day 7	Alert Management, Testing and Final Review	Upcoming

The development timeline may be adjusted based on team discussions, module dependencies, and internship requirements.

---

# Internship Information

| Field | Details |
|-------|---------|
| Organization | Axlero Solutions |
| Internship | Python Development Internship |
| Project | VisionEdge AI Surveillance Studio |
| Domain | Computer Vision and Edge AI |

---

# Team Members

This project is being developed collaboratively as part of the **Python Development Internship at Axlero Solutions**.

| Sl. No. | Team Member |
|---------|-------------|
| 1 | Ishita Bhariya |
| 2 | Shri Abishek M K |
| 3 | Bairi Saivardhan |
| 4 | Saifuddin |
| 5 | Ravikumar S |
| 6 | Anthati Venkatesh |

Work distribution and module assignments are coordinated collaboratively among the team members.

---

# Contributors

| Contributor | Current Status |
|-------------|----------------|
| Ishita Bhariya | Repository Owner |
| Anthati Venkatesh | Team Member |
| Shri Abishek M K | Team Member |
| Bairi Saivardhan | Team Member |
| Saifuddin | Team Member |
| Ravikumar S (@Ravikumar07-Byte) | Backend Development and Repository Contributor |

---

# Current Status

Project Version: `0.4.0`

## Completed Modules

- Project Structure
- Backend Initialization
- Configuration System
- Camera Manager
- Camera Frame Capture
- Camera Testing
- Frame Processing Pipeline
- Frame Validation
- Frame Resizing
- Frame Processing Testing
- SQLite Database Manager
- Events Table
- Event Insertion
- Event Retrieval
- Database Testing

## Modules Under Development

- YOLO / AI Inference Integration
- Video Recording
- Snapshot Management
- Alert Management
- Dashboard Integration
- Backend Integration
- End-to-End Testing

---

# Future Enhancements

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

# Repositories

## Team Repository

https://github.com/Ishita985-alt/VisionEdge

## Backend Development Repository

https://github.com/Ravikumar07-Byte/VisionEdge-Backend

The team repository is used for collaborative project development. The backend development repository maintains the backend development history and contributions.

---

# License

This project is developed as part of the **Python Development Internship at Axlero Solutions** for educational, learning, and demonstration purposes.

---

# Acknowledgements

Special thanks to **Axlero Solutions** for providing the internship opportunity and project guidance, and to all contributors collaborating on the development of VisionEdge AI Surveillance Studio.