"""VisionEdge Tkinter dashboard.

This GUI provides a left-side control panel with Start/Stop Live Camera,
Start/Stop Recording, Photo Analysis, class filters, sensitivity slider,
snapshot and export CSV. The right side shows the video, KPIs, a live
matplotlib graph of detections over time, and a table of recent detections.

The backend uses OpenCV and Ultralytics YOLO when available. Import-time
side effects are avoided by initializing heavy components lazily.
"""

import importlib
import threading
import time
import queue
import csv
import os
from datetime import datetime

try:
    TKINTER_MODULE = importlib.import_module("tkinter")
    from tkinter import ttk, filedialog, messagebox
except ImportError:
    TKINTER_MODULE = None

# Lazy imports for heavy dependencies
CV2_MODULE = None
YOLO = None
PIL_Image = None
ImageTk = None
MATPLOTLIB = None
PANDAS = None

# Dashboard configuration
MODEL_PATH = "yolov8n.pt"
OUT_FILE = "VisionEdge_Output.avi"


class VisionEdgeApp:
    def __init__(self, root):
        if TKINTER_MODULE is None:
            raise RuntimeError("tkinter is not available in this environment")

        self.root = root
        self.root.title("VisionEdge AI Dashboard")
        self.root.geometry("1200x800")

        # State
        self.camera = None
        self.model = None
        self.capture_thread = None
        self.capture_running = threading.Event()
        self.recording = False
        self.video_writer = None
        self.frame_queue = queue.Queue(maxsize=10)
        self.detections = []  # list of dicts
        self.fps = 0.0
        self.last_frame_time = None
        self.class_filters = set()
        self.sensitivity = 0.5

        self._lazy_imports()
        self._build_ui()

    def _lazy_imports(self):
        global CV2_MODULE, YOLO, PIL_Image, ImageTk, MATPLOTLIB, PANDAS
        try:
            CV2_MODULE = importlib.import_module("cv2")
        except ImportError:
            CV2_MODULE = None

        try:
            YOLO_MODULE = importlib.import_module("ultralytics")
            YOLO = YOLO_MODULE.YOLO
        except ImportError:
            YOLO = None

        try:
            PIL_Image = importlib.import_module("PIL.Image")
            ImageTk = importlib.import_module("PIL.ImageTk")
        except ImportError:
            PIL_Image = None
            ImageTk = None

        try:
            MATPLOTLIB = importlib.import_module("matplotlib")
            import matplotlib.pyplot as plt  # noqa: F401
        except ImportError:
            MATPLOTLIB = None

        try:
            PANDAS = importlib.import_module("pandas")
        except ImportError:
            PANDAS = None

    def _build_ui(self):
        # Left control panel
        left = TKINTER_MODULE.Frame(self.root, width=280)
        left.pack(side="left", fill="y", padx=10, pady=10)

        title = TKINTER_MODULE.Label(left, text="Controls", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))

        self.start_btn = TKINTER_MODULE.Button(left, text="Start Live Camera", width=25, command=self.start_camera)
        self.start_btn.pack(pady=6)

        self.stop_btn = TKINTER_MODULE.Button(left, text="Stop Live Camera", width=25, command=self.stop_camera, state="disabled")
        self.stop_btn.pack(pady=6)

        self.record_btn = TKINTER_MODULE.Button(left, text="Start Recording", width=25, command=self.toggle_recording, state="disabled")
        self.record_btn.pack(pady=6)

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)

        self.photo_btn = TKINTER_MODULE.Button(left, text="Analyze Photo", width=25, command=self.analyze_photo)
        self.photo_btn.pack(pady=6)

        self.snapshot_btn = TKINTER_MODULE.Button(left, text="Snapshot", width=25, command=self.snapshot, state="disabled")
        self.snapshot_btn.pack(pady=6)

        TKINTER_MODULE.Label(left, text="Sensitivity").pack(pady=(12, 0))
        self.sens_scale = TKINTER_MODULE.Scale(left, from_=0, to=1, resolution=0.05, orient="horizontal", length=200, command=self._on_sensitivity_change)
        self.sens_scale.set(self.sensitivity)
        self.sens_scale.pack(pady=6)

        TKINTER_MODULE.Label(left, text="Class Filters").pack(pady=(12, 0))
        self.class_var = TKINTER_MODULE.StringVar(value="All")
        self.class_combo = ttk.Combobox(left, textvariable=self.class_var, values=["All"], state="readonly")
        self.class_combo.pack(pady=6)
        self.class_combo.bind("<<ComboboxSelected>>", lambda e: self._on_class_filter())

        TKINTER_MODULE.Button(left, text="Export CSV", width=25, command=self.export_csv).pack(pady=10)

        TKINTER_MODULE.Button(left, text="Exit", width=25, command=self._on_exit).pack(side="bottom", pady=20)

        # Right main area
        right = TKINTER_MODULE.Frame(self.root)
        right.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Video display
        self.video_panel = TKINTER_MODULE.Label(right)
        self.video_panel.pack(fill="both", expand=True)

        # KPI bar
        kpi_frame = TKINTER_MODULE.Frame(right)
        kpi_frame.pack(fill="x", pady=6)

        self.kpi_detections = TKINTER_MODULE.Label(kpi_frame, text="Detections: 0", font=("Arial", 12, "bold"))
        self.kpi_detections.pack(side="left", padx=6)

        self.kpi_fps = TKINTER_MODULE.Label(kpi_frame, text="FPS: 0", font=("Arial", 12, "bold"))
        self.kpi_fps.pack(side="left", padx=6)

        # Bottom: graph and table
        bottom = TKINTER_MODULE.PanedWindow(right, orient="horizontal")
        bottom.pack(fill="both", expand=True)

        # Graph area
        graph_frame = TKINTER_MODULE.Frame(bottom, width=400)
        bottom.add(graph_frame)

        if MATPLOTLIB is not None:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib.pyplot as plt
            self.fig, self.ax = plt.subplots(figsize=(5, 3))
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.graph_x = []
            self.graph_y = []
        else:
            TKINTER_MODULE.Label(graph_frame, text="matplotlib not installed").pack()
            self.canvas = None

        # Table area
        table_frame = TKINTER_MODULE.Frame(bottom)
        bottom.add(table_frame)

        self.tree = ttk.Treeview(table_frame, columns=("time", "object", "conf"), show="headings")
        self.tree.heading("time", text="Time")
        self.tree.heading("object", text="Object")
        self.tree.heading("conf", text="Confidence")
        self.tree.pack(fill="both", expand=True)

        # Start UI update loop
        self._schedule_ui_update()

    def _on_sensitivity_change(self, val):
        try:
            self.sensitivity = float(val)
        except Exception:
            pass

    def _on_class_filter(self):
        val = self.class_var.get()
        if val == "All":
            self.class_filters = set()
        else:
            self.class_filters = {val}

    def start_camera(self):
        if CV2_MODULE is None:
            messagebox.showerror("Dependency missing", "OpenCV (cv2) is not installed")
            return
        if YOLO is None:
            messagebox.showerror("Dependency missing", "ultralytics YOLO is not installed")
            return

        if not self.capture_running.is_set():
            # Initialize model lazily
            try:
                if self.model is None:
                    self.model = YOLO(MODEL_PATH)
                    # Populate class combobox if model exposes names
                    names = getattr(self.model, "names", None)
                    if names:
                        values = ["All"] + [names[i] for i in range(len(names))]
                        self.class_combo.config(values=values)
                # Open camera
                if self.camera is None:
                    self.camera = CV2_MODULE.VideoCapture(0)
                    if not self.camera.isOpened():
                        messagebox.showerror("Camera error", "Could not open camera")
                        self.camera = None
                        return

                self.capture_running.set()
                self.start_btn.config(state="disabled")
                self.stop_btn.config(state="normal")
                self.record_btn.config(state="normal")
                self.snapshot_btn.config(state="normal")

                self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
                self.capture_thread.start()
            except Exception as exc:
                messagebox.showerror("Error", f"Failed to start camera/model: {exc}")

    def stop_camera(self):
        self.capture_running.clear()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.record_btn.config(state="disabled")
        self.snapshot_btn.config(state="disabled")
        if self.camera is not None:
            try:
                self.camera.release()
            except Exception:
                pass
            self.camera = None
        if self.video_writer is not None:
            try:
                self.video_writer.release()
            except Exception:
                pass
            self.video_writer = None
            self.recording = False
            self.record_btn.config(text="Start Recording")

    def toggle_recording(self):
        if not self.recording:
            # Start
            if self.camera is None:
                messagebox.showwarning("Not running", "Start the camera before recording")
                return
            width = int(self.camera.get(CV2_MODULE.CAP_PROP_FRAME_WIDTH))
            height = int(self.camera.get(CV2_MODULE.CAP_PROP_FRAME_HEIGHT))
            if width == 0 or height == 0:
                messagebox.showerror("Camera error", "Invalid frame size from camera")
                return
            fourcc = CV2_MODULE.VideoWriter_fourcc(*"MJPG")
            self.video_writer = CV2_MODULE.VideoWriter(OUT_FILE, fourcc, 20.0, (width, height))
            if not self.video_writer.isOpened():
                messagebox.showerror("Recording error", "Could not open video writer")
                self.video_writer = None
                return
            self.recording = True
            self.record_btn.config(text="Stop Recording")
        else:
            # Stop
            self.recording = False
            if self.video_writer is not None:
                try:
                    self.video_writer.release()
                except Exception:
                    pass
                self.video_writer = None
            self.record_btn.config(text="Start Recording")

    def snapshot(self):
        # Save latest frame from queue if available
        try:
            frame = None
            while not self.frame_queue.empty():
                frame = self.frame_queue.get_nowait()
            if frame is None:
                messagebox.showwarning("No frame", "No frame available to snapshot")
                return
            filename = datetime.now().strftime("snapshot_%Y%m%d_%H%M%S.jpg")
            CV2_MODULE.imwrite(filename, frame)
            messagebox.showinfo("Snapshot", f"Saved {filename}")
        except Exception as exc:
            messagebox.showerror("Snapshot error", str(exc))

    def analyze_photo(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not path:
            return
        if CV2_MODULE is None or YOLO is None:
            messagebox.showerror("Dependency missing", "cv2 and ultralytics are required for photo analysis")
            return
        try:
            img = CV2_MODULE.imread(path)
            results = self.model(img)
            annotated = results[0].plot()
            # store detections
            for box in results[0].boxes:
                cls = int(box.cls)
                name = self.model.names[cls]
                conf = float(box.conf)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._record_detection(timestamp, name, conf)
            # show annotated in a simple window
            tempfile = "analysis_result.jpg"
            CV2_MODULE.imwrite(tempfile, annotated)
            os.startfile(tempfile) if os.name == "nt" else os.system(f"xdg-open {tempfile} &")
        except Exception as exc:
            messagebox.showerror("Analysis error", str(exc))

    def export_csv(self):
        if not self.detections:
            messagebox.showinfo("No data", "No detections to export")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        keys = ["time", "object", "confidence"]
        try:
            with open(path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for d in self.detections:
                    writer.writerow({"time": d["time"], "object": d["object"], "confidence": d["confidence"]})
            messagebox.showinfo("Exported", f"Exported {len(self.detections)} rows to {path}")
        except Exception as exc:
            messagebox.showerror("Export error", str(exc))

    def _capture_loop(self):
        # Continuous capture and detection loop
        while self.capture_running.is_set():
            start = time.time()
            ret, frame = self.camera.read()
            if not ret:
                time.sleep(0.1)
                continue

            # Run detection
            try:
                results = self.model(frame)
            except Exception:
                results = None

            annotated = frame
            if results is not None:
                try:
                    annotated = results[0].plot()
                    for box in results[0].boxes:
                        cls = int(box.cls)
                        name = self.model.names[cls]
                        conf = float(box.conf)
                        # Filter by class if set
                        if self.class_filters and name not in self.class_filters:
                            continue
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self._record_detection(timestamp, name, conf)
                except Exception:
                    pass

            # Enqueue frame for UI
            try:
                if not self.frame_queue.full():
                    self.frame_queue.put_nowait(annotated)
            except queue.Full:
                pass

            # Write to file if recording
            if self.recording and self.video_writer is not None:
                try:
                    self.video_writer.write(annotated)
                except Exception:
                    pass

            # Update FPS
            now = time.time()
            if self.last_frame_time is None:
                delta = 0.0
            else:
                delta = now - self.last_frame_time
            self.last_frame_time = now
            self.fps = 1.0 / delta if delta > 0 else 0.0

            # Throttle loop a bit to avoid 100% CPU
            elapsed = time.time() - start
            if elapsed < 0.01:
                time.sleep(0.01)

    def _record_detection(self, timestamp, name, conf):
        d = {"time": timestamp, "object": name, "confidence": round(conf, 3)}
        self.detections.append(d)
        # Keep recent 100
        if len(self.detections) > 1000:
            self.detections = self.detections[-1000:]

    def _schedule_ui_update(self):
        # Called via Tk 'after' to update UI from main thread
        try:
            frame = None
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
            if frame is not None and PIL_Image is not None and ImageTk is not None:
                # Convert BGR (OpenCV) to RGB and to PIL image
                try:
                    rgb = CV2_MODULE.cvtColor(frame, CV2_MODULE.COLOR_BGR2RGB)
                    img = PIL_Image.fromarray(rgb)
                    img = img.resize((800, 450))
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.video_panel.imgtk = imgtk
                    self.video_panel.config(image=imgtk)
                except Exception:
                    pass

            # Update KPIs
            self.kpi_detections.config(text=f"Detections: {len(self.detections)}")
            self.kpi_fps.config(text=f"FPS: {int(self.fps)}")

            # Update table with last 10 detections
            for i in self.tree.get_children():
                self.tree.delete(i)
            for d in self.detections[-10:][::-1]:
                self.tree.insert("", "end", values=(d["time"], d["object"], d["confidence"]))

            # Update graph
            if self.canvas is not None:
                # simple count over time: x = indices, y = cumulative counts per second
                ts = [d["time"][11:19] for d in self.detections[-60:]]  # HH:MM:SS
                counts = list(range(len(ts)))
                try:
                    self.ax.clear()
                    self.ax.plot(counts, marker="o")
                    self.ax.set_title("Detections (recent)")
                    self.canvas.draw()
                except Exception:
                    pass

        except Exception:
            pass
        finally:
            self.root.after(200, self._schedule_ui_update)

    def _on_exit(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.capture_running.clear()
            # wait briefly for thread to stop
            time.sleep(0.2)
            try:
                if self.camera is not None:
                    self.camera.release()
            except Exception:
                pass
            self.root.destroy()


def run_gui():
    if TKINTER_MODULE is None:
        raise RuntimeError("tkinter is not available in this environment")
    root = TKINTER_MODULE.Tk()
    app = VisionEdgeApp(root)
    root.protocol("WM_DELETE_WINDOW", app._on_exit)
    root.mainloop()


if __name__ == "__main__":
    try:
        run_gui()
    except (ImportError, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}")
