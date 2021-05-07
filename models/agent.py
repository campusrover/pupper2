import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.boundary_detection import *
from src.geometry import * 
import yaml

params = yaml.load(open('params.yaml'), Loader=yaml.FullLoader)

ego_agent = Shape()


x_dim = params['model_settings']['ego_agent_dim_x']
y_dim = params['model_settings']['ego_agent_dim_y']

ego_agent_points = [Point(-x_dim/2, y_dim/2), Point(x_dim/2, y_dim/2), Point(x_dim/2, -y_dim/2), Point(-x_dim/2, -y_dim/2)]

ego_agent.set_center(Point(0, 0))
ego_agent.set_points(ego_agent_points)
ego_agent = interpolate_shape(ego_agent, params['model_settings']['model_interpolation'])