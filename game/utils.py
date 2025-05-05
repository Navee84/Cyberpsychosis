import pyglet
import pyglet.window.mouse
from math import cos, sin, atan, degrees, radians
import os

class Utils:
    def console_prefix(state):
        console_prefix_error = "[ERROR]"
        console_prefix_info = "[INFO]"
        console_prefix_warning = "[WARNING]"
        
        match state:
            case "error":
                return console_prefix_error
            case "info":
                return console_prefix_info
            case "warning":
                return console_prefix_warning

    def sprite_load(path:str) -> pyglet.sprite.Sprite:
        image = pyglet.image.load(path)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        return pyglet.sprite.Sprite(image)

    def animated_sprite_load(images:dict) -> pyglet.sprite.Sprite:
        '''
        images must be the following format : dict = {frame1_path: duration, frame2_path: duration}
        where framex_path is a str and duration can be None or a float
        '''
        frame_list = []

        for frame in images.keys():
            image = pyglet.image.load(frame)
            image.anchor_x = image.width // 2
            image.anchor_y = image.height // 2

            formated_frame = pyglet.image.animation.AnimationFrame(image, images[frame])
            frame_list.append(formated_frame)

        animation = pyglet.image.animation.Animation(frame_list)

        return pyglet.sprite.Sprite(animation)

    
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
        angle = atan((point_b[1]-point_a[1])/(point_b[0]-point_a[0]+0.01)) # +0.01 is here to prevent divisons by 0
        return angle
    
    def get_vector(point_a:tuple, point_b:tuple) -> tuple:
        # return the vector from point a to point b
        x = point_b[0] - point_a[0]
        y = point_b[1] - point_a [1]

        return (x,y)

    def translate(point: tuple | list, vector:tuple) -> tuple | list:
        # return the modified point values
        transtated_x = point[0] + vector[0]
        transtated_y = point[1] + vector[1]

        if type(point) == tuple:
            return (transtated_x, transtated_y)
        return [transtated_x, transtated_y]



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
        
class MusicManager(pyglet.media.Player):
    def __init__(self):
        super().__init__()
    
        self.music_dict = {}

        for music in os.listdir("prototype/assets/musics"):
            source = pyglet.media.load("prototype/assets/musics/"+music)
            name = music.lower()
            name = name.replace(" ","_")
            name = name[:len(music)-4]

            self.music_dict[name] = source

        print(self.music_dict)
        