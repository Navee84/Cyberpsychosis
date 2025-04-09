import utils
from main import *

class World:
    def __init__(self,parent:Main):
        self.parent = parent
        self.objects_list = []
        
        self.camera = Camera(self)
        self.environment = Environment(self,"prototype/assets/images/textures/blueprint-background_HD.png", 0)

        self.alpha_player = Player(self, "misc/default_texture.png", 1)
        self.alpha_player.hitbox = Hitbox(self.alpha_player, "rectangle", (100,100))
        self.alpha_player.hitbox.render = True
        self.alpha_player.world_coords = [350,150]

        self.debug_object = DebugObject(self, "misc/default_texture.png", 1)
        self.debug_object.hitbox = Hitbox(self.debug_object, "rectangle", (150,150))
        self.debug_object.hitbox.render = True
        self.debug_object.world_coords = [-350,-150]
        


    def update_objects_positions(self): # object must be WorldObject type
        for object in self.objects_list:
            object.update_hitbox_position()
            object.update_sprite_position()
    
    def add_to_batch(self,object): # object must be WorldObject type
        object.sprite.batch = self.parent.rendering_engine.batch
    
    def remove_from_batch(self,object): # object must be WorldObject type
        pass

    def add_to_object_list(self, object):
        self.objects_list.append(object)
    
    def update_camera_position(self):
        self.camera.set_pos(self.alpha_player.world_coords)


class WorldObject:
    def __init__(self, parent:World, texture:str, group:int):
        self.parent = parent

        # Defining all default values for a WorldObject
        self.sprite = utils.Utils.sprite_load(texture)
        self.world_coords = [0,0]
        self.orientation = 0 # 0 means facing right
        self.fov = 1
        self.hitbox = None

        # Render related initialisation
        self.sprite.batch = parent.parent.rendering_engine.batch
        self.sprite.group = self.get_correct_batch_group(group)
        self.add_to_world_object_list()

    def update_sprite_position(self):
        self.sprite.scale = self.fov
        self.sprite.x = self.world_coords[0]*self.fov - self.parent.camera.pos[0]*self.fov + self.parent.parent.rendering_engine.window_center[0]
        self.sprite.y = self.world_coords[1]*self.fov - self.parent.camera.pos[1]*self.fov + self.parent.parent.rendering_engine.window_center[1]
    
    def update_hitbox_position(self):
        if not self.hitbox == None:
            self.hitbox.update()


    def add_to_world_object_list(self):
        self.parent.add_to_object_list(self)

    def get_correct_batch_group(self,number:int):
        match number:
            case 0:
                return self.parent.parent.rendering_engine.batch_layer_background
            case 1:
                return self.parent.parent.rendering_engine.batch_layer_middleground
            case 2:
                return self.parent.parent.rendering_engine.batch_layer_foreground
            case 3:
                return self.parent.parent.rendering_engine.batch_layer_ui
            case _:
                return None


class Player(WorldObject):
    def __init__(self, parent, texture:str, group:int):
        super().__init__(parent, texture, group)

        self.speed = 4
    
    def go_up(self):
        self.world_coords[1] += self.speed

    def go_down(self):
        self.world_coords[1] -= self.speed

    def go_left(self):
        self.world_coords[0] -= self.speed

    def go_right(self):
        self.world_coords[0] += self.speed



class Environment(WorldObject): # UNIQUE OBJECT, DEFiNE THE BACKGROUND ENVIRONMENT
    def __init__(self, parent, texture:str, group:int):
        super().__init__(parent, texture, group)


class Camera:
    def __init__(self, parent):
        self.pos = [0,0]

    def set_pos(self,coords:list):
        self.pos = coords

class DebugObject(WorldObject):
    def __init__(self, parent, texture:str, group:int):
        super().__init__(parent, texture, group)



class Hitbox:
    def __init__(self, parent:WorldObject, preset:str, dimensions:tuple):
        self.parent = parent

        allowed_presets = ("rectangle","triangle","circle","hexagon")
        if not preset in allowed_presets:
            raise TypeError(f"preset '{preset}' is not a valid preset")
        
        self.dimensions = dimensions
        self.preset = preset
        self.render = True

        self.size = 1
        self.hitbox_coordinates = None # Coordinates always go from top left in clockwise order
        
        # once everything is setup, updates the hitbox coordinates a first time
        self.update()

    def update(self):
        match self.preset:
            case "rectangle":
                self.hitbox_coordinates = self.preset_rectangle(self.dimensions[0], self.dimensions[1])

            case "triangle":
                self.hitbox_coordinates = self.preset_triangle(self.dimensions[0],self.dimensions[1])
        
        if self.render:
            for i in range(len(self.hitbox_coordinates)-1):
                self.parent.parent.parent.rendering_engine.debug_render_queue.enqueue(utils.Utils.create_line((self.hitbox_coordinates[i][0]*self.parent.fov - self.parent.parent.camera.pos[0]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[0] , self.hitbox_coordinates[i][1]*self.parent.fov - self.parent.parent.camera.pos[1]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[1]),
                                                                                                               (self.hitbox_coordinates[i+1][0]*self.parent.fov - self.parent.parent.camera.pos[0]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[0] , self.hitbox_coordinates[i+1][1]*self.parent.fov - self.parent.parent.camera.pos[1]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[1])
                                                                                                               ))

            self.parent.parent.parent.rendering_engine.debug_render_queue.enqueue(utils.Utils.create_line((self.hitbox_coordinates[-1][0]*self.parent.fov - self.parent.parent.camera.pos[0]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[0] , self.hitbox_coordinates[-1][1]*self.parent.fov - self.parent.parent.camera.pos[1]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[1]),
                                                                                                            (self.hitbox_coordinates[0][0]*self.parent.fov - self.parent.parent.camera.pos[0]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[0] , self.hitbox_coordinates[0][1]*self.parent.fov - self.parent.parent.camera.pos[1]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[1])
                                                                                                            ))
    def preset_rectangle(self,height, width):
        top_left = (self.parent.world_coords[0] - width//2 , self.parent.world_coords[1] + height//2)
        top_right = (self.parent.world_coords[0] + width//2, self.parent.world_coords[1] + height//2)

        bottom_left = (self.parent.world_coords[0] - width//2 , self.parent.world_coords[1] - height//2)
        bottom_right = (self.parent.world_coords[0] + width//2, self.parent.world_coords[1] - height//2)
        return [top_left,top_right,bottom_right,bottom_left]
    
    def preset_triangle(self):
        pass

    def preset_circle(self):
        pass
    
    def preset_hexagon(self):
        pass
    



class PhysicsEngine:
    pass