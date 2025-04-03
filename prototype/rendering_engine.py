import pyglet
import utils
import world
from main import *

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


class RenderingEngine(pyglet.window.Window):
        def __init__(self, parent:Main):
            super().__init__(caption="prototype window", width = 1280, height = 720,)
            self.parent = parent
            self.window_center = (self.width // 2, self.height // 2)
            self.fps_display = pyglet.window.FPSDisplay(self) # ONLY FOR DEBUG AND DEVELOPMENT

            self.layer1 = Queue()
            self.batch = pyglet.graphics.Batch()
            self.batch_layer_background = pyglet.graphics.Group(order=0)
            self.batch_layer_middleground = pyglet.graphics.Group(order=1)
            self.batch_layer_foreground = pyglet.graphics.Group(order=3)

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
            def update():
                pass

            @self.event
            def on_draw():
                self.clear()
                self.batch.draw()
                self.render_layer(self.layer1)
                self.fps_display.draw() # ONLY FOR DEBUG AND DEVELOPMENT


        # METHODS
        def render_layer(self,layer:Queue):
            while not layer.is_empty():
                elem = layer.dequeue()
                elem.sprite.draw()


        def add_to_layer(self,layer:int,object:world.WorldObject):
            object.sprite.x, object.sprite.y = self.calculate_relative_camera_position(object)
            match layer:
                case 1:
                    self.layer1.enqueue(object)
                
                case _ :
                    print(f"{utils.Utils.console_prefix_error} layer {layer} does not exist.")

        def calculate_relative_camera_position(self,object:world.WorldObject):
            # extract verticies
            camera_x, camera_y = self.camera.pos
            window_center_x, window_center_y = self.window_center
            object_x, object_y = object.world_coords

            # calculate verticies
            new_x = object_x + window_center_x - camera_x
            new_y = object_y + window_center_y - camera_y

            return (new_x,new_y)



