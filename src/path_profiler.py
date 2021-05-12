import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geometry import *
from boundary_detection import *
#from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
import time
import yaml

params = yaml.load(open('params.yaml'), Loader=yaml.FullLoader)

class Profiler: 
    def __init__(self):
        self.path = None

    def add_path(self, path):
        self.path = path

    def smooth_path(self):
        return
        #path_x = list(map(lambda p: p.x, self.path))
        #path_y = list(map(lambda p: p.y, self.path))
        #weights = [1 for w in range(1, len(path_x) + 1)]
        #print(weights)
        #weights[0] = 100
        #spline = interpolate.UnivariateSpline(path_x, path_y, w=weights)
        #xs = np.linspace(0, 3, 1000)
        #plt.plot(xs, spline(xs), 'y', lw=2)
        #plt.show()

    def get_profile(self):
        profiled_path = []
        for i in range(0, len(self.path) - 1):
            current_point = self.path[i]
            next_point = self.path[i + 1]
            angle = get_angle(current_point, next_point)
            dist = current_point.dist(next_point)
            profiled_path.append((dist, angle))
        return profiled_path
