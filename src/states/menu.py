import stddraw
import time
import random
from color import Color


class MenuPage:
    def __init__(self, width: int, height: int):
        self.finished = False
        self.timer = time.time()
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

        stddraw.setXscale(0, 1)
        stddraw.setYscale(0, 1)
        stddraw.setCanvasSize(width, height)

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
        stddraw.rectangle(0.09, 0.29, 0.82, 0.42 )
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0.1, 0.3, 0.8, 0.4)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontFamily("Courier New")
        stddraw.setFontSize(min(self.width, self.height) // 10)
        stddraw.text(0.5, 0.9, "SPACE INVADERS")

        instructions = [
            "USE THE LEFT AND RIGHT ARROW KEYS TO MOVE SIDEWAYS",
            "USE THE UP ARROW TO SHOOT",
            "",
            "PRESS SPACE TO PLAY!",
            "",
            "PRESS ESCAPE TO EXIT"
        ]

        stddraw.setFontSize(min(self.width, self.height) // 40)
        line_height = 1 / 20
        start_y = 0.6

        for i, line in enumerate(instructions):
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
        return "MENU"