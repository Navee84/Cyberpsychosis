import utils
import gc
from main import *


class World:
    def __init__(self,parent:Main):
        self.parent = parent
        self.music_manager = utils.MusicManager()
        self.objects_list = []
        self.enemy_list = []
        self.game_object_list = utils.Queue()
        self.game_state = "MainMenu"
        self.button_click = False
        self.can_skip = False

        # DEVELOPEMENT VALUES
        self.music_manager.volume = 0 # DEVELOPEMENT ONLY
        self.can_skip = True
        
        self.physics_engine = PhysicsEngine(self)
        self.camera = Camera(self)


        self.player = Player(self, "game/assets/textures/entity/default_texture.png", 1)
        self.player.hide()
        
        self.instanciate_main_menu()

    def tick(self):
        match self.game_state:
            # case "LoadingScreen":
            #     self.loading()
                
            case "MainMenu":
                self.main_menu()

            case "PreGame1":
                self.pre_game1()

            case "PreGame2":
                self.pre_game2()

            case "PreGame3":
                self.pre_game3()

            case "Game":
                self.game()

            case "PostGame1":
                self.post_game1()
            
            case "PostGame2":
                self.post_game2()
    # def show_loading_screen(self):
    #     self.loading_screen = PlainImage(self,"game/assets/textures/ui/loading_screen.png",(0,0),0, 5)
    #     self.game_state = "LoadingScreen"

    # def loading(self):
    def empty_music_queue(self):
        while self.music_manager.source != None:
            self.music_manager.next_source()





    def instanciate_main_menu(self):
        self.main_menu_button = None
        self.empty_music_queue()
        self.music_manager.queue(self.music_manager.music_dict["modern_anthill"])
        self.music_manager.play()
        self.music_manager.loop = True

        self.title_image = PlainImage(self, "game/assets/textures/title.png",(0,275),0, 2)
        self.background_image = PlainImage(self, "game/assets/textures/menu_image.png", (0,0), 0, 0)
        button_sprite = utils.Utils.animated_sprite_load({"game/assets/textures/ui/play_button_1.png":None, "game/assets/textures/ui/play_button_2.png":None})
        self.play_button = Button(self, (0,0), (150,75), button_sprite)

        self.game_state = "MainMenu"

    def main_menu(self):
        if self.play_button.is_clicked((self.parent.rendering_engine._mouse_x, self.parent.rendering_engine._mouse_y)):
            # self.show_loading_screen()
            self.instanciate_pre_game(1)
    


    def instanciate_pre_game(self, phase):
        self.title_image = None
        self.play_button = None
        self.background_image = None
        match phase:
            case 1:
                print("PREGAME")
                self.music_manager.queue(self.music_manager.music_dict['pre_game_1'])
                self.music_manager.queue(self.music_manager.music_dict["pre_game_2"])
                self.music_manager.queue(self.music_manager.music_dict["pre_game_3"])
                try:
                    self.music_manager.next_source()
                except Exception as e:
                    print(utils.Utils.console_prefix("warning") + str(e))
                self.music_manager.loop = False
                context_button_sprite = utils.Utils.animated_sprite_load({"game/assets/textures/ui/context_screen.png":None, "game/assets/textures/ui/context_screen.png":None})
                self.context_button = Button(self, (0,0), (1280,720), context_button_sprite)

                self.has_looped = False
                self.game_state = "PreGame1"

            case 2:
                instructions_button_sprite = utils.Utils.animated_sprite_load({"game/assets/textures/ui/instruction_screen.png":None, "game/assets/textures/ui/instruction_screen.png":None})
                self.instruction_button = Button(self, (0,0), (1280,720), instructions_button_sprite)

                self.game_state = "PreGame2"

            case 3:
                self.music_manager.loop = False
                self.pre_game_quote1 = PlainImage(self, "game/assets/textures/ui/pre_game_quote1.png", (0,0), 0, 2)
                self.pre_game_quote1.sprite.opacity = 0

                self.pre_game_quote2 = PlainImage(self, "game/assets/textures/ui/pre_game_quote2.png", (0,0), 0, 2)
                self.pre_game_quote2.sprite.opacity = 0

                self.opacity = 0
                self.fade_out = False
                self.quote_sentence = 1

                self.game_state = "PreGame3"
        
    def pre_game1(self):
        if self.music_manager.source == self.music_manager.music_dict["pre_game_2"] and self.has_looped != True:
            self.music_manager.loop = True
            self.has_looped = True

        if self.context_button.is_clicked((self.parent.rendering_engine._mouse_x, self.parent.rendering_engine._mouse_y)):

            self.instanciate_pre_game(2)


    def pre_game2(self):
        if self.music_manager.source == self.music_manager.music_dict["pre_game_2"] and self.has_looped != True:
            self.music_manager.loop = True
            self.has_looped = True

        self.context_button = None
        if self.instruction_button.is_clicked((self.parent.rendering_engine._mouse_x, self.parent.rendering_engine._mouse_y)):

            self.instanciate_pre_game(3)

    def pre_game3(self):
        image_opacity_label = pyglet.text.Label("Opacity : "+str(self.opacity),
                          font_size=18,
                          x=10, y=560)
        self.parent.rendering_engine.debug_render_queue.enqueue(image_opacity_label)

        if self.music_manager.source == self.music_manager.music_dict["pre_game_1"]:
            self.music_manager.next_source()
            self.music_manager.next_source()
        
        self.instruction_button = None
        # self.music_manager.next_source()
        # self.instanciate_game()

        
        '''
        __        ___    ____  _   _ ___ _   _  ____ 
        \ \      / / \  |  _ \| \ | |_ _| \ | |/ ___|
         \ \ /\ / / _ \ | |_) |  \| || ||  \| | |  _ 
          \ V  V / ___ \|  _ <| |\  || || |\  | |_| |
           \_/\_/_/   \_\_| \_\_| \_|___|_| \_|\____|
        Remember to un-comment the following lines for release, this is disabled only for developement purposes.
        '''


        if self.music_manager.source == self.music_manager.music_dict["pre_game_2"]:
            return None

        if self.opacity < 255 and self.fade_out == False:
            self.opacity += 1
        
        if self.opacity == 255:
            self.fade_out = True

        if self.opacity > 0 and self.fade_out == True:
            self.opacity -= 2
        
        if self.quote_sentence > 2 and self.music_manager.source == None or self.can_skip == True:
            self.instanciate_game()

        if self.opacity <= 0 and self.fade_out == True:
            self.quote_sentence += 1
            self.fade_out = False
            self.opacity = 0



        if self.quote_sentence == 1:
            self.pre_game_quote1.sprite.opacity = self.opacity
        elif self.quote_sentence == 2:
            self.pre_game_quote2.sprite.opacity = self.opacity
        
        

    def instanciate_game(self):

        # Clear main menu elements
        self.tite_image = None
        self.play_button = None
        self.background_image = None

        # Instanciate game elements
        self.empty_music_queue()
        self.music_manager.queue(self.music_manager.music_dict["extraction_action"])
        self.music_manager.play()
        self.music_manager.loop = True

        self.environment = Environment(self,"game/assets/textures/environment/blueprint-background_HD.png", 0)
        self.environment.fixed = True

        self.player.show()
        self.player.hitbox = Hitbox(self.player, "rectangle", (100,100))
        self.player.hitbox.render = True
        self.player.world_coords = [350,150]

        self.debug_object = Enemy(self, "NCPD")
        self.debug_object.hitbox = Hitbox(self.debug_object, "triangle", (150,20))
        self.debug_object.hitbox.render = True
        self.debug_object.world_coords = [-350,-150]

        self.debug_object = Enemy(self, "NCPD")
        self.debug_object.hitbox = Hitbox(self.debug_object, "rectangle", (100,150))
        self.debug_object.hitbox.render = True
        self.debug_object.world_coords = [260,-190]

        # DEBUG STUFF
        self.skip_to_end_button_sprite = utils.Utils.animated_sprite_load({"game/assets/textures/ui/play_button_1.png":None,"game/assets/textures/ui/play_button_2.png":None})
        self.skip_to_end_button = Button(self,(420, -260), (155,75),self.skip_to_end_button_sprite)
        # self.loading_screen = None
        self.game_state = "Game"

    def game(self):
        self.update_objects_positions()
        self.update_camera_position()
        self.player.render_values()
        self.player.face_mouse()
        self.enemy_think()

        if self.skip_to_end_button.is_clicked((self.parent.rendering_engine._mouse_x, self.parent.rendering_engine._mouse_y)):
            self.instanciate_post_game(1)



    def debug_instanciate_post_game(self):
        self.instanciate_post_game(1)

    def instanciate_post_game(self, phase):
        print("POSTGAME")



        match phase:
            case 1:
                # DEBUG STUFF
                self.skip_to_end_button.sprite.batch = None
                del self.skip_to_end_button


                self.player.hide()
                while len(self.objects_list) > 1:
                    if self.objects_list[-1] != self.player:
                        self.objects_list[-1].suicide()

                self.music_manager.queue(self.music_manager.music_dict["post_game"])
                self.music_manager.loop = False
                self.music_manager.next_source()

                self.post_game_quote1 = PlainImage(self,"game/assets/textures/ui/post_game_quote_1.png", (0,0), 0, 2)
                self.post_game_quote1.sprite.opacity = 0

                self.post_game_quote2 = PlainImage(self,"game/assets/textures/ui/post_game_quote_2.png", (0,0), 0, 2)
                self.post_game_quote2.sprite.opacity = 0


                self.opacity = 0
                self.fade_out = False
                self.quote_sentence = 1

                self.game_state = "PostGame1"
            
            case 2:
                main_menu_button_sprite = utils.Utils.animated_sprite_load({"game/assets/textures/ui/main_menu_button.png":None})
                self.main_menu_button = Button(self,(0,0), (1280,720), main_menu_button_sprite)

                self.game_state = "PostGame2"

    
    def post_game1(self):

        if self.opacity < 255 and self.fade_out == False:
            self.opacity += 1
        
        if self.opacity == 255:
            self.fade_out = True

        if self.opacity > 0 and self.fade_out == True and self.quote_sentence == 1:
            self.opacity -= 1
        
        if self.quote_sentence == 2 and self.opacity == 255 or self.can_skip == True:
            self.instanciate_post_game(2)

        if self.opacity <= 0 and self.fade_out == True:
            self.quote_sentence += 1
            self.fade_out = False
            self.opacity = 0
        
        if self.quote_sentence == 1:
            self.post_game_quote1.sprite.opacity = self.opacity
        elif self.quote_sentence == 2:
            self.post_game_quote2.sprite.opacity = self.opacity

    def post_game2(self):
        if self.main_menu_button.is_clicked((self.parent.rendering_engine._mouse_x, self.parent.rendering_engine._mouse_y)):
            self.post_game_quote2 = None
            self.can_skip = True
            self.instanciate_main_menu()





    def instanciate_enemy(self):
        self.debug_object3 = Enemy(self, "NCPD")
        self.debug_object3.hitbox = Hitbox(self.debug_object3, "triangle", (170,20))
        self.debug_object3.hitbox.render = False
        self.debug_object3.world_coords = [-50,140]

    def add_to_enemy_list(self, object):
        '''
        object must be Enemy tyme
        '''
        self.enemy_list.append(object)

    def enemy_think(self):
        for object in self.enemy_list:
            object.think()



    
    def add_to_batch(self, object, group:int):
        '''
        object must be WorldObject | PlainImage | Button type
        ''' 
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
            case 4:
                return self.parent.rendering_engine.batch_layer_loadingscreen
            case _:
                return None

    def add_to_object_list(self, object):
        self.objects_list.append(object)
    
    def terminate(self,object):
        if object in self.objects_list:
            self.objects_list.remove(object)
        if hasattr(self, 'debug_object') and self.debug_object is object:
            self.debug_object.sprite.batch = None
            self.debug_object = None
        if hasattr(self, 'environment') and self.environment is object:
            self.environment.sprite.batch = None
            self.debug_object = None
        gc.collect()


    def update_objects_positions(self):
        '''
        object must be WorldObject type
        '''
        for object in self.objects_list:
            object.apply_physics()
            object.update_sprite_position()
    
    def update_camera_position(self):
        # Change this to change the camera focus
        self.camera.set_pos(self.player.world_coords)

