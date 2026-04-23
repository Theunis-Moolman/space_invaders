import stddraw # type: ignore
import math
from src.Music.music import Music
from picture import Picture
from color import Color
import time
import random


class Projectile:
    """
    Handle projectile that the player shoots and that the boss enemy shoots

    Args:
        x: x coordinate of the projectile
        y: y coordinate of the projectile


    Author: Sydwell and Theunis
    """
    def __init__(self, x: float, y: float, dx: float, dy: float):
        #Co-ordinates and speed of the projectile
        self.x: float = x
        self.y: float = y
        self.dx: float = dx
        self.dy: float = dy

    def move(self):
        #Movement update for the projectile
        self.x += self.dx
        self.y += self.dy


class Player:
    """
    Handle the spaceship drawing, moving, shooting, turret rotating and projectiles shot by the player

    Args:
        x: x coordinate of the player
        y: y coordinate of the player
        radius: radius of the player
        direction: direction of the player movement
        speed: speed of the player movement
        angle: angle of the player's turret

    Author: Sydwell and Theunis
    """
    def __init__(self, x: float, y: float, radius: float, direction: int, speed: float, angle: float, player_num: int):
        #Specify co-ordinates
        self.x  = x
        self.y = y

        #Specify radius
        self.radius = radius

        #Specify direction of movement
        self.direction = direction
        #Specify speed
        self.speed = speed

        #Specify angle of the turret
        self.angle = angle

        #Variables to keep movement increments
        self.dx = 0
        self.dy = 0

        #Pixel size
        self.size = 0.02

        #Player number for multiplayer
        self.player_num = player_num

        #Keep track of all projectiles
        self.projectiles: list[Projectile] = []

        #Check if a projectile is hit
        self.projectile_shot = False

        #Shooting cooldown timer
        self.shooting_cooldown = time.time()

        #Shield cooldown setting
        self.shield_cooldown = 10

        #Keeps track of how long a shield is displayed
        self.shield_timer = 0

        #Player lives and score that gets carried over to next levels
        self.lives = 5
        self.score = 0

        #Boolean to make sure a laser only hits the player once
        self.hit = True

    def control_player(self):
        #Boolean list of all keys pressed
        keys = stddraw.getKeysPressed()
        if self.player_num == 1:
            #Player 1 controls
            self.projectile_shot = controls1(self, keys)
        else:
            #Player 2 controls handler
            self.projectile_shot = controls2(self, keys)

    #Move player horizontally
    def move_circle(self, width: float, direction: int, speed: float):
        if self.x - self.radius < -1: #Prevents going off left edge
            self.x = -1 + self.radius
        if self.x + self.radius > width: #Prevents going off right edge
            self.x = 1 - self.radius
        self.x += direction * speed

    def clean_up(self):
        #Deletes projectiles that are out of the frame
        copy_projectile: list = []
        for projectile in self.projectiles:
            if 0 <= projectile.x <= 1 and 0 <= projectile.y <= 1:
                copy_projectile.append(projectile)

        self.projectiles = copy_projectile


    #Controls aiming direction
    def line_rotate(self, is_clockwise: bool, counterclockwise: bool, rotation_speed: float):
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

    def _pixel(self, px: float, py: float, color: Color):
        stddraw.setPenColor(color)
        px = (px + 1)/2
        py = (py + 1)/2
        stddraw.filledSquare(px, py, self.size)

    def draw_spaceship(self, line_length, change_color):
        hit_color = change_color
        is_hit = False
        # Tip of ship
        pixels = [(0, 10, hit_color)]

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
        #radian = math.radians(angle)-math.pi/2
        radians = math.radians(self.angle)

        # Draw each part of the ship after rotation(Relative to ship position)
        for dx, dy, color in pixels:
            self._pixel(self.x + dx * self.size, self.y + dy * self.size, color)

        # Optional: Draw a direction line
        end_x = self.x + line_length * math.cos(radians)
        end_y = self.y + line_length * math.sin(radians)
        stddraw.setPenRadius(0.01)
        stddraw.setPenColor(stddraw.RED)
        stddraw.line((self.x + 1)/2, (self.y + 1)/ 2 , (end_x + 1)/2, (end_y + 1)/2) #Shows where you are aiming

    def shoot(self, speed_projectile: float):
        if time.time() - self.shooting_cooldown > 0.8:
            radians = math.radians(self.angle) #Convert angles
            #Calculate movement direction
            dx = speed_projectile * math.cos(radians)
            dy = speed_projectile * math.sin(radians)

            projectile = Projectile((self.x + 1)/2, (self.y + 1)/2, dx, dy)
            self.projectiles.append(projectile)
            self.projectile_shot = False
            self.shooting_cooldown = time.time()

    def _draw_shield(self, x, y, radius, pen_radius) -> None:
        #Set shield color to Cyan
        stddraw.setPenColor(stddraw.CYAN)

        #List of points of hexagon
        points  = []
        for i in range(6):
            #Determine angle based so that the hexagon rotates
            angle = math.radians(60 * i + time.time() * 60)

            #Calculate vertices
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)

            #Add tuple of points to the list
            points.append((px, py))

        #Set pen radius
        stddraw.setPenRadius(pen_radius)

        #Draw the hexagon
        for i in range(6):
            x1, y1 = points[i - 1]
            x2, y2 = points[i]
            stddraw.line(x1, y1, x2, y2)

        #Restore pen color
        stddraw.setPenColor(stddraw.RED)

    def shield(self):
        #Check if the shield should be drawn based on cooldown
        if time.time() - self.shield_timer < self.shield_cooldown:
            #Convert co-ordinates from [-1, 1] to [0, 1]
            x = (self.x + 1) / 2
            y = (self.y + 1) / 2

            #Draw the shield with flickering
            if random.random() < 0.9:
                self._draw_shield(x, y, self.radius * 0.8, 0.005)
                self._draw_shield(x, y, self.radius * 0.9, 0.002)

    def draw_projectiles(self) -> None:
        for projectile in self.projectiles:
            #Draw projectile image
            stddraw.picture(Picture("assets/images/Projectile.png"), projectile.x, projectile.y)

    def move_projectiles(self):
        for projectile in self.projectiles:
            projectile.move()

    def check_hit_laser(self, enemy):
        #Check if player is hit
        if (self.x + 1) / 2 - self.radius * 0.65 <= enemy.x <= (self.x + 1) / 2 + self.radius * 0.65:
            if time.time() - self.shield_timer > self.shield_cooldown and not self.hit: #If not shielded subtract a life
                self.hit = True
                self.lives -= 1
            return True #Return true regardless of hit to make the laser not go over the player when shielded or not
        return False

    def check_hit_projectile(self, projectiles):
        projectiles_to_remove = [] #Array to make sure projectiles are not removed while iterating
        for projectile in projectiles[:]:
            #Check distance to determine a hit
            if math.hypot((self.x + 1)/2 - projectile.x, (self.y + 1)/2 - projectile.y) < self.radius * 0.7:
                if time.time() - self.shield_timer > self.shield_cooldown:
                    self.lives -= 1
                projectiles_to_remove.append(projectile) #Remove regardless of hit or shield hit

        #Return updates list of projectiles
        return [projectile for projectile in projectiles if projectile not in projectiles_to_remove]



