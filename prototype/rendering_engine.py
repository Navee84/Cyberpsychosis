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
        super().__init__(caption="prototype window", width = 1280, height = 720)
        cursor_image = pyglet.image.load("prototype/assets/images/cursor/arrow.png")
        cursor = pyglet.window.ImageMouseCursor(cursor_image, 3, 21)
        #self.set_exclusive_mouse(True)
        self.set_mouse_cursor(cursor)
        self.set_mouse_visible(True)

        self.parent = parent
        self.window_center = (self.width // 2, self.height // 2)
        self.fps_display = pyglet.window.FPSDisplay(self) # ONLY FOR DEBUG AND DEVELOPMENT

        self.batch = pyglet.graphics.Batch()
        self.batch_layer_background = pyglet.graphics.Group(order=0)
        self.batch_layer_middleground = pyglet.graphics.Group(order=1)
        self.batch_layer_foreground = pyglet.graphics.Group(order=2)
        self.batch_layer_ui = pyglet.graphics.Group(order=3)

        self.debug_render_queue = Queue()


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

            self.clear()
            self.parent.prepare_to_render()
            self.batch.draw()
            self.render_debug(self.debug_render_queue)
            self.parent.input_manager.execute()
            self.fps_display.draw() # ONLY FOR DEBUG AND DEVELOPMENT


    # METHODS

    def render_debug(self,queue:Queue):
        while not queue.is_empty():
            queue.dequeue().draw()



