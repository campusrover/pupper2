import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geometry import *
from boundary_detection import *
import time
import yaml

params = yaml.load(open('params.yaml'), Loader=yaml.FullLoader)

class Profiler: 
    def __init__(self):
        self.path = None

    def add_path(self, path):
        self.path = path

    def get_profile(self):
        profiled_path = []
        for i in range(0, len(self.path) - 1):
            current_point = self.path[i]
            next_point = self.path[i + 1]
            angle = get_angle(current_point, next_point)
            dist = current_point.dist(next_point)
            profiled_path.append((dist, angle))
        return profiled_path
