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
    
    def create_line(starting_point:tuple, ending_point:tuple):
        return pyglet.shapes.Line(starting_point[0], starting_point[1],
                                  ending_point[0], ending_point[1],
                                  thickness= 7, color=(75,75,255)
                                  )


