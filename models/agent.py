import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.boundary_detection import *
from src.geometry import * 
import yaml

params = yaml.load(open('params.yaml'), Loader=yaml.FullLoader)

ego_agent = Shape()


# length = 0.6m, width = 0.4m
ego_agent_points = [Point(-0.2, 0.3), Point(0.2, 0.3), Point(0.2, -0.3), Point(-0.2, -0.3)]

ego_agent.set_center(Point(0, 0))
ego_agent.set_points(ego_agent_points)
ego_agent = interpolate_shape(ego_agent, params['model_settings']['model_interpolation'])