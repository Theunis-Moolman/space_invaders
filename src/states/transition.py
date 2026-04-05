import random
import stddraw

class TransitionPage:
    def __init__(self, heading: str, paragraph: str, stars: list):
        self.heading = heading
        self.paragraph = paragraph.splitlines()

        self.stars = stars

    def draw(self):
        for i in range(120):
            stddraw.clear()
            stddraw.setPenColor(stddraw.BLACK)
            stddraw.filledRectangle(0, 0, 1, 1)
            stddraw.setPenRadius(0.001)

            t = i / 120
            y_scroll = 1 - 1.5 * t * t * (2 - 2 * t)

            print(y_scroll)

            for x, y, radius, colour in self.stars:
                probability = random.random()
                if probability < 0.99:
                    stddraw.setPenColor(colour)
                    stddraw.filledCircle(x, y, radius)

            stddraw.setFontSize(100)
            stddraw.setPenColor(stddraw.WHITE)
            stddraw.text(0.5, y_scroll, self.heading)
            stddraw.setFontSize(20)
            for j, line in enumerate(self.paragraph):
                stddraw.text(0.5, y_scroll - 0.1 - j * 0.06, line)

            stddraw.show(30)