class PlainImage:
    def __init__(self, parent:World, sprite_path:str, position:tuple, orientation, layer):
        self.parent = parent
        self.sprite = utils.Utils.sprite_load(sprite_path)
        self.pos = position
        self.orientation = orientation
        self.parent.add_to_batch(self,layer)

        self.uptade_sprite()
    
    def set_position(self,coords:tuple):
        self.pos = coords

    def set_orientation(self,orientation):
        self.orientation = orientation
    
    def uptade_sprite(self):
        self.sprite.x = self.pos[0] + self.parent.parent.rendering_engine.window_center[0]
        self.sprite.y = self.pos[1] + self.parent.parent.rendering_engine.window_center[1]
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
        self.click_phase = 0

        self.parent.add_to_batch(self,2)
        self.uptade_sprite()


    def uptade_sprite(self):
        self.sprite.x = self.pos[0] + self.parent.parent.rendering_engine.window_center[0]
        self.sprite.y = self.pos[1] + self.parent.parent.rendering_engine.window_center[1]

    def is_hovered(self, mouse_pos:tuple)->bool:
        mousex, mousey = mouse_pos
        width, height = self.dimentions
        self.sprite.frame_index = 0

        if mousex < self.pos[0] + self.parent.parent.rendering_engine.window_center[0] - width//2:
            return False
        if mousex > self.pos[0] + self.parent.parent.rendering_engine.window_center[0] + width//2:
            return False

        if mousey < self.pos[1] + self.parent.parent.rendering_engine.window_center[1] - height//2:
            return False
        if mousey > self.pos[1] + self.parent.parent.rendering_engine.window_center[1] + height//2:
            return False
        
        self.sprite.frame_index = 1
        return True
        
    
    def is_clicked(self, mouse_pos:tuple)->bool:
        mouse_state_label = pyglet.text.Label("Click phase : "+str(self.click_phase),
                          font_size=18,
                          x=10, y=560)
        self.parent.parent.rendering_engine.debug_render_queue.enqueue(mouse_state_label)
        if not self.is_hovered(mouse_pos):
            self.click_phase = 0

        if self.click_phase == 1:
            if self.is_hovered(mouse_pos):
                if self.parent.parent.input_manager.mouse_inputs_state["LMB"] == False :
                    self.click_phase = 2
        if self.click_phase == 0:
            if self.is_hovered(mouse_pos):
                if self.parent.parent.input_manager.mouse_inputs_state["LMB"] == True :
                    self.click_phase = 1
    
        if self.click_phase == 2:
            self.click_phase = 0
            print("CLICKED")
            return True
        return False
        

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
        self.parent.add_to_batch(self, group)
        # self.sprite.batch = parent.parent.rendering_engine.batch
        # self.sprite.group = self.get_correct_batch_group(group)
        self.add_to_world_object_list()
    

    def suicide(self):
        self.parent.terminate(self)

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

    def hide(self):
        self.sprite.visible = False

    def show(self):
        self.sprite.visible = True

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

