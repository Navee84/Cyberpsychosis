import pyglet
import utils
import world
from main import *

class RenderingEngine(pyglet.window.Window):
        def __init__(self, parent:Main):
            super().__init__(caption="prototype window", width = 1280, height = 720,)
            self.parent = parent
            self.window_center = (self.width // 2, self.height // 2)
            self.layer1 = []
            self.fps_display = pyglet.window.FPSDisplay(self) # ONLY FOR DEBUG AND DEVELOPMENT
            self.camera = Camera(self)


            # GAME EVENTS
            @self.event
            def on_key_release(symbol, modifiers):
                parent.input_manager.input_remove(symbol)

            @self.event
            def on_key_press(symbol, modifiers):
                parent.input_manager.input_add(symbol)
            
            @self.event
            def update_inputs():
                self.parent.input_manager.execute()

            @self.event
            def on_draw():
                self.clear()
                self.render_layer(self.layer1)
                self.fps_display.draw() # ONLY FOR DEBUG AND DEVELOPMENT

        def get_camera(self,camera_object):
            self.camera = camera_object
            
        def render_layer(self,layer:list):
            for elem in layer:
                elem.sprite.draw()


        def add_to_layer(self,layer:int,object:world.WorldObject):
            object.sprite.x, object.sprite.y = self.calculate_relative_camera_position(object)
            match layer:
                case 1:
                    self.layer1.append(object)
                
                case _ :
                    print(f"{utils.Utils.console_prefix_error} layer {layer} does not exist.")

        def calculate_relative_camera_position(self,object:world.WorldObject):
            camera_x, camera_y = self.camera.pos
            window_x, window_y = self.window_center
            object_x, object_x = object.world_coords

            # calculate verticies

            return (-camera_x,-camera_y)

class Camera:
    def __init__(self, parent):
        self.pos = (0,0)
