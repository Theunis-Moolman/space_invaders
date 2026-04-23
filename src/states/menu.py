import stddraw
import time
import random
from color import Color


class MenuPageSingle:
    """
    Menu page that is shown just at the start of the game:
        - Displays high score
        - Instructions on how to play the game

    Args:
        width (int): width of the window
        height (int): height of the window

    Author: Sydwell and Theunis
    """

    def __init__(self, width: int, height: int, highscore: int):
        self.finished = False
        self.timer = time.time()
        self.width = width
        self.height = height
        self.stars = []
        self.highscore = highscore
        self.fontsize = min(self.width, self.height) // 40

        for i in range(250):
            rand_x = random.random()
            rand_y = random.random()
            radius = random.random() * min(self.width, self.height) / 100000
            #

            colour = Color(random.randrange(130, 220), random.randrange(130, 220), 255)
            self.stars.append((rand_x, rand_y, radius, colour))

        stddraw.setXscale(0, 1)
        stddraw.setYscale(0, 1)

        self.instructions = [
            f"Highscore: {self.highscore}",
            "USE THE a AND d KEYS TO MOVE SIDEWAYS",
            "USE THE w KEY TO SHOOT",
            "USE Q AND E TO CHANGE SHOOTING ANGLE",
            "PRESS SPACE TO PLAY!",
            "",
            "PRESS ESCAPE TO EXIT",
            "PRESS M TO ENABLE MULTIPLAYER",
        ]

    def draw(self):
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)
        stddraw.setPenColor(stddraw.WHITE)
        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0.8, 1, 0.5)
        stddraw.setPenRadius(0.1)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.rectangle(0.09, 0.19, 0.82, 0.52)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0.1, 0.2, 0.8, 0.5)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontFamily("Courier New")
        stddraw.setFontSize(self.fontsize * 2)
        stddraw.text(0.5, 0.9, "SPACE INVADERS")

        stddraw.setFontSize(self.fontsize)
        line_height = 1 / 20
        start_y = 0.6

        for i, line in enumerate(self.instructions):
            y = start_y - i * line_height
            stddraw.text(0.5, y, line)

        stddraw.show(20)

    def run(self):
        self.draw()
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == " ":
                return "PLAY"
            if key == chr(27):
                return "ESCAPE"
            if key == "m":
                return "MULTI"
        return "MENU"


class MenuPageMulti(MenuPageSingle):
    def __init__(self, width: int, height: int, highscore: int):
        super().__init__(width, height, highscore)
        self.instructions = self.instructions = [
            f"Highscore: {self.highscore}",
            "PLAYER 1: a/d MOVE, w SHOOT, q/e ANGLE",
            "PLAYER 2: j/l MOVE, i SHOOT, u/o ANGLE",
            "PRESS SPACE TO PLAY!",
            "",
            "PRESS ESCAPE TO EXIT",
            "PRESS S TO ENABLE SINGLEPLAYER",
        ]
        self.fontsize = min(self.width, self.height) // 40

    def run(self):
        self.draw()
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == " ":
                return "PLAY"
            if key == chr(27):
                return "ESCAPE"
            if key == "s":
                return "SINGLE"
        return "MENU"
