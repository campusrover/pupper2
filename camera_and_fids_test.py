from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import cv2
import time

def get_detector():
    options = apriltag.DetectorOptions(families="tag36h11")
    return apriltag.Detector(options)

def detect(detector, img):

    results = detector.detect(gray)
    print("[INFO] {} total AprilTags detected".format(len(results)))
    # loop over the AprilTag detection results
    for r in results:
        # extract the bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        print(r.corners)

def init_camera():

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    return PiRGBArray(camera, size=(640, 480))

rawCapture = init_camera()

detector = get_detector()
 
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    image = cv2.flip(image, 0)

    detect(detector, image)

