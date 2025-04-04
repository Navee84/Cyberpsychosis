import pyglet


class Main:
    def __init__(self):
        self.rendering_engine = rendering_engine.RenderingEngine(self)
        self.world = world.World(self)
        self.input_manager = InputManager(self)
    
    def prepare_to_render(self):
        self.world.update_sprites_positions()
        self.world.update_camera_position()
    
    


class InputManager:
    def __init__(self, parent:Main):
        super().__init__()
        self.input_commands = {pyglet.window.key.Z: parent.world.debug_object.go_up,
                               pyglet.window.key.S: parent.world.debug_object.go_down,
                               pyglet.window.key.Q: parent.world.debug_object.go_left,
                               pyglet.window.key.D: parent.world.debug_object.go_right
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
        pass

# scripts
import rendering_engine
import world