import stddraw
from Game.enemies import Enemies
from Game.spaceship import Player
import random
from color import Color
import time

class GamePlay:
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

        self.enemies.create_enemies(3, 3, 5)
        self.enemy_creation_timer = time.time()
        self.cooldown_timer = time.time()

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
        stddraw.filledRectangle(0, 0, self.width, self.height)

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
            stddraw.setFontSize(80)
            stddraw.setPenColor(stddraw.RED)
            stddraw.text(0.5, 0.7, "GAME OVER")
            stddraw.setFontSize(25)
            stddraw.text(0.5, 0.5, "PRESS R TO RESTART")
            stddraw.text(0.5, 0.4, "PRESS ESC TO EXIT")
            self.alive = False
        stddraw.show(20)

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        elif keys[stddraw.K_RIGHT]:
            self.player.move_circle(1, 1, 0.02)
        elif keys[stddraw.K_LEFT]:
            self.player.move_circle(1, -1, 0.02)
        elif keys[stddraw.K_a]:
            self.player.line_rotate(False, True, 5)
        elif keys[stddraw.K_d]:
            self.player.line_rotate(True, False, 5)
        if keys[stddraw.K_UP]:
            self.projectile_shot = True
        if not self.alive and keys[stddraw.K_r]:
            return "RESTART"

        return "PLAY"
        

