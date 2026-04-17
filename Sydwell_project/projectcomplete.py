import stdio
import stddraw
import math
import time
import random
import sys
from picture import Picture
import threading
import stdaudio
from Music.music import Music
 
def move_circle(x,radius,direction,speed):
    if x - radius < 0:
        x = radius
    if x + radius > 100:
        x = 100 - radius
    x += direction * speed
    return x

def line_rotate(angle , clockwise , counterclockwise , rotation_speed):
    if counterclockwise:
        angle += rotation_speed
        if angle >= 180:
            angle = 180
            counterclockwise = False

    if clockwise:
        angle -= rotation_speed
        if angle <= 0:
            angle = 0
            clockwise = True

    return angle , counterclockwise , clockwise

def pixel(px, py, color):
    size=0.5
    stddraw.setPenColor(color)
    stddraw.filledSquare(px, py, size)

def draw_spaceship(x, y, radius, angle, line_length,change_color,is_hit=False):
    size = 0.5  # Size of each pixel/block
    hit_color=change_color if is_hit else stddraw.WHITE

    # Define the spaceship shape using relative coordinates (dx, dy, color)
    pixels = []

    # Tip
    pixels.append((0, 10, hit_color))

    # Layered wings and body using for loops
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

    # Draw each part of the ship after rotation
    for dx, dy, color in pixels:
        pixel(x + dx * size, y + dy * size, color)

    # Optional: Draw a direction line
    end_x = x + line_length * math.cos(radians)
    end_y = y + line_length * math.sin(radians)
    stddraw.setPenColor(stddraw.RED)
    stddraw.line(x, y, end_x, end_y)

def shoot(x,y,angle,speed_projectile):
    radians = math.radians(angle)
    dx = speed_projectile * math.cos(radians)
    dy = speed_projectile * math.sin(radians)

    Music.sound(1000,44100)

    return {'x':x , 'y':y , 'dx':dx , 'dy':dy}

def is_enemy_hit_by_laser(enemy, laser_origin, laser_direction, enemy_radius):
    ex  = enemy['x']
    ey  = enemy['y']
    lx, ly = laser_origin
    dx, dy = laser_direction

    #playsound("Explode")
                    
    numerator = abs((ey - ly) * dx - (ex - lx) * dy)
    denominator = math.hypot(dx, dy)
    distance = numerator / denominator
    return distance <= enemy_radius

def create_enemies(level):
    enemies = []
    enemy_r = 5
    enemy_rows = 2
    enemy_col  = 5
    enemy_spacing = 15
    enemy_x = 15
    enemy_y = 90

    for row in range(enemy_rows):
        for col in range(enemy_col):
            x_pos = enemy_x + col * enemy_spacing
            y_pos = enemy_y - row * enemy_spacing
            color = stddraw.BLUE if level == 1 else stddraw.RED if row == 1 else stddraw.BLUE
            enemies.append({'x': x_pos,'y':y_pos, 'color': color})
    return enemies
def enemy_update(enemies, enemy_dir,enemy_speed, enemy_radius):
    should_decend = False

    for enemy in enemies:
        next_x = enemy['x'] + enemy_dir * enemy_speed
        if next_x + enemy_radius > 100 or next_x - enemy_radius < 0:
            should_decend = True
            break
    
    for enemy in enemies:
        if should_decend:
            enemy['y'] -= 5
        else:
            enemy['x'] += enemy_dir * enemy_speed

    if should_decend:
        enemy_dir *= -1

    return enemies, enemy_dir
def startscreen():
    stddraw.setPenColor(stddraw.WHITE)
    stddraw.setFontSize(30)
    stddraw.text(50,90,"COSMIC CONQUISTADORS")
    stddraw.setFontSize(25)
    stddraw.text(50,80,"INSTRUCTIONS:")

    stddraw.setFontSize(22)

    stddraw.text(50,70, "PLAYER ONE (RED)")
    stddraw.text(50,65,"[A]move left,[S]stop move,[D]move right") 
    stddraw.text(50,60,"[Q]rotate left,[W]stop rotate,[E]rotate right")
    stddraw.text(50,55,"[SPACE] to shoot")

    stddraw.text(50,45, "PLAYER TWO (GREEN)")
    stddraw.text(50,40, "[J]move left,[K]stop move,[L]move right") 
    stddraw.text(50,35,"[I]rotate left,[O]stop rotate,[P]rotate right")
    stddraw.text(50,30,"[M] to shoot")

    stddraw.text(50,20,"[X] to quit")
    stddraw.text(50,10,"PRESS ANY KEY TO START")
    stddraw.show(50)

