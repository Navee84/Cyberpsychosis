import utils
import gc
from main import *


class World:
    def __init__(self,parent:Main):
        self.parent = parent
        self.music_manager = utils.MusicManager()
        self.sound_effects_manager = utils.SoundManager("game/assets/sounds/misc")
        self.objects_list = []
        self.enemy_list = []
        self.bullet_list = []
        self.game_object_list = utils.Queue()
        self.game_state = "MainMenu"
        self.button_click = False
        self.can_skip = False
        self.cahos = 0
        self.enemy_spawn_locations = (
            ((-925,1270), (-430,990)),
            ((-790,-1255), (-415,-1520)),
            ((-890,1345),(490,-1145))
        )

        # DEVELOPEMENT VALUES
        self.music_manager.volume = 0 # DEVELOPEMENT ONLY
        self.can_skip = True
        
        self.physics_engine = PhysicsEngine(self)
        self.camera = Camera(self)


        self.player = Player(self, "game/assets/textures/entity/player.png", 1)
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

        self.title_image = PlainImage(self, "game/assets/textures/title.png",(0,275),0, (self.parent.rendering_engine.width/1280,self.parent.rendering_engine.height/720),2)
        self.background_image = PlainImage(self, "game/assets/textures/menu_image.png", (0,0), 0, (self.parent.rendering_engine.width/1280,self.parent.rendering_engine.height/720), 0)
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
                self.pre_game_quote1 = PlainImage(self, "game/assets/textures/ui/pre_game_quote1.png", (0,0), 0, (self.parent.rendering_engine.width/1280,self.parent.rendering_engine.height/720), 2)
                self.pre_game_quote1.sprite.opacity = 0

                self.pre_game_quote2 = PlainImage(self, "game/assets/textures/ui/pre_game_quote2.png", (0,0), 0, (self.parent.rendering_engine.width/1280,self.parent.rendering_engine.height/720), 2)
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
        self.music_manager.next_source()
        self.instanciate_game()

        
        '''
        __        ___    ____  _   _ ___ _   _  ____ 
        \ \      / / \  |  _ \| \ | |_ _| \ | |/ ___|
         \ \ /\ / / _ \ | |_) |  \| || ||  \| | |  _ 
          \ V  V / ___ \|  _ <| |\  || || |\  | |_| |
           \_/\_/_/   \_\_| \_\_| \_|___|_| \_|\____|
        Remember to un-comment the following lines for release, this is disabled only for developement purposes.
        '''


        # if self.music_manager.source == self.music_manager.music_dict["pre_game_2"]:
        #     return None

        # if self.opacity < 255 and self.fade_out == False:
        #     self.opacity += 1
        
        # if self.opacity == 255:
        #     self.fade_out = True

        # if self.opacity > 0 and self.fade_out == True:
        #     self.opacity -= 2
        
        # if self.quote_sentence > 2 and self.music_manager.source == None or self.can_skip == True:
        #     self.instanciate_game()

        # if self.opacity <= 0 and self.fade_out == True:
        #     self.quote_sentence += 1
        #     self.fade_out = False
        #     self.opacity = 0



        # if self.quote_sentence == 1:
        #     self.pre_game_quote1.sprite.opacity = self.opacity
        # elif self.quote_sentence == 2:
        #     self.pre_game_quote2.sprite.opacity = self.opacity
        
        

    def instanciate_game(self):

        # Clear main menu elements
        self.title_image = None
        self.play_button = None
        self.background_image = None

        # Game values
        self.cahos = 0

        # Instanciate game elements
        self.empty_music_queue()
        self.music_manager.queue(self.music_manager.music_dict["extraction_action"])
        self.music_manager.play()
        self.music_manager.loop = True

        self.environment = Environment(self,"game/assets/textures/environment/map.png", 0)
        self.environment.fixed = True

        self.player.show()
        self.add_to_batch(self.player.inventory.slots[0],2)
        self.player.hitbox = Hitbox(self.player, "rectangle", (64,64))
        self.player.world_coords = [170,-1290]


        # DEBUG STUFF
        self.skip_to_end_button_sprite = utils.Utils.animated_sprite_load({"game/assets/textures/ui/play_button_1.png":None,"game/assets/textures/ui/play_button_2.png":None})
        self.skip_to_end_button = Button(self,(420, -260), (155,75),self.skip_to_end_button_sprite)
        # self.loading_screen = None

        self.sound_effects_manager.play_specific_sound("enter_game")
        self.game_state = "Game"

    def game(self):
        self.update_objects_positions()
        self.update_camera_position()

        self.player.render_values()

        self.enemy_think()

        self.player.face_mouse()
        self.player.think()
        for bullet in self.bullet_list:
            bullet.range_limiter()

        if self.cahos == 1:
            self.instanciate_enemy()
            self.sound_effects_manager.play_specific_sound("enemy_wave")
            self.cahos += 15
        
        elif len(self.enemy_list) == 0 and self.cahos > 10:
            self.sound_effects_manager.play_specific_sound("enemy_wave")
            for i in range(self.cahos//10):
                self.instanciate_enemy()
        self.cahos = min(self.cahos, 300)





        if self.skip_to_end_button.is_clicked((self.parent.rendering_engine._mouse_x, self.parent.rendering_engine._mouse_y)):
            self.instanciate_post_game(1)


    def instanciate_post_game(self, phase):
        print("POSTGAME")



        match phase:
            case 1:
                # DEBUG STUFF
                self.skip_to_end_button.sprite.batch = None
                del self.skip_to_end_button


                self.player.hide()
                self.player.inventory.slots[0].sprite.batch = None
                while len(self.objects_list) > 1:
                    if self.objects_list[-1] != self.player:
                        self.objects_list[-1].suicide()

                self.music_manager.queue(self.music_manager.music_dict["post_game"])
                self.music_manager.loop = False
                self.music_manager.next_source()

                self.post_game_quote1 = PlainImage(self,"game/assets/textures/ui/post_game_quote_1.png", (0,0), 0, (self.parent.rendering_engine.width/1280,self.parent.rendering_engine.height/720), 2)
                self.post_game_quote1.sprite.opacity = 0

                self.post_game_quote2 = PlainImage(self,"game/assets/textures/ui/post_game_quote_2.png", (0,0), 0, (self.parent.rendering_engine.width/1280,self.parent.rendering_engine.height/720), 2)
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



    # ENEMY

    def instanciate_enemy(self):
        self.enemy = Enemy(self, "NCPD")
        self.enemy.hitbox = Hitbox(self.enemy, "rectangle", (64,64))
        self.enemy.world_coords = self.get_enemy_spawn_location()
        self.cahos += 1

    def add_to_enemy_list(self, object):
        '''
        object must be Enemy type
        '''
        self.enemy_list.append(object)

    def enemy_think(self):
        for object in self.enemy_list:
            object.think()

    # BULLETS

    def instanciate_bullet(self, firing_position:tuple, direction:float, speed:float, damage:int, shooting_range:int, dispersion:float):
        self.bullet_object = Bullet(self, firing_position, direction, speed, damage, shooting_range, dispersion)
        self.cahos += 1
    
    def add_bullet_to_list(self, object):
        '''
        Object must be Bullet type
        '''
        self.bullet_list.append(object)


    
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
    
    def get_enemy_spawn_location(self) -> list:
        area = self.enemy_spawn_locations[randint(0,len(self.enemy_spawn_locations)-1)]

        location_x = randint(min(area[0][0],area[1][0]),max(area[0][0],area[1][0]))
        location_y = randint(min(area[0][1],area[1][1]),max(area[0][1],area[1][1]))

        return [location_x,location_y]

    def add_to_object_list(self, object):
        self.objects_list.append(object)
    
    def terminate(self,object):
        if object in self.objects_list:
            self.objects_list.remove(object)
        
        if object in self.bullet_list:
            self.bullet_list.remove(object)

        if object in self.enemy_list:
            self.enemy_list.remove(object)

        if hasattr(self, 'enemy') and self.enemy is object:
            self.enemy.sprite.batch = None
            self.enemy = None

        if hasattr(self, 'environment') and self.environment is object:
            self.environment.sprite.batch = None
            self.environment = None

        if hasattr(self, 'bullet_object') and object.sprite.batch != None:
            object.sprite.batch = None
            object = None
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
        # self.camera.set_pos((0,0))

class PlainImage:
    def __init__(self, parent:World, sprite_path:str, position:tuple, orientation, size:tuple, layer):
        self.parent = parent
        self.sprite = utils.Utils.sprite_load(sprite_path)
        self.pos = position
        self.size = size
        self.orientation = orientation


        self.uptade_sprite()
        self.parent.add_to_batch(self,layer)
    
    def set_position(self,coords:tuple):
        self.pos = coords

    def set_orientation(self,orientation):
        self.orientation = orientation
    
    def uptade_sprite(self):
        self.sprite.scale_x, self.sprite.scale_y = (self.size)
        self.sprite.x = (self.pos[0] + self.parent.parent.rendering_engine.window_center[0])# *self.size[0]
        self.sprite.y = (self.pos[1] + self.parent.parent.rendering_engine.window_center[1])# *self.size[1]
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
            self.parent.sound_effects_manager.play_specific_sound("button_click")
            return True
        return False
        

class WorldObject:
    def __init__(self, parent:World, texture:str, group:int, fixation:bool):

        self.parent = parent
        self.fixed = fixation

        # Defining all default values for a WorldObject
        self.sprite = utils.Utils.sprite_load(texture)
        self.orientation = 0 # 0 means facing right
        self.fov = 1.3 # Game fov = 1.5
        self.hitbox = None

        # Movement values
        self.acceleration = 0
        self.max_speed = 0
        self.friction = 0.45 # Keep this value between 0 and 1 : 1 is no friction and 0 is maximum friction 

        # Collisions related settings
        self.transparent = False


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
        if type(self) == Environment:
            for hitbox in self.hitbox_list:
                hitbox.update()

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
        self.health = 100

    def move_up(self):
        self.speed[1] = round(min(self.max_speed,self.speed[1]+self.acceleration),2)

    def move_down(self):
        self.speed[1] = round(max(-self.max_speed,self.speed[1]-self.acceleration),2)

    def move_left(self):
        self.speed[0] = round(max(-self.max_speed,self.speed[0]-self.acceleration),2)

    def move_right(self):
        self.speed[0] = round(min(self.max_speed,self.speed[0]+self.acceleration),2)



class Player(WorldObject,Entity):
    def __init__(self, parent, texture:str, group:int):
        WorldObject.__init__(self, parent, texture, group, False)
        Entity.__init__(self)

        # movement values:
        self.acceleration = 5 #set 2 for the game
        self.max_speed = 26 # set 6 for the game

        # Inventory values:
        self.inventory = Inventory(self)

        # Cooldown values:
        self.dash_cooldown = 0

    def think(self):
        if self.parent.parent.input_manager.mouse_inputs_state["LMB"] == True:
            self.inventory.slots[self.inventory.active_slot].fire()
        for weapon in self.inventory.slots:
            if type(weapon) == Copperhead:
                weapon.tick()
        
        self.dash_cooldown -= 1
    

    def face_mouse(self):
        angle = utils.Utils.get_angle(self.get_screen_pos(),(self.parent.parent.rendering_engine._mouse_x,self.parent.parent.rendering_engine._mouse_y))
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
    
    def dash(self):
        if self.dash_cooldown <= 0:
            print("DASH")

            self.dash_cooldown = 45

class Enemy(WorldObject, Entity):
    def __init__(self, parent:World, preset:str):
        Entity.__init__(self)
        self.parent = parent

        allowed_presets = ("NCPD","MAXTAC")
        if not preset in allowed_presets:
            raise TypeError(f"{utils.Utils.console_prefix("error")} enemy preset : '{preset}' is not a valid preset")
        
        match preset:
            case "NCPD":
                texture = "game/assets/textures/entity/ncpd.png"
                self.brain_phase = 0
                self.brain_speed = 10
            case "MAXTAC":
                texture = "game/assets/textures/entity/default_texture.png"
                self.brain_phase = 0
                self.brain_speed = 2
        
        WorldObject.__init__(self, parent, texture, 2, False)

        # movement values:
        self.acceleration = 3
        self.max_speed = 10

        self.death_sound_player = utils.SoundManager("game/assets/sounds/enemy_death")


        self.distance_to_player = utils.Utils.distance(self.world_coords,self.parent.player.world_coords)

        self.inventory = Inventory(self)

        self.brain_activation_number = randint(0,self.brain_speed)

        self.parent.add_to_enemy_list(self)

        # DEBUG
        self.braindead = True
    
    def think(self):
        '''
        Cette fonction gère l'ia des ennemis et les actionnent
        '''
        if self.health <= 0:
            self.die()

        if self.braindead:
            return None
        
        for weapon in self.inventory.slots:
            if type(weapon) == Copperhead:
                weapon.tick()


        if self.brain_phase == self.brain_activation_number:
            self.face_player()
            if self.inventory.slots[self.inventory.active_slot].active_magazine <= 0:
                self.inventory.slots[self.inventory.active_slot].reload()

            self.distance_to_player = utils.Utils.distance(self.world_coords,self.parent.player.world_coords)
            if self.distance_to_player < (self.inventory.slots[self.inventory.active_slot].shooting_range / 1.5) - 20:
                self.shoot()
            
        if self.distance_to_player >= (self.inventory.slots[self.inventory.active_slot].shooting_range / 1.5) - 25 :
            self.update_route("follow")

        if self.distance_to_player <= (self.inventory.slots[self.inventory.active_slot].shooting_range / 2.5) or self.inventory.slots[self.inventory.active_slot].active_magazine <= 0:
            self.update_route("flee")
        
        self.brain_phase = (self.brain_phase + 1)%self.brain_speed
    
    def update_route(self,state:str):
        '''
        Utilise la trigonométrie pour déterminer dans quelle direction aller
        Si cos() > 1/2 alors l'ennemi avance vers la droite
        Si sin() > 1/2 alors l'ennemi vas vers le haut
        et inversement
        '''
        angle_to_player = utils.Utils.get_angle(self.world_coords,self.parent.player.world_coords)
        vertical_angle = utils.sin(angle_to_player)
        horizontal_angle = utils.cos(angle_to_player)
        if vertical_angle > 1/2:
            if state == "follow":
                self.move_up()
            else:
                self.move_down()
        elif vertical_angle < -1/2:
            if state == "follow":
                self.move_down()
            else:
                self.move_up()

        if horizontal_angle > 1/2:
            if state == "follow":
                self.move_right()
            else:
                self.move_left()
        elif horizontal_angle < -1/2:
            if state == "follow":
                self.move_left()
            else:
                self.move_right()

    def face_player(self):
        self.orientation = utils.Utils.get_angle(self.world_coords,self.parent.player.world_coords)

    def shoot(self):
        self.inventory.slots[self.inventory.active_slot].fire()
    
    def die(self):
        self.death_sound_player.play_sound()
        print("NEW CAHOS :", self.parent.cahos)
        self.suicide()



class Environment(WorldObject): # UNIQUE OBJECT, DEFiNE THE BACKGROUND ENVIRONMENT
    def __init__(self, parent, texture:str, group:int):
        super().__init__(parent, texture, group, True)
        self.hitbox_list = []

        self.hitbox_values=[
            ("rectangle", (-978,285),(-1400,1500), 0, "auto"), # top left corner [DONE]
            ("rectangle", (-830,-190),(-1400,-1800), 0, "auto"), # bottom left corner [DONE]
            ("rectangle", (8,1600),(357,778), 0, "auto"), # top right corner [DONE]
            ("rectangle", (-388,1045),(-135,340), 0, "auto"), # middle top seethrough [DONE]
            ("triangle", (175,18), (-320,320), 0, "manual"), # middle top seethrough [DONE]
            ("rectangle", (260,25), (-260,298), -68, "manual"), # middle top seethrough [DONE]

            # NCPD BARRICADES
            ("rectangle", (-1025,290),(-1155,-185), 0, "auto"), # top left barricade [DONE]
            ("rectangle", (440,87), (172, 377), 46, "manual"), #top right barricade
            ("rectangle", (-978,1330),(8,1600), 0, "auto") # top middle barricade [DONE]
        ]
        # game.world.environment.hitbox_list[7].dimensions
        for elem in self.hitbox_values:
            if elem[4] == "auto":
                self.hitbox_list.append(Hitbox(self,elem[0], utils.Utils.get_dimensions(elem[1],elem[2]), utils.Utils.get_rectangle_center(elem[1],elem[2]),elem[3]))
            else:
                self.hitbox_list.append(Hitbox(self, elem[0], elem[1], elem[2], utils.radians(elem[3])))

class Camera:
    def __init__(self, parent):
        self.pos = [0,0]

    def set_pos(self,coords:list):
        self.pos = coords



class Hitbox:
    def __init__(self, parent:WorldObject, preset:str, dimensions:tuple, *args):
        self.parent = parent
        self.default_origin = False

        if not args:
            self.default_origin = True
        else:
            self.origin = args[0]
            self.orientation = args[1]
            print(self.origin)

        # Vérifie que le preset entré en argument est dans la liste des presets disponibles
        allowed_presets = ("rectangle","triangle","circle","hexagon")
        if not preset in allowed_presets:
            raise TypeError(f"{utils.Utils.console_prefix("error")} preset '{preset}' is not a valid preset")
        
        self.dimensions = dimensions
        self.preset = preset
        self.render = True
        self.is_colliding = False

        self.size = 1
        self.hitbox_coordinates = None # Coordinates always go from top left in clockwise order
        
        # once everything is setup, updates the hitbox coordinates a first time
        self.update()

    def update(self):
        '''
        Updates hitbox coordinates
        '''
        if self.default_origin:
            self.origin = self.parent.world_coords
            self.orientation = self.parent.orientation
            
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
        '''
        Returns rectangle shaped coordinates for the hitbox
        '''
        top_left = (self.origin[0] - width//2 , self.origin[1] + height//2)
        top_right = (self.origin[0] + width//2, self.origin[1] + height//2)

        bottom_left = (self.origin[0] - width//2 , self.origin[1] - height//2)
        bottom_right = (self.origin[0] + width//2, self.origin[1] - height//2)

        point_list = [top_left, top_right,bottom_right, bottom_left]

        rotated_list = []
        for point in point_list:
            rotated_list.append(utils.Utils.apply_rotation(self.origin,point,self.orientation))

        return rotated_list
    
    def preset_triangle(self, width, down_offset):
        '''
        Returns triangle shaped coordinates for the hitbox
        '''
        top = (self.origin[0], self.origin[1] + int((2/3)*((3**0.5)*(width//2))) - down_offset)

        bottom_middle = (self.origin[0],self.origin[1] - int((1/3)*((3**0.5)*(width//2))) - down_offset)
        bottom_left = (bottom_middle[0] - width//2, bottom_middle[1])
        bottom_right = (bottom_middle[0] + width//2, bottom_middle[1])

        point_list = [top,bottom_right, bottom_left]

        rotated_list = []
        for point in point_list:
            rotated_list.append(utils.Utils.apply_rotation(self.origin,point,self.orientation- (utils.radians(90))))

        return rotated_list

    def preset_circle(self):
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
        
        # Environment will never go through the physics engin as active
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
            if type(object) == Environment:
                for hitbox in object.hitbox_list:
                    if max(hitbox.dimensions[0], hitbox.dimensions[1])*1.5 > utils.Utils.distance(active_object.world_coords,hitbox.origin):
                        candidate_queue.enqueue(hitbox)

            elif object.hitbox != None:
                if object != active_object:
                    if max(object.hitbox.dimensions[0], object.hitbox.dimensions[1])*1.5 > utils.Utils.distance(active_object.world_coords,object.world_coords):
                        candidate_queue.enqueue(object.hitbox)

        while not candidate_queue.is_empty():
            tested_hitbox = candidate_queue.dequeue()

            collision_result = (False,None)
            if type(tested_hitbox.parent) != Bullet: # Avoid useless calculations between bullets
                collision_result = self.is_colliding(active_object.hitbox,tested_hitbox)

        # RESOLVING COLLISION
            if collision_result[0]:
                if active_object.transparent == False or tested_hitbox.parent.transparent == False:


                    active_object.hitbox.is_colliding = True
                    tested_hitbox.is_colliding = True
                    if active_object.fixed == True:
                        return None
        
                    if type(active_object) == Bullet:
                        if type(tested_hitbox.parent) != Environment:
                            tested_hitbox.parent.health -= active_object.damage
                        active_object.suicide()
                        return None
                    else:
                        active_object.world_coords = (utils.Utils.translate(active_object.world_coords, collision_result[1]))


                else:
                    active_object.hitbox.is_colliding = False
                    tested_hitbox.is_colliding = False
        




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

                vector_a_b = utils.Utils.get_vector(hitbox1.origin, hitbox2.origin)
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
        '''
        self explanatory, math stuff
        '''
        # simple formule de vecteur normal
        return (-1*(point_b[1]-point_a[1]), point_b[0]-point_a[0])
        
    
    def get_scalar_coefficient(self, vector:tuple, point:tuple):
        '''
        self explanatory, math stuff
        '''
        k = (vector[0]*point[0] + vector[1]*point[1]) / (vector[0]**2 + vector[1]**2)
        rounded = round(k,3)
        return rounded
    

from weapon_system import *
