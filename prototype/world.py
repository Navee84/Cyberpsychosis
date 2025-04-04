import utils
from main import *

class World:
    def __init__(self,parent:Main):
        self.parent = parent
        self.objects_list = []
        
        self.camera = Camera(self)
        self.environment = Environment(self,"misc/blueprint-background_HD.png")
        self.debug_object = DebugObject(self, "misc/default_texture.png")
        self.debug_object.world_coords = [350,150]


    def update_sprites_positions(self): # object must be WorldObject type
        for object in self.objects_list:
            object.update_sprite_position()
    
    def add_to_batch(self,object): # object must be WorldObject type
        object.sprite.batch = self.parent.rendering_engine.batch
    
    def remove_from_batch(self,object): # object must be WorldObject type
        pass
    def add_to_object_list(self,object):
        self.objects_list.append(object)
    
    def update_camera_position(self):
        self.camera.set_pos(self.debug_object.world_coords)


class WorldObject:
    def __init__(self, parent:World, texture:str):
        self.parent = parent
        self.sprite = utils.Utils.sprite_load(texture)
        self.world_coords = [0,0]
        self.sprite.batch = parent.parent.rendering_engine.batch

        self.add_to_world_object_list()

    def update_sprite_position(self):
        self.sprite.x = self.world_coords[0] - self.parent.camera.pos[0] + self.parent.parent.rendering_engine.window_center[0]
        self.sprite.y = self.world_coords[1] - self.parent.camera.pos[1] + self.parent.parent.rendering_engine.window_center[1]
    
    def add_to_world_object_list(self):
        self.parent.add_to_object_list(self)


class Player(WorldObject):
    def __init__(self,texture:str):
        super().__init__(texture)


class Environment(WorldObject):
    def __init__(self, parent, texture:str):
        super().__init__(parent, texture)
        pass

class Camera:
    def __init__(self, parent):
        self.pos = [0,0]

    def set_pos(self,coords:list):
        self.pos = coords

class DebugObject(WorldObject):
    def __init__(self, parent, texture):
        super().__init__(parent,texture)

        self.speed = 4
    
    def go_up(self):
        self.world_coords[1] += self.speed

    def go_down(self):
        self.world_coords[1] -= self.speed

    def go_left(self):
        self.world_coords[0] -= self.speed

    def go_right(self):
        self.world_coords[0] += self.speed
