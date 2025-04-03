import pyglet

class Utils:
    def __init__(self):
        self.console_prefix_error = "[ERROR]"
        self.console_prefix_info = "[INFO]"
        self.console_prefix_warning = "[WARNING]"
    
    def sprite_load(self,path:str) -> pyglet.sprite.Sprite:
        image = pyglet.image.load(path)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        return pyglet.sprite.Sprite(image)
    



