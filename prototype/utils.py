import pyglet

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