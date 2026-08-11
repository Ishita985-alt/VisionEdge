import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

function App() {
    const [backendOnline, setBackendOnline] = useState(false);
    const [cameraStatus, setCameraStatus] = useState("OFFLINE");
    const [databaseStatus, setDatabaseStatus] = useState("UNKNOWN");
    const [events, setEvents] = useState([]);
    const [currentTime, setCurrentTime] = useState(new Date());
    const [loading, setLoading] = useState(false);
    const [activeNav, setActiveNav] = useState("Dashboard");

    useEffect(() => {
        checkBackend();
        loadStatus();
        loadEvents();

        const statusInterval = setInterval(() => {
            loadStatus();
        }, 5000);

        const clockInterval = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);

        return () => {
            clearInterval(statusInterval);
            clearInterval(clockInterval);
        };
    }, []);

    const checkBackend = async () => {
        try {
            const response = await fetch(`${API_URL}/health`);

            if (!response.ok) {
                throw new Error("Backend unavailable");
            }

            setBackendOnline(true);
        } catch (error) {
            console.error("Backend connection failed:", error);
            setBackendOnline(false);
        }
    };

    const loadStatus = async () => {
        try {
            const response = await fetch(`${API_URL}/api/status`);

            if (!response.ok) {
                throw new Error("Status request failed");
            }

            const data = await response.json();

            setBackendOnline(true);

            if (data.camera) {
                setCameraStatus(
                    String(data.camera).toUpperCase()
                );
            }

            if (data.database) {
                setDatabaseStatus(
                    String(data.database).toUpperCase()
                );
            }
        } catch (error) {
            console.error("Status error:", error);
            setBackendOnline(false);
        }
    };

    const loadEvents = async () => {
        try {
            const response = await fetch(`${API_URL}/api/events`);

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            if (Array.isArray(data)) {
                setEvents(data);
            }
        } catch (error) {
            console.error("Events error:", error);
        }
    };

    const startCamera = async () => {
        setLoading(true);

        try {
            const response = await fetch(
                `${API_URL}/start_camera`,
                {
                    method: "POST",
                }
            );

            const data = await response.json();

            if (data.success) {
                setCameraStatus("ONLINE");
            } else {
                alert(data.message || "Unable to start camera");
            }
        } catch (error) {
            console.error(error);
            alert("Could not connect to backend.");
        }

        setLoading(false);
        loadStatus();
    };

    const stopCamera = async () => {
        try {
            await fetch(
                `${API_URL}/stop_camera`,
                {
                    method: "POST",
                }
            );

            setCameraStatus("OFFLINE");
        } catch (error) {
            console.error(error);
        }

        loadStatus();
    };

    const captureSnapshot = async () => {
        try {
            const response = await fetch(
                `${API_URL}/capture_snapshot`,
                {
                    method: "POST",
                }
            );

            const data = await response.json();

            if (data.success) {
                alert("Snapshot captured successfully.");
            } else {
                alert(data.message || "Snapshot failed.");
            }
        } catch (error) {
            console.error(error);
            alert("Could not capture snapshot.");
        }
    };

    const cameraOnline =
        cameraStatus === "ONLINE" ||
        cameraStatus === "RUNNING";

    const formattedTime = currentTime.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        }
    );

    return (
        <div className="app">

            {/* SIDEBAR */}

            <aside className="sidebar">

                <div className="brand">
                    <div className="brand-logo">
                        VE
                    </div>

                    <div>
                        <h2>VisionEdge</h2>
                        <span>AI Surveillance</span>
                    </div>
                </div>

                <nav className="navigation">

                    <button
                        className={`nav-item ${
                            activeNav === "Dashboard"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveNav("Dashboard")
                        }
                    >
                        <span>⌂</span>
                        Dashboard
                    </button>

                    <button
                        className={`nav-item ${
                            activeNav === "Live Camera"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveNav("Live Camera")
                        }
                    >
                        <span>◉</span>
                        Live Camera
                    </button>

                    <button
                        className={`nav-item ${
                            activeNav === "Events"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveNav("Events")
                        }
                    >
                        <span>◈</span>
                        Security Events
                    </button>

                    <button
                        className={`nav-item ${
                            activeNav === "Snapshots"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveNav("Snapshots")
                        }
                    >
                        <span>▣</span>
                        Snapshots
                    </button>

                    <button
                        className={`nav-item ${
                            activeNav === "Analytics"
                                ? "active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveNav("Analytics")
                        }
                    >
                        <span>◫</span>
                        Analytics
                    </button>

                </nav>

                <div className="sidebar-bottom">

                    <div className="system-mini">

                        <span
                            className={`status-dot ${
                                backendOnline
                                    ? "online"
                                    : "offline"
                            }`}
                        />

                        <div>
                            <strong>
                                System
                            </strong>

                            <small>
                                {backendOnline
                                    ? "Operational"
                                    : "Offline"}
                            </small>
                        </div>

                    </div>

                </div>

            </aside>


            {/* MAIN */}

            <main className="main">

                {/* TOPBAR */}

                <header className="topbar">

                    <div>
                        <div className="breadcrumb">
                            VisionEdge / Dashboard
                        </div>

                        <h1>
                            AI Surveillance Dashboard
                        </h1>

                        <p>
                            Real-time monitoring and intelligent
                            security analysis
                        </p>
                    </div>

                    <div className="topbar-right">

                        <div className="system-online">

                            <span
                                className={`status-dot ${
                                    backendOnline
                                        ? "online"
                                        : "offline"
                                }`}
                            />

                            {backendOnline
                                ? "SYSTEM ONLINE"
                                : "SYSTEM OFFLINE"}

                        </div>

                        <div className="clock">
                            {formattedTime}
                        </div>

                        <div className="profile">
                            A
                        </div>

                    </div>

                </header>


                {/* STAT CARDS */}

                <section className="stats-grid">

                    <div className="stat-card">

                        <div className="stat-header">
                            <span>
                                CAMERA STATUS
                            </span>

                            <span className="stat-icon">
                                ◉
                            </span>
                        </div>

                        <div
                            className={`stat-value ${
                                cameraOnline
                                    ? "green"
                                    : "red"
                            }`}
                        >
                            {cameraStatus}
                        </div>

                        <div className="stat-subtitle">
                            Primary surveillance camera
                        </div>

                    </div>


                    <div className="stat-card">

                        <div className="stat-header">
                            <span>
                                SECURITY EVENTS
                            </span>

                            <span className="stat-icon">
                                ◈
                            </span>
                        </div>

                        <div className="stat-value">
                            {events.length}
                        </div>

                        <div className="stat-subtitle">
                            Recorded security events
                        </div>

                    </div>


                    <div className="stat-card">

                        <div className="stat-header">
                            <span>
                                AI MODEL
                            </span>

                            <span className="stat-icon">
                                ✦
                            </span>
                        </div>

                        <div className="stat-value green">
                            READY
                        </div>

                        <div className="stat-subtitle">
                            YOLO object detection
                        </div>

                    </div>


                    <div className="stat-card">

                        <div className="stat-header">
                            <span>
                                DATABASE
                            </span>

                            <span className="stat-icon">
                                ◫
                            </span>
                        </div>

                        <div className="stat-value green">
                            {databaseStatus}
                        </div>

                        <div className="stat-subtitle">
                            Event storage system
                        </div>

                    </div>

                </section>


                {/* CAMERA + STATUS */}

                <section className="dashboard-grid">

                    {/* CAMERA */}

                    <div className="panel camera-panel">

                        <div className="panel-header">

                            <div>
                                <h2>
                                    Live Surveillance
                                </h2>

                                <span>
                                    Primary camera feed
                                </span>
                            </div>

                            <div
                                className={`live-badge ${
                                    cameraOnline
                                        ? "online"
                                        : ""
                                }`}
                            >
                                {cameraOnline
                                    ? "● LIVE"
                                    : "● OFFLINE"}
                            </div>

                        </div>


                        <div className="camera-container">

                            {cameraOnline ? (
                                <img
                                    src={`${API_URL}/video_feed`}
                                    alt="Live camera feed"
                                    className="camera-feed"
                                />
                            ) : (
                                <div className="camera-placeholder">

                                    <div className="camera-icon">
                                        ◉
                                    </div>

                                    <h3>
                                        Camera Offline
                                    </h3>

                                    <p>
                                        Start the camera to begin
                                        live surveillance.
                                    </p>

                                </div>
                            )}

                        </div>


                        <div className="camera-controls">

                            <button
                                className="btn btn-start"
                                onClick={startCamera}
                                disabled={
                                    loading ||
                                    cameraOnline
                                }
                            >
                                ▶ Start Camera
                            </button>

                            <button
                                className="btn btn-stop"
                                onClick={stopCamera}
                                disabled={!cameraOnline}
                            >
                                ■ Stop Camera
                            </button>

                            <button
                                className="btn btn-snapshot"
                                onClick={captureSnapshot}
                                disabled={!cameraOnline}
                            >
                                ◎ Snapshot
                            </button>

                        </div>

                    </div>


                    {/* STATUS */}

                    <div className="panel">

                        <div className="panel-header">

                            <div>
                                <h2>
                                    System Status
                                </h2>

                                <span>
                                    Infrastructure health
                                </span>
                            </div>

                        </div>


                        <div className="status-list">

                            <div className="status-row">

                                <div>
                                    <strong>
                                        Backend API
                                    </strong>

                                    <small>
                                        Flask server
                                    </small>
                                </div>

                                <span
                                    className={`badge ${
                                        backendOnline
                                            ? "ready"
                                            : "offline"
                                    }`}
                                >
                                    {backendOnline
                                        ? "ONLINE"
                                        : "OFFLINE"}
                                </span>

                            </div>


                            <div className="status-row">

                                <div>
                                    <strong>
                                        Camera
                                    </strong>

                                    <small>
                                        Video capture device
                                    </small>
                                </div>

                                <span
                                    className={`badge ${
                                        cameraOnline
                                            ? "ready"
                                            : "offline"
                                    }`}
                                >
                                    {cameraOnline
                                        ? "ONLINE"
                                        : "OFFLINE"}
                                </span>

                            </div>


                            <div className="status-row">

                                <div>
                                    <strong>
                                        YOLO AI Model
                                    </strong>

                                    <small>
                                        Object detection engine
                                    </small>
                                </div>

                                <span className="badge ready">
                                    READY
                                </span>

                            </div>


                            <div className="status-row">

                                <div>
                                    <strong>
                                        Database
                                    </strong>

                                    <small>
                                        Event persistence
                                    </small>
                                </div>

                                <span className="badge ready">
                                    {databaseStatus}
                                </span>

                            </div>

                        </div>

                    </div>

                </section>


                {/* EVENTS */}

                <section className="panel events-panel">

                    <div className="panel-header">

                        <div>
                            <h2>
                                Recent Security Events
                            </h2>

                            <span>
                                Latest events detected by VisionEdge
                            </span>
                        </div>

                        <button
                            className="refresh-btn"
                            onClick={loadEvents}
                        >
                            ↻ Refresh
                        </button>

                    </div>


                    <div className="table-container">

                        <table>

                            <thead>

                                <tr>
                                    <th>Time</th>
                                    <th>Event</th>
                                    <th>Camera</th>
                                    <th>Severity</th>
                                    <th>Status</th>
                                </tr>

                            </thead>

                            <tbody>

                                {events.length === 0 ? (

                                    <tr>

                                        <td
                                            colSpan="5"
                                            className="empty-state"
                                        >
                                            No security events
                                            recorded yet.
                                        </td>

                                    </tr>

                                ) : (

                                    events.map(
                                        (event, index) => (

                                            <tr key={index}>

                                                <td>
                                                    {event.timestamp ||
                                                        event.time ||
                                                        "—"}
                                                </td>

                                                <td>
                                                    {event.event ||
                                                        event.type ||
                                                        "Detection"}
                                                </td>

                                                <td>
                                                    {event.camera ||
                                                        "Camera 1"}
                                                </td>

                                                <td>
                                                    <span className="severity-info">
                                                        {event.severity ||
                                                            "INFO"}
                                                    </span>
                                                </td>

                                                <td>
                                                    <span className="badge ready">
                                                        DETECTED
                                                    </span>
                                                </td>

                                            </tr>

                                        )
                                    )

                                )}

                            </tbody>

                        </table>

                    </div>

                </section>

            </main>

        </div>
    );
}

export default App;