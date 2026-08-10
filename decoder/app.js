"use strict";

/*
 * VisionEdge AI Surveillance Studio
 * Dashboard Controller
 *
 * Connects the frontend to Flask:
 *
 * GET  /api/status
 * GET  /api/events
 * POST /start_camera
 * POST /stop_camera
 * POST /capture_snapshot
 */


// =========================================================
// ELEMENTS
// =========================================================

const cameraFeed = document.getElementById("cameraFeed");
const cameraPlaceholder = document.getElementById("cameraPlaceholder");

const startButton = document.getElementById("startCamera");
const stopButton = document.getElementById("stopCamera");
const snapshotButton = document.getElementById("captureSnapshot");

const cameraStatus = document.getElementById("cameraStatus");
const connectionStatus = document.getElementById("connectionStatus");

const fpsValue = document.getElementById("fpsValue");
const detectionValue = document.getElementById("detectionValue");
const inferenceValue = document.getElementById("inferenceValue");
const resolutionValue = document.getElementById("resolutionValue");

const eventsBody = document.getElementById("eventsBody");

const notification = document.getElementById("notification");


// =========================================================
// APPLICATION STATE
// =========================================================

let cameraRunning = false;
let statusInterval = null;
let eventsInterval = null;


// =========================================================
// NOTIFICATION
// =========================================================

function showNotification(message, type = "success") {

    if (!notification) {
        return;
    }

    notification.textContent = message;

    notification.classList.remove(
        "show",
        "success",
        "error"
    );

    notification.classList.add(type);
    notification.classList.add("show");

    setTimeout(() => {

        notification.classList.remove("show");

    }, 3000);
}


// =========================================================
// API HELPER
// =========================================================

async function apiRequest(url, options = {}) {

    try {

        const response = await fetch(url, options);

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.message || "Server request failed."
            );
        }

        return data;

    } catch (error) {

        console.error(
            `API error: ${url}`,
            error
        );

        throw error;
    }
}


// =========================================================
// START CAMERA
// =========================================================

async function startCamera() {

    if (cameraRunning) {
        return;
    }

    if (startButton) {
        startButton.disabled = true;
    }

    try {

        const data = await apiRequest(
            "/start_camera",
            {
                method: "POST"
            }
        );

        if (!data.success) {

            throw new Error(
                data.message || "Camera failed to start."
            );
        }

        cameraRunning = true;

        updateCameraUI(true);

        showNotification(
            "Camera started successfully.",
            "success"
        );

        /*
         * Small delay gives Flask time to start
         * the camera before requesting the stream.
         */
        setTimeout(() => {

            if (cameraFeed) {

                cameraFeed.src =
                    "/video_feed?time=" +
                    Date.now();

            }

        }, 300);

    } catch (error) {

        cameraRunning = false;

        updateCameraUI(false);

        showNotification(
            error.message,
            "error"
        );

    } finally {

        if (startButton) {
            startButton.disabled = false;
        }
    }
}


// =========================================================
// STOP CAMERA
// =========================================================

async function stopCamera() {

    if (!cameraRunning) {
        return;
    }

    if (stopButton) {
        stopButton.disabled = true;
    }

    try {

        const data = await apiRequest(
            "/stop_camera",
            {
                method: "POST"
            }
        );

        if (!data.success) {

            throw new Error(
                data.message || "Camera failed to stop."
            );
        }

        cameraRunning = false;

        updateCameraUI(false);

        showNotification(
            "Camera stopped.",
            "success"
        );

    } catch (error) {

        showNotification(
            error.message,
            "error"
        );

    } finally {

        if (stopButton) {
            stopButton.disabled = false;
        }
    }
}


// =========================================================
// SNAPSHOT
// =========================================================

async function captureSnapshot() {

    if (!cameraRunning) {

        showNotification(
            "Start the camera before capturing a snapshot.",
            "error"
        );

        return;
    }

    if (snapshotButton) {
        snapshotButton.disabled = true;
    }

    try {

        const data = await apiRequest(
            "/capture_snapshot",
            {
                method: "POST"
            }
        );

        if (!data.success) {

            throw new Error(
                data.message || "Snapshot failed."
            );
        }

        showNotification(
            "Snapshot captured successfully.",
            "success"
        );

    } catch (error) {

        showNotification(
            error.message,
            "error"
        );

    } finally {

        if (snapshotButton) {
            snapshotButton.disabled = false;
        }
    }
}


// =========================================================
// UPDATE CAMERA UI
// =========================================================

function updateCameraUI(isOnline) {

    cameraRunning = isOnline;

    if (cameraFeed) {

        if (isOnline) {

            cameraFeed.style.display = "block";

        } else {

            cameraFeed.style.display = "none";
            cameraFeed.removeAttribute("src");
        }
    }

    if (cameraPlaceholder) {

        cameraPlaceholder.style.display =
            isOnline ? "none" : "block";
    }

    if (startButton) {
        startButton.disabled = isOnline;
    }

    if (stopButton) {
        stopButton.disabled = !isOnline;
    }

    if (snapshotButton) {
        snapshotButton.disabled = !isOnline;
    }

    if (cameraStatus) {

        cameraStatus.textContent =
            isOnline ? "ONLINE" : "OFFLINE";

        cameraStatus.classList.remove(
            "online",
            "offline"
        );

        cameraStatus.classList.add(
            isOnline ? "online" : "offline"
        );
    }
}


