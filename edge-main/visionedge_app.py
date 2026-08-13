import os
import queue
import sqlite3
import threading
import time
from datetime import datetime, timezone

import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO

try:
    import face_recognition
except Exception:  # pragma: no cover - optional dependency fallback
    face_recognition = None

try:
    from alertsystem import send_alert
except Exception:  # pragma: no cover - fallback if module import fails
    send_alert = None


class VisionEdgeApp:
    def __init__(self, root=None, headless=False):
        self.headless = headless
        self.root = root if root is not None else (None if headless else tk.Tk())
        self.running = False
        self.recording = False
        self.mode = "object"
        self.frame_queue = queue.Queue(maxsize=2)
        self.latest_frame = None
        self.frame_count = 0
        self.detection_count = 0
        self.last_snapshot_path = None
        self.status_text = "Ready"
        self.model = None
        self.cap = None
        self.writer = None
        self.capture_thread = None
        self.db_path = os.path.join(os.path.dirname(__file__), "visionedge.db")
        self.snapshot_dir = os.path.join(os.path.dirname(__file__), "motion_images")
        os.makedirs(self.snapshot_dir, exist_ok=True)

        self.known_names = []
        self.known_encodings = []
        self._load_known_faces()
        self._init_db()
        self._load_model()

        if not self.headless:
            self._build_ui()
            self.root.after(100, self._refresh_ui)

    def _load_model(self):
        if self.model is None:
            model_path = os.path.join(os.path.dirname(__file__), "yolov8n.pt")
            if os.path.exists(model_path):
                self.model = YOLO(model_path)
            else:
                self.model = YOLO("yolov8n.pt")

    def _load_known_faces(self):
        if face_recognition is None:
            return
        known_dir = os.path.join(os.path.dirname(__file__), "known_faces")
        if not os.path.isdir(known_dir):
            return
        for filename in sorted(os.listdir(known_dir)):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            image_path = os.path.join(known_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.known_encodings.append(encodings[0])
                self.known_names.append(os.path.splitext(filename)[0])

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mode TEXT NOT NULL,
                label TEXT NOT NULL,
                confidence REAL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def _build_ui(self):
        self.root.title("VisionEdge AI Surveillance Studio")
        self.root.geometry("1420x900")
        self.root.minsize(1200, 760)
        self.root.configure(bg="#07111f")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#0b1424")
        style.configure("Sidebar.TFrame", background="#08111f")
        style.configure("Panel.TFrame", background="#0f1b31")
        style.configure("Accent.TButton", padding=8, relief="flat", background="#1a73ff")
        style.configure("Secondary.TButton", padding=8, relief="flat", background="#2b3c5d")
        style.map(
            "Accent.TButton",
            background=[("active", "#2b84ff"), ("pressed", "#0f5fd6")],
            foreground=[("active", "white")],
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#3a4d71"), ("pressed", "#23324d")],
            foreground=[("active", "white")],
        )
        style.configure("Heading.TLabel", background="#07111f", foreground="#f5fbff", font=("Helvetica", 20, "bold"))
        style.configure("Sub.TLabel", background="#07111f", foreground="#8fa5c1", font=("Helvetica", 10))
        style.configure("Metric.TLabel", background="#0f1b31", foreground="#eff7ff", font=("Helvetica", 12, "bold"))
        style.configure("MetricSmall.TLabel", background="#0f1b31", foreground="#8fa5c1", font=("Helvetica", 10))

        outer = ttk.Frame(self.root, padding=18, style="Card.TFrame")
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(outer, width=320, padding=18, style="Sidebar.TFrame")
        sidebar.grid(row=0, column=0, sticky="nswe", padx=(0, 16))
        sidebar.columnconfigure(0, weight=1)

        ttk.Label(sidebar, text="VisionEdge", style="Heading.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))
        ttk.Label(sidebar, text="AI security and edge analytics", style="Sub.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 16))

        info_frame = ttk.Frame(sidebar, padding=12, style="Panel.TFrame")
        info_frame.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        ttk.Label(info_frame, text="System State", style="Metric.TLabel").pack(anchor="w")
        self.status_badge = tk.Label(info_frame, text="Ready", bg="#183b2e", fg="#73f2aa", padx=10, pady=4, font=("Helvetica", 10, "bold"), bd=0)
        self.status_badge.pack(anchor="w", pady=(8, 0))

        self.start_button = ttk.Button(sidebar, text="Start Camera", command=self.start_camera, style="Accent.TButton")
        self.start_button.grid(row=3, column=0, sticky="ew", pady=6)
        self.stop_button = ttk.Button(sidebar, text="Stop Camera", command=self.stop_camera, style="Secondary.TButton")
        self.stop_button.grid(row=4, column=0, sticky="ew", pady=6)
        self.record_button = ttk.Button(sidebar, text="Toggle Recording", command=self.toggle_recording, style="Secondary.TButton")
        self.record_button.grid(row=5, column=0, sticky="ew", pady=6)
        self.snapshot_button = ttk.Button(sidebar, text="Save Snapshot", command=self.save_snapshot, style="Secondary.TButton")
        self.snapshot_button.grid(row=6, column=0, sticky="ew", pady=6)
        self.alert_button = ttk.Button(sidebar, text="Send Alert", command=self.send_alert, style="Secondary.TButton")
        self.alert_button.grid(row=7, column=0, sticky="ew", pady=6)

        mode_frame = ttk.LabelFrame(sidebar, text="Detection Mode", padding=12)
        mode_frame.grid(row=8, column=0, sticky="ew", pady=(16, 10))
        self.mode_var = tk.StringVar(value="object")
        ttk.Radiobutton(mode_frame, text="Object Detection", variable=self.mode_var, value="object", command=self._set_mode).pack(anchor="w")
        ttk.Radiobutton(mode_frame, text="Face Recognition", variable=self.mode_var, value="face", command=self._set_mode).pack(anchor="w")

        main = ttk.Frame(outer, padding=0, style="Card.TFrame")
        main.grid(row=0, column=1, sticky="nswe")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        header = ttk.Frame(main, padding=(16, 16, 16, 10), style="Card.TFrame")
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Live Edge Vision Console", style="Heading.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Monitor live streams, detect objects, protect spaces, and capture evidence in one place.", style="Sub.TLabel").grid(row=1, column=0, sticky="w", pady=(3, 8))

        metrics = ttk.Frame(main, padding=(16, 0, 16, 8), style="Card.TFrame")
        metrics.grid(row=1, column=0, sticky="ew")
        metrics.columnconfigure(0, weight=1)
        metrics.columnconfigure(1, weight=1)
        metrics.columnconfigure(2, weight=1)
        metrics.columnconfigure(3, weight=1)

        self.metric_camera = ttk.Label(metrics, text="Camera: Off", style="Metric.TLabel")
        self.metric_camera.grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self.metric_mode = ttk.Label(metrics, text="Mode: Object", style="Metric.TLabel")
        self.metric_mode.grid(row=0, column=1, padx=8, pady=4, sticky="w")
        self.metric_detections = ttk.Label(metrics, text="Detections: 0", style="Metric.TLabel")
        self.metric_detections.grid(row=0, column=2, padx=8, pady=4, sticky="w")
        self.metric_recording = ttk.Label(metrics, text="Recording: Off", style="Metric.TLabel")
        self.metric_recording.grid(row=0, column=3, padx=8, pady=4, sticky="w")

        preview_panel = ttk.Frame(main, padding=10, style="Card.TFrame")
        preview_panel.grid(row=2, column=0, sticky="nsew")
        preview_panel.columnconfigure(0, weight=1)
        preview_panel.rowconfigure(0, weight=1)
        self.preview_frame = ttk.Frame(preview_panel, padding=6, style="Panel.TFrame")
        self.preview_frame.grid(row=0, column=0, sticky="nsew")
        self.preview_label = tk.Label(self.preview_frame, bg="#050b16", bd=0, anchor="center")
        self.preview_label.pack(fill="both", expand=True)

        log_frame = ttk.LabelFrame(main, text="Activity Log", padding=10)
        log_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        self.log_text = tk.Text(log_frame, height=8, bg="#07111f", fg="#e9f7ff", relief="flat")
        self.log_text.pack(fill="both", expand=True)
        self.log_text.insert("end", "VisionEdge is ready. Start the stream to begin processing frames.\n")
        self.log_text.configure(state="disabled")

    def _set_mode(self):
        self.mode = self.mode_var.get()
        self._append_log(f"Mode switched to {self.mode}")
        self._refresh_metrics()

    def start_camera(self):
        if self.running:
            return
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", "Unable to access the webcam.")
            return
        self.running = True
        self.status_text = "Streaming"
        self._append_log("Camera started")
        self._refresh_metrics()
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()

    def stop_camera(self):
        self.running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if self.writer is not None:
            self.writer.release()
            self.writer = None
        self.recording = False
        self.status_text = "Stopped"
        self._append_log("Camera stopped")
        self._refresh_metrics()

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            self._append_log("Recording enabled")
        else:
            self._append_log("Recording disabled")
        self._refresh_metrics()

    def save_snapshot(self):
        if self.latest_frame is None:
            messagebox.showinfo("Snapshot", "No frame available yet.")
            return
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.snapshot_dir, f"snapshot_{timestamp}.jpg")
        success = cv2.imwrite(path, self.latest_frame)
        if success:
            self.last_snapshot_path = path
            self._append_log(f"Snapshot saved to {path}")
        else:
            self._append_log("Snapshot save failed")

    def send_alert(self):
        if self.last_snapshot_path is None:
            self.save_snapshot()
        if self.last_snapshot_path is None:
            messagebox.showinfo("Alert", "No snapshot available to send.")
            return
        if send_alert is None:
            self._append_log("Alert delivery is not configured")
            return
        try:
            result = send_alert(self.last_snapshot_path)
            if result:
                self._append_log("Alert sent")
            else:
                self._append_log("Alert skipped")
        except Exception as exc:  # pragma: no cover - runtime fallback
            self._append_log(f"Alert failed: {exc}")

    def _capture_loop(self):
        while self.running:
            if self.cap is None or not self.cap.isOpened():
                break
            ok, frame = self.cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            annotated = self._process_frame(frame)
            self.frame_queue.put(annotated)
            if not self.headless:
                self.root.after(0, self._refresh_preview)
            time.sleep(0.03)
        self.stop_camera()

    def _process_frame(self, frame):
        if self.mode == "object":
            if self.model is None:
                self._load_model()
            results = self.model(frame, imgsz=320, conf=0.45, stream=False)
            annotated = results[0].plot()
            boxes = results[0].boxes
            labels = [self.model.names[int(item.cls)] for item in boxes] if boxes else []
            self.detection_count = len(labels)
            if labels:
                self._log_event("Object", labels[0], 0.0)
        else:
            annotated = frame.copy()
            if face_recognition is not None:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb)
                face_encodings = face_recognition.face_encodings(rgb, face_locations)
                for face_encoding, face_location in zip(face_encodings, face_locations):
                    if self.known_encodings:
                        matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.55)
                        label = "Unknown"
                        if True in matches:
                            label = self.known_names[matches.index(True)]
                        else:
                            self._log_event("Face", "Unknown visitor", 0.0)
                    else:
                        label = "Visitor"
                    top, right, bottom, left = face_location
                    cv2.rectangle(annotated, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(annotated, label, (left, max(top - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    self.detection_count = len(face_locations)
                    if label != "Unknown":
                        self._log_event("Face", label, 0.0)
            else:
                self.detection_count = 0
        self.frame_count += 1
        if self.recording:
            self._ensure_writer(frame.shape[1], frame.shape[0])
            if self.writer is not None and self.writer.isOpened():
                self.writer.write(annotated)
        cv2.putText(annotated, f"Mode: {self.mode}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(annotated, f"Frames: {self.frame_count}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        self.latest_frame = annotated
        return annotated

    def _ensure_writer(self, width, height):
        if self.writer is not None and self.writer.isOpened():
            return
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.snapshot_dir, f"recording_{timestamp}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(path, fourcc, 20.0, (width, height))
        self._append_log(f"Recording started: {path}")

    def _refresh_preview(self):
        if self.frame_queue.qsize() == 0:
            return
        try:
            frame = self.frame_queue.get_nowait()
        except queue.Empty:
            return
        height, width, _ = frame.shape
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = image.resize((900, 500))
        photo = ImageTk.PhotoImage(image=image)
        self.preview_label.configure(image=photo)
        self.preview_label.image = photo
        self._refresh_metrics()

    def _refresh_ui(self):
        self._refresh_metrics()
        if not self.headless:
            self.root.after(200, self._refresh_ui)

    def _refresh_metrics(self):
        if self.headless:
            return
        state = "On" if self.running else "Off"
        self.metric_camera.config(text=f"Camera: {state}")
        self.metric_mode.config(text=f"Mode: {self.mode.title()}")
        self.metric_detections.config(text=f"Detections: {self.detection_count}")
        self.metric_recording.config(text=f"Recording: {'On' if self.recording else 'Off'}")
        self.status_badge.config(text=self.status_text)
        if self.running:
            self.status_badge.config(bg="#183b2e", fg="#73f2aa")
        else:
            self.status_badge.config(bg="#3f2f18", fg="#ffcb6b")

    def _append_log(self, message):
        if self.headless:
            return
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{datetime.now(timezone.utc).strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _log_event(self, category, label, confidence):
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        self._append_log(f"{category}: {label} at {timestamp}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO detections (mode, label, confidence, created_at) VALUES (?, ?, ?, ?)",
            (self.mode, label, confidence, timestamp),
        )
        conn.commit()
        conn.close()

    def _on_close(self):
        self.stop_camera()
        if self.root is not None:
            self.root.destroy()


def launch():
    root = tk.Tk()
    app = VisionEdgeApp(root=root)
    root.mainloop()


if __name__ == "__main__":
    launch()
