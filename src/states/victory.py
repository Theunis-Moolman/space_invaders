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

        # Store the timer reference to calculate the auto-restart countdown
        self.win_timer = win_timer

        # Flag to make sure victory music only play once
        self.played_victory = False

        # Initialise the music and handler and load the victory track
        self.music_handler = Music()
        self.music_handler.load(["assets/Music/Victory"])

        # Update high score if any player beats it
        for player in self.players:
            if player.score > highscore:
                highscore = player.score
                with open("src/Stored/Highscore.txt", "w") as f:
                    f.write(str(highscore))

    def draw(self):
        #Cleaar screen and set black background
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        # Play victory music on the first draw call 
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
            # Multiplayer: determine winner by comparing scores
            if self.players[0].score > self.players[1].score:
                stddraw.text(
                    0.5, 0.5, f"Player 1 won with score: {self.players[0].score}"
                )
            elif self.players[1].score > self.players[0].score:
                stddraw.text(
                    0.5, 0.5, f"Player 2 won with score: {self.players[1].score}"
                )
            else:
                # Draw if scores are equal
                stddraw.text(0.5, 0.5, f"Draw: {self.players[0].score}")
        else:
            # Simply show score if single palyer
            stddraw.text(0.5, 0.5, f"Score: {self.players[0].score}")

        # Restart and player instructions
        stddraw.setFontSize(25)
        stddraw.text(0.5, 0.3, "PRESS R TO RESTART")
        stddraw.text(0.5, 0.2, "PRESS ESC TO EXIT")

        # Calculate and display seconds before auto restart
        stddraw.text(
            0.5,
            0.1,
            f"AUTO RESTARTING IN {int(15 - time.time() + self.win_timer)} SECONDS",
        )

    def stop_music(self):
        # Stop the victory music
        self.music_handler.stop()
