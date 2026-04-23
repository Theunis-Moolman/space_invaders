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
        # Inherits functions from Enemy
        # Level specifies the power up type
        super().__init__(x, y, level, radius)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image = None

        # Different imagegs for each type of power up
        if self.level == 1:
            self.image = Picture("assets/images/Shield.png")
        elif self.level == 2:
            self.image = Picture("assets/images/Star.png")
        elif self.level == 3:
            self.image = Picture("assets/images/Heart.png")

    def is_hit_by_projectile(self, projectile: Projectile):
        # Inherits is hit by projectile from enemy
        return super().is_hit_by_projectile(projectile)

    def draw(self):
        # Draw the picture of the power up
        stddraw.picture(self.image, self.x, self.y)

    def update(self):
        # Update position of the image
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
        # Handles timer for cooldown
        self.last_power_up = time.time()

        # List of all power up objects
        self.power_ups: list[PowerUp] = []

        # Cooldown setting
        self.cooldown = 20

    def update(self):
        # Check if cooldown condition is met
        if time.time() - self.last_power_up > self.cooldown:
            # Randomly spawn the power up in a position
            x = random.random()
            y = random.random() * 0.4 + 0.5
            # Gives a random speed to the power up
            dx = random.random() * 0.001 + 0.001
            dy = random.random() * dx

            # Creates a power up object
            power_up = PowerUp(x, y, 0.02, random.randint(1, 3), dx, dy)

            # Add the power up object to the list
            self.power_ups.append(power_up)

            # Update cooldown manager
            self.last_power_up = time.time()
        for power_up in self.power_ups:
            # Update all power up positions
            power_up.update()

    def draw(self):
        for power_up in self.power_ups:
            # Draw all power ups
            power_up.draw()

    def check_hit(self, projectile: Projectile):
        for power_up in self.power_ups:
            # Check if the power up is hit and return the power up type
            if power_up.is_hit_by_projectile(projectile):
                self.power_ups.remove(power_up)
                return power_up.level

        return -1
