from boundary_detection import *
from transforms import *
from geometry import *
from agent import ego_agent
from obstacle import obstacle
from viz import Vizualizer
import copy
import math

viz = Vizualizer()

obstacle = transform_shape(obstacle, [0, 0, 0], [1, 0, 2])
for p in ego_agent.points:
    print(p)
ego_agent.points = rotate_points(ego_agent.points, ego_agent.center, math.pi/2)
for p in ego_agent.points:
    print(p)
viz.set_ego(ego_agent)
viz.set_obs([obstacle])
viz.show()