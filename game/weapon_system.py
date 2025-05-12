import utils
import world

class Inventory:
    def __init__(self, parent:world.Player | world.Enemy):
        self.parent = parent
        self.slots = [None]*4
        self.slots[0] = Copperhead(self, 30, 25, 11, 20, 10, 20)


class Bullet(world.WorldObject):
    def __init__(self, parent, firing_position:tuple, direction:float, speed:float, damage:int, shooting_range:int):
        super().__init__(parent, "game/assets/textures/weapons/bullet.png", 1, False)
        self.firing_position = firing_position
        self.shooting_range = shooting_range

        # updating  worldobject values :

        self.orientation = direction  - utils.radians(90)
        direction_vector = utils.Utils.decompose_into_vector(30,utils.degrees(self.orientation))
        self.world_coords = [firing_position[0]+direction_vector[0],firing_position[1]+direction_vector[1]]

        self.acceleration = speed
        self.speed = utils.Utils.decompose_into_vector(speed,utils.degrees(self.orientation))
        self.damage = damage
        self.range = range
        self.hitbox = world.Hitbox(self,"rectangle", (20,20))
        self.hitbox.render = True
        self.friction = 1

        self.parent.add_bullet_to_list(self)
        
    def range_limiter(self):
        if utils.Utils.distance(self.firing_position,self.world_coords) > self.shooting_range:
            self.suicide()

class Weapon:
    def __init__(self, parent:Inventory, magazine_capacity:int, magazines_number:int, fire_rate:int, damage:int, dispersion:int, shooting_range:int):
        self.parent = parent
        self.mag_capacity = magazine_capacity
        self.magazines = utils.Queue()
        for i in range(magazines_number):
            self.magazines.enqueue(self.mag_capacity)

        self.fire_rate = fire_rate
        self.damage = damage
        self.active_magazine = self.magazines.dequeue()
        self.dispersion = dispersion
        self.shooting_range = shooting_range
    
    def reload(self):
        self.active_magazine = self.magazines.dequeue()
    
    def fire(self):
        if self.active_magazine > 0:
            self.parent.parent.parent.instanciate_bullet((self.parent.parent.world_coords, self.parent.parent.orientation, 20, 50, self.shooting_range))
            self.active_magazine -= 1


class Copperhead(Weapon):
    def __init__(self, parent:Inventory, magazine_capacity:int, magazines_number:int, fire_rate:int, damage:int, dispersion:int, range:int):
        super().__init__(parent, magazine_capacity, magazines_number, fire_rate, damage, dispersion, range)