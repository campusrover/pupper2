def interpolate_line(a, b, n):
    slope = (b.y - a.y)/(b.x - a.x)
    angle = math.atan2(slope)
    dist = ((b.y - a.y) ** 2 + (b.x - a.x) ** 2) ** 0.5
    step = dist / n
    points = []
    for i in range(0, n):
        p = Point(a.x + math.cos(angle) * step * i, a.y + math.sin(angle) * step * i)
        points.append(p)
    return points

def interpolate_shape(shape, n):
    all_points = []
    for i in range(1, len(shape.points)):
        p1 = shape.points[i - 1]
        p2 = shape.points[i]
        section_points = interpolate_line(p1, p2, n)
        for point in section_points:
            all_points.append(point)
    shape.points = all_points