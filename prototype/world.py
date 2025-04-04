import pyglet
import utils
from main import *

class World:
    def __init__(self,parent:Main):
        self.parent = parent
        
        self.camera = Camera(self)
        self.environment = Environment(self,"misc/blueprint-background_HD.png")
        self.debug_object = WorldObject(self, "misc/default_texture.png")
        self.debug_object.world_coords = (350,150)
        parent.rendering_engine.add_to_layer(1,self.environment)
        parent.rendering_engine.add_to_layer(1,self.debug_object)


    def update_sprite_positions(self,object):
        object.sprite.x, object.sprite.y = object.calculate_relative_position()


class WorldObject:
    def __init__(self, parent:World, texture:str):
        self.parent = parent
        self.sprite = utils.Utils.sprite_load(texture)
        self.world_coords = (0,0)
        self.sprite.batch = parent.parent.rendering_engine.batch

    def calculate_relative_position(self):
        relative_x = self.world_coords[0] - self.parent.camera.pos[0] + self.parent.parent.rendering_engine.window_center[0]
        relative_y = self.world_coords[1] - self.parent.camera.pos[1] + self.parent.parent.rendering_engine.window_center[1]

        return (relative_x,relative_y)


class Player(WorldObject):
    def __init__(self,texture:str):
        super().__init__(texture)


class Environment(WorldObject):
    def __init__(self, parent, texture:str):
        super().__init__(parent, texture)
        pass

class Camera:
    def __init__(self, parent):
        self.pos = (100,0)

    def set_pos(self,coords:tuple):
        self.pos = coords

