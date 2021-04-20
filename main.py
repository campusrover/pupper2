from fiducial_vision import Vision
from boundary_detection import *
from agent import ego_agent
from obstacle import obstacle

if __name__ == "__main__":
    cv = Vision()
    frames = cv.capture_continuous()
    env = Enviorment()
    ego = ego_agent
    while True:
        results = next(frames)
        if results:
            print("Got results")

