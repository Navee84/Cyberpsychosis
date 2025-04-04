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
            def update():
                pass

            @self.event
            def on_draw():

                self.parent.prepare_to_render()
                self.clear()
                self.batch.draw()
                self.parent.input_manager.execute()
                self.fps_display.draw() # ONLY FOR DEBUG AND DEVELOPMENT


        # METHODS



