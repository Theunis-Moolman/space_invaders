import stddraw # type: ignore
import math
from music import Music

#Move player horizontally
def move_circle(x,radius,direction,speed):
    if x - radius < 0: #Prevents going off left edge
        x = radius
    if x + radius > 100: #Prevents going off right edge
        x = 100 - radius
    x += direction * speed
    return x #Returns updatd position

#Controls aiming direction
def line_rotate(angle , clockwise , counterclockwise , rotation_speed):
    #Rotate left
    if counterclockwise:
        angle += rotation_speed #increase angle
        if angle >= 180: #Clamp at 180 degrees cannot go further
            angle = 180
            counterclockwise = False
    
    #Rotate right
    if clockwise:
        angle -= rotation_speed #Decrease angle
        if angle <= 0:
            angle = 0
            clockwise = True

    return angle , counterclockwise , clockwise  #Returns updated values

def pixel(px, py, color):
    size=0.5
    stddraw.setPenColor(color)
    stddraw.filledSquare(px, py, size)

def draw_spaceship(x, y, radius, angle, line_length,change_color,is_hit=False):
    size = 0.5  # Size of each pixel/block
    hit_color = change_color if is_hit else stddraw.WHITE  #If hit, flash color

    # Define the spaceship shape using relative coordinates (dx, dy, color)
    pixels = [] #List of ship parts

    # Tip of ship
    pixels.append((0, 10, hit_color))

    # wings and body using for loops
    for i in [-1, 1]:
        pixels.append((i, 9, hit_color))
        pixels.append((2 * i, 8, hit_color))
        pixels.append((3 * i, 7, hit_color))
        pixels.append((3 * i, 6, hit_color))
        pixels.append((3 * i, 5, hit_color))
        pixels.append((4 * i, 4, hit_color))
        pixels.append((5 * i, 3, hit_color))
        pixels.append((6 * i, 2, hit_color))

        for j in range(-1, -4, -1):
            pixels.append((7 * i, j, hit_color))

        pixels.append((7 * i, 0, hit_color))
        pixels.append((7 * i, 1, hit_color))
        pixels.append((6 * i, -4, hit_color))
        pixels.append((5 * i, -4, hit_color))
        pixels.append((4 * i, -3, hit_color))
        pixels.append((3 * i, -3, hit_color))
        pixels.append((2 * i, -3, hit_color))
        pixels.append((1 * i, -3, hit_color))

        # Flame in red
        for k in range(1, 5):
            pixels.append((k * i, -2, stddraw.RED if not is_hit else hit_color))

        # Vertical midsection
        for k in range(-1, 4):
            pixels.append((2 * i, k, hit_color))
    
    # Convert angle to radians for math functions
    radian = math.radians(angle)-math.pi/2
    radians = math.radians(angle)

    # Draw each part of the ship after rotation(Relative to ship position)
    for dx, dy, color in pixels:
        pixel(x + dx * size, y + dy * size, color)

    # Optional: Draw a direction line
    end_x = x + line_length * math.cos(radians)
    end_y = y + line_length * math.sin(radians)
    stddraw.setPenColor(stddraw.RED)
    stddraw.line(x, y, end_x, end_y) #Shows where you are aiming 

def shoot(x,y,angle,speed_projectile):
    radians = math.radians(angle) #Convert angles
    
    #Calculate movement direction
    dx = speed_projectile * math.cos(radians)
    dy = speed_projectile * math.sin(radians)

    Music.sound(1000,44100) #Play shooting sound
    
    

    return {'x':x , 'y':y , 'dx':dx , 'dy':dy}
