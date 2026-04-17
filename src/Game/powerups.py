import time
from picture import Picture
from src.Game.spaceship import Projectile
from src.Game.enemies import Enemy
import random
import stddraw


class PowerUp(Enemy):
    """
    Power up object that inherits from enemy to handle being hit by projectiles

    Args:
        x: x co-ordinate of the power up object
        y: y co-ordinate of the power up object
        radius: radius of the power up object
        level: Level specifies the power up object type:
            1: Shield
            2: Star
            3: Heart
        dx: change applied with each frame in the x-position
        dy: change applied with each frame in the y-position


    Author: Theunis and Sydwell
    """
    def __init__(self, x: float, y: float, radius, level: int, dx: float, dy: float):
        super().__init__(x, y, level, radius)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image = None

        if self.level == 1:
            self.image = Picture("assets/images/Shield.png")
        elif self.level == 2:
            self.image = Picture("assets/images/Star.png")
        elif self.level == 3:
            self.image = Picture("assets/images/Heart.png")

    def is_hit_by_projectile(self, projectile: Projectile):
        return super().is_hit_by_projectile(projectile)

    def draw(self):
        stddraw.picture(self.image, self.x, self.y)

    def update(self):
        self.x += self.dx
        self.y += self.dy

class PowerUpHandler:
    """
    Power up object handler that handles updating, drawing and checking if a power up is hit

    Args:
        None

    Author: Sydwell and Theunis
    """
    def __init__(self):
        self.last_power_up = time.time()
        self.power_ups: list[PowerUp] = []
        self.cooldown = 20
        self.picture = Picture

    def update(self):
        if time.time() - self.last_power_up > self.cooldown:
            x = random.random()
            y = random.random() * 0.4 + 0.5
            dx = random.random() * 0.001 + 0.001
            dy = random.random() * dx
            power_up = PowerUp(x, y, 0.02, random.randint(1, 3), dx, dy)
            self.power_ups.append(power_up)
            self.last_power_up = time.time()
        for power_up in self.power_ups:
            power_up.update()

    def draw(self):
        for power_up in self.power_ups:
            power_up.draw()

    def check_hit(self, projectile: Projectile):
        for power_up in self.power_ups:
            if power_up.is_hit_by_projectile(projectile):
                self.power_ups.remove(power_up)
                return power_up.level

        return -1
