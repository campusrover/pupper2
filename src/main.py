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

from controller import Controller


if __name__ == "__main__":

    # import object to stream camera frames
    cv = Vision()
    frames = cv.capture_continuous()
    env = Environment()

    # set ego agent as env agent
    env.set_agent(ego_agent)

    # goal object
    goal_ = None

    c = Controller()

    # Controller needs to be set up manually before continuing
    # Activate robot and then set it to throt mode.
    while not c.ready:
        time.sleep(20/1000)

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
        print("Done creating boundaries")
        
        # create a planner with current env, agent, and goal location and solve for a path
        planner = PathFinder(env, env.agent, goal_.points[0])
        planner.solve()
        print("Done solving")

        profiler = Profiler()
        profiler.add_path(planner.export_path())
        smooth_path = profiler.get_profile()
        
        i = 0

        # The following parameters may need to be tuned
        step_size = 0.01
        step_size_rot = 0.005
        threshold = 0.05
        rot_threshold = 0.01

        pose = (0, 0)
        next_point = smooth_path[i]
        
        while i < len(smooth_path):
            # Rotation right
            if pose[1] - next_point[1] < -rot_threshold:

                # send right rotation command 
                c.rotate_right()
                pose[1] += step_size_rot
            # Rotation left
            elif pose[1] - next_point[1] > rot_threshold:

                # send left rotation command 
                c.rotate_left()
                pose[1] -= step_size_rot
            #Move forward
            elif pose[0] - next_point[0] > threshold:

                # send move forward command 
                c.move_forward()
                pose[0] += step_size
            else:
                i += 1
                next_point = smooth_path[i]
            
            time.sleep(20/1000)

        # update and display/save plots
        # env.add_path(planner.export_path())
        # env.add_nodes(planner.export_nodes())
        # env.update_viz()
        # env.show_viz()
        # print("Plot saved")
        # time.sleep(100)

        # reset obstacle boundaries for next iteration
        env.clear_boundaries()