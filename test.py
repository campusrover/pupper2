from boundary_detection import *
from transforms import *
from geometry import *
from agent import ego_agent
from obstacle import obstacle
from viz import Vizualizer
import copy
import math
import time

viz = Vizualizer()

ego_agent.points = rotate_points(ego_agent.points, ego_agent.center, math.pi/4)
viz.set_ego(ego_agent)
viz.set_obs([obstacle])
viz.show()
time.sleep(100)