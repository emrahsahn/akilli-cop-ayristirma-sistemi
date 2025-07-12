import cv2
from ultralytics import YOLO
"""
class YOLOv8Detector:
    def __init__(self):
        self.model_path = None
        self.model = None

    def set_model_path(self, model_path):
        self.model_path = model_path

    def load_model(self):
        if self.model_path:
            self.model = YOLO(self.model_path)

    def predict_and_show(self, source=0, confidence=0.6):
        if self.model:
            results = self.model.predict(source=source, show=True, conf=confidence)
            return results
        else:
            print("Model yüklenmedi. Lütfen önce modeli yükleyin.")


# sınıfın çalıştırılması
if __name__ == "__main__":
    detector = YOLOv8Detector()
    detector.set_model_path("C:\\Users\\sahin\\Downloads\\train5\\train6\\weights\\best.pt")
    detector.load_model()
    detector.predict_and_show(source=0, confidence=0.6)
"""


import cv2
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
import threading
import queue


class YOLOv11ObjectDetection:
    def __init__(self, model_path, source, canvas, frame_queue):
        self.model = YOLO(model_path)
        self.source = source
        self.canvas = canvas
        self.frame_queue = frame_queue
        self.detection_running = False

    def detect_objects(self):
        cap = cv2.VideoCapture(self.source)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not cap.isOpened():
            print("Error: Unable to open video source.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video stream or cannot read frame.")
                break

            if self.detection_running:
                results = self.model.predict(frame, conf=0.65)
                annotated_frame = results[0].plot()
                image = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
            else:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            image = image.resize((self.canvas.winfo_width(), self.canvas.winfo_height()), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=image)
            self.frame_queue.put(imgtk)

        cap.release()

    def start_detection(self):
        self.detection_running = True

    def stop_detection(self):
        self.detection_running = False


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Akıllı Çöp Ayıştırma")
        # self.root.iconbitmap("C:\\Users\\sahin\\Downloads\\favicon_icon.jpg")

        window_width = 1280
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
        self.root.config(bg="#121212")

        self.canvas = tk.Canvas(self.root, bg="#1e1e1e")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.root, bg="#121212")
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        self.open_camera_button = self.create_button(self.button_frame, "Open Camera", self.open_camera, "#28a745",
                                                     "#218838")
        self.start_detection_button = self.create_button(self.button_frame, "Start Detection", self.start_detection,
                                                         "#007bff", "#0056b3")
        self.stop_detection_button = self.create_button(self.button_frame, "Stop Detection", self.stop_detection,
                                                        "#dc3545", "#c82333")
        self.close_button = self.create_button(self.button_frame, "Close", self.close_application, "#6c757d", "#5a6268")

        self.model_path = "C:\\Users\\sahin\\Downloads\\train5\\train6\\weights\\best.pt"
        self.source = 0
        self.frame_queue = queue.Queue()
        self.detector = None

        self.update_canvas()

    def create_button(self, parent, text, command, bg_color, active_bg):
        """Helper function to create styled buttons with hover and click effects."""
        button = tk.Button(parent, text=text, command=command,
                           bg=bg_color, fg="white", font=("Helvetica", 12, "bold"),
                           relief="flat", width=18, height=2, bd=0,
                           activebackground=active_bg, activeforeground="white")

        # Hover effect: Change background color when mouse enters
        button.bind("<Enter>", lambda e: button.config(bg=active_bg))
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))

        button.pack(side=tk.LEFT, padx=10)
        return button

    def open_camera(self):
        self.detector = YOLOv11ObjectDetection(self.model_path, self.source, self.canvas, self.frame_queue)
        detection_thread = threading.Thread(target=self.detector.detect_objects, daemon=True)
        detection_thread.start()

    def start_detection(self):
        if self.detector:
            self.detector.start_detection()

    def stop_detection(self):
        if self.detector:
            self.detector.stop_detection()

    def close_application(self):
        if self.detector:
            self.detector.stop_detection()
        self.root.quit()

    def update_canvas(self):
        try:
            if not self.frame_queue.empty():
                imgtk = self.frame_queue.get()
                self.canvas.create_image(0, 0, image=imgtk, anchor=tk.NW)
                self.canvas.imgtk = imgtk
        except Exception as e:
            print(f"Error displaying frame: {e}")

        self.root.after(20, self.update_canvas)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
