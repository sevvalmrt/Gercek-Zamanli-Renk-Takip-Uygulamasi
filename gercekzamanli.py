import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider

class ColorDetector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Detector")
        self.setGeometry(100, 100, 800, 600)

        # UI Elements
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)

        self.start_button = QPushButton("Start Camera", self)
        self.start_button.clicked.connect(self.start_camera)

        self.stop_button = QPushButton("Stop Camera", self)
        self.stop_button.clicked.connect(self.stop_camera)

        self.hue_slider = QSlider()
        self.hue_slider.setMinimum(0)
        self.hue_slider.setMaximum(179)
        self.hue_slider.setValue(50)
        self.hue_slider.setOrientation(1)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.hue_slider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        if self.capture:
            self.capture.release()

    def update_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hue = self.hue_slider.value()
        lower_bound = np.array([hue - 10, 100, 100])
        upper_bound = np.array([hue + 10, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        self.display_image(result)

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        bytes_per_line = ch * w
        q_img = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorDetector()
    window.show()
    sys.exit(app.exec_())
