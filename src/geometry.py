import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from src.boundary_detection import * 

def get_angle(a, b):
    slope_num = (b.y - a.y)
    slope_denom = (b.x - a.x)
    return math.atan2(slope_num, slope_denom)

def interpolate_line(a, b, n):
    angle = get_angle(a, b)
    dist = ((b.y - a.y) ** 2 + (b.x - a.x) ** 2) ** 0.5
    step = dist / n
    points = []
    for i in range(0, n):
        p = Point(a.x + math.cos(angle) * step * i, a.y + math.sin(angle) * step * i)
        points.append(p)
    return points

def interpolate_shape(shape, n):
    all_points = []
    for i in range(0, len(shape.points)):
        p1 = shape.points[i]
        p2 = shape.points[(i + 1) % len(shape.points)]
        section_points = interpolate_line(p1, p2, n)
        for point in section_points:
            all_points.append(point)
    shape.points = all_points
    return shape