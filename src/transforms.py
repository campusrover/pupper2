import math
import numpy as np
from boundary_detection import Point
import yaml

params = yaml.load(open('params.yaml'), Loader=yaml.FullLoader)

def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

def rotationMatrixToEulerAngles(R):

    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return [x, y, z]

def hypot(tf):
    return (tf[0] ** 2 + tf[1] ** 2 + tf[2] ** 2) ** 0.5

def rotate_points(points, origin, angle):
    for point in points:
        rotate_point(point, origin, angle)
    return points

def rotate_point(point, origin, angle):
    s = math.sin(angle)
    c = math.cos(angle)

    p_x = point.x - origin.x
    p_y = point.y - origin.y
    t_x = p_x * c - p_y * s
    t_y = p_x * s + p_y * c
    point.x = t_x + origin.x
    point.y = t_y + origin.y
    return point

def transform_shape(shape, rotation, translation):
    rot_euler = rotationMatrixToEulerAngles(rotation)
    yaw = rot_euler[1]
    #print(yaw)
    if abs(yaw) < 0.2: yaw = 0
    translation_x = -1 * translation[0] * params['transform_settings']['x_coefficent']
    translation_z = translation[2] * params['transform_settings']['z_coefficent']
    shape.transform_center(translation_x, translation_z)
    shape.transform_points(translation_x, translation_z)
    shape.points = rotate_points(shape.points, shape.center, yaw)
    return shape