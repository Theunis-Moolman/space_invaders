import stddraw # type: ignore
import math
from Music.music import Music


class Player:
    def __init__(self, x, y, radius, direction, speed, angle):
        self.x  = x
        self.y = y
        self.radius = radius
        self.direction = direction
        self.speed = speed
        self.angle = angle
        self.dx = 0
        self.dy = 0
        self.size = 0.02
        self.pixels = []
        self.music = Music()

    #Move player horizontally
    def move_circle(self, width, direction,speed):
        if self.x - self.radius < -1: #Prevents going off left edge
            self.x = -1 + self.radius
        if self.x + self.radius > width: #Prevents going off right edge
            self.x = 1 - self.radius
        self.x += direction * speed


    #Controls aiming direction
    def line_rotate(self, is_clockwise , counterclockwise , rotation_speed):
        #Rotate left
        if counterclockwise:
            self.angle += rotation_speed #increase angle
            if self.angle >= 180: #Clamp at 180 degrees cannot go further
                self.angle = 180
                counterclockwise = False

        #Rotate right
        if is_clockwise:
            self.angle -= rotation_speed #Decrease angle
            if self.angle <= 0:
                self.angle = 0
                is_clockwise = True

        return counterclockwise, is_clockwise  #Returns updated values

    def pixel(self, px, py, color):
        stddraw.setPenColor(color)
        px = (px + 1)/2
        py = (py + 1)/2
        stddraw.filledSquare(px, py, self.size)

    def draw_spaceship(self, line_length,change_color,is_hit=False):
        hit_color = change_color if is_hit else stddraw.WHITE  #If hit, flash color

        # Define the spaceship shape using relative coordinates (dx, dy, color)
        self.pixels = []
        # Tip of ship
        self.pixels.append((0, 10, hit_color))

        # wings and body using for loops
        for i in [-1, 1]:
            self.pixels.append((i, 9, hit_color))
            self.pixels.append((2 * i, 8, hit_color))
            self.pixels.append((3 * i, 7, hit_color))
            self.pixels.append((3 * i, 6, hit_color))
            self.pixels.append((3 * i, 5, hit_color))
            self.pixels.append((4 * i, 4, hit_color))
            self.pixels.append((5 * i, 3, hit_color))
            self.pixels.append((6 * i, 2, hit_color))

            for j in range(-1, -4, -1):
                self.pixels.append((7 * i, j, hit_color))

            self.pixels.append((7 * i, 0, hit_color))
            self.pixels.append((7 * i, 1, hit_color))
            self.pixels.append((6 * i, -4, hit_color))
            self.pixels.append((5 * i, -4, hit_color))
            self.pixels.append((4 * i, -3, hit_color))
            self.pixels.append((3 * i, -3, hit_color))
            self.pixels.append((2 * i, -3, hit_color))
            self.pixels.append((1 * i, -3, hit_color))

            # Flame in red
            for k in range(1, 5):
                self.pixels.append((k * i, -2, stddraw.RED if not is_hit else hit_color))

            # Vertical midsection
            for k in range(-1, 4):
                self.pixels.append((2 * i, k, hit_color))

        # Convert angle to radians for math functions
        #radian = math.radians(angle)-math.pi/2
        radians = math.radians(self.angle)

        # Draw each part of the ship after rotation(Relative to ship position)
        for dx, dy, color in self.pixels:
            self.pixel(self.x + dx * self.size, self.y + dy * self.size, color)

        # Optional: Draw a direction line
        end_x = self.x + line_length * math.cos(radians)
        end_y = self.y + line_length * math.sin(radians)
        stddraw.setPenRadius(0.01)
        stddraw.setPenColor(stddraw.RED)
        stddraw.line((self.x + 1)/2, (self.y + 1)/ 2 , (end_x + 1)/2, (end_y + 1)/2) #Shows where you are aiming

    def shoot(self, speed_projectile):
        radians = math.radians(self.angle) #Convert angles
        #Calculate movement direction
        dx = self.x + speed_projectile * math.cos(radians)
        dy = self.y + speed_projectile * math.sin(radians)

        self.music.sound(1000,44100) #Play shooting sound

        return dx, dy #use Player.x and Player.y to get x and y
