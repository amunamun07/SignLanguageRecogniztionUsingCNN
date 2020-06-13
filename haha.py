import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import cv2
import numpy as np


class ColorDetector(QDialog):

    def __init__(self):
        super(ColorDetector, self).__init__()
        loadUi('cv.ui', self)
        self.image = None
        self.start_button.clicked.connect(self.start_webcam)
        self.stop_button.clicked.connect(self.stop_webcam)



    def start_webcam(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.image = cv2.flip(self.image, 1)
        self.displayImage(self.image)


    def stop_webcam(self):
        self.capture.release()
        self.timer.stop()

    def displayImage(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:  # [0]=rows, [1]=cols, [2]=channels
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        # BGR to RGB
        outImage = outImage.rgbSwapped()

        self.image_label1.setPixmap(QPixmap.fromImage(outImage))
        self.image_label1.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ColorDetector()
    window.setWindowTitle('OpenCV Color Detector')
    window.show()
    sys.exit(app.exec_())
