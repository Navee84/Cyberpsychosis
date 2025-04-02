import utils

class World:
    def __init__(self):
        camera = Camera(self)
        environment = Environment(self)

class Camera:
    def __init__(self, parent):
        self.world_coords = (0,0)

class Player:
    def __init__(self):
        pass

class Environment:
    def __init__(self, parent):
        self.background = utils.Utils.sprite_load("misc/blueprint-background_HD.png")
        self.world_coords = (0,0)
