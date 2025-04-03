import pyglet



class Main:
    def __init__(self):
        self.rendering_engine = rendering_engine.RenderingEngine(self)
        self.world = world.World(self)
        self.input_manager = InputManager(self)
    
    


class InputManager:
    def __init__(self, parent:Main):
        super().__init__()
        # self.input_commands = {pyglet.window.key.Z: parent.rendering_engine.background_up,
        #                        pyglet.window.key.S: parent.rendering_engine.background_down,
        #                        pyglet.window.key.Q: parent.rendering_engine.background_left,
        #                        pyglet.window.key.D: parent.rendering_engine.background_right
        #                        }
        self.input_list = []

    def input_add(self,input):
        self.input_list.append(input)

    def input_remove(self,input):
        self.input_list.remove(input)
    
    def execute(self):
        # for input in self.input_list:
        #     if input in self.input_commands.keys():
        #         self.input_commands[input]()
        pass

# scripts
import rendering_engine
import world