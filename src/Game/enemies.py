import math
import stddraw
import random
from Music.music import Music
from picture import Picture
import time
from src.Game.spaceship import Projectile

class Enemy:
    def __init__(self, x, y, level, radius):
        self.enemy_x = x
        self.enemy_y = y
        self.level = level
        self.radius = radius

    def is_enemy_hit_by_projectile(self, projectile: Projectile):
        for i in range(20):
            px = projectile.x - projectile.dx * (i/20)
            py = projectile.y - projectile.dy * (i/20)
            distance = math.sqrt((self.enemy_x - px) ** 2 + (self.enemy_y - py) ** 2)
            print(self.radius)
            if distance <= self.radius + 0.01:
                return True
        return False



class Enemies:
    def __init__(self):
        self.enemies = []
        self.enemy_radius = 0.02


    def create_enemies(self, level, rows, cols):
        enemy_x = 0.05
        enemy_y = 0.90

        enemy_spacing = 0.15

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
            if next_x + enemy.radius > 1 or next_x - enemy.radius < 0:
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
            return random_enemy
        return None

    #Sydwell made this
    def draw_enemies(self): #made for 0 to 1 scale
        i = int(time.time() % 1 < 0.5)
        for enemy in self.enemies:
            if enemy.level == 1:
                stddraw.setPenColor(stddraw.WHITE)
            elif enemy.level == 2:
                stddraw.setPenColor(stddraw.RED)

            alien_shape = [
                [0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 0, 1, 1, 0],
                [i + 1, i, 0, 0, 0, i, i + 1],
                [i + 1, i, 0, 0, 0, i, i + 1],
            ]
            pixel_size = 2 * self.enemy_radius / 7

            grid_size = len(alien_shape)

            start_x = enemy.enemy_x - (grid_size / 2) * pixel_size
            start_y = enemy.enemy_y + (grid_size / 2) * pixel_size

            for row in range(grid_size):
                for col in range(grid_size):
                    if alien_shape[row][col] == 1:
                        xcod = start_x + col * pixel_size
                        ycod = start_y - row * pixel_size
                        stddraw.filledSquare(xcod, ycod, pixel_size / 2)

    def check_hit(self, projectile: Projectile):
        for enemy in self.enemies:
            if enemy.is_enemy_hit_by_projectile(projectile):
                self.enemies.remove(enemy)
                return True
        return False

