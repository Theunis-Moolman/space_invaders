import stddraw
from Game.enemies import Enemies
from Game.spaceship import Player
import random
from color import Color
import pygame

class GamePlay:
    def __init__(self, width: int, height: int):
        self.score: int = 0
        self.alive: bool = True
        self.iteration_num: int = 0
        self.player = Player(0, -0.85, 0.2, 0, 0, 90)
        self.enemies = Enemies(2, 5)
        self.width = width
        self.height = height

        self.projectile_shot: bool = False
        self.projectile_dx = 0
        self.projectile_dy = 0

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
        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        self.player.draw_spaceship(0.1, stddraw.WHITE, False)
        stddraw.setPenRadius(0.001)
        stddraw.setPenColor(stddraw.WHITE)
        for i in range(100):
            x = i / 100
            stddraw.filledCircle(x, 0.205, 0.002)

        if self.projectile_shot:
            stddraw.setPenColor(stddraw.RED)
            self.projectile_dx = (self.projectile_dx + 1) / 2
            self.projectile_dy = (self.projectile_dy + 1) / 2
            stddraw.line((self.player.x + 1)/2, (self.player.y + 1)/2, self.projectile_dx, self.projectile_dy)
            self.projectile_shot = False
        stddraw.show(20)

    def run(self):
        self.draw()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return "ESCAPE"
        elif keys[pygame.K_RIGHT]:
            self.player.move_circle(1, 1, 0.02)
        elif keys[pygame.K_LEFT]:
            self.player.move_circle(1, -1, 0.02)
        elif keys[pygame.K_a]:
            self.player.line_rotate(True, False, 5)
        elif keys[pygame.K_d]:
            self.player.line_rotate(False, True, 5)
        if keys[pygame.K_UP]:
            self.projectile_dx, self.projectile_dy = self.player.shoot(5)
            self.projectile_shot = True

        return "PLAY"
        