class Enemy(WorldObject):
    def __init__(self, parent:World, preset:str):
        self.parent = parent
        allowed_presets = ("NCPD","MAXTAC")
        if not preset in allowed_presets:
            raise TypeError(f"{utils.Utils.console_prefix("error")} enemy preset : '{preset}' is not a valid preset")
        
        match preset:
            case "NCPD":
                texture = "game/assets/textures/entity/default_texture.png"
                self.brain_phase = 0
                self.brain_speed = 5
            case "MAXTAC":
                texture = "game/assets/textures/entity/default_texture.png"
                self.brain_phase = 0
                self.brain_speed = 2
        
        super().__init__(parent, texture, 2, False)
        self.parent.add_to_enemy_list(self)
    
    def think(self):
        if self.brain_phase == 0:
            pass
        
        if utils.Utils.distance(self.world_coords,self.parent.player.world_coords) < 350:
            self.face_player()
        self.brain_phase = (self.brain_phase + 1)%self.brain_speed
    
    def update_route(self):
        pass


    

    def face_player(self):
        self.orientation = utils.Utils.get_angle(self.world_coords,self.parent.player.world_coords)




class Environment(WorldObject): # UNIQUE OBJECT, DEFiNE THE BACKGROUND ENVIRONMENT
    def __init__(self, parent, texture:str, group:int):
        super().__init__(parent, texture, group, True)


class Camera:
    def __init__(self, parent):
        self.pos = [0,0]

    def set_pos(self,coords:list):
        self.pos = coords



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