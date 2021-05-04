from geometry import *
from boundary_detection import *
from node import Node
from tqdm import tqdm
import time

class PathFinder:
    def __init__(self, env, start, goal):
        self.env = env
        self.boundaries = self.env.boundaries
        self.smart_boundaries = self.get_smart_boundaries()
        #print(self.smart_boundaries)
        self.start = start.center
        self.goal = goal
        self.path = []

        self.inflation = 0.05
        self.step = 0.5
        self.dim_x = 2
        self.dim_y = 2
        self.max_dist = float('inf')
        self.range_x = int(self.dim_x // self.step)
        self.range_y = int(self.dim_y // self.step)
        self.scale = 1 / self.step
        self.map = self.explore()
        self.map_height = len(self.map)
        self.map_width = len(self.map[0])
        self.map_center_x = self.map_width // 2
        self.map_center_y = self.map_height // 2

        a = self.get_node_quick(2, 2)
        print(a.point.x, a.point.y)
        print("DID TEST")
        input()

        

    def get_smart_boundaries(self):
        smart_boundaries = []
        #print(len(self.boundaries))
        for boundary in self.boundaries:
            max_x = -float('inf')
            min_x = float('inf')
            max_y = -float('inf')
            min_y = float('inf')
            for p in boundary:
                if p.x > max_x: max_x = p.x
                if p.x < min_x: min_x = p.x
                if p.y > max_y: max_y = p.y
                if p.y < min_y: min_y = p.y
            smart_boundaries.append((max_x, min_x, max_y, min_y))
        return smart_boundaries

    def in_range_of_boundary(self, point):
        for boundary in self.boundaries:
            for boundary_point in boundary:
                if point.dist(boundary_point) < self.inflation:
                    return True
        return False

    def in_range_of_boundary_quick(self, point):
        for boundary in self.smart_boundaries:
            if point.x < boundary[0] and point.x > boundary[1] and point.y < boundary[2] and point.y > boundary[3]:
                #print("GOTTEM!!!")
                return True
        return False


    def get_point_or_boundary(self, col, row):
        p = Point(col, row)
        if not self.in_range_of_boundary(p): return p
        return None

    def explore(self):
        all_points = [[Point(col, row) for col in range(-self.range_x, self.range_x)] for row in range(-self.range_y, self.range_y)]
        return [[Node(point, False, self.max_dist, None)  for point in row] for row in tqdm(all_points)]

    def get_node(self, x, y):
        for row in self.map:
            for node in row:
                if node.point.x == x and node.point.y == y: return node
        return None

    def get_node_quick(self, x, y):
        node_x = self.map_center_x + x
        node_y = self.map_center_y + y
        print(node_x, node_y)
        if node_x > self.range_x or node_x < -self.range_x or node_y > self.range_y or node_y < -self.range_y:
            return None
        return self.map[int(node_y)][int(node_x)]
       

    def get_next_node(self):
        next_node = None
        for row in self.map:
            for node in row:
                if not next_node or (not node.explored and node.distance < next_node.distance):
                    next_node = node
        return next_node

    def get_edge_weight(self, node1, node2):
        if self.in_range_of_boundary(node2.point) or self.in_range_of_boundary(node1.point): return self.max_dist
        return node1.point.dist(node2.point)

    def update_node_neighbor_dist(self, current_node):
        node_left = self.get_node_quick(current_node.point.x - 1, current_node.point.y)
        node_right = self.get_node_quick(current_node.point.x + 1, current_node.point.y)
        node_up = self.get_node_quick(current_node.point.x, current_node.point.y + 1)
        node_down = self.get_node_quick(current_node.point.x, current_node.point.y - 1)
        node_up_left = self.get_node_quick(current_node.point.x - 1, current_node.point.y + 1)
        node_up_right = self.get_node_quick(current_node.point.x + 1, current_node.point.y + 1)
        node_down_left = self.get_node_quick(current_node.point.x - 1, current_node.point.y - 1)
        node_down_right = self.get_node_quick(current_node.point.x + 1, current_node.point.y - 1)

        if node_left:
            new_distance = current_node.distance + self.get_edge_weight(current_node, node_left)
            if new_distance < node_left.distance: 
                node_left.distance = new_distance
                node_left.previous = current_node
        
        if node_right: 
            new_distance = current_node.distance + self.get_edge_weight(current_node, node_right)
            if new_distance < node_right.distance: 
                node_right.distance = new_distance
                node_right.previous = current_node

        if node_up: 
            new_distance = current_node.distance + self.get_edge_weight(current_node, node_up)
            if new_distance < node_up.distance: 
                node_up.distance = new_distance
                node_up.previous = current_node

        if node_down: 
            new_distance = current_node.distance + self.get_edge_weight(current_node, node_down)
            if new_distance < node_down.distance: 
                node_down.distance = new_distance
                node_down.previous = current_node
        
        if node_up_left:
            new_distance = current_node.distance + self.get_edge_weight(current_node, node_up_left)
            if new_distance < node_up_left.distance: 
                node_up_left.distance = new_distance
                node_up_left.previous = current_node
        
        if node_up_right: 
            new_distance = current_node.distance + self.get_edge_weight(current_node, node_up_right)
            if new_distance < node_up_right.distance: 
                node_up_right.distance = new_distance
                node_up_right.previous = current_node

        if node_down_left: 
            new_distance = current_node.distance + self.get_edge_weight(current_node, node_down_left)
            if new_distance < node_down_left.distance: 
                node_down_left.distance = new_distance
                node_down_left.previous = current_node

        if node_down_right: 
            new_distance = current_node.distance + self.get_edge_weight(current_node, node_down_right)
            if new_distance < node_down_right.distance: 
                node_down_right.distance = new_distance
                node_down_right.previous = current_node


    def solve(self):
        start = time.time()
        self.get_node_quick(self.start.x * self.scale, self.start.y * self.scale).distance = 0.0
        while True: 
            current_node = self.get_next_node()
            if current_node.point.x == self.goal.x * self.scale and current_node.point.y == self.goal.y * self.scale:
                break
            current_node.explored = True
            self.update_node_neighbor_dist(current_node)
        end = time.time()
        print("SECONDS: ", end - start)
        self.resolve_path()

    def resolve_path(self):
        self.recurse_path(self.get_node_quick(self.goal.x * self.scale, self.goal.y * self.scale))

    def recurse_path(self, node):
        if node.previous:
            self.recurse_path(node.previous) 
        self.path.append(node)

    def export_path(self):
        [node.point.scale(self.step) for node in self.path]
        return [node.point for node in self.path]