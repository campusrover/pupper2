from fiducial_vision import Vision
from boundary_detection import *
from agent import ego_agent
from obstacle import obstacle
from copy import deepcopy

if __name__ == "__main__":
    cv = Vision()
    frames = cv.capture_continuous()
    env = Enviorment()
    env.set_agent = ego_agent
    while True:
        results = next(frames)
        if not results: 
            #print("No fiducials found")
            continue
        for result in results:
            uid = result.tag_id
            #print("Found fiducial " + str(uid))
            found_uid = env.find_obstacle_by_uid(uid)
            if found_uid == -1:
                new_obstacle = deepcopy(obstacle)
                new_obstacle.set_uid = found_uid
                env.add_obstacle(new_obstacle)
        env.create_boundaries()
        env.list_boundaries()
        env.clear_boundaries()


