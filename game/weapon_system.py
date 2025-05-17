import utils
import world
from random import randint


class Inventory:
    def __init__(self, parent:world.Player | world.Enemy):
        self.parent = parent
        self.slots = [None]*4
        self.slots[0] = Copperhead(self, 30, 25, 8, 20, 4, 700)
        self.active_slot = 0



class Weapon:
    '''
    Base class for all weapons
    '''
    def __init__(self, parent:Inventory, magazine_capacity:int, magazines_number:int, fire_rate:int, damage:int, dispersion:int, shooting_range:int):
        self.parent = parent

        # Sprite caracteristics
        if type(self.parent.parent) == world.Enemy:
            self.sprite = utils.Utils.sprite_load("game/assets/textures/weapons/Copperhead_enemy.png")
        else:
            self.sprite = utils.Utils.sprite_load("game/assets/textures/weapons/Copperhead_player.png")

        self.parent.parent.parent.add_to_batch(self,2)
        self.fire_sound_player = utils.SoundManager("game/assets/sounds/weapons/shoot")
        self.dry_fire_sound_player = utils.SoundManager("game/assets/sounds/weapons/dry fire")
        self.reload_sound_player = utils.SoundManager("game/assets/sounds/weapons/reload")

        # weapon specific caracteristics
        self.mag_capacity = magazine_capacity
        self.magazines = utils.Queue()
        for i in range(magazines_number):
            self.magazines.enqueue(self.mag_capacity)

        self.fire_rate = fire_rate
        self.damage = damage
        self.active_magazine = self.magazines.dequeue()
        self.dispersion = dispersion
        self.shooting_range = shooting_range

        # Cooldown values
        self.reload_input_cooldown = 0
        self.firing_cooldown = 0
        self.reloading_time = 0
        self.reloading = False


    def tick(self) -> None:
        '''
        Executed each frame for the player, allows the weapons to function correctly
        '''
        self.reload_input_cooldown -= 1
        self.firing_cooldown -= 1
        self.reloading_time -= 1

        if self.reloading == True and self.reloading_time <= 0:
            self.active_magazine = self.magazines.dequeue()
            self.reloading = False
            print("RELOADED")
        
        self.update_sprite()


    def reload(self) -> None:
        '''
        Self explanatory
        '''
        if not self.magazines.is_empty():
            if self.reload_input_cooldown <= 0 :
                self.reloading = True
                self.reloading_time = 110
                self.reload_input_cooldown = 150
                self.active_magazine = 0
                self.reload_sound_player.play_sound()
                print("RELOADING")
            else:
                print("ON COOLDOWN")
        else:
            print("NOT ENOUGH MAGAZINES")
    

    def fire(self) -> None:
        '''
        Self explanatory
        Instanciate a Bullet object in the world
        '''
        if self.active_magazine <= 0 and self.firing_cooldown <= 0 and self.reloading == False:
            self.dry_fire_sound_player.play_sound()
            self.firing_cooldown = round(90*(1/self.fire_rate))

        if self.active_magazine > 0 and self.firing_cooldown <= 0:
            self.parent.parent.parent.instanciate_bullet(utils.Utils.apply_rotation(self.parent.parent.world_coords,(self.parent.parent.world_coords[0] + (40* self.parent.parent.fov),self.parent.parent.world_coords[1] - (20 * self.parent.parent.fov)),self.parent.parent.orientation), -utils.radians(self.sprite.rotation), 25, self.damage, self.shooting_range, utils.radians(randint(-self.dispersion,self.dispersion)))
            self.firing_cooldown = round(45*(1/self.fire_rate))
            self.active_magazine -= 1
            self.fire_sound_player.play_sound()
    

    def update_sprite(self) -> None:
        self.sprite.scale = self.parent.parent.fov
        screen_pos = self.parent.parent.get_screen_pos()
        rotated_screen_pos = utils.Utils.apply_rotation(screen_pos,(screen_pos[0] + (40* self.parent.parent.fov),screen_pos[1] - (20 * self.parent.parent.fov)),self.parent.parent.orientation)
        self.sprite.x = rotated_screen_pos[0]
        self.sprite.y = rotated_screen_pos[1]
        
        if type(self.parent.parent) == world.Player:
            self.sprite.rotation = -utils.degrees(utils.Utils.get_angle(rotated_screen_pos, (self.parent.parent.parent.parent.rendering_engine._mouse_x,self.parent.parent.parent.parent.rendering_engine._mouse_y)))
        else:
            self.sprite.rotation = utils.degrees(-self.parent.parent.orientation)



class Bullet(world.WorldObject):
    def __init__(self, parent, firing_position:tuple, direction:float, speed:float, damage:int, shooting_range:int, dispersion:float):
        super().__init__(parent, "game/assets/textures/weapons/bullet.png", 1, False)
        self.firing_position = firing_position
        self.shooting_range = shooting_range

        # updating  worldobject values :
        self.orientation = direction
        direction_vector = utils.Utils.decompose_into_vector(10,self.orientation)
        self.world_coords = [firing_position[0]+direction_vector[0],firing_position[1]+direction_vector[1]]
        self.transparent = True

        self.orientation += dispersion

        self.acceleration = speed
        self.speed = utils.Utils.decompose_into_vector(speed,self.orientation)
        self.damage = damage
        self.range = range
        self.hitbox = world.Hitbox(self,"rectangle", (10,25))
        self.friction = 1

        # DEBUG SETTINGS
        # self.speed = [0,0]

        self.parent.add_bullet_to_list(self)
        

    def range_limiter(self) -> None:
        '''
        Prevent the bullet from flying indefinetly
        '''
        if utils.Utils.distance(self.firing_position,self.world_coords) > self.shooting_range:
            self.sprite.opacity -=40
            if self.sprite.opacity <= 0:
                self.suicide()



class Copperhead(Weapon):
    def __init__(self, parent:Inventory, magazine_capacity:int, magazines_number:int, fire_rate:int, damage:int, dispersion:int, range:int):
        super().__init__(parent, magazine_capacity, magazines_number, fire_rate, damage, dispersion, range)