import stddraw
import keyboard

class MenuPage():
    def __init__(self):
        self.finished = False

    def draw(self):
        stddraw.clear()
        stddraw.text(0.6, 0.6, "Space Invaders")
        stddraw.text(0.5, 0.4, "Press SPACE to start!")
        stddraw.show(20)
    
    def handle_input:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if even.name == 'space':
                return true
        return false

    def run(self):
        while not self.finished:
            if(self.handle_input()):
                self.finished = True
            self.draw()
        return "PLAY"
