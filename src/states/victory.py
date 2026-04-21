import stddraw
import time
from src.Music.music import Music

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
        self.played_victory = False
        self.music_handler = Music()

        self.music_handler.load(["assets/Music/Victory"])

    def draw(self):
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)
        if not self.played_victory:
            self.music_handler.play("assets/Music/Victory")
            self.played_victory = True

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

        stddraw.text(0.5, 0.1, f"AUTO RESTARTING IN {int(15 - time.time() + self.win_timer)} SECONDS")


        