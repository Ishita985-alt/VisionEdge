document.addEventListener("DOMContentLoaded", () => {

    const startButton =
        document.getElementById("startCamera");

    const stopButton =
        document.getElementById("stopCamera");

    const snapshotButton =
        document.getElementById("snapshotButton");

    const cameraFeed =
        document.getElementById("cameraFeed");

    const cameraPlaceholder =
        document.getElementById("cameraPlaceholder");

    const cameraStatus =
        document.getElementById("cameraStatus");

    const fpsValue =
        document.getElementById("fpsValue");

    const inferenceValue =
        document.getElementById("inferenceValue");

    const detectionsValue =
        document.getElementById("detectionsValue");

    const liveBadge =
        document.getElementById("liveBadge");

    const cameraBadge =
        document.getElementById("cameraBadge");

    const resolutionValue =
        document.getElementById("resolutionValue");

    const databaseBadge =
        document.getElementById("databaseBadge");

    const connectionDot =
        document.getElementById("connectionDot");

    const connectionText =
        document.getElementById("connectionText");

    const systemDot =
        document.getElementById("systemDot");

    const systemStatus =
        document.getElementById("systemStatus");

    const eventsTable =
        document.getElementById("eventsTable");

    const refreshEvents =
        document.getElementById("refreshEvents");

    const snapshotUrl =
        "/capture_snapshot";


    // ==========================================
    // TIME
    // ==========================================

    function updateTime() {

        const element =
            document.getElementById("currentTime");

        if (!element) {
            return;
        }

        element.textContent =
            new Date().toLocaleTimeString();

    }

    updateTime();

    setInterval(updateTime, 1000);


    // ==========================================
    // NOTIFICATION
    // ==========================================

    function showNotification(message, type = "success") {

        const notification =
            document.getElementById("notification");

        notification.textContent = message;

        notification.className =
            "notification show " + type;

        setTimeout(() => {

            notification.className =
                "notification";

        }, 3000);

    }


    // ==========================================
    // SYSTEM STATUS
    // ==========================================

    async function loadStatus() {

        try {

            const response =
                await fetch("/api/status");

            if (!response.ok) {
                throw new Error("Status request failed");
            }

            const data =
                await response.json();


            connectionDot.className =
                "status-dot online";

            connectionText.textContent =
                "Backend Connected";

            systemDot.className =
                "status-dot online";

            systemStatus.textContent =
                "Online";


            cameraStatus.textContent =
                data.camera_status || "OFFLINE";


            fpsValue.textContent =
                Number(data.fps || 0).toFixed(1);


            inferenceValue.textContent =
                Number(data.inference_time || 0).toFixed(1)
                + " ms";


            detectionsValue.textContent =
                data.total_detections || 0;


            resolutionValue.textContent =
                data.resolution || "-- × --";


            databaseBadge.textContent =
                data.database || "DISABLED";


            if (data.database === "CONNECTED") {

                databaseBadge.className =
                    "badge ready";

            } else {

                databaseBadge.className =
                    "badge warning";

            }


            updateCameraUI(
                data.camera_status === "ONLINE"
            );

        }

        catch (error) {

            console.error(error);

            connectionDot.className =
                "status-dot offline";

            connectionText.textContent =
                "Backend Offline";

            systemDot.className =
                "status-dot offline";

            systemStatus.textContent =
                "Offline";

        }

    }


    // ==========================================
    // CAMERA UI
    // ==========================================

    function updateCameraUI(isOnline) {

        if (isOnline) {

            cameraStatus.textContent =
                "ONLINE";

            cameraBadge.textContent =
                "ONLINE";

            cameraBadge.className =
                "badge ready";

            liveBadge.textContent =
                "LIVE";

            liveBadge.className =
                "live-badge online";

            cameraPlaceholder.style.display =
                "none";

            cameraFeed.style.display =
                "block";

            startButton.disabled =
                true;

            stopButton.disabled =
                false;

            snapshotButton.disabled =
                false;

        }

        else {

            cameraStatus.textContent =
                "OFFLINE";

            cameraBadge.textContent =
                "OFFLINE";

            cameraBadge.className =
                "badge offline";

            liveBadge.textContent =
                "OFFLINE";

            liveBadge.className =
                "live-badge";

            cameraPlaceholder.style.display =
                "block";

            cameraFeed.style.display =
                "none";

            cameraFeed.src = "";

            startButton.disabled =
                false;

            stopButton.disabled =
                true;

            snapshotButton.disabled =
                true;

        }

    }


    // ==========================================
    // START CAMERA
    // ==========================================

    startButton.addEventListener(
        "click",
        async () => {

            startButton.disabled =
                true;

            try {

                const response =
                    await fetch(
                        "/start_camera",
                        {
                            method: "POST"
                        }
                    );

                const data =
                    await response.json();


                if (!data.success) {

                    throw new Error(
                        data.message ||
                        "Camera could not start"
                    );

                }


                cameraFeed.src =
                    "/video_feed?t=" +
                    Date.now();


                updateCameraUI(true);

                showNotification(
                    "Camera started successfully.",
                    "success"
                );

            }

            catch (error) {

                console.error(error);

                updateCameraUI(false);

                showNotification(
                    error.message,
                    "error"
                );

            }

        }
    );


    // ==========================================
    // STOP CAMERA
    // ==========================================

    stopButton.addEventListener(
        "click",
        async () => {

            try {

                const response =
                    await fetch(
                        "/stop_camera",
                        {
                            method: "POST"
                        }
                    );

                const data =
                    await response.json();


                if (!data.success) {

                    throw new Error(
                        data.message ||
                        "Camera could not stop"
                    );

                }


                cameraFeed.src = "";

                updateCameraUI(false);

                showNotification(
                    "Camera stopped.",
                    "success"
                );

            }

            catch (error) {

                console.error(error);

                showNotification(
                    error.message,
                    "error"
                );

            }

        }
    );


    // ==========================================
    // SNAPSHOT
    // ==========================================

    snapshotButton.addEventListener(
        "click",
        async () => {

            try {

                const response =
                    await fetch(
                        snapshotUrl,
                        {
                            method: "POST"
                        }
                    );

                const data =
                    await response.json();


                if (!data.success) {

                    throw new Error(
                        data.message ||
                        "Snapshot failed"
                    );

                }


                showNotification(
                    "Snapshot captured: " +
                    data.filename,
                    "success"
                );

            }

            catch (error) {

                console.error(error);

                showNotification(
                    error.message,
                    "error"
                );

            }

        }
    );


    // ==========================================
    // LOAD EVENTS
    // ==========================================

    async function loadEvents() {

        try {

            const response =
                await fetch("/api/events");

            if (!response.ok) {
                throw new Error(
                    "Could not load events"
                );
            }

            const events =
                await response.json();


            eventsTable.innerHTML = "";


            if (!Array.isArray(events) ||
                events.length === 0) {

                eventsTable.innerHTML = `
                    <tr>
                        <td
                            colspan="6"
                            class="empty-state"
                        >
                            No detection events yet.
                        </td>
                    </tr>
                `;

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
                    <td>${event.id ?? "-"}</td>

                    <td>
                        ${event.camera_id ?? "-"}
                    </td>

                    <td>
                        ${event.event_type ?? "-"}
                    </td>

                    <td>
                        ${event.description ?? "-"}
                    </td>

                    <td class="severity-${severity}">
                        ${event.severity ?? "INFO"}
                    </td>

                    <td>
                        ${event.created_at ?? "-"}
                    </td>
                `;


                eventsTable.appendChild(row);

            });

        }

        catch (error) {

            console.error(error);

            eventsTable.innerHTML = `
                <tr>
                    <td
                        colspan="6"
                        class="empty-state"
                    >
                        Unable to load events.
                    </td>
                </tr>
            `;

        }

    }


    refreshEvents.addEventListener(
        "click",
        loadEvents
    );


    // ==========================================
    // INITIAL LOAD
    // ==========================================

    loadStatus();

    loadEvents();


    // ==========================================
    // AUTO REFRESH
    // ==========================================

    setInterval(
        loadStatus,
        2000
    );

    setInterval(
        loadEvents,
        5000
    );

});