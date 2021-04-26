from boundary_detection import *

obstacle = Shape()


# length = 0.4m, width = 0.1m
obstacle_points = [Point(-0.2, 0.05), Point(0.2, 0.05), Point(0.2, -0.05), Point(-0.2, -0.05)]

obstacle.set_center(Point(0, 0))
obstacle.set_points(obstacle_points)