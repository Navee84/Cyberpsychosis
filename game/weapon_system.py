import utils
import world
from random import randint

class Inventory:
    def __init__(self, parent:world.Player | world.Enemy):
        self.parent = parent
        self.slots = [None]*4
        self.slots[0] = Copperhead(self, 30, 25, 8, 20, 4, 1000)
        self.active_slot = 0

class Weapon:
    def __init__(self, parent:Inventory, magazine_capacity:int, magazines_number:int, fire_rate:int, damage:int, dispersion:int, shooting_range:int):
        self.parent = parent

        self.sound_player = utils.SoundManager("game/assets/sounds/weapons/shoot")

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
        self.reload_cooldown = 0
        self.firing_cooldown = 0


    def tick(self):
        self.reload_cooldown -= 1
        self.firing_cooldown -= 1

    def reload(self):
        if not self.magazines.is_empty():
            if self.reload_cooldown <= 0:
                self.active_magazine = self.magazines.dequeue()
                self.reload_cooldown = 90
                print("RELOAD")
            else:
                print("ON COOLDOWN")
        else:
            print("NOT ENOUGH MAGAZINES")
    
    def fire(self):
        if self.active_magazine > 0 and self.firing_cooldown <= 0:
            self.parent.parent.parent.instanciate_bullet(self.parent.parent.world_coords, self.parent.parent.orientation, 25, 50, self.shooting_range, utils.radians(randint(-self.dispersion,self.dispersion)))
            self.firing_cooldown = round(45*(1/self.fire_rate))
            self.active_magazine -= 1
            self.sound_player.play_sound(randint(0,len(self.sound_player.sound_list)-1))

class Bullet(world.WorldObject):
    def __init__(self, parent, firing_position:tuple, direction:float, speed:float, damage:int, shooting_range:int, dispersion:float):
        super().__init__(parent, "game/assets/textures/weapons/bullet.png", 1, False)
        self.firing_position = firing_position
        self.shooting_range = shooting_range

        # updating  worldobject values :

        self.orientation = direction
        direction_vector = utils.Utils.decompose_into_vector(50,self.orientation)
        self.world_coords = [firing_position[0]+direction_vector[0],firing_position[1]+direction_vector[1]]
        self.transparent = True

        self.orientation += dispersion

        self.acceleration = speed
        self.speed = utils.Utils.decompose_into_vector(speed,self.orientation)
        self.damage = damage
        self.range = range
        self.hitbox = world.Hitbox(self,"rectangle", (10,25))
        self.hitbox.render = True
        self.friction = 1

        # DEBUG SETTINGS
        # self.speed = [0,0]

        self.parent.add_bullet_to_list(self)
        
    def range_limiter(self):
        if utils.Utils.distance(self.firing_position,self.world_coords) > self.shooting_range:
            self.suicide()



class Copperhead(Weapon):
    def __init__(self, parent:Inventory, magazine_capacity:int, magazines_number:int, fire_rate:int, damage:int, dispersion:int, range:int):
        super().__init__(parent, magazine_capacity, magazines_number, fire_rate, damage, dispersion, range)