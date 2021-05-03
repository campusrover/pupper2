from picamera import PiCamera
from picamera.array import PiRGBArray
from picamera.array import PiRGBArray
from picamera import PiCamera
from pupil_apriltags import Detector
import argparse
import cv2
import time
import math
import numpy as np


class Vision:

    def __init__(self, camera_resolution=(640, 480), camera_framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = camera_resolution
        self.camera.framerate = camera_framerate

        self.capture = PiRGBArray(self.camera, size=camera_resolution)

        self.detector = Detector(families="tag36h11")

        self.show_image = False

    def capture_continuous(self, format="bgr", use_video_port=True):
        def frame_generator():
            for frame in self.camera.capture_continuous(self.capture, format=format, use_video_port=use_video_port):
                image = frame.array
                image = cv2.flip(image, -1)
                self.capture.truncate(0)
                yield self.detect(image)
        return frame_generator()

    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return self.detector.detect(gray, estimate_tag_pose=True, camera_params=(2571.4, 2571.4, 320, 240), tag_size=0.03)