// =========================================================
// LOAD SYSTEM STATUS
// =========================================================

async function loadStatus() {

    try {

        const status = await apiRequest(
            "/api/status"
        );

        // ---------------------------------------------
        // CAMERA
        // ---------------------------------------------

        const isOnline =
            status.camera_status === "ONLINE";

        if (isOnline !== cameraRunning) {

            updateCameraUI(isOnline);
        }

        // ---------------------------------------------
        // FPS
        // ---------------------------------------------

        if (fpsValue) {

            fpsValue.textContent =
                Number(status.fps || 0).toFixed(1);
        }

        // ---------------------------------------------
        // DETECTIONS
        // ---------------------------------------------

        if (detectionValue) {

            detectionValue.textContent =
                status.total_detections || 0;
        }

        // ---------------------------------------------
        // INFERENCE
        // ---------------------------------------------

        if (inferenceValue) {

            inferenceValue.textContent =
                `${Number(
                    status.inference_time || 0
                ).toFixed(1)} ms`;
        }

        // ---------------------------------------------
        // RESOLUTION
        // ---------------------------------------------

        if (resolutionValue) {

            resolutionValue.textContent =
                status.resolution || "--";
        }

        // ---------------------------------------------
        // CONNECTION
        // ---------------------------------------------

        if (connectionStatus) {

            connectionStatus.textContent =
                "Backend Connected";
        }

    } catch (error) {

        console.error(
            "Could not load system status:",
            error
        );

        if (connectionStatus) {

            connectionStatus.textContent =
                "Backend Offline";
        }
    }
}


// =========================================================
// LOAD EVENTS
// =========================================================

async function loadEvents() {

    try {

        const events = await apiRequest(
            "/api/events"
        );

        if (!eventsBody) {
            return;
        }

        eventsBody.innerHTML = "";

        if (!Array.isArray(events) || events.length === 0) {

            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td colspan="5" class="empty-state">
                    No surveillance events recorded.
                </td>
            `;

            eventsBody.appendChild(row);

            return;
        }

        events.forEach(event => {

            const row =
                document.createElement("tr");

            const severity =
                String(
                    event.severity || "INFO"
                ).toLowerCase();

            row.innerHTML = `
                <td>
                    ${escapeHTML(
                        formatTimestamp(
                            event.timestamp
                        )
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        event.camera_id || "-"
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        event.event_type || "-"
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        event.description || "-"
                    )}
                </td>

                <td>
                    <span class="severity-${severity}">
                        ${escapeHTML(
                            event.severity || "INFO"
                        )}
                    </span>
                </td>
            `;

            eventsBody.appendChild(row);

        });

    } catch (error) {

        console.error(
            "Could not load events:",
            error
        );
    }
}


// =========================================================
// FORMAT TIMESTAMP
// =========================================================

function formatTimestamp(timestamp) {

    if (!timestamp) {
        return "-";
    }

    try {

        const date =
            new Date(timestamp);

        if (Number.isNaN(date.getTime())) {
            return timestamp;
        }

        return date.toLocaleString();

    } catch {

        return timestamp;
    }
}


// =========================================================
// HTML ESCAPE
// =========================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        String(value ?? "");

    return div.innerHTML;
}


// =========================================================
// REFRESH EVENTS
// =========================================================

function refreshEvents() {

    loadEvents();
}


// =========================================================
// INITIALIZE DASHBOARD
// =========================================================

async function initializeDashboard() {

    console.log(
        "VisionEdge Dashboard initializing..."
    );

    updateCameraUI(false);

    await loadStatus();

    await loadEvents();

    /*
     * Update live status every second.
     */
    statusInterval = setInterval(
        loadStatus,
        1000
    );

    /*
     * Update event table every 3 seconds.
     */
    eventsInterval = setInterval(
        loadEvents,
        3000
    );

    console.log(
        "VisionEdge Dashboard ready."
    );
}


// =========================================================
// EVENT LISTENERS
// =========================================================

if (startButton) {

    startButton.addEventListener(
        "click",
        startCamera
    );
}

if (stopButton) {

    stopButton.addEventListener(
        "click",
        stopCamera
    );
}

if (snapshotButton) {

    snapshotButton.addEventListener(
        "click",
        captureSnapshot
    );
}


// =========================================================
// PAGE LOAD
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);


// =========================================================
// PAGE CLOSE
// =========================================================

window.addEventListener(
    "beforeunload",
    () => {

        if (statusInterval) {
            clearInterval(statusInterval);
        }

        if (eventsInterval) {
            clearInterval(eventsInterval);
        }
    }
);