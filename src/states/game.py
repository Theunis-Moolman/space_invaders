import stddraw
from Game.enemies import Enemies
from Game.spaceship import Player
import random
from color import Color

class GamePlay:
    def __init__(self, width: int, height: int):
        self.score: int = 0
        self.alive: bool = True
        self.iteration_num: int = 0
        self.player = Player(width/2, 0, 20, 0, 0, 0)
        self.enemies = Enemies(2, 5)
        self.width = width
        self.height = height

        self.stars = []

        for i in range(250):
            rand_x = random.random()
            rand_y = random.random()
            radius = random.random() * min(self.width, self.height) / 100000
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

        self.player.draw_spaceship(0.1,False, False)

        stddraw.show(20)

    def run(self):
        self.draw()
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == chr(27):
                return "ESCAPE"

        return "PLAY"
        