def main():

    with open('../src/Stored/Highscore.txt', 'r') as f:
        line = f.read().strip()

    if line == "":
        highscore = 99999
    else:
        highscore = float(line)

        
    stddraw.setCanvasSize(500,500)
    stddraw.setXscale(0,100)
    stddraw.setYscale(0,100)
    Logo=Picture("Logo.png")
    stddraw.picture(Logo)
    stddraw.show(500)

    Music.play("Music")
    
    # Game setup
    hit_flash_duration=0.5
    hit_p1=False
    hit_p2=False
    hit_time_p1=0
    hit_time_p2=0
    change_color=stddraw.WHITE
    
    # Starfield background
    numstars=100
    size=0.5
    vy=0.2
    stars=[]
    for i in range(numstars):
        a = random.randint(0,100)
        b = random.randint(0, 100)
        stars.append([a, b])
    
    level = 1
    skip_intro = False
    
    # Initialize boss variables
    boss = {'x': 50, 'y': 90, 'r':10, 'dir': 1}
    boss_health = 10
    boss_projectiles = []
    last_boss_shot_time = time.time()
    
    # Initialize bunkers for all levels
    bunkers = []
    bunker_hitpoints = []
    for i in range(4):
        x_pos = 20 + i * 20
        bunkers.append({'x': x_pos, 'y': 25})
        bunker_hitpoints.append(2)
    
    while True:
        while True:
            if not skip_intro:
                 stddraw.clear(stddraw.BLACK)
                 stddraw.setPenColor(stddraw.WHITE)
                 for star in stars:
                    x,y=star
                    stddraw.filledSquare(x,y,size)
                    star[1]-=vy
                    if star[1]<0:
                        star[0]=random.randint(0,100)
                        star[1]=100

                 startscreen()
                 if stddraw.hasNextKeyTyped():
                     stddraw.nextKeyTyped()
                     break
            else:
                skip_intro = False
                break     
            stddraw.clear()

        starttime = time.time()

        # Player 1 setup
        x = 50
        y = 10
        direction = 0
        speed = 1.5
        radius = 5
        angle = 90
        line_length = 6
        rotation_speed = 1
        counterclockwise = False
        clockwise = False
        last_shot = 0
        projectiles = []

        # Player 2 setup
        x2 = 30
        y2 = 10
        direction2 = 0
        angle2 = 90
        clockwise2 = False
        counterclockwise2 = False
        last_shot2 = 0
        projectiles2 = []

        # Enemies setup
        enemy_projectiles = []
        last_enemy_shot_time = time.time()
        enemies = []
        enemy_r = 5
        enemy_rows = 2
        enemy_col  = 5
        enemy_spacing = 15
        enemy_x = 15
        enemy_y = 90
        enemy_dir = 1
        enemy_speed = 0.25

        # Powerups setup
        powerups = []
        last_powerup_time = time.time()
        laser_ready = False
        laser_ready2 = False
        shield_active = False
        shield_active2 = False

        # Game state
        game_over = False
        lives = 5
        game_over_message = ""

        enemies = create_enemies(level)
        
        while True:
            current_time = time.time()
            stddraw.clear(stddraw.BLACK)
            stddraw.setPenColor(stddraw.WHITE)
            
            # Draw starfield background
            for star in stars:
                a,b=star
                stddraw.filledSquare(a,b,size)
                star[1]-=vy
                if star[1]<0:
                    star[0]=random.randint(0,100)
                    star[1]=100
            
            # Draw bunkers for levels 2 and 3
            if level >= 2:
                for i in range(len(bunkers)):
                    if bunker_hitpoints[i] > 0:
                        # Different colors based on hitpoints
                        if level == 2:
                            color = stddraw.GREEN if bunker_hitpoints[i] == 2 else stddraw.ORANGE
                        else:  # level 3
                            if bunker_hitpoints[i] >= 3:
                                color = stddraw.GREEN
                            elif bunker_hitpoints[i] == 2:
                                color = stddraw.ORANGE
                            else:
                                color = stddraw.RED
                        stddraw.setPenColor(color)
                        stddraw.filledRectangle(bunkers[i]['x'] - 3, bunkers[i]['y'], 6, 6)

            # Level 3 boss logic
            if level == 3: 
                boss['x'] += boss['dir'] * 0.5
                if boss['x'] - boss['r'] <= 0 or boss['x'] + boss['r'] >= 100:
                    boss['dir'] *= -1

                # Check for projectile collisions with boss
                new_projectiles = []
                for p in projectiles:
                    p['x'] += p['dx']
                    p['y'] += p['dy']
                    if 0 <= p['x'] <= 100 and 0 <= p['y'] <= 100:
                        if math.hypot(p['x'] - boss['x'], p['y'] - boss['y']) < boss['r'] + 1:
                            boss_health -= 1

                            #playsound("Explode")

                        else:
                            stddraw.picture(Picture("Projectile.png"), p['x'], p['y'])
                            new_projectiles.append(p)
                projectiles = new_projectiles

                # Player 2 projectiles
                new_projectiles2 = []
                for p2 in projectiles2:
                    p2['x'] += p2['dx']
                    p2['y'] += p2['dy']
                    if 0 <= p2['x'] <= 100 and 0 <= p2['y'] <= 100:
                        if math.hypot(p2['x'] - boss['x'], p2['y'] - boss['y']) < boss['r'] + 1:
                            boss_health -= 1

                            #playsound("Explode")

                        else:
                            stddraw.picture(Picture("Projectile.png"), p2['x'], p2['y'])
                            new_projectiles2.append(p2)
                projectiles2 = new_projectiles2

                # Boss shooting
                if time.time() - last_boss_shot_time >= 2:
                    angles = [-45, -22.5, 0, 22.5, 45] 
                    for a in angles:
                        radians = math.radians(270 + a)
                        dx = 2 * math.cos(radians)
                        dy = 2 * math.sin(radians)
                        boss_projectiles.append({'x': boss['x'], 'y': boss['y'], 'dx': dx, 'dy': dy})
                    last_boss_shot_time = time.time()

                # Draw boss
                stddraw.picture(Picture("Boss.png"),boss['x'],boss['y'])

                # Handle boss projectiles
                new_boss_projectiles = []
                for p in boss_projectiles:
                    p['x'] += p['dx']
                    p['y'] += p['dy']
                    if 0 <= p['x'] <= 100 and 0 <= p['y'] <= 100:
                        # Check bunker collisions first
                        hit_bunker = False
                        for i in range(len(bunkers)):
                            if bunker_hitpoints[i] > 0 and abs(p['x'] - bunkers[i]['x']) < 4 and abs(p['y'] - bunkers[i]['y']) < 3:
                                bunker_hitpoints[i] -= 1
                                hit_bunker = True
                                break
                        
                        if not hit_bunker:
                            stddraw.picture(Picture("EnemyProjectile.png"),p['x'],p['y'])
                            
                            if math.hypot(p['x'] - x, p['y'] - y) < radius + 1:
                                if shield_active:
                                    shield_active = False
                                else:
                                    lives -= 1

                                    #playsound("Explode")

                                continue
                            if math.hypot(p['x'] - x2, p['y'] - y2) < radius + 1:
                                if shield_active2:
                                    shield_active2 = False
                                else:
                                    lives -= 1

                                    #playsound("Explode")

                                continue
                            new_boss_projectiles.append(p)
                boss_projectiles = new_boss_projectiles
                
                # Draw boss health bar
                for i in range(10):
                    if i < boss_health:
                        stddraw.setPenColor(stddraw.RED)
                    else:
                        stddraw.setPenColor(stddraw.WHITE)
                    stddraw.filledRectangle(5 + i*3 , 95, 3, 2)

                if boss_health <= 0:
                    game_over = True
                    game_over_message = "Victory!!!"
                    level = 1

                if lives <= 0:
                    game_over = True
                    game_over_message = "Game Over! All lives lost"
                    level = 1

            # Draw UI elements
            stddraw.setPenColor(stddraw.RED)
            stddraw.setFontSize(14)
            stddraw.text(85,5,f"Lives remaining {lives}")
            
            # Draw lives as hearts
            for i in range(lives):
                stddraw.picture(Picture("Heart.png"),4+i*8,4)
                
            # Handle game over state
            if game_over:
                stddraw.setPenColor(stddraw.RED if "Game Over" in game_over_message else stddraw.GREEN)
                stddraw.setFontSize(25)
                stddraw.text(50,60,game_over_message)


                #HIGHSCORE DISPLAY

                endtime = time.time()


                stddraw.setFontSize(20)
                if "Game Over" in game_over_message:
                    stddraw.text(50, 20, "Score: DNF")
                    Music.play("Defeat")
                else:
                    score = round(endtime-starttime, 2)

                    if score < highscore:
                        highscore = score

                        with open('../src/Stored/Highscore.txt', 'w') as f:
                            f.write(str(highscore))

                    stddraw.text(50, 20, "Score: " + str(score))
                    stddraw.text(50, 10, "Highscore: " + str(highscore))

                    Music.play("Victory")

                if highscore == 99999:
                    stddraw.text(50, 10, "Highscore: NO HIGHSCORE YET")
                else:
                    stddraw.text(50, 10, "Highscore: " + str(highscore))

                stddraw.show(20)
                stddraw.setFontSize(15)
                stddraw.text(50,40,"Game Restarting in 5 seconds!")
                stddraw.show(20)
                time.sleep(3)
                
                while True:
                    stddraw.clear(stddraw.BLACK)
                    stddraw.setPenColor(stddraw.WHITE)
                    for star in stars:
                        x,y=star
                        stddraw.filledSquare(x,y,size)
                        star[1]-=vy
                        if star[1]<0:
                            star[0]=random.randint(0,100)
                            star[1]=100
                    startscreen()
                    if stddraw.hasNextKeyTyped():
                        stddraw.nextKeyTyped()
                        break
                level = 1
                skip_intro = True
                break
                
            # Check for game over conditions
            if level < 3:
                for enemy in enemies:
                    if enemy['y'] - enemy_r <= 0:
                        game_over = True
                        game_over_message = "Game Over"
                        level = 1
                        break
                    elif math.hypot(enemy['x'] - x, enemy['y'] - y) <= enemy_r + radius:
                        game_over = True
                        game_over_message = "Game Over"
                        level = 1
                        break

            # Level progression
            if not game_over and not enemies and level < 3:
                if level == 1:
                    stddraw.setPenColor(stddraw.GREEN)
                    stddraw.setFontSize(25)
                    stddraw.text(50, 60, "Level 2 Starting...")
                    stddraw.show(100)
                    time.sleep(3)

                    level = 2
                    enemies = create_enemies(level)
                    projectiles = []
                    projectiles2 = []
                    enemy_projectiles = []
                    # Reset bunkers for level 2
                    bunkers = []
                    bunker_hitpoints = []
                    for i in range(4):
                        x_pos = 20 + i * 20
                        bunkers.append({'x': x_pos, 'y': 25})
                        bunker_hitpoints.append(2)
                    continue
                elif level == 2:
                    stddraw.setPenColor(stddraw.ORANGE)
                    stddraw.setFontSize(25)
                    stddraw.text(50, 60, "Final Boss Incoming...")
                    stddraw.show(100)
                    time.sleep(3)

                    level = 3
                    boss = {'x': 50, 'y': 90, 'r':10, 'dir': 1}
                    boss_health = 10 
                    boss_projectiles = []
                    last_boss_shot_time = time.time()
                    enemy_projectiles = []
                    projectiles = []
                    projectiles2 = []
                   
                    # Reset bunkers for level 3 with more hitpoints
                    bunkers = []
                    bunker_hitpoints = []
                    for i in range(4):
                        x_pos = 20 + i * 20
                        bunkers.append({'x': x_pos, 'y': 25})
                        bunker_hitpoints.append(3)
                    continue
                else:
                    game_over = True
                    game_over_message = "Victory!!!"
                    level = 1

            # Draw spaceships
            draw_spaceship(x, y, radius, angle, line_length, change_color,
                          hit_p1 and (current_time - hit_time_p1 < hit_flash_duration) and int((current_time - hit_time_p1) * 16) % 2 == 0)
            draw_spaceship(x2, y2, radius, angle2, line_length, change_color,
                          hit_p2 and (current_time - hit_time_p2 < hit_flash_duration) and int((current_time - hit_time_p2) * 16) % 2 == 0)

            # Draw shields if active
            if shield_active:
                stddraw.setPenColor(stddraw.BLUE)
                stddraw.circle(x,y,6)
            if shield_active2: 
                stddraw.setPenColor(stddraw.BLUE)
                stddraw.circle(x2,y2,6)

            # Handle projectiles for levels 1 and 2
            if level < 3:
                new_projectiles = []
                new_projectiles2 = []
                new_enemies =[]

                # Player 1 projectiles
                for p in projectiles:
                    p['x'] += p['dx']
                    p['y'] += p['dy']
                    hit = False
                    for e in enemies:
                        if math.hypot(p['x'] - e['x'], p['y'] - e['y']) < enemy_r + 1:
                            hit = True

                            #playsound("Explode")

                            break

                    if not hit and 0 <= p['x'] <= 100 and 0 <= p['y'] <= 100:
                        stddraw.picture(Picture("Projectile.png"),p['x'],p['y'])
                        new_projectiles.append(p)

                # Player 2 projectiles
                for p2 in projectiles2:
                    p2['x'] += p2['dx']
                    p2['y'] += p2['dy']
                    hit = False
                    for e in enemies:
                        if math.hypot(p2['x'] - e['x'], p2['y'] - e['y']) < enemy_r + 1:
                            hit = True

                            #playsound("Explode")

                            break

                    if not hit and 0 <= p2['x'] <= 100 and 0 <= p2['y'] <= 100:
                        stddraw.picture(Picture("Projectile.png"),p2['x'],p2['y'])
                        new_projectiles2.append(p2)

                # Check which enemies were hit
                for e in enemies:
                    hit_by_p1 = any(math.hypot(p['x'] - e['x'], p['y'] - e['y']) < enemy_r + 1 for p in projectiles)
                    hit_by_p2 = any(math.hypot(p2['x'] - e['x'], p2['y'] - e['y']) < enemy_r + 1 for p2 in projectiles2)
                    if not (hit_by_p1 or hit_by_p2):
                        new_enemies.append(e)

                projectiles = new_projectiles
                projectiles2 = new_projectiles2
                enemies = new_enemies
                                                                    
            # Enemy shooting
            current_time = time.time()
            if current_time - last_enemy_shot_time >=1 and enemies:
                shooter = random.choice(enemies)
                projectile_speed = -1 if level == 1 else -2
                projectile ={ 'x':shooter['x'],'y':shooter['y'],'dx':0,'dy':projectile_speed}
                enemy_projectiles.append(projectile)

                Music.sound(600, 44100)

                last_enemy_shot_time = current_time

            # Draw enemies
            i = int(time.time() % 1 < 0.5)
            for enemy in enemies:
                stddraw.setPenColor(enemy['color'])

                alien_shape = [
                    [0, 1, 0, 1, 0, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 1, 1, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1],
                    [0, 1, 1, 0, 1, 1, 0],
                    [i+1, i, 0, 0, 0, i, i+1],
                    [i+1, i, 0, 0, 0, i, i+1],
                ]
                pixel_size = radius / 4
                grid_size = len(alien_shape)

                # Calculate top-left starting point to center the alien
                start_x = enemy['x'] - (grid_size / 2) * pixel_size
                start_y = enemy['y'] + (grid_size / 2) * pixel_size

                for row in range(grid_size):
                    for col in range(grid_size):
                        if alien_shape[row][col] == 1:
                            xcod = start_x + col * pixel_size
                            ycod = start_y - row * pixel_size
                            stddraw.filledSquare(xcod, ycod, pixel_size / 2)
                
            # Handle enemy projectiles
            stddraw.setPenColor(stddraw.RED)
            new_enemy_projectiles = []

            for p in enemy_projectiles:
                p['x'] += p['dx']
                p['y'] += p['dy']
                hit_player = False

                # Check bunker collisions first
                hit_bunker = False
                if level >= 2:
                    for i in range(len(bunkers)):
                        if bunker_hitpoints[i] > 0 and abs(p['x'] - bunkers[i]['x']) < 4 and abs(p['y'] - bunkers[i]['y']) < 3:
                            bunker_hitpoints[i] -= 1
                            hit_bunker = True
                            break

                if not hit_bunker:
                    if math.hypot(p['x']-x,p['y']-y) < radius + 1:
                        if shield_active:
                            shield_active = False
                        else:
                            lives -= 1
                        hit_player = True
                        hit_p1=True
                        change_color=stddraw.RED
                        hit_time_p1=time.time()

                        #playsound("Explode")

                    if math.hypot(p['x']-x2,p['y']-y2) < radius + 1:
                        if shield_active2:
                            shield_active2 = False
                        else:
                            lives -= 1
                        hit_player = True
                        hit_p2=True
                        change_color=stddraw.RED
                        hit_time_p2=time.time()

                        #playsound("Explode")

                    if lives <=0:
                        game_over = True
                        game_over_message = "Game Over! All lives lost"
                        level = 1

                    if not hit_player and p['y']>0:
                        stddraw.picture(Picture("EnemyProjectile.png"),p['x'],p['y']) 
                        new_enemy_projectiles.append(p)

            enemy_projectiles = new_enemy_projectiles

            # Handle powerups
            if current_time - last_powerup_time >= 5:
                powerup_type = random.choice(['laser','shield','heart'])
                new_powerup = {'x': random.uniform(10, 90), 'y': 100, 'type': powerup_type, 'active': True}
                powerups.append(new_powerup)
                last_powerup_time = current_time

            new_powerups = []

            for p in powerups:
                p['y'] -= 0.5
                if p['y'] < 0:
                    continue

                if p['type'] == 'laser':
                    stddraw.picture(Picture("Star.png"),p['x'],p['y'])                  
                elif p['type'] == 'shield':
                    stddraw.picture(Picture("Shield.png"),p['x'],p['y'])   
                    stddraw.setPenColor(stddraw.BLUE)
                    stddraw.circle(p['x'],p['y'],3)
                elif p['type'] == 'heart':
                    stddraw.picture(Picture("Heart.png"),p['x'],p['y'])

                # Collision with p1
                if math.hypot(p['x'] - x, p['y'] - y) < radius + 2:
                    if p['type'] == 'laser':
                        laser_ready = True
                        hit_p1=True
                        change_color=stddraw.YELLOW
                        hit_time_p1=time.time()

                        Music.sound(1000,10000)

                    elif p['type'] == 'shield':
                        shield_active = True
                        hit_p1=True
                        change_color=stddraw.BLUE
                        hit_time_p1=time.time()

                        Music.sound(1000,10000)

                    elif p['type'] == 'heart':
                        hit_p1=True
                        change_color=stddraw.PINK
                        hit_time_p1=time.time()
                        lives += 1

                        Music.sound(1000,10000)

                    continue

                # Collision with p2
                elif math.hypot(p['x'] - x2, p['y'] - y2) < radius + 2:
                    if p['type'] == 'laser':
                        laser_ready2 = True
                        hit_p2=True
                        change_color=stddraw.GREEN
                        hit_time_p2=time.time()

                        Music.sound(1000,10000)


                    elif p['type'] == 'shield':
                        shield_active2 = True
                        hit_p2=True
                        change_color=stddraw.BLUE
                        hit_time_p2=time.time()

                        Music.sound(1000,10000)

                    elif p['type'] == 'heart':
                        hit_p2=True
                        change_color=stddraw.PINK
                        hit_time_p2=time.time()
                        lives += 1

                        Music.sound(1000,10000)
                    continue

                new_powerups.append(p)

            powerups = new_powerups

            # Handle keyboard input
            if stddraw.hasNextKeyTyped():
                key = stddraw.nextKeyTyped()

                # Player 1 controls
                if key == 'a':                 #move left
                    direction = -1
                elif key == 'd':               #move right
                    direction = 1
                elif key == 's':               #stop moving
                    direction = 0
                elif key == 'q':               #rotate line counterclockwise
                    counterclockwise = True
                    clockwise = False
                elif key == 'e':               #rotate line clockwise
                    clockwise = True
                    counterclockwise = False
                elif key == 'w':               #stop rotation
                    counterclockwise = False
                    clockwise = False
                elif key == ' ':               #shoot projectile
                    current_time = time.time()
                    if current_time - last_shot >= 1 : 
                        if laser_ready:
                            laser_ready = False
                            radians = math.radians(angle)
                            laser_dx = math.cos(radians)
                            laser_dy = math.sin(radians)
                            laser_length = 100  
                            laser_end_x = x + laser_dx * laser_length
                            laser_end_y = y + laser_dy * laser_length
                            stddraw.setPenRadius(0.8)
                            stddraw.setPenColor(stddraw.YELLOW)
                            stddraw.line(x, y, laser_end_x, laser_end_y)
                            stddraw.setPenRadius(0.002)
                            
                            if level == 3:
                                boss_hit = is_enemy_hit_by_laser(boss, (x, y), (laser_dx, laser_dy), boss['r'])
                                if boss_hit:
                                    boss_health -= 2
                            else:
                                enemies = [e for e in enemies if not is_enemy_hit_by_laser(e,(x,y),(laser_dx,laser_dy),enemy_r)]
                        else:
                            speed_projectile = 2
                            projectile = shoot(x,y,angle,speed_projectile)
                            projectiles.append(projectile)
                        last_shot = current_time
                elif key == 'x':
                    return
                
                # Player 2 controls
                if key == 'j':                 #move left
                    direction2 = -1
                elif key == 'l':              #move right
                    direction2 = 1
                elif key =='k':               #stop moving
                    direction2 = 0
                elif key == 'u':               #rotate line counterclockwise
                    counterclockwise2 = True
                    clockwise2 = False
                elif key == 'o':               #rotate line clockwise
                    counterclockwise2 = False
                    clockwise2 = True
                elif key =='i':                #stop rotation
                    counterclockwise2 = False
                    clockwise2 = False
                elif key == 'm':               #shoot projectile
                    current_time = time.time()
                    if current_time - last_shot2 >= 1:
                        if laser_ready2:  
                            laser_ready2 = False
                            radians2 = math.radians(angle2)
                            laser_dx2 = math.cos(radians2)
                            laser_dy2 = math.sin(radians2)
                            laser_length2 = 100  
                            laser_end_x2 = x2 + laser_dx2 * laser_length2
                            laser_end_y2 = y2 + laser_dy2 * laser_length2
                            stddraw.setPenRadius(0.8)
                            stddraw.setPenColor(stddraw.YELLOW)
                            stddraw.line(x2, y2, laser_end_x2, laser_end_y2) 
                            stddraw.setPenRadius(0.002)

                            if level == 3:
                                boss_hit = is_enemy_hit_by_laser(boss, (x2, y2), (laser_dx2, laser_dy2), boss['r'])
                                if boss_hit:
                                    boss_health -= 2
                            else:
                                enemies = [e for e in enemies if not is_enemy_hit_by_laser(e,(x2,y2),(laser_dx2,laser_dy2),enemy_r)]
                        else:
                            speed_projectile2 = 2
                            projectile2 = shoot(x2,y2,angle2,speed_projectile2)
                            projectiles2.append(projectile2)
                        last_shot2 = current_time

            # Update angles and positions
            angle , counterclockwise ,clockwise = line_rotate(angle,clockwise,counterclockwise,rotation_speed)
            angle2 , counterclockwise2 ,clockwise2 = line_rotate(angle2,clockwise2,counterclockwise2,rotation_speed)

            x = move_circle(x,radius,direction,speed)
            x2 = move_circle(x2,radius,direction2,speed)
            
            enemies , enemy_dir = enemy_update(enemies, enemy_dir,enemy_speed,enemy_r)
            stddraw.show(20)


if __name__ == "__main__":
    main()
