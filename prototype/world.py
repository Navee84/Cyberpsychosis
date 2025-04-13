import utils
from main import *

class World:
    def __init__(self,parent:Main):
        self.parent = parent
        self.objects_list = []
        
        self.physics_engine = PhysicsEngine()
        self.camera = Camera(self)
        self.environment = Environment(self,"prototype/assets/images/textures/blueprint-background_HD.png", 0)

        self.alpha_player = Player(self, "misc/default_texture.png", 1)
        self.alpha_player.hitbox = Hitbox(self.alpha_player, "rectangle", (100,100))
        self.alpha_player.hitbox.render = True
        self.alpha_player.world_coords = [350,150]

        self.debug_object = DebugObject(self, "misc/default_texture.png", 1)
        self.debug_object.hitbox = Hitbox(self.debug_object, "triangle", (150,20))
        self.debug_object.hitbox.render = True
        self.debug_object.world_coords = [-350,-150]

    def check_colision(self): # DEBUG FUNCTION, DO NOT USE FOR FINAL PROGRAM
        if self.physics_engine.is_colliding(self.alpha_player.hitbox,self.debug_object.hitbox):
            self.alpha_player.hitbox.is_colliding = True
            self.debug_object.hitbox.is_colliding = True
        else:
            self.alpha_player.hitbox.is_colliding = False
            self.debug_object.hitbox.is_colliding = False
        


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
        self.fov = 1.6
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

class Entity:
    def __init__(self):
        self.acceleration = None
        self.max_speed = None
        self.vertical_speed = None
        self.horizontal_speed = None
    

