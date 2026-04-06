import stddraw
from Game.enemies import Enemies
from Game.spaceship import Player
import random
from color import Color
from src.Game.controls import controls
from src.states.end import EndPage
import time
from Music.music import Music

class Level1:
    def __init__(self, width: int, height: int):
        self.score: int = 0
        self.alive: bool = True
        self.iteration_num: int = 0
        self.player = Player(0, -0.85, 0.2, 0, 0, 90)
        self.enemies = Enemies()
        self.width = width
        self.height = height
        self.enemy_speed = 0.001

        self.projectile_shot: bool = False
        self.projectile_dx = 0
        self.projectile_dy = 0

        self.enemies.create_enemies(1, 3, 5)
        self.enemy_creation_timer = time.time()
        self.cooldown_timer = time.time()

        self.end_page = None

        self.stars = []

        for i in range(600):
            rand_x = random.random()
            rand_y = random.random()
            radius = random.random() * min(self.width, self.height) / 500000
            #

            colour = Color(random.randrange(130, 220), random.randrange(130, 220), 255)
            self.stars.append((rand_x, rand_y, radius, colour))

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.5, 0.9, f"Score: {self.score}")
        spawn_interval = 3 * (0.25 ** (self.score / 25000))
        if (time.time() - self.enemy_creation_timer) > spawn_interval:
            self.enemies.create_enemies(1, 1, random.randint(1, 5))
            self.enemy_creation_timer = time.time()

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)
        if not self.enemies.check_death():
            self.player.draw_spaceship(0.1, stddraw.WHITE, False)
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            self.enemies.enemy_update(1, 0.01, self.enemy_speed, True)
            self.enemies.draw_enemies()

            if self.projectile_shot and (time.time() - self.cooldown_timer) > 0.2:
                stddraw.setPenColor(stddraw.RED)
                self.cooldown_timer = time.time()
                speed = 5
                self.projectile_dx, self.projectile_dy = self.player.shoot(speed)
                self.projectile_dx = (self.projectile_dx + 1) / 2
                self.projectile_dy = (self.projectile_dy + 1) / 2
                if self.enemies.check_hit( ((self.player.x + 1)/2, (self.player.y + 1)/2), (self.projectile_dx, self.projectile_dy)):
                    stddraw.setPenColor(stddraw.WHITE)
                    stddraw.setPenRadius(0.006)
                    self.score += 100
                    self.enemy_speed += 0.000015
                else:
                    stddraw.setPenRadius(0.001)
                    stddraw.setPenColor(stddraw.ORANGE)
                stddraw.line((self.player.x + 1) / 2, (self.player.y + 1) / 2, self.projectile_dx, self.projectile_dy)
                self.projectile_shot = False
        else:
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.score)
            self.end_page.draw()
            self.alive = False
        stddraw.show(20)

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        self.projectile_shot = controls(self.player, keys)
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and keys[stddraw.K_r]:
            return "RESTART"

        return "PLAY"
        
