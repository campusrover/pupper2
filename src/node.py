class Node: 
    def __init__(self, point, explored, distance, previous):
        self.point = point
        self.explored = explored 
        self.distance = distance
        self.previous = previous
