import utils
from main import *

class World:
    def __init__(self,parent:Main):
        self.parent = parent
        
        self.camera = Camera()
        self.environment = Environment(self,"misc/blueprint-background_HD.png")
        self.debug_object = WorldObject("misc/default_texture.png")
        self.debug_object.world_coords = (350,150)
        parent.rendering_engine.add_to_layer(1,self.environment)
        parent.rendering_engine.add_to_layer(1,self.debug_object)

    def pack_sprites(self):
        pass


class WorldObject:
    def __init__(self, parent:World, texture:str):
        self.parent = parent
        self.sprite = utils.Utils.sprite_load(texture,)
        self.world_coords = (0,0)




class Player(WorldObject):
    def __init__(self,texture:str):
        super().__init__(texture)


class Environment(WorldObject):
    def __init__(self, texture:str):
        super().__init__(texture)
        pass

class Camera:
    def __init__(self, parent):
        self.pos = (100,0)

    def set_pos(self,coords:tuple):
        self.pos = coords

