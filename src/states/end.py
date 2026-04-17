from color import Color
import random
import stddraw
import time

class EndPage:
    """
    End screen that shows the player's score and a game over message

    Args:
        width (int): width of the window
        height (int): height of the window
        score (int): score of the player

    Author: Theunis
    """
    def __init__(self, width: int, height: int, score: int, death_timer: float):
        self.stars = []
        self.score = score
        self.death_timer = death_timer

        for i in range(600):
            rand_x = random.random()
            rand_y = random.random()
            radius = random.random() * min(width, height) / 500000
            #

            colour = Color(random.randrange(130, 220), random.randrange(130, 220), 255)
            self.stars.append((rand_x, rand_y, radius, colour))

    def draw(self):
        stddraw.clear()
        stddraw.setPenRadius(0.001)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        stddraw.setFontSize(80)
        stddraw.setPenColor(stddraw.RED)
        stddraw.text(0.5, 0.7, "GAME OVER")
        stddraw.setFontSize(40)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.5, 0.5, f"Score: {self.score}")
        stddraw.setFontSize(25)
        stddraw.text(0.5, 0.3, "PRESS R TO RESTART")
        stddraw.text(0.5, 0.2, "PRESS ESC TO EXIT")
        stddraw.text(0.5, 0.1, f"AUTO RESTARTING IN {int(5 - time.time() + self.death_timer)} SECONDS")