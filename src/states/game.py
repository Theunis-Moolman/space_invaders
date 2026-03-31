import stddraw
from picture import Picture
from Game.enemies import Enemies
from Game.spaceship import Player

class GamePlay:
    def __init__(self, width, height):
        self.score: int = 0
        self.alive: bool = True
        self.iteration_num: int = 0
        self.player = Player(0.5, 0, 0.2, 0, 0, 0)
        self.enemies = Enemies(2, 5)
        self.width = width
        self.height = height

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, self.width, self.height)
        self.player.draw_spaceship(0.1,False, False)

        stddraw.show(20)

    def run(self):
        self.draw()
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == chr(27):
                return "ESCAPE"

        return "PLAY"
        

