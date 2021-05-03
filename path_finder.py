from geometry import *
from boundary_detection import *

class PathFinder:
    def __init__(self, env, start, goal):
        self.env = env
        self.boundaries = self.env.boundaries
        self.start = start
        self.goal = goal
        self.path = None

        self.inflation = 0.05
        self.step = 0.1
        self.dim_x = 10
        self.dim_y = 10
        self.max_dist = float('inf')
        self.range_x = int(self.dim_x / self.step)
        self.range_y = int(self.dim_y / self.step)
        self.scale = 1 / self.step
        self.map = self.explore()

    def in_range_of_boundary(self, point):
        for boundary in self.boundaries:
            for boundary_point in boundary:
                if point.dist(boundary_point) < self.inflation:
                    return True
        return False

    def get_point_or_boundary(self, col, row):
        p = Point(col, row)
        if not self.in_range_of_boundary(p): return p
        return None

    def explore(self):
        all_points = [[(Point(col, row), False, self.max_dist, None) for col in range(-self.range_x, self.range_x)] for row in range(-self.range_y, self.range_y)]
        return [[self.get_point_or_boundary(point_d.x, point_d.y) for point_d in row] for row in all_points]

    def get_point(self, x, y):
        for row in self.map:
            for point_d in row:
                if point_d[0].x == x and point_d[0].y == y: return point_d[0]
        return None

    def solve(self):

        return self.path