def is_enemy_hit_by_laser(enemy, laser_origin, laser_direction, enemy_radius):
    #Enemy position
    ex  = enemy['x']
    ey  = enemy['y']

    #Laser start + direction
    lx, ly = laser_origin
    dx, dy = laser_direction

    #playsound("Explode")

    #Distance from line formula                
    numerator = abs((ey - ly) * dx - (ex - lx) * dy)
    denominator = math.hypot(dx, dy)
    distance = numerator / denominator
    return distance <= enemy_radius #Hit if close enough

def create_enemies(level):
    enemies = []
    enemy_r = 5
    enemy_rows = 2
    enemy_col  = 5
    enemy_spacing = 15
    enemy_x = 15
    enemy_y = 90

    #Create grid
    for row in range(enemy_rows):
        for col in range(enemy_col):
            x_pos = enemy_x + col * enemy_spacing
            y_pos = enemy_y - row * enemy_spacing
            #Level-based coloring
            color = stddraw.BLUE if level == 1 else stddraw.RED if row == 1 else stddraw.BLUE
            enemies.append({'x': x_pos,'y':y_pos, 'color': color})
    return enemies

def enemy_update(enemies, enemy_dir,enemy_speed, enemy_radius):
    should_decend = False

    for enemy in enemies:
        next_x = enemy['x'] + enemy_dir * enemy_speed
        #Check wall collision
        if next_x + enemy_radius > 100 or next_x - enemy_radius < 0:
            should_decend = True
            break
    
    for enemy in enemies:
        #Move enemies
        if should_decend:
            enemy['y'] -= 5
        else:
            enemy['x'] += enemy_dir * enemy_speed
            
    #Reverse direction
    if should_decend:
        enemy_dir *= -1

    return enemies, enemy_dir
