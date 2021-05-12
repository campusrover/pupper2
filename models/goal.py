import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.boundary_detection import *
from src.geometry import * 

goal = Shape()


# length = 0m, width = 0m
goal_point = [Point(0,0)]

goal.set_center(Point(0, 0))
goal.set_points(goal_point)