def controls1(player: Player, keys: list):
    """
    Function that handles player controls built on a key array passed to the function

    Args:
        player: Player object to be moved
        keys: array of bools of each key that is pressed (True if pressed)

    Returns:
        True - Projectile is shot
        False - Projectile is not shot

    Author: Theunis
    """

    #Key to go right
    if keys[stddraw.K_d]:
        player.move_circle(1, 1, 0.02)

    #Key to go left
    elif keys[stddraw.K_a]:
        player.move_circle(1, -1, 0.02)

    #Key to rotate turret counterclockwise
    elif keys[stddraw.K_q]:
        player.line_rotate(False, True, 5)

    #Key to rotate turret clockwise
    elif keys[stddraw.K_e]:
        player.line_rotate(True, False, 5)

    #Key to shoot (Updates projectile_shot boolean)
    if keys[stddraw.K_w]:
        return True
    return False

def controls2(player: Player, keys: list):
    """
    Function that handles player controls built on a key array passed to the function

    Args:
        player: Player object to be moved
        keys: array of bools of each key that is pressed (True if pressed)

    Returns:
        True - Projectile is shot
        False - Projectile is not shot

    Author: Theunis
    """

    #Key to move right
    if keys[stddraw.K_l]:
        player.move_circle(1, 1, 0.02)

    #Key to move left
    elif keys[stddraw.K_j]:
        player.move_circle(1, -1, 0.02)

    #Key to rotate turret counterclockwise
    elif keys[stddraw.K_u]:
        player.line_rotate(False, True, 5)

    #Key to rotate turret clockwise
    elif keys[stddraw.K_o]:
        player.line_rotate(True, False, 5)

    #Key to shoot (Updates projectile_shot boolean)
    if keys[stddraw.K_i]:
        return True
    return False