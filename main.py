from fiducial_vision import Vision

if __name__ == "__main__":
    cv = Vision()
    frames = cv.capture_continuous()

    while True:
        results = next(frames)
        if results:
            print("Got results")