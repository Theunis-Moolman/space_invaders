from src.Game.spaceship import Player
import stddraw

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
    if keys[stddraw.K_d]:
        player.move_circle(1, 1, 0.02)
    elif keys[stddraw.K_a]:
        player.move_circle(1, -1, 0.02)
    elif keys[stddraw.K_q]:
        player.line_rotate(False, True, 5)
    elif keys[stddraw.K_e]:
        player.line_rotate(True, False, 5)
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
    if keys[stddraw.K_l]:
        player.move_circle(1, 1, 0.02)
    elif keys[stddraw.K_j]:
        player.move_circle(1, -1, 0.02)
    elif keys[stddraw.K_o]:
        player.line_rotate(False, True, 5)
    elif keys[stddraw.K_u]:
        player.line_rotate(True, False, 5)
    if keys[stddraw.K_i]:
        return True
    return False