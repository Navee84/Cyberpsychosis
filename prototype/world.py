import utils
from main import *

class World:
    def __init__(self,parent:Main):
        self.environment = Environment(self,"misc/blueprint-background_HD.png")

        parent.rendering_engine.add_to_layer(1,self.environment)



class WorldObject:
    def __init__(self, texture:str):
        self.sprite = utils.Utils.sprite_load(texture)
        self.world_coords = (0,0)


class Player(WorldObject):
    def __init__(self,texture:str):
        super().__init__(texture)


class Environment(WorldObject):
    def __init__(self, parent:World, texture:str):
        super().__init__(texture)
        pass

