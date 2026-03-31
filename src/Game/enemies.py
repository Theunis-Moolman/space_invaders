import math
import stddraw
from Music.music import Music

class Enemy:
    def __init__(self, x, y, colour, radius):
        self.enemy_x = x
        self.enemy_y = y
        self.colour = colour
        self.radius = radius
        self.music = Music()

    def is_enemy_hit_by_laser(self, laser_origin, laser_direction):
        #Laser start + direction
        lx, ly = laser_origin
        dx, dy = laser_direction

        #playsound("Explode")

        #Distance from line formula
        numerator = abs((self.enemy_y - ly) * dx - (self.enemy_y - lx) * dy)
        denominator = math.hypot(dx, dy)
        distance = numerator / denominator
        return distance <= self.radius #Hit if close enough


class Enemies:
    def __init__(self, rows, cols):
        self.enemies = []
        self.enemy_spacing = 15
        self.enemy_rows = rows # 2
        self.enemy_cols = cols # 5

    def create_enemies(self, level):
        enemy_x = 15
        enemy_y = 90

        #Create grid
        for row in range(self.enemy_rows):
            for col in range(self.enemy_cols):
                x_pos = enemy_x + col * self.enemy_spacing
                y_pos = enemy_y - row * self.enemy_spacing

                #Level-based coloring
                colour = stddraw.BLUE if level == 1 else stddraw.RED if row == 1 else stddraw.BLUE

                new_enemy = Enemy(x_pos, y_pos, colour)

                self.enemies.append(new_enemy)

    def enemy_update(self, enemy_dir, enemy_speed):
        should_descend = False

        for enemy in self.enemies:
            next_x = enemy.enemy_x + enemy_dir * enemy_speed
            #Check wall collision
            if next_x + enemy.radius > 100 or next_x - enemy.radius < 0:
                should_descend = True
                break

        for enemy in self.enemies:
            #Move enemies
            if should_descend:
                enemy.enemy_y -= 5
            else:
                enemy.enemy_x += enemy_dir * enemy_speed

        #Reverse direction
        if should_descend:
            enemy_dir *= -1

        return enemy_dir
