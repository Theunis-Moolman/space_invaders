import stddraw
import time
from src.Music.music import Music


class Victory:
    """
    Victory screen that shows a congratulatory message and final score
    Author Ben
    """

    def __init__(
        self, width: int, height: int, players, win_timer: float, highscore: int
    ):
        self.width = width
        self.players = players
        self.win_timer = win_timer
        self.played_victory = False
        self.music_handler = Music()

        self.music_handler.load(["assets/Music/Victory"])

        for player in self.players:
            if player.score > highscore:
                highscore = player.score
                with open("src/Stored/Highscore.txt", "w") as f:
                    f.write(str(highscore))

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
        stddraw.setFontSize(20)
        # Score
        if len(self.players) > 1:
            if self.players[0].score > self.players[1].score:
                stddraw.text(
                    0.5, 0.5, f"Player 1 won with score: {self.players[0].score}"
                )
            elif self.players[1].score > self.players[0].score:
                stddraw.text(
                    0.5, 0.5, f"Player 2 won with score: {self.players[1].score}"
                )
            else:
                stddraw.text(0.5, 0.5, f"Draw: {self.players[0].score}")
        else:
            stddraw.text(0.5, 0.5, f"Score: {self.players[0].score}")

        # Restart / Exit instructions
        stddraw.setFontSize(25)
        stddraw.text(0.5, 0.3, "PRESS R TO RESTART")
        stddraw.text(0.5, 0.2, "PRESS ESC TO EXIT")

        stddraw.text(
            0.5,
            0.1,
            f"AUTO RESTARTING IN {int(15 - time.time() + self.win_timer)} SECONDS",
        )

    def stop_music(self):
        self.music_handler.stop()
