from copy import deepcopy
from fiducial_vision import Vision
from boundary_detection import *
from transforms import *
from agent import ego_agent
from obstacle import obstacle
import time


if __name__ == "__main__":
    cv = Vision()
    frames = cv.capture_continuous()
    env = Enviorment()
    env.set_agent(ego_agent)
    while True:
        results = next(frames)
        if not results: 
            continue
        for result in results:
            uid = result.tag_id
            print("Found fiducial " + str(uid))
            rotation = result.pose_R
            translation = result.pose_t
            
            found_uid = env.find_obstacle_by_uid(uid)
            if found_uid == -1:
                new_obstacle = deepcopy(obstacle)
                new_obstacle = transform_shape(new_obstacle, rotation, translation)
                new_obstacle.set_uid(found_uid)
                env.add_obstacle(new_obstacle)
            else:
                new_obstacle = deepcopy(obstacle)
                new_obstacle = transform_shape(new_obstacle, rotation, translation)
                env.update_obstacle(new_obstacle)
        env.update_viz()
        env.show_viz()
        time.sleep(100)
        # env.create_boundaries()
        # env.clear_boundaries()


