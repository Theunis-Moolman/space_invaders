from color import Color
import random
import stddraw
import time

from src.Music.music import Music


class EndPage:
    """
    End screen that shows the player's score and a game over message

    Args:
        width (int): width of the window
        height (int): height of the window
        players (Player): Player objects to evaluate scores
        death_timer: Timer to display time left before game restarts
        highscore: For saving high score

    Author: Theunis
    """

    def __init__(
        self, width: int, height: int, players, death_timer: float, highscore: int
    ):
    # --- BASIC SETUP ---
        # Initializes core attributes: players, timer, and prepares music + star storage
        self.stars = []
        self.players = players
        self.death_timer = death_timer
    # --- MUSIC SETUP ---
        # Loads and continuously plays the "game over" background music
        self.music = Music()
        self.music.load(["assets/Music/gameover"])
        self.music.play("assets/Music/gameover", loop=True)
        
    # --- STAR BACKGROUND GENERATION ---
        # Creates 600 randomly positioned stars with small radii and soft blue colors
        # These are stored once and reused every frame
        for i in range(600):
            rand_x = random.random()
            rand_y = random.random()
            radius = random.random() * min(width, height) / 500000
            #

            colour = Color(random.randrange(130, 220), random.randrange(130, 220), 255)
            self.stars.append((rand_x, rand_y, radius, colour))
            
    # --- HIGHSCORE CHECK & SAVE ---
        # Compares all player scores and updates the stored highscore if needed
        for player in self.players:
            if player.score > highscore:
                highscore = player.score
                with open("src/Stored/Highscore.txt", "w") as f:
                    f.write(str(highscore))

    def draw(self):
    # --- BACKGROUND RENDERING ---
        # Clears screen and draws a black background
        stddraw.clear()
        stddraw.setPenRadius(0.001)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)
        
    # --- STAR RENDERING (TWINKLE EFFECT) ---
        # Draws stars with a slight randomness so they appear to flicker     probability = random.random()
        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

    # --- GAME OVER TITLE ---
        # Displays the main "GAME OVER" message
        stddraw.setFontSize(80)
        stddraw.setPenColor(stddraw.RED)
        stddraw.text(0.5, 0.7, "GAME OVER")
        stddraw.setFontSize(20)
        stddraw.setPenColor(stddraw.WHITE)
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

    # --- USER INSTRUCTIONS ---
        # Displays controls for restarting or exiting the game
        stddraw.setFontSize(25)
        stddraw.text(0.5, 0.3, "PRESS R TO RESTART")
        stddraw.text(0.5, 0.2, "PRESS ESC TO EXIT")
         # Display countdown timer until auto-restart
        stddraw.text(
            0.5,
            0.1,
            f"AUTO RESTARTING IN {int(5 - time.time() + self.death_timer)} SECONDS",
        )

    def stop_music(self):
    # --- MUSIC CONTROL ---
        # Stops the game over music when leaving this screen
        self.music.stop()
