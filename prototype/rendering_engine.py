import pyglet
import utils
import world
from main import *


class RenderingEngine(pyglet.window.Window):
    def __init__(self, parent:Main):
        super().__init__(caption="prototype window", width = 1280, height = 720)

        cursor_image = pyglet.image.load("prototype/assets/textures/cursor/arrow.png")
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

        self.debug_render_queue = utils.Queue()


        # GAME EVENTS
        @self.event
        def on_key_release(symbol, modifiers):
            parent.input_manager.input_remove(symbol)

        @self.event
        def on_key_press(symbol, modifiers):
            parent.input_manager.input_add(symbol)

        @self.event
        def on_draw():
            
            self.parent.prepare_to_render()
            self.parent.input_manager.execute()
            self.clear()
            self.batch.draw()
            self.render_debug(self.debug_render_queue)
            self.parent.input_manager.execute()
            self.fps_display.draw() # ONLY FOR DEBUG AND DEVELOPMENT


    # METHODS

    def render_debug(self,queue:utils.Queue):
        while not queue.is_empty():
            queue.dequeue().draw()



