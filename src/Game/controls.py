from src.Game.spaceship import Player
import stddraw

def controls(player: Player, keys):
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
    if keys[stddraw.K_RIGHT]:
        player.move_circle(1, 1, 0.02)
    elif keys[stddraw.K_LEFT]:
        player.move_circle(1, -1, 0.02)
    elif keys[stddraw.K_a]:
        player.line_rotate(False, True, 5)
    elif keys[stddraw.K_d]:
        player.line_rotate(True, False, 5)
    if keys[stddraw.K_UP]:
        return True
    return False