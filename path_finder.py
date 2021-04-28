from geometry import *
from boundary_detection import *

class PathFinder:
    def __init__(self, env, start, goal):
        self.env = env
        self.start = start
        self.goal = goal
        self.path = None

    def setup(self):
        pass

    def solve(self):
        return self.path