import math
import stddraw
import random
from picture import Picture
import time
from src.Game.spaceship import Projectile
from src.Music.music import Music

class Enemy:
    """
    Enemy object for level 1 and level 2 of the game

    Args:
        x (float): x position
        y (float): y position
        level (int): level
        radius (float): radius of enemy


    Author: Theunis and Sydwell
    """
    def __init__(self, x: float, y: float, level: int, radius: float):
        self.x = x
        self.y = y
        self.level = level
        self.radius = radius


    def is_hit_by_projectile(self, projectile: Projectile) -> bool:
        #Retrace to make sure all collisions are detected
        for i in range(20):
            px = projectile.x - projectile.dx * (i/20)
            py = projectile.y - projectile.dy * (i/20)
            #Use distance formula to see if distance is small enough to detect a hit
            distance = math.sqrt((self.x - px) ** 2 + (self.y - py) ** 2)
            if distance <= self.radius + 0.01:
                return True
        return False

class Boss(Enemy):
    """
    Boss object for level 3 of the game

    Args:
        x (float): x position
        y (float): y position
        level (int): level for initializing enemy object due to inheritance
        radius


    Author: Theunis and Sydwell
    """
    def __init__(self, x: float, y: float, level, radius):
        super().__init__(x, y, level, radius)
        #Load images
        self.image = Picture("assets/images/Boss.png")
        self.projectile_image = Picture("assets/images/EnemyMissile.png")
        #Create music object and load appropriate audio files
        self.music = Music()
        self.music.load(["assets/Music/boss_cannon"])
        #Shooting cooldown tracker
        self.cooldown = time.time()
        #List to store projectiles
        self.projectiles = []

        self.health = 100

    #Inherit from enemy object
    def is_hit_by_projectile(self, projectile: Projectile) -> bool:
        return super().is_hit_by_projectile(projectile)

    def move(self, enemy_dir: int, enemy_speed: float, descend_speed: float, should_descend: bool):
        #Possible next co-ordinate
        next_x = self.x + enemy_dir * enemy_speed

        #Check for wall collision to determine if it should descend
        if next_x + self.radius > 1 or next_x - self.radius < 0:
            should_descend = True

        #Apply movement
        if should_descend:
            self.y -= descend_speed
        else:
            self.x += enemy_dir * enemy_speed

        #Reverse direction
        if should_descend:
            enemy_dir *= -1

        return enemy_dir

    def shoot(self):
        #Make enemy shoot if random cooldown is complete
        if time.time() - self.cooldown > random.randint(3,20):
            #Play Tchaikovsky Cannon sound effect
            self.music.play("assets/Music/boss_cannon")

            #Shoot projectiles at different angles
            angles = [-45, -22.5, 0, 22.5, 45]
            for a in angles:
                radians = math.radians(270 + a)
                dx = 0.002 * math.cos(radians)
                dy = 0.002 * math.sin(radians)
                self.projectiles.append(Projectile(self.x, self.y, dx, dy))
            #Update cooldown time
            self.cooldown = time.time()

    def draw(self):
        #Draw health bar
        for i in range(100):
            if i < self.health:
                stddraw.setPenColor(stddraw.RED)
                stddraw.filledRectangle(0.05 + i * 0.009, 0.95, 0.008, 0.02)

        #Draw boss picture
        stddraw.picture(self.image, self.x, self.y)

        #draw and move projectiles
        for projectile in self.projectiles:
            projectile.move()
            stddraw.picture(self.projectile_image, projectile.x, projectile.y)



class Enemies:
    """
    Enemy handler for handling enemy creation, updating enemies, checking hits, , shooting

    Args:
        None


    Author: Sydwell and Theunis
    """
    def __init__(self):
        #Store enemy list
        self.enemies = []

        self.enemy_radius = 0.02


    def create_enemies(self, level: int, rows: int, cols: int):
        enemy_x = 0.05
        enemy_y = 0.90

        enemy_spacing = 0.15

        #Create grid
        for row in range(rows):
            for col in range(cols):
                if cols == 1:
                    #This is added to handle a degenerate case in case the game is adjusted in future versions
                    x_pos = random.random() * 0.8 + 0.1
                else:
                    #Space out enemies in the grid horizontally
                    x_pos = enemy_x + col * enemy_spacing

                #Space out enemy in the grid vertically
                y_pos = enemy_y - row * enemy_spacing

                #Create enemy object at predetermined co-ordinate
                new_enemy = Enemy(x_pos, y_pos, level, self.enemy_radius)

                #Add enemy to the list
                self.enemies.append(new_enemy)

    def enemy_update(self, enemy_dir: int, enemy_speed: float, descend_speed: float, should_descend: bool):
        for enemy in self.enemies:
            next_x = enemy.x + enemy_dir * enemy_speed
            #Check wall collision
            if next_x + enemy.radius > 1 or next_x - enemy.radius < 0:
                should_descend = True
                break

        for enemy in self.enemies:
            #Move enemies
            if should_descend:
                enemy.y -= descend_speed
            else:
                enemy.x += enemy_dir * enemy_speed

        #Reverse direction
        if should_descend:
            enemy_dir *= -1

        return enemy_dir

    def check_death(self):
        #Cheks if enemy reaches the line to determine if the player dies
        for enemy in self.enemies:
            if enemy.y - enemy.radius <= 0.205:
                return True
        return False

    def shoot(self):
        if len(self.enemies) > 0:
            #Determines a random enemy to shoot
            random_enemy = random.choice(self.enemies)
            return random_enemy
        return None

    def draw_enemies(self): #made for 0 to 1 scale
        i = int(time.time() % 1 < 0.5)
        for enemy in self.enemies:
            if enemy.level == 1:
                stddraw.setPenColor(stddraw.WHITE)
            elif enemy.level == 2:
                stddraw.setPenColor(stddraw.RED)

            #Matrix of the alien to determine where pixels should be drawn
            #Adds movement too
            alien_shape = [
                [0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 0, 1, 1, 0],
                [i + 1, i, 0, 0, 0, i, i + 1],
                [i + 1, i, 0, 0, 0, i, i + 1],
            ]

            #Adjusts pixel size
            pixel_size = 2 * self.enemy_radius / 7

            #Determine grid size
            grid_size = len(alien_shape)

            start_x = enemy.x - (grid_size / 2) * pixel_size
            start_y = enemy.y + (grid_size / 2) * pixel_size

            for row in range(grid_size):
                for col in range(grid_size):
                    #Draws a pixel if the matrix is 1 at a point
                    if alien_shape[row][col] == 1:
                        xcod = start_x + col * pixel_size
                        ycod = start_y - row * pixel_size
                        stddraw.filledSquare(xcod, ycod, pixel_size / 2)

    def check_hit(self, projectile: Projectile):
        #Check through each enemy to see if they are hit
        for enemy in self.enemies:
            if enemy.is_hit_by_projectile(projectile):
                self.enemies.remove(enemy)
                return True
        return False



