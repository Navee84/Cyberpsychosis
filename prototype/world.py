import utils
from main import *


class World:
    def __init__(self,parent:Main):
        self.parent = parent
        self.objects_list = []
        self.game_state = "MainMenu"
        
        self.physics_engine = PhysicsEngine(self)
        self.camera = Camera(self)


        self.alpha_player = Player(self, "prototype/assets/textures/entity/default_texture.png", 1)
        self.alpha_player.hitbox = Hitbox(self.alpha_player, "rectangle", (100,100))
        self.alpha_player.hitbox.render = True
        self.alpha_player.world_coords = [350,150]
        
        self.instanciate_main_menu()

    def tick(self):
        match self.game_state:
            case "MainMenu":
                self.main_menu()

            case "Game":
                self.update_objects_positions()
                self.update_camera_position()
                self.alpha_player.render_values()



    def instanciate_main_menu(self):
        self.tite_image = PlainImage(self, "prototype/assets/textures/title.png",(640,660),0)
        button_sprite = utils.Utils.animated_sprite_load({"prototype/assets/textures/ui/play_button_1.png":None, "prototype/assets/textures/ui/play_button_2.png":None})
        self.play_button = Button(self, (200,200), (150,75), button_sprite)

    def main_menu(self):
        if self.play_button.is_clicked((self.parent.rendering_engine._mouse_x, self.parent.rendering_engine._mouse_y), True):
            self.instanciate_game()

    def instanciate_game(self):
        self.environment = Environment(self,"prototype/assets/textures/environment/blueprint-background_HD.png", 0)
        self.environment.fixed = True

        self.debug_object = DebugObject(self, "prototype/assets/textures/entity/default_texture.png", 1, True)
        self.debug_object.hitbox = Hitbox(self.debug_object, "triangle", (150,20))
        self.debug_object.hitbox.render = True
        self.debug_object.world_coords = [-350,-150]

        self.debug_object2 = DebugObject(self, "prototype/assets/textures/entity/default_texture.png", 1, False)
        self.debug_object2.hitbox = Hitbox(self.debug_object2, "rectangle", (100,150))
        self.debug_object2.hitbox.render = True
        self.debug_object2.world_coords = [260,-190]

        self.game_state = "Game"

    def instanciate_debug(self):
        self.debug_object3 = DebugObject(self, "prototype/assets/textures/entity/default_texture.png", 1, False)
        self.debug_object3.hitbox = Hitbox(self.debug_object3, "triangle", (170,20))
        self.debug_object3.hitbox.render = False
        self.debug_object3.world_coords = [-50,140]

    def update_objects_positions(self): # object must be WorldObject type
        for object in self.objects_list:
            object.apply_physics()
            object.update_sprite_position()
    
    def add_to_batch(self, object, group:int): # object must be WorldObject | PlainImage type
        object.sprite.batch = self.parent.rendering_engine.batch
        object.sprite.group = self.get_correct_batch_group(group)

    def get_correct_batch_group(self,number:int):
        match number:
            case 0:
                return self.parent.rendering_engine.batch_layer_background
            case 1:
                return self.parent.rendering_engine.batch_layer_middleground
            case 2:
                return self.parent.rendering_engine.batch_layer_foreground
            case 3:
                return self.parent.rendering_engine.batch_layer_ui
            case _:
                return None
    
    def remove_from_batch(self,object): # object must be WorldObject type
        pass

    def add_to_object_list(self, object):
        self.objects_list.append(object)
    
    def update_camera_position(self):
        # Change this to change the camera focus
        self.camera.set_pos(self.alpha_player.world_coords)