class Player(WorldObject,Entity):
    def __init__(self, parent, texture:str, group:int):
        super().__init__(parent, texture, group)

        # movement values:
        self.acceleration = 4
        self.max_speed = 5
        self.vertical_speed = 0
        self.horizontal_speed = 0
    
    def move_up(self):
        self.world_coords[1] += self.acceleration

    def move_down(self):
        self.world_coords[1] -= self.acceleration

    def move_left(self):
        self.world_coords[0] -= self.acceleration   

    def move_right(self):
        self.world_coords[0] += self.acceleration



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
            raise TypeError(f"{utils.Utils.console_prefix_error} preset '{preset}' is not a valid preset")
        
        self.dimensions = dimensions
        self.preset = preset
        self.render = True
        self.is_colliding = False

        self.size = 1
        self.hitbox_coordinates = None # Coordinates always go from top left in clockwise order
        
        # once everything is setup, updates the hitbox coordinates a first time
        self.update()

    def update(self):
        color = (75,100,255)
        if self.is_colliding:
            color = (255,100,75)

        match self.preset:
            case "rectangle":
                self.hitbox_coordinates = self.preset_rectangle(self.dimensions[0], self.dimensions[1])

            case "triangle":
                self.hitbox_coordinates = self.preset_triangle(self.dimensions[0], self.dimensions[1])
        
        if self.render:
            for i in range(len(self.hitbox_coordinates)-1):
                self.parent.parent.parent.rendering_engine.debug_render_queue.enqueue(utils.Utils.create_line((self.hitbox_coordinates[i][0]*self.parent.fov - self.parent.parent.camera.pos[0]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[0] , self.hitbox_coordinates[i][1]*self.parent.fov - self.parent.parent.camera.pos[1]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[1]),
                                                                                                               (self.hitbox_coordinates[i+1][0]*self.parent.fov - self.parent.parent.camera.pos[0]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[0] , self.hitbox_coordinates[i+1][1]*self.parent.fov - self.parent.parent.camera.pos[1]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[1]),
                                                                                                               color
                                                                                                               ))

            self.parent.parent.parent.rendering_engine.debug_render_queue.enqueue(utils.Utils.create_line((self.hitbox_coordinates[-1][0]*self.parent.fov - self.parent.parent.camera.pos[0]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[0] , self.hitbox_coordinates[-1][1]*self.parent.fov - self.parent.parent.camera.pos[1]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[1]),
                                                                                                            (self.hitbox_coordinates[0][0]*self.parent.fov - self.parent.parent.camera.pos[0]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[0] , self.hitbox_coordinates[0][1]*self.parent.fov - self.parent.parent.camera.pos[1]*self.parent.fov + self.parent.parent.parent.rendering_engine.window_center[1]),
                                                                                                            color
                                                                                                            ))
    def preset_rectangle(self,height, width):
        top_left = (self.parent.world_coords[0] - width//2 , self.parent.world_coords[1] + height//2)
        top_right = (self.parent.world_coords[0] + width//2, self.parent.world_coords[1] + height//2)

        bottom_left = (self.parent.world_coords[0] - width//2 , self.parent.world_coords[1] - height//2)
        bottom_right = (self.parent.world_coords[0] + width//2, self.parent.world_coords[1] - height//2)

        return [top_left,top_right,bottom_right,bottom_left]
    
    def preset_triangle(self, width, down_offset):
        top = (self.parent.world_coords[0], self.parent.world_coords[1] + int((2/3)*((3**0.5)*(width//2))) - down_offset)

        bottom_middle = (self.parent.world_coords[0],self.parent.world_coords[1] - int((1/3)*((3**0.5)*(width//2))) - down_offset)
        bottom_left = (bottom_middle[0] - width//2, bottom_middle[1])
        bottom_right = (bottom_middle[0] + width//2, bottom_middle[1])

        return [top, bottom_right, bottom_left]

    def preset_circle(self):
        pass
    
    def preset_hexagon(self):
        pass

    def dump(self):
        print(f"Preset : {self.preset}")
        print(f"Coords : {self.hitbox_coordinates}")

    



class PhysicsEngine:
    def update_position(self,object:Entity) -> list:
        '''
        Input : an entity object
        Calculate new posistion in the word using object's defined acceleration, current horizontal and vertical speed, maximum speed
        Output : a list of x and y coordinates -> [x,y]
        '''
        pass

    def is_colliding(self,hitbox1:Hitbox,hitbox2:Hitbox) -> bool:
        '''
        Returns True if the hitboxes overlap, False if the hitboxes are not touching
        '''
        normals = []
        for i in range(len(hitbox1.hitbox_coordinates)-1):
            normals.append(self.get_normals(hitbox1.hitbox_coordinates[i],hitbox1.hitbox_coordinates[i+1]))
        normals.append(self.get_normals(hitbox1.hitbox_coordinates[-1],hitbox1.hitbox_coordinates[0]))

        for i in range(len(hitbox2.hitbox_coordinates)-1):
            normals.append(self.get_normals(hitbox2.hitbox_coordinates[i],hitbox2.hitbox_coordinates[i+1]))
        normals.append(self.get_normals(hitbox2.hitbox_coordinates[-1],hitbox2.hitbox_coordinates[0]))

        for normal in normals:
            k1_values = []
            for point in hitbox1.hitbox_coordinates:
                k1_values.append(self.get_scalar_coefficient(normal,point))

            k2_values = []
            for point in hitbox2.hitbox_coordinates:
                k2_values.append(self.get_scalar_coefficient(normal,point))

            if not self.is_overlapping(k1_values,k2_values):
                return False

        return True

            
    def is_overlapping(self, list1, list2) -> bool:
        k1_max = utils.Utils.get_max(list1)
        k1_min = utils.Utils.get_min(list1)
        k2_max = utils.Utils.get_max(list2)
        k2_min = utils.Utils.get_min(list2)

        if k1_max - k2_min <= 0:
            return False

        if k2_max - k1_min <= 0:
            return False
        
        return True




    def get_normals(self, point_a:tuple, point_b:tuple)-> tuple:
        # simple formule de vecteur normal
        return (-1*(point_b[1]-point_a[1]), point_b[0]-point_a[0])
        
    
    def get_scalar_coefficient(self, vector:tuple, point:tuple):
        k = (vector[0]*point[0] + vector[1]*point[1]) / (vector[0]**2 + vector[1]**2)
        rounded = round(k,3)
        return rounded