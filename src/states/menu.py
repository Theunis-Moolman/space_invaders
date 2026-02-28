import stddraw
import time
from picture import Picture

class MenuPage():
    def __init__(self):
        self.finished = False
        self.timer = time.time()

    def draw(self):
        stddraw.clear()
        stddraw.setXscale(0, 1)
        stddraw.setYscale(0, 1)
        background = Picture("assets/images/SPACE INVADERS.png")
        text = Picture("assets/images/PRESS SPACE TO CONTINUE.png")
        stddraw.picture(background, 0.5, 0.5)
        if int((time.time() - self.timer) * 1.5) % 2 == 0:
            stddraw.picture(text, 0.5, 0.6)
        stddraw.show(20)
    
    def handle_input(self):
        if(stddraw.hasNextKeyTyped()):
            key = stddraw.nextKeyTyped()
            if key == " ":
                return True
        return False

    def run(self):
        while not self.finished:
            if(self.handle_input()):
                self.finished = True
            self.draw()
        return "PLAY"