class PlainImage:
    def __init__(self, parent:World, sprite_path:str, position:tuple, orientation):
        self.parent = parent
        self.sprite = utils.Utils.sprite_load(sprite_path)
        self.pos = position
        self.orientation = orientation
        self.parent.add_to_batch(self,2)

        self.uptade_sprite()

    def set_position(self,coords:tuple):
        self.pos = coords

    def set_orientation(self,orientation):
        self.orientation = orientation
    
    def uptade_sprite(self):
        self.sprite.x = self.pos[0]
        self.sprite.y = self.pos[1]
        self.sprite.orientation = utils.degrees(-self.orientation)

class Button:
    def __init__(self, parent:World, position:tuple, dimentions:tuple, sprite):
        '''
        sprite argument must be pyglet.sprite.Sprite type
        '''
        self.parent = parent
        self.sprite = sprite
        self.pos = position
        self.dimentions = dimentions

        self.parent.add_to_batch(self,2)
        self.uptade_sprite()


    def uptade_sprite(self):
        self.sprite.x = self.pos[0]
        self.sprite.y = self.pos[1]

    def is_hovered(self, mouse_pos:tuple)->bool:
        mousex, mousey = mouse_pos
        width, height = self.dimentions
        self.sprite.frame_inex = 0

        if mousex < self.pos[0] - width//2:
            return False
        if mousex > self.pos[0] + width//2:
            return False

        if mousey < self.pos[1] - height//2:
            return False
        if mousey > self.pos[1] + height//2:
            return False
        
        self.sprite.frame_index = 1
        return True
        
    
    def is_clicked(self, mouse_pos:tuple, mouse_state)->bool:
        if not self.is_hovered(mouse_pos):
            return False
        
        return True
        

class WorldObject:
    def __init__(self, parent:World, texture:str, group:int, fixation:bool):

        self.parent = parent
        self.fixed = fixation

        # Defining all default values for a WorldObject
        self.sprite = utils.Utils.sprite_load(texture)
        self.orientation = 0 # 0 means facing right
        self.fov = 1
        self.hitbox = None

        # Movement values
        self.acceleration = 0
        self.max_speed = 0
        self.friction = 0.8 # Keep this value between 0 and 1 : 1 is no friction and 0 is maximum friction 

        self.world_coords = [0,0]
        self.speed = [0,0]

        if self.fixed:
            self.world_coords = (0,0)
            self.speed = (0,0)


        # Render related initialisation
        self.sprite.batch = parent.parent.rendering_engine.batch
        self.sprite.group = self.get_correct_batch_group(group)
        self.add_to_world_object_list()

    def apply_physics(self):
        self.parent.physics_engine.update_position(self)
        self.update_hitbox_position()

    def get_screen_pos(self):
        return (self.world_coords[0]*self.fov - self.parent.camera.pos[0]*self.fov + self.parent.parent.rendering_engine.window_center[0], self.world_coords[1]*self.fov - self.parent.camera.pos[1]*self.fov + self.parent.parent.rendering_engine.window_center[1])

    def update_sprite_position(self):
        self.sprite.scale = self.fov
        self.sprite.rotation = utils.degrees(-self.orientation)
        screen_pos = self.get_screen_pos()
        self.sprite.x = screen_pos[0]
        self.sprite.y = screen_pos[1]
    
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
        super().__init__(parent, texture, group, False)

        # movement values:
        self.acceleration = 2
        self.max_speed = 6
    
    def move_up(self):
        self.speed[1] = round(min(self.max_speed,self.speed[1]+self.acceleration),2)

    def move_down(self):
        self.speed[1] = round(max(-self.max_speed,self.speed[1]-self.acceleration),2)

    def move_left(self):
        self.speed[0] = round(max(-self.max_speed,self.speed[0]-self.acceleration),2)

    def move_right(self):
        self.speed[0] = round(min(self.max_speed,self.speed[0]+self.acceleration),2)

    def face_mouse(self):
        angle = utils.Utils.get_angle((self.parent.parent.rendering_engine._mouse_x,self.parent.parent.rendering_engine._mouse_y),self.get_screen_pos())
        self.orientation = angle

    def render_values(self):
        coords_label = pyglet.text.Label("Coords : "+str(self.world_coords),
                          font_size=18,
                          x=10, y=690)
        
        speed_label = pyglet.text.Label("Speed : "+str(self.speed),
                          font_size=18,
                          x=10, y=660)

        orientation_label = pyglet.text.Label("Orientation : "+str(self.orientation),
                          font_size=18,
                          x=10, y=620)

        mouse_pos_label = pyglet.text.Label("Mousepos : "+str((self.parent.parent.rendering_engine._mouse_x,self.parent.parent.rendering_engine._mouse_y)),
                          font_size=18,
                          x=240, y=690)

        self.parent.parent.rendering_engine.debug_render_queue.enqueue(coords_label)
        self.parent.parent.rendering_engine.debug_render_queue.enqueue(speed_label)
        self.parent.parent.rendering_engine.debug_render_queue.enqueue(orientation_label)
        self.parent.parent.rendering_engine.debug_render_queue.enqueue(mouse_pos_label)


