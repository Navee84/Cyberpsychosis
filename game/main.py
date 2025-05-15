import pyglet
import pyglet.window.mouse


class Main:
    def __init__(self):
        self.rendering_engine = rendering_engine.RenderingEngine(self)
        self.world = world.World(self)
        self.input_manager = InputManager(self)
    
    def prepare_to_render(self):
        self.world.tick()

        mouse_state_label = pyglet.text.Label("Mouse states : "+str(self.input_manager.mouse_inputs_state),
                          font_size=18,
                          x=10, y=60)
        self.rendering_engine.debug_render_queue.enqueue(mouse_state_label)
    
    


class InputManager:
    def __init__(self, parent:Main):
        super().__init__()
        self.parent = parent
        self.input_commands = {pyglet.window.key.Z: parent.world.player.move_up,
                               pyglet.window.key.S: parent.world.player.move_down,
                               pyglet.window.key.Q: parent.world.player.move_left,
                               pyglet.window.key.D: parent.world.player.move_right,
                               pyglet.window.key.R: parent.world.player.inventory.slots[parent.world.player.inventory.active_slot].reload,
                               pyglet.window.key.UP: parent.world.instanciate_enemy
                               }
        self.mouse_inputs_state = {"LMB" : False,
                                   "RMB" : False,
                                   "MBM": False
                                   }
        self.input_list = []

    def input_add(self,input):
        self.input_list.append(input)

    def input_remove(self,input):
        self.input_list.remove(input)
    
    def mouse_inputs_add(self,button):
        match button:
            case pyglet.window.mouse.LEFT:
                self.mouse_inputs_state["LMB"] = True
            case pyglet.window.mouse.RIGHT:
                self.mouse_inputs_state["RMB"] = True
            case pyglet.window.mouse.MIDDLE:
                self.mouse_inputs_state["MBM"] = True

    def mouse_inputs_remove(self,button):
        match button:
            case pyglet.window.mouse.LEFT:
                self.mouse_inputs_state["LMB"] = False
            case pyglet.window.mouse.RIGHT:
                self.mouse_inputs_state["RMB"] = False
            case pyglet.window.mouse.MIDDLE:
                self.mouse_inputs_state["MBM"] = False
    
    def execute(self):
        for input in self.input_list:
            if input in self.input_commands.keys():
                self.input_commands[input]()

# scripts
import rendering_engine
import world