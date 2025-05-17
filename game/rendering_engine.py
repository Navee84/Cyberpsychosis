import pyglet
import pyglet.window.mouse
import utils
import world
from main import *


class RenderingEngine(pyglet.window.Window):
    def __init__(self, parent:Main):
        super().__init__(caption="Cyberpsychosis", fullscreen = True)

        cursor_image = pyglet.image.load("game/assets/textures/cursor/arrow.png")
        cursor = pyglet.window.ImageMouseCursor(cursor_image, 3, 21)

        self.set_mouse_cursor(cursor)
        self.set_mouse_visible(True)
        self.parent = parent
        self.window_center = (self.width // 2, self.height // 2)
        # self.fps_display = pyglet.window.FPSDisplay(self) # ONLY FOR DEBUG AND DEVELOPMENT

        self.batch = pyglet.graphics.Batch()
        self.batch_layer_background = pyglet.graphics.Group(order=0)
        self.batch_layer_middleground = pyglet.graphics.Group(order=1)
        self.batch_layer_foreground = pyglet.graphics.Group(order=2)
        self.batch_layer_ui = pyglet.graphics.Group(order=3)
        self.batch_layer_loadingscreen = pyglet.graphics.Group(order=5)

        self.debug_render_queue = utils.Queue()

        #WINDOW EVENTS
        @self.event
        def on_deactivate():
            self.parent.input_manager.input_list = []

        # GAME EVENTS
        @self.event
        def on_key_release(symbol, modifiers):
            parent.input_manager.input_remove(symbol)

        @self.event
        def on_key_press(symbol, modifiers):
            parent.input_manager.input_add(symbol)

        @self.event
        def on_mouse_press(x,y, button, modifiers):
            parent.input_manager.mouse_inputs_add(button)

        @self.event
        def on_mouse_release(x,y, button, modifiers):
            parent.input_manager.mouse_inputs_remove(button)

        @self.event
        def on_draw():
            
            self.parent.prepare_to_render()
            self.parent.input_manager.execute()
            self.clear()
            self.batch.draw()
            self.render_debug(self.debug_render_queue)
            self.parent.input_manager.execute()
            # self.fps_display.draw() # ONLY FOR DEBUG AND DEVELOPMENT


    # METHODS

    def render_debug(self,queue:utils.Queue) -> None:
        while not queue.is_empty():
            queue.dequeue().draw()