class Environment(WorldObject): # UNIQUE OBJECT, DEFiNE THE BACKGROUND ENVIRONMENT
    def __init__(self, parent, texture:str, group:int):
        super().__init__(parent, texture, group, True)


class Camera:
    def __init__(self, parent):
        self.pos = [0,0]

    def set_pos(self,coords:list):
        self.pos = coords

class DebugObject(WorldObject):
    def __init__(self, parent, texture:str, group:int, fixation:bool):
        super().__init__(parent, texture, group, fixation)



class Hitbox:
    def __init__(self, parent:WorldObject, preset:str, dimensions:tuple):
        self.parent = parent

        # Vérifie que le preset entré en argument est dans la liste des presets disponibles
        allowed_presets = ("rectangle","triangle","circle","hexagon")
        if not preset in allowed_presets:
            raise TypeError(f"{utils.Utils.console_prefix_error} preset '{preset}' is not a valid preset")
        
        self.dimensions = dimensions
        self.preset = preset
        self.render = False
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

        point_list = [top_left, top_right,bottom_right, bottom_left]

        rotated_list = []
        for point in point_list:
            rotated_list.append(utils.Utils.apply_rotation(self.parent.world_coords,point,self.parent.orientation))

        return rotated_list
    
    def preset_triangle(self, width, down_offset):
        top = (self.parent.world_coords[0], self.parent.world_coords[1] + int((2/3)*((3**0.5)*(width//2))) - down_offset)

        bottom_middle = (self.parent.world_coords[0],self.parent.world_coords[1] - int((1/3)*((3**0.5)*(width//2))) - down_offset)
        bottom_left = (bottom_middle[0] - width//2, bottom_middle[1])
        bottom_right = (bottom_middle[0] + width//2, bottom_middle[1])

        point_list = [top,bottom_right, bottom_left]

        rotated_list = []
        for point in point_list:
            rotated_list.append(utils.Utils.apply_rotation(self.parent.world_coords,point,self.parent.orientation))

        return rotated_list

    def preset_circle(self):
        pass
    
    def preset_hexagon(self):
        pass

    def dump(self):
        print(f"Preset : {self.preset}")
        print(f"Coords : {self.hitbox_coordinates}")
        print(f"Rotation : {self.parent.orientation}")

    



class PhysicsEngine:
    def __init__(self, parent:World):
        self.parent = parent

    def update_position(self,active_object:WorldObject) -> None:
        '''
        Input : an entity object
        Calculate new posistion in the word using object's defined acceleration, current horizontal and vertical speed, maximum speed
        Output : same object but with modified world_pos values
        '''
        # UPDATING POSITIONS

        if active_object.fixed:
            return None

        candidate_queue = utils.Queue()

        # prevent stucking speed at low values
        for i in range(2):
            if (active_object.speed[i]**2)**(1/2) < (0.1):
                active_object.speed[i] = 0


        active_object.speed[0] = round(active_object.speed[0] * active_object.friction,2)
        active_object.speed[1] = round(active_object.speed[1] * active_object.friction,2)

        active_object.world_coords[0] = round(active_object.world_coords[0]+active_object.speed[0])
        active_object.world_coords[1] = round(active_object.world_coords[1]+active_object.speed[1])

        # CHECKING COLLISION

        for object in self.parent.objects_list:
            if object.hitbox != None:
                if object != active_object:
                    if max(object.hitbox.dimensions[0], object.hitbox.dimensions[1])*1.5 > utils.Utils.distance(active_object.world_coords,object.world_coords):
                        candidate_queue.enqueue(object)

        while not candidate_queue.is_empty():
            tested_object = candidate_queue.dequeue()

        # RESOLVING COLLISION
            collision_result = self.is_colliding(active_object.hitbox,tested_object.hitbox)
            if collision_result[0]:
                active_object.hitbox.is_colliding = True
                tested_object.hitbox.is_colliding = True
    
                if active_object.fixed == False:
                    active_object.world_coords = (utils.Utils.translate(active_object.world_coords, collision_result[1]))


            else:
                active_object.hitbox.is_colliding = False
                tested_object.hitbox.is_colliding = False
        




    def is_colliding(self,hitbox1:Hitbox,hitbox2:Hitbox) -> tuple:
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


        minimum_depth_value = 1*(10**9)
        retained_vector = None
        for normal in normals:
            k1_values = []
            for point in hitbox1.hitbox_coordinates:
                k1_values.append(self.get_scalar_coefficient(normal,point))

            k2_values = []
            for point in hitbox2.hitbox_coordinates:
                k2_values.append(self.get_scalar_coefficient(normal,point))
        
            # Test separation
            overlap_test = self.is_overlapping(k1_values,k2_values)
            if not overlap_test[0]:
                return (False, None)
            
            # Retain minimum depth value and its associated vector (used to resolve collision)
            if min(minimum_depth_value,overlap_test[1]) == overlap_test[1]:
                minimum_depth_value = overlap_test[1]

                # Check normal direction and invert it if needed
                retained_vector = (round(normal[0]*minimum_depth_value), round(normal[1]*minimum_depth_value))

                vector_a_b = utils.Utils.get_vector(hitbox1.parent.world_coords, hitbox2.parent.world_coords)
                scalar_coefficient = self.get_scalar_coefficient(normal,vector_a_b)
                if scalar_coefficient > 0:
                    retained_vector = (-1*retained_vector[0], -1*retained_vector[1])



        # If no separation is found in all normals :
        collision_label = pyglet.text.Label("Colliding : "+str(hitbox1)+" and "+str(hitbox2),
                font_size=18,
                x=10, y=580)

        self.parent.parent.rendering_engine.debug_render_queue.enqueue(collision_label)
        return (True,retained_vector)

            
    def is_overlapping(self, list1, list2) -> tuple:
        k1_max = utils.Utils.get_max(list1)
        k1_min = utils.Utils.get_min(list1)
        k2_max = utils.Utils.get_max(list2)
        k2_min = utils.Utils.get_min(list2)

        overlap_value = min(k1_max - k2_min, k2_max - k1_min)
        # if k1_max - k2_min <= 0:
        #     return False

        # if k2_max - k1_min <= 0:
        #     return False
        if overlap_value <= 0:
            return (False, overlap_value)
        
        return (True, overlap_value)


    def get_normals(self, point_a:tuple, point_b:tuple)-> tuple:
        # simple formule de vecteur normal
        return (-1*(point_b[1]-point_a[1]), point_b[0]-point_a[0])
        
    
    def get_scalar_coefficient(self, vector:tuple, point:tuple):
        k = (vector[0]*point[0] + vector[1]*point[1]) / (vector[0]**2 + vector[1]**2)
        rounded = round(k,3)
        return rounded