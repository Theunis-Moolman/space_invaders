import random
import stddraw


class TransitionPage:
    """
    Transition page for in between level that displays a title and a description with a scrolling effect

    Args:
        heading: String of the title to be displayed
        paragraph: String of the paragraph to be displayed
        stars: co-ordinates of the stars to display


    Author: Theunis  
    """

    def __init__(self, heading: str, paragraph: str, stars: list):
        self.heading = heading
        self.paragraph = paragraph.splitlines()

        self.stars = stars

    def draw(self):
        # Animate over 120 frames
        for i in range(120):
            # Clear screen and set black background
            stddraw.clear()
            stddraw.setPenColor(stddraw.BLACK)
            stddraw.filledRectangle(0, 0, 1, 1)
            stddraw.setPenRadius(0.001)

            # Calculate scoll position
            t = i / 120
            y_scroll = 1 - 1.5 * t * t * (2 - 2 * t)

            # Draw background stars
            for x, y, radius, colour in self.stars:
                # Randomly skip 1% of stars to create twinkling effect
                probability = random.random()
                if probability < 0.99:
                    stddraw.setPenColor(colour)
                    stddraw.filledCircle(x, y, radius)

            # Draw heading
            stddraw.setFontSize(100)
            stddraw.setPenColor(stddraw.WHITE)
            stddraw.text(0.5, y_scroll, self.heading)

            # Draw paragraph lines
            stddraw.setFontSize(20)

            # Stack each line below the heading, spaced, 0.06 units apart
            for j, line in enumerate(self.paragraph):
                stddraw.text(0.5, y_scroll - 0.1 - j * 0.06, line)

            # Display frame for 30ms before moving to the next
            stddraw.show(30)
