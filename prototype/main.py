import pyglet
import pyglet.window.mouse


class Main:
    def __init__(self):
        self.rendering_engine = rendering_engine.RenderingEngine(self)
        self.world = world.World(self)
        self.input_manager = InputManager(self)
    
    def prepare_to_render(self):
        self.world.tick()
        self.rendering_engine.push_handlers(self.rendering_engine.mouse_state)
    
    


class InputManager:
    def __init__(self, parent:Main):
        super().__init__()
        self.parent = parent
        self.input_commands = {pyglet.window.key.Z: parent.world.alpha_player.move_up,
                               pyglet.window.key.S: parent.world.alpha_player.move_down,
                               pyglet.window.key.Q: parent.world.alpha_player.move_left,
                               pyglet.window.key.D: parent.world.alpha_player.move_right,
                               pyglet.window.key.UP: parent.world.instanciate_debug
                               }
        self.input_list = []

    def input_add(self,input):
        self.input_list.append(input)

    def input_remove(self,input):
        self.input_list.remove(input)
    
    def execute(self):
        for input in self.input_list:
            if input in self.input_commands.keys():
                self.input_commands[input]()

# scripts
import rendering_engine
import world