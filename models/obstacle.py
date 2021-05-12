import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.boundary_detection import *
from src.geometry import *
import yaml

params = yaml.load(open('params.yaml'), Loader=yaml.FullLoader)

obstacle = Shape()


dim_x = params['model_settings']['obstacle_dim_x']
dim_y = params['model_settings']['obstacle_dim_y']

obstacle_points = [Point(-dim_x/2, dim_y/2), Point(dim_x/2, dim_y/2), Point(dim_x/2, -dim_y/2), Point(-dim_x/2, -dim_y/2)]

obstacle.set_center(Point(0, 0))
obstacle.set_points(obstacle_points)
obstacle = interpolate_shape(obstacle, params['model_settings']['model_interpolation'])