import pyglet
from math import cos, sin, atan, degrees, radians

class Utils:
    def __init__(self):
        self.console_prefix_error = "[ERROR]"
        self.console_prefix_info = "[INFO]"
        self.console_prefix_warning = "[WARNING]"
    
    def sprite_load(path:str) -> pyglet.sprite.Sprite:
        image = pyglet.image.load(path)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        return pyglet.sprite.Sprite(image)
    
    def create_line(starting_point:tuple, ending_point:tuple, color):
        return pyglet.shapes.Line(starting_point[0], starting_point[1],
                                  ending_point[0], ending_point[1],
                                  thickness= 5, color = color
                                  )
    def get_min(lst):
        min = lst[0]
        for elem in lst:
            if elem < min:
                min = elem
        return min
    
    def get_max(lst):
        max = lst[0]
        for elem in lst:
            if elem > max:
                max = elem
        return max
    
    def distance(point_a:list,point_b:list):
        return ((point_a[0]-point_b[0])**2+(point_a[1]-point_b[1])**2)**(1/2)
    
    def apply_rotation(origin:tuple,point:tuple,theta) -> tuple:
        origin_vector = origin
        normalized_point = (point[0]-origin_vector[0],point[1]-origin_vector[1])

        rotated_point = (normalized_point[0]*cos(theta) - normalized_point[1]*sin(theta), normalized_point[1]*cos(theta) + normalized_point[0]*sin(theta))

        final_point = (rotated_point[0]+origin_vector[0], rotated_point[1]+origin_vector[1])
        return final_point
    
    def get_angle(point_a, point_b):
        angle = atan((point_b[1]-point_a[1])/(point_b[0]-point_a[0]+0.01))
        return angle


class Queue:
    def __init__(self):
        self.queue = []
    
    def is_empty(self):
        return self.queue == []
    
    def enqueue(self,object):
        self.queue.append(object)
    
    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)