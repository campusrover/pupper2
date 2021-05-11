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
import yaml

params = yaml.load(open('params.yaml'), Loader=yaml.FullLoader)

class Vision:

    def __init__(self, camera_resolution=(640, 480), camera_framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = camera_resolution
        self.camera.framerate = camera_framerate

        self.capture = PiRGBArray(self.camera, size=camera_resolution)

        self.detector = Detector(families="tag36h11")

        self.show_image = False
        self.tag_size = params['vision_settings']['tag_size']
        self.lens_size = params['vision_settings']['lens_size']
        self.camera_x_center = params['vision_settings']['camera_x_center']
        self.camera_y_center = params['vision_settings']['camera_y_center']

    def capture_continuous(self, format="bgr", use_video_port=True):
        def frame_generator():
            for frame in self.camera.capture_continuous(self.capture, format=format, use_video_port=use_video_port):
                image = frame.array
                image = cv2.flip(image, -1)
                self.capture.truncate(0)
                result = self.detect(image)
                (ptA, ptB, ptC, ptD) = result.corners
                ptB = (int(ptB[0]), int(ptB[1]))
                ptC = (int(ptC[0]), int(ptC[1]))
                ptD = (int(ptD[0]), int(ptD[1]))
                ptA = (int(ptA[0]), int(ptA[1]))
                # draw the bounding box of the AprilTag detection
                cv2.line(image, ptA, ptB, (0, 255, 0), 2)
                cv2.line(image, ptB, ptC, (0, 255, 0), 2)
                cv2.line(image, ptC, ptD, (0, 255, 0), 2)
                cv2.line(image, ptD, ptA, (0, 255, 0), 2)
                # draw the center (x, y)-coordinates of the AprilTag
                (cX, cY) = (int(result.center[0]), int(result.center[1]))
                cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
                cv2.imshow("Fiducial Detection Image", image)
        return frame_generator()

    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return self.detector.detect(gray, estimate_tag_pose=True, camera_params=(self.lens_size, self.lens_size, self.camera_x_center, self.camera_y_center), tag_size=self.tag_size)
