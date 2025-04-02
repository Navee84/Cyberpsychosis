import pyglet
import utils
from main import *

class RenderingEngine(pyglet.window.Window):
        def __init__(self, parent:Main):
            super().__init__(caption="prototype window", width = 1280, height = 720,)
            self.window_center = (self.width // 2, self.height // 2)

            self.layer1 = []
            

            @self.event
            def on_draw():
                self.clear()
                self.background_sprite.draw()
                parent.input_manager.execute()

            @self.event
            def on_key_press(symbol, modifiers):
                parent.input_manager.input_add(symbol)

            @self.event
            def on_key_release(symbol, modifiers):
                parent.input_manager.input_remove(symbol)

        def background_up(self):
            if self.background_sprite.y > -360:
                self.background_sprite.y -= 8
            else:
                self.background_sprite.y = -360
            self.show_coords()

        def background_down(self):
            if self.background_sprite.y < 1080:
                self.background_sprite.y += 8
            else:
                self.background_sprite.y = 1080
            self.show_coords()

        def background_right(self):
            if self.background_sprite.x > -640:
                self.background_sprite.x -= 8
            else:
                self.background_sprite.x = -640
            self.show_coords()

        def background_left(self):
            if self.background_sprite.x < 1920:
                self.background_sprite.x += 8
            else:
                self.background_sprite.x = 1920
            self.show_coords()

        def show_coords(self):
            print(f"X,Y coords : {self.background_sprite.x},{self.background_sprite.y}")
        
        def render_layer(self,layer:list):
            for elem in layer:
                elem.draw()
        
        def add_to_layer(self,layer:int,object):
            match layer:
                case 1:
                    self.layer1.append(object)
                
                case _ :
                    print(f"{utils.Utils.console_prefix_error} layer {layer} does not exist.")
            
