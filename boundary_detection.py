import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "X: " + str(self.x) + ", Y: " + str(self.y)


class Shape:
    def __init__(self):
        self.points = []
        self.center = None
        self.uid = None

    def set_id(self, uid):
        self.uid = uid

    def set_points(self, points):
        self.points = points

    def add_point(self, point):
        self.points.append(point)

    def set_center(self, center):
        self.center = center

    def make_centered(self):
        if not self.is_valid():
            return False
        max_x = -(2**31)
        min_x = (2**31)
        max_y = -(2**31)
        min_y = (2**31)
        for point in self.points:
            if point.x > max_x:
                max_x = point.x
            if point.x < min_x:
                min_x = point.x
            if point.y > max_y:
                max_y = point.y
            if point.y > min_y:
                min_y = point.y
        x_range = max_x - min_x
        y_range = max_y - min_y
        delta_x = -x_range/2
        delta_y = -y_range/2
        self.transform_points(delta_x, delta_y)

    def transform_points(self, delta_x, delta_y):
        for point in self.points:
            point.x += delta_x
            point.y += delta_y

    def is_valid(self):
        return self.center is not None and len(self.points) > 0

    def __add__(self, other):
        result = []
        for self_point in self.points:
            for other_point in other.points:
                result.append(self_point + other_point)
        return result


class Enviorment: 
    def __init__(self):
        self.agent = None
        self.obstacles = []
        self.boundaries = []
    
    def set_agent(self, agent):
        self.agent = agent

    def set_obstacles(self, obs):
        self.obstacles = obs

    def find_obstacle(self, search_ob):
        count = 0
        for ob in self.obstacles:
            if ob.uid == search_ob.uid: return count
            count += 1
        return -1

    def add_obstacle(self, ob):
        if self.find_obstacle == -1:
            self.obstacles.append(ob)

    def remove_obstacle(self, ob):
        ob_index = self.find_obstacle(ob)
        if ob_index > 0:
            self.obstacles.pop(ob_index)

    def is_valid(self):
        return self.agent is not None and len(self.obstacles) > 0

    def create_boundaries(self):
        if not self.is_valid(): return
        for ob in self.obstacles:
            self.obstacles.append(self.agent + ob)