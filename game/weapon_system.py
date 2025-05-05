import utils
from world import Hitbox, WorldObject

class Bullet(WorldObject):
    def __init__(self, firing_position:tuple, direction:float, speed:float, damage:int, range:int):
        super().__init__()
        self.position = firing_position
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.range = range


class Weapon:
    def __init__(self, magazine_capacity:int, magazines_number:int, fire_rate:int, damage:int, dispersion:int, range:int):
        self.mag_capacity = magazine_capacity
        self.magazines = utils.Queue()
        for i in range(magazines_number):
            self.magazines.enqueue(self.mag_capacity)

        self.fire_rate = fire_rate
        self.damage = damage
        self.active_magazine = self.magazines.dequeue()
        self.dispersion = dispersion
    
    def reload(self):
        self.active_magazine = self.magazines.dequeue()

class Copperhead:
    def __init__(self):
        super().__init__()