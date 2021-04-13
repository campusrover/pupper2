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

class Camera:

    def __init__(self, camera_resolution=(640, 480), camera_framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = camera_resolution
        self.camera.framerate = camera_framerate

        self.capture = PiRGBArray(self.camera, size=camera_resolution)

        self.detector = Detector(families="tag36h11")

    def capture_continuous(self, format="bgr", use_video_port=True):
        for frame in self.camera.capture_continuous(self.capture, format=format, use_video_port=use_video_port):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array
            image = cv2.flip(image, -1)
            # show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            self.capture.truncate(0)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

            self.detect(image)

    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        results = self.detector.detect(gray, estimate_tag_pose=True, camera_params=(3.6, 3.6, 0, 0), tag_size=0.065)
        print("[INFO] {} total AprilTags detected".format(len(results)))
        # loop over the AprilTag detection results
        for r in results:
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = r.corners
            rot_mat = r.pose_R
            euler_angles = self.rotationMatrixToEulerAngles(rot_mat)
            transform = r.pose_t
            #print(euler_angles)
            print(self.hypot(transform))
 
    # Checks if a matrix is a valid rotation matrix.
    def isRotationMatrix(self, R) :
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype = R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6


    # Calculates rotation matrix to euler angles
    # The result is the same as MATLAB except the order
    # of the euler angles ( x and z are swapped ).
    def rotationMatrixToEulerAngles(self, R) :

        assert(self.isRotationMatrix(R))
        
        sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
        
        singular = sy < 1e-6

        if  not singular :
            x = math.atan2(R[2,1] , R[2,2])
            y = math.atan2(-R[2,0], sy)
            z = math.atan2(R[1,0], R[0,0])
        else :
            x = math.atan2(-R[1,2], R[1,1])
            y = math.atan2(-R[2,0], sy)
            z = 0

        return np.array([x, y, z])

    def hypot(self, tf):
        return (tf[0] ** 2 + tf[1] ** 2 + tf[2] ** 2) ** 0.5

if __name__ == "__main__":
    c = Camera()
    c.capture_continuous()