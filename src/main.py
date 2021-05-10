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
from path_profiler import Profiler
import time
import _pickle as pickle


if __name__ == "__main__":

    # import object to stream camera frames
    cv = Vision()
    frames = cv.capture_continuous()
    env = Enviorment()

    # set ego agent as env agent
    env.set_agent(ego_agent)

    # goal object
    goal_ = None

    # wait until we have a stream of fiducials
    while True:
        results = next(frames)
        if not results: 
            continue
        
        # for each fiducial in the image
        for result in results:

            # get tag id and transform
            uid = result.tag_id
            print("Found fiducial " + str(uid))
            rotation = result.pose_R
            translation = result.pose_t

            # search for the fiducial in existing env
            found_uid = env.find_obstacle_by_uid(uid)

            # transform goal
            if uid == 0:
                goal_ = goal
                goal_ = transform_shape(goal_, rotation, translation)

            # transform and add new tag to env
            elif found_uid == -1:
                new_obstacle = deepcopy(obstacle)
                new_obstacle = transform_shape(new_obstacle, rotation, translation)
                new_obstacle.set_uid(uid)
                env.add_obstacle(new_obstacle)

            # update position of existing tag
            else:
                new_obstacle = deepcopy(obstacle)
                new_obstacle = transform_shape(new_obstacle, rotation, translation)
                env.update_obstacle(new_obstacle)

        # create boundaries for obstacles
        env.create_boundaries()
        
        # create a planner with current env, agent, and goal location and solve for a path
        planner = PathFinder(env, env.agent, goal_)
        planner.solve()

        # profiler = Profiler()
        # profiler.add_path(planner.export_path())
        # smooth_path = profiler.get_profile()

        # update and display/save plots
        env.add_path(p.export_path())
        env.update_viz()
        env.show_viz()
        time.sleep(100)

        # reset obstacle boundaries for next iteration
        env.clear_boundaries()