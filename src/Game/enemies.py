import math
import stddraw
import random
from Music.music import Music
from picture import Picture

class Enemy:
    def __init__(self, x, y, level, radius):
        self.enemy_x = x
        self.enemy_y = y
        self.level = level
        self.radius = radius
        self.music = Music()

    def is_enemy_hit_by_laser(self, laser_origin, laser_direction):
        # Laser start + direction
        lx, ly = laser_origin
        dx, dy = laser_direction
        px, py = self.enemy_x, self.enemy_y

        # Vector along the laser
        line_dx = dx - lx
        line_dy = dy - ly

        # Handle degenerate line (laser points are the same)
        if line_dx == 0 and line_dy == 0:
            distance = math.sqrt((px - lx) ** 2 + (py - ly) ** 2)
        else:
            # Distance from point to line formula
            numerator = abs(line_dy * px - line_dx * py + line_dx * ly - line_dy * lx)
            denominator = math.sqrt(line_dx ** 2 + line_dy ** 2)
            distance = numerator / denominator

        return distance <= self.radius  # Hit if close enough


class Enemies:
    def __init__(self):
        self.enemies = []
        self.enemy_radius = 0.05
        self.enemy_picture_1 = Picture("assets/images/TIE_1.png")
        self.enemy_picture_2 = Picture("assets/images/TIE_2.svg")

    def create_enemies(self, level, rows, cols):
        enemy_x = 0.1
        enemy_y = 0.90

        enemy_spacing = 1 / cols

        #Create grid
        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    x_pos = random.random() * 0.8 + 0.1
                else:
                    x_pos = enemy_x + col * enemy_spacing
                y_pos = enemy_y - row * enemy_spacing

                new_enemy = Enemy(x_pos, y_pos, level, self.enemy_radius)

                self.enemies.append(new_enemy)

    def enemy_update(self, enemy_dir, enemy_speed, descend_speed, should_descend):
        for enemy in self.enemies:
            next_x = enemy.enemy_x + enemy_dir * enemy_speed
            #Check wall collision
            if next_x + enemy.radius > 100 or next_x - enemy.radius < 0:
                should_descend = True
                break

        for enemy in self.enemies:
            #Move enemies
            if should_descend:
                enemy.enemy_y -= descend_speed
            else:
                enemy.enemy_x += enemy_dir * enemy_speed

        #Reverse direction
        if should_descend:
            enemy_dir *= -1

        return enemy_dir

    def check_death(self):
        for enemy in self.enemies:
            if enemy.enemy_y - enemy.radius <= 0.205:
                return True
        return False

    def shoot(self):
        if len(self.enemies) > 0:
            random_enemy = random.choice(self.enemies)
            stddraw.setPenColor(stddraw.RED)
            stddraw.line(random_enemy.enemy_x, random_enemy.enemy_y, random_enemy.enemy_x, 0)
            return random_enemy.enemy_x
        return -1

    def draw_enemies(self): #made for 0 to 1 scale
        for enemy in self.enemies:
            if enemy.level == 1:
                stddraw.picture(self.enemy_picture_1, enemy.enemy_x, enemy.enemy_y, 0.1, 0.07)
            elif enemy.level == 2:
                stddraw.picture(self.enemy_picture_2, enemy.enemy_x, enemy.enemy_y, 0.1, 0.07)

    def check_hit(self, laser_origin, laser_direction):
        for enemy in self.enemies:
            if enemy.is_enemy_hit_by_laser(laser_origin, laser_direction):
                self.enemies.remove(enemy)
                return True
        return False

