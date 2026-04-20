import stddraw
import time

class Victory:
    """
    Victory screen that shows a congratulatory message and final score
    Author Ben
    """
    def __init__(self, width: int, height: int, score: int, win_timer: float):
        self.width = width
        self.height = height
        self.score = score
        self.win_timer = win_timer

    def draw(self):
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        # Victory message
        stddraw.setFontSize(80)
        stddraw.setPenColor(stddraw.GREEN)
        stddraw.text(0.5, 0.7, "YOU WIN!")

        # Score
        stddraw.setFontSize(40)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.5, 0.5, f"Final Score: {self.score}")

        # Restart / Exit instructions
        stddraw.setFontSize(25)
        stddraw.text(0.5, 0.3, "PRESS R TO RESTART")
        stddraw.text(0.5, 0.2, "PRESS ESC TO EXIT")
        