from boundary_detection import *
from geometry import * 
ego_agent = Shape()


# length = 0.5m, width = 0.4m
ego_agent_points = [Point(-0.25, 0.2), Point(0.25, 0.2), Point(0.25, -0.2), Point(-0.25, -0.2)]

ego_agent.set_center(Point(0, 0))
ego_agent.set_points(ego_agent_points)
ego_agent = interpolate_shape(ego_agent, 16)