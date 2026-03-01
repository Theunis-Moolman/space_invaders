import stddraw

class GamePlay():
    def __init__(self):
        self.score: int = 0
        self.alive: bool = True
        self.iteration_num: int = 0

    def draw():
        stddraw.clear()
        stddraw.setXscale(0, 1)
        stddraw.setYscale(0, 1)
        background = Picture("assets/images/SPACE INVADERS.png")
        stddraw.picture(background, 0.5, 0.5)
        

