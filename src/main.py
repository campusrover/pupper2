import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from copy import deepcopy
from fiducial_vision import Vision
from boundary_detection import *
from transforms import *
from models.goal import goal
from models.agent import ego_agent
from models.obstacle import obstacle
from path_finder import PathFinder
import time
import _pickle as pickle


if __name__ == "__main__":
    cv = Vision()
    frames = cv.capture_continuous()
    env = Enviorment()
    env.set_agent(ego_agent)
    goal_ = None
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
            if uid == 0:
                goal_ = goal
                goal_ = transform_shape(goal_, rotation, translation)
            elif found_uid == -1:
                new_obstacle = deepcopy(obstacle)
                new_obstacle = transform_shape(new_obstacle, rotation, translation)
                new_obstacle.set_uid(uid)
                env.add_obstacle(new_obstacle)
            else:
                new_obstacle = deepcopy(obstacle)
                new_obstacle = transform_shape(new_obstacle, rotation, translation)
                env.update_obstacle(new_obstacle)
        env.create_boundaries()
        pickle.dump(env, open('sample_env.pkl', 'wb'))
        print("PICKLE DUMPED")
        time.sleep(100)
        # p = PathFinder(env, env.agent, goal_)
        # r = p.solve()
        # env.add_path(r)
        # env.update_viz()
        # env.show_viz()
        # time.sleep(100)
        env.clear_boundaries()