#Template for level 2
class Level2:
    def __init__(self, width: int, height: int, stars: list):
        self.score: int = 15000
        self.alive: bool = True
        self.iteration_num: int = 0
        self.player = Player(0, -0.85, 0.08, 0, 0, 90)
        self.enemies = Enemies()
        self.width = width
        self.height = height
        self.enemy_speed = 0.0005
        self.block = False
        self.lives = 5
        self.music = Music()
        self.music.load(["assets/Music/enemy_shoot", "assets/Music/shoot"])
        self.shoot_countdown = -1
        self.enemies_shooting = []

        self.end_page = None

        self.projectile_shot: bool = False
        self.projectile_dx = 0
        self.projectile_dy = 0

        self.enemies.create_enemies(2, 2, 3)
        self.enemy_creation_timer = time.time()
        self.cooldown_timer = time.time()
        self.block_cooldown = time.time()
        self.hit = False

        self.stars = stars

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.3, 0.9, f"Score: {self.score}")
        stddraw.text(0.6, 0.9, f"Lives: {self.lives}")

        spawn_interval = 5 * 0.25 ** (self.score / 50000)

        if (time.time() - self.enemy_creation_timer) > spawn_interval:
            self.enemies.create_enemies(2, 1, random.randint(1, 5))
            self.enemy_creation_timer = time.time()

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        if not self.enemies.check_death() and self.lives > 0:
            self.player.draw_spaceship(0.1, stddraw.WHITE, False)
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            self.enemies.enemy_update(1, 0.01, self.enemy_speed, True)
            self.enemies.draw_enemies()
            if random.randint(0,60) < self.score // 10000 and self.shoot_countdown < 0 and len(self.enemies.enemies) > 0:
                self.shoot_countdown = 60
                self.hit = False
                for i in range(random.randint(1,5)):
                    random_enemy = self.enemies.shoot()
                    if random_enemy is not None and random_enemy not in self.enemies_shooting:
                        self.enemies_shooting.append(self.enemies.shoot())
                #self.music.play("assets/Music/enemy_charge")

            self.shoot_countdown -= 1
            if self.shoot_countdown == 20:
                self.music.play("assets/Music/enemy_shoot")
            for enemy in self.enemies_shooting:
                if enemy in self.enemies.enemies:
                    if 20 < self.shoot_countdown < 60:
                        for i in range(100):
                            stddraw.filledCircle(enemy.enemy_x, enemy.enemy_y - i/100, 0.002)

                    if 0 < self.shoot_countdown <= 20:
                        stddraw.setPenColor(stddraw.RED)
                        stddraw.setPenRadius(0.003)
                        stddraw.line(enemy.enemy_x, enemy.enemy_y, enemy.enemy_x, 0)
                        if (self.player.x + 1)/2 - self.player.radius <= enemy.enemy_x <= (self.player.x + 1)/2 + self.player.radius:
                            stddraw.setPenColor(stddraw.RED)
                            stddraw.setPenRadius(0.003)
                            stddraw.line(enemy.enemy_x, enemy.enemy_y, enemy.enemy_x, 0)
                            if not self.hit:
                                self.lives -= 1
                            self.hit = True

            if self.projectile_shot and (time.time() - self.cooldown_timer) > 0.2:
                stddraw.setPenColor(stddraw.RED)
                self.cooldown_timer = time.time()
                speed = 5
                self.projectile_dx, self.projectile_dy = self.player.shoot(speed)
                self.projectile_dx = (self.projectile_dx + 1) / 2
                self.projectile_dy = (self.projectile_dy + 1) / 2
                if self.enemies.check_hit( ((self.player.x + 1)/2, (self.player.y + 1)/2), (self.projectile_dx, self.projectile_dy)):
                    #self.music.play("assets/Music/shoot")
                    stddraw.setPenColor(stddraw.WHITE)
                    stddraw.setPenRadius(0.006)
                    self.score += 100
                    self.enemy_speed += 0.000015
                else:
                    stddraw.setPenRadius(0.001)
                    stddraw.setPenColor(stddraw.ORANGE)
                stddraw.line((self.player.x + 1) / 2, (self.player.y + 1) / 2, self.projectile_dx, self.projectile_dy)
                self.projectile_shot = False

        else:
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.score)
            self.end_page.draw()
            self.alive = False
        stddraw.show(20)

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        self.projectile_shot = controls(self.player, keys)
        self.block = keys[stddraw.K_b]
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and keys[stddraw.K_r]:
            return "RESTART"

        return "PLAY"

#Template for level 3
class Level3:
    def __init__(self, width: int, height: int, stars: list):
        self.score: int = 40000
        self.alive: bool = True
        self.iteration_num: int = 0
        self.player = Player(0, -0.85, 0.2, 0, 0, 90)
        self.enemies = Enemies()
        self.width = width
        self.height = height
        self.enemy_speed = 0.001

        self.projectile_shot: bool = False
        self.projectile_dx = 0
        self.projectile_dy = 0

        #self.enemies.create_enemies(3, 3, 5)
        #self.enemy_creation_timer = time.time()
        #self.cooldown_timer = time.time()

        self.end_page = None

        self.stars = stars

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.5, 0.9, f"Score: {self.score}")

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        if not self.enemies.check_death():
            self.player.draw_spaceship(0.1, stddraw.WHITE, False)
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

        else:
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.score)
            self.end_page.draw()
            self.alive = False
        stddraw.show(20)

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        self.projectile_shot = controls(self.player, keys)
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and keys[stddraw.K_r]:
            return "RESTART"

        return "PLAY"