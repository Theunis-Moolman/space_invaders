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
            rand_x = random.randint(0, self.width)
            rand_y = random.randint(0, self.height)
            radius = random.random() * min(self.width, self.height) / 100
            #

            colour = Color(random.randrange(130, 220), random.randrange(130, 220), 255)
            self.stars.append((rand_x, rand_y, radius, colour))

        stddraw.setXscale(0, width)
        stddraw.setYscale(0, height)
        stddraw.setCanvasSize(width, height)

    def draw(self):
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, self.width, self.height)
        stddraw.setPenColor(stddraw.WHITE)
        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, self.height * 0.8, self.width, self.height / 5)
        stddraw.setPenRadius(0.1)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.rectangle(self.width * 0.09, self.height * 0.29, self.width * 0.82, self.height * 0.42 )
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(self.width * 0.1, self.height * 0.3, self.width * 0.8, self.height * 0.4)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontFamily("Courier New")
        stddraw.setFontSize(min(self.width, self.height) // 10)
        stddraw.text(self.width/2, self.height * 0.9, "SPACE INVADERS")

        instructions = [
            "USE THE LEFT AND RIGHT ARROW KEYS TO MOVE SIDEWAYS",
            "USE THE UP ARROW TO SHOOT",
            "",
            "PRESS SPACE TO PLAY!"
        ]

        stddraw.setFontSize(min(self.width, self.height) // 40)
        line_height = self.height / 20
        start_y = self.height * 0.6

        for i, line in enumerate(instructions):
            y = start_y - i * line_height
            stddraw.text(self.width / 2, y, line)
        stddraw.show(20)
    
    def handle_input(self):
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == " ":
                return True
        return False

    def run(self):
        self.draw()
        if self.handle_input():
            return "PLAY"
        return "MENU"