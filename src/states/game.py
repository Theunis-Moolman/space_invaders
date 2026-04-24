import stddraw

from src.Game.enemies import Enemies, Boss
from src.Game.spaceship import Player, Projectile
import random
from color import Color
from src.Game.powerups import PowerUpHandler
from src.states.end import EndPage
import time
from src.Music.music import Music
import math
from src.states.victory import Victory


class Level1:
    """
    Level 1 with players not shooting back at all
    Basic space invaders type game play

    Args:
        width: width of the game window
        height: height of the game window


    Author: Sydwell and Theunis
    """

    def __init__(self, width: int, height: int, multiplayer: bool, highscore: int):
        # Keep track of player score
        self.score: int = 0

        # Check if player is alive
        self.alive: bool = True

        # Array of players to handle multi-player case
        self.players = []

        # Keep track of player high score
        self.highscore = highscore

        # Multiplayer bool for setting multiplayer mode
        self.multiplayer: bool = multiplayer

        # Create players depending on multiplayer setting
        if multiplayer:
            self.players.append(Player(0.1, -0.85, 0.2, 0, 0, 90, 1))
            self.players.append(Player(0.9, -0.85, 0.2, 0, 0, 90, 2))
        else:
            self.players.append(Player(0.1, -0.85, 0.2, 0, 0, 90, 1))

        # List of all enemy objects
        self.enemies = Enemies()

        # Keep track of width and height for dynamic star size generation
        self.width = width
        self.height = height

        # Set enemy speed
        self.enemy_speed = 0.001

        # Set initial enemy direction (To the right)
        self.enemy_dir = 1

        # Create enemies (5 by 5)
        self.enemies.create_enemies(1, 5, 5)

        # Keep track of how long the player has been dead
        self.death_timer = 0

        # Music handler
        self.music = Music()

        # Preload the level1 music
        self.music.load(["assets/Music/level1"])

        # Play level 1 music in a continuous loop
        self.music.play("assets/Music/level1", loop=True)

        # Variable for handling self.end_page
        self.end_page = None

        # List of star co-ordinates, radii and colors
        self.stars = []

        # Generate 600 stars
        for i in range(600):
            # Generate random star co-ordinate
            rand_x = random.random()
            rand_y = random.random()

            # Generate random radius for variable star size
            radius = random.random() * min(self.width, self.height) / 500000
            #

            # Set color of star with Color(130 to 220, 130 - 220, 255) -> Values found through experimentation
            colour = Color(random.randrange(130, 220), random.randrange(130, 220), 255)

            # Append stars to list of stars
            self.stars.append((rand_x, rand_y, radius, colour))

    def draw(self) -> None:
        # Clear the canvas
        stddraw.clear()

        # Draw a black background
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        # Draw all the stars
        for x, y, radius, colour in self.stars:
            probability = random.random()

            # Using probability to create a flickering effect for the stars
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        # Check if the player has died and continue with game if not
        if not self.enemies.check_death():
            # Smaller pen radius for line to determine where the enemies hit the player will die
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)

            # Create a dotted line where if the enemy hit this line the player dies
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            # Go through each player object
            for i, player in enumerate(self.players):
                # Different colors for each player
                if i % 2 == 0:
                    player.draw_spaceship(0.1, stddraw.WHITE)
                else:
                    player.draw_spaceship(0.1, stddraw.LIGHT_GRAY)

                # List to keep track of projectiles to remove to make sure objects aren't removed while iterating
                projectiles_to_remove = None
                for projectile in player.projectiles:
                    # Check if an enemy is hit, update score, delete projectile and make enemies faster
                    if self.enemies.check_hit(projectile):
                        player.score += 100
                        self.enemy_speed += 0.00008
                        projectiles_to_remove = projectile
                        break
                # Delete the projectile used to destroy an enemy object
                if projectiles_to_remove is not None:
                    player.projectiles.remove(projectiles_to_remove)

                # Update projectile co-ordinates
                player.move_projectiles()

                # Draw all the projectiles
                player.draw_projectiles()

                # Check for player controls
                player.control_player()

                # Check if player shoots
                if player.projectile_shot:
                    player.shoot(0.008)

                # Clean up projectiles that have left the screen
                player.clean_up()

            # Handle enemy movement
            self.enemy_dir = self.enemies.enemy_update(
                self.enemy_dir, self.enemy_speed, self.enemy_speed * 12, False
            )
            # Draw enemies
            self.enemies.draw_enemies()
        else:
            if self.alive:
                # Stop music to prevent audio clashes
                self.music.stop()

                # Keep track of how long the player is dead
                self.death_timer = time.time()
            if self.end_page is None:
                # Create an end page that counts down before restarting
                self.end_page = EndPage(
                    self.width, self.height, self.players, time.time(), self.highscore
                )

            # Draw the end page
            self.end_page.draw()

            # Update that the player is dead
            self.alive = False

        # Draw scores and lives of the players
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0.85, 1, 0.15)
        stddraw.setPenColor(stddraw.ORANGE)
        stddraw.setFontSize(20)
        if not self.multiplayer:
            stddraw.text(0.3, 0.9, f"Score: {self.players[0].score}")
            stddraw.text(0.6, 0.9, f"Lives: {self.players[0].lives}")
        else:
            stddraw.text(0.225, 0.95, "PLAYER 1")
            stddraw.text(0.125, 0.9, f"Score: {self.players[0].score}")
            stddraw.text(0.4, 0.9, f"Lives: {self.players[0].lives}")
            stddraw.text(0.8, 0.95, "PLAYER 2")
            stddraw.text(0.65, 0.9, f"Score: {self.players[1].score}")
            stddraw.text(0.9, 0.9, f"Lives: {self.players[1].lives}")

        stddraw.show(20)

        # Check if game is completed to stop music to prevent audio clashes in the next level
        if self.check_completion():
            self.music.stop()

    def run(self):
        # Draw the level 1 page
        self.draw()

        # Array of bools of all keys pressed to handle escape
        keys = stddraw.getKeysPressed()

        # Check if escape is pressed to stop the game
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"

        # Check if r is pressed in end game page to restart the game before 5 seconds are over
        if not self.alive and (keys[stddraw.K_r] or time.time() - self.death_timer > 5):
            self.end_page.stop_music()
            return "RESTART"

        # Default to continue game play state
        return "PLAY"

    def check_completion(self):
        # Completion condition
        return len(self.enemies.enemies) == 0


class Level2:
    """
    Level 2 with the following additional features:
        - Enemies shooting lasers
        - Power ups:
            - Heart: Extra life
            - Star: Bonus points(500)
            - Shield: Blocking enemy laser

    Args:
        width: width of the game window
        height: height of the game window
        stars: array of co-ordinates for stars from previous level

    Author: Sydwell and Theunis
    """

    def __init__(
        self,
        width: int,
        height: int,
        stars: list,
        multiplayer: bool,
        players,
        highscore: int,
    ):
        # Check if player is alive
        self.alive: bool = True

        # Array of players to handle multi-player case
        self.players = players

        # Reset projectile state for all players carried over from previous level
        for player in players:
            player.projectile_shot = False
            player.projectiles = []

        # Keep track of player high score
        self.highscore = highscore

        # List of all enemy objects
        self.enemies = Enemies()

        # Keep track of width and height for dynamic star size generation
        self.width = width
        self.height = height

        # Multiplayer bool for setting multiplayer mode
        self.multiplayer = multiplayer

        # Set enemy speed
        self.enemy_speed = 0.001

        # Bool for blocking enemy laser
        self.block = False

        # Music handler
        self.music = Music()

        # Preload level 2 music and enemy shoot sound effect
        self.music.load(["assets/Music/enemy_shoot", "assets/Music/level2"])

        # Play level 2 music in a continuous loop
        self.music.play("assets/Music/level2", loop=True)

        # Countdown before enemy fires laser (-1 means not active)
        self.shoot_countdown = -1

        # List of enemies currently shooting
        self.enemies_shooting = []

        # Set initial enemy direction (To the right)
        self.enemy_dir = 1

        # Power up handler to manage power up spawning and collection
        self.power_up_handler = PowerUpHandler()

        # Timer for shield power up duration
        self.shield_timer = 0

        # Cooldown period for shield power up in seconds
        self.shield_cooldown = 10

        # Variable for handling self.end_page
        self.end_page = None

        # Bool for tracking if a projectile has been shot
        self.projectile_shot: bool = False

        # Projectile direction components
        self.projectile_dx = 0
        self.projectile_dy = 0

        # Create enemies (5 by 5)
        self.enemies.create_enemies(2, 5, 5)

        # Cooldown timers for each player to prevent rapid shooting
        self.cooldown_timers = [time.time(), time.time()]

        # Cooldown timer for block ability
        self.block_cooldown = time.time()

        # Keep track of how long the player has been dead
        self.death_timer = 0

        # Bool for tracking if an enemy has been hit
        self.hit = False

        # Reuse star co-ordinates from previous level for visual continuity
        self.stars = stars

    def draw(self) -> None:
        # Clear the canvas
        stddraw.clear()

        # Draw a black background
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        # Draw all the stars
        for x, y, radius, colour in self.stars:
            probability = random.random()

            # Using probability to create a flickering effect for the stars
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        # Check if the player has died and continue with game if not
        if not self.enemies.check_death() and self.alive:
            # Smaller pen radius for line to determine where the enemies hit the player will die
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)

            # Create a dotted line where if the enemy hits this line the player dies
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            # Handle enemy movement
            self.enemy_dir = self.enemies.enemy_update(
                self.enemy_dir, self.enemy_speed, self.enemy_speed * 12, False
            )

            # Draw enemies
            self.enemies.draw_enemies()

            # Update and draw all active power ups
            self.power_up_handler.update()
            self.power_up_handler.draw()

            # enemy shooting logic
            # Randomly trigger enemy shoot sequence if no shoot is already in progress
            if (
                random.randint(0, 120) == 1
                and self.shoot_countdown < 0
                and len(self.enemies.enemies) > 0
            ):
                # Reset shoot countdown
                self.shoot_countdown = 60

                # Reset hit state for all players
                for player in self.players:
                    player.hit = False

                # Select a random enemy to shoot
                random_enemy = self.enemies.shoot()

                # Add enemy to shooting list if not already in it
                if (
                    random_enemy is not None
                    and random_enemy not in self.enemies_shooting
                ):
                    self.enemies_shooting.append(random_enemy)

            # Decrement the shoot countdown each frame
            self.shoot_countdown -= 1

            # Play enemy shoot sound effect at the correct moment in the countdown
            if self.shoot_countdown == 20:
                self.music.play("assets/Music/enemy_shoot", sfx=True)

            # List of lasers to skip drawing
            lasers_to_not_draw: list = []

            # Remove enemies from shooting list that have been destroyed
            self.enemies_shooting = [
                enemy
                for enemy in self.enemies_shooting
                if enemy in self.enemies.enemies
            ]

            # Go through each player object
            for i, player in enumerate(self.players):
                # Different colors for each player
                if i % 2 == 0:
                    player.draw_spaceship(0.1, stddraw.WHITE)
                else:
                    player.draw_spaceship(0.1, stddraw.LIGHT_GRAY)

                # Update projectile co-ordinates
                player.move_projectiles()

                # Draw all the projectiles
                player.draw_projectiles()

                # Check for player controls
                player.control_player()

                # Check if player shoots
                if player.projectile_shot:
                    player.shoot(0.008)

                # Clean up projectiles that have left the screen
                player.clean_up()

                # check hits every frame
                # List to keep track of projectiles to remove
                projectile_to_remove = None
                for projectile in player.projectiles[:]:
                    # Check if a power up is hit by the projectile
                    power_up = self.power_up_handler.check_hit(projectile)

                    # Check if an enemy is hit, update score and make enemies faster
                    if self.enemies.check_hit(projectile):
                        player.score += 100
                        self.enemy_speed += 0.00008
                        projectile_to_remove = projectile
                        break
                    elif power_up != -1:
                        # Apply the corresponding power up effect
                        if power_up == 1:
                            # Shield power up
                            player.shield_timer = time.time()
                        elif power_up == 2:
                            # Bonus points power up
                            player.score += 500
                        elif power_up == 3:
                            # Extra life power up
                            player.lives += 1
                        break

                # Delete the projectile used to destroy an enemy or collect a power up
                if projectile_to_remove is not None:
                    player.projectiles.remove(projectile_to_remove)

                # Draw shield if active
                player.shield()

                # Check if player has run out of lives
                if player.lives <= 0:
                    self.alive = False
                    self.music.stop()
                    self.death_timer = time.time()

            # Draw laser warning beam during wind-up phase of the shoot countdown
            for enemy in self.enemies_shooting:
                if 20 < self.shoot_countdown < 60:
                    for i in range(100):
                        stddraw.filledCircle(enemy.x, enemy.y - i / 100, 0.002)

            # Stop music if level is completed
            if self.check_completion():
                self.music.stop()

            # Draw the actual laser beam once countdown reaches firing phase
            if 0 < self.shoot_countdown <= 20:
                for enemy in self.enemies_shooting:
                    stddraw.setPenColor(stddraw.RED)
                    stddraw.setPenRadius(0.003)

                    # Shorten laser if it hits a player, otherwise draw full length
                    if not any(
                        player.check_hit_laser(enemy) for player in self.players
                    ):
                        stddraw.line(enemy.x, enemy.y, enemy.x, 0)
                    else:
                        stddraw.line(enemy.x, enemy.y, enemy.x, self.players[0].radius)

        else:
            # Create an end page if the player has died
            if self.end_page is None:
                self.end_page = EndPage(
                    self.width, self.height, self.players, time.time(), self.highscore
                )

            # Draw the end page
            self.end_page.draw()

            # Update that the player is dead
            self.alive = False

        # Draw scores and lives of the players
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0.85, 1, 0.15)
        stddraw.setPenColor(stddraw.ORANGE)
        stddraw.setFontSize(20)
        if not self.multiplayer:
            stddraw.text(0.3, 0.9, f"Score: {self.players[0].score}")
            stddraw.text(0.6, 0.9, f"Lives: {self.players[0].lives}")
        else:
            stddraw.text(0.225, 0.95, "PLAYER 1")
            stddraw.text(0.125, 0.9, f"Score: {self.players[0].score}")
            stddraw.text(0.4, 0.9, f"Lives: {self.players[0].lives}")
            stddraw.text(0.8, 0.95, "PLAYER 2")
            stddraw.text(0.65, 0.9, f"Score: {self.players[1].score}")
            stddraw.text(0.9, 0.9, f"Lives: {self.players[1].lives}")
        stddraw.show(20)

    def run(self):
        # Draw the level 2 page
        self.draw()

        # Array of bools of all keys pressed to handle escape
        keys = stddraw.getKeysPressed()

        # Check if escape is pressed to stop the game
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"

        # Check if r is pressed in end game page to restart the game before 5 seconds are over
        if not self.alive and (keys[stddraw.K_r] or time.time() - self.death_timer > 5):
            self.end_page.stop_music()
            return "RESTART"

        # Default to continue game play state
        return "PLAY"

    def check_completion(self):
        # Completion condition
        return len(self.enemies.enemies) == 0


class Level3:
    """
    FINAL BOSS BATTLE:
    One giant enemty that shoots projectiles in multiple directions
    For fairness when player and enemy projectiles collide they destroy one another
    Power ups are the same as in level 2
    Lives are carried over from level 2

    Args:
        width: width of the game window
        height: height of the game window
        stars: array of co-ordinates to specify positions of stars from previous level
        score: score carried over from previous level
        lives: lives carried over from previous level

    Author: Theunis and Sydwell
    """

    def __init__(
        self,
        width: int,
        height: int,
        stars: list,
        players: list[Player],
        highscore: int,
    ):
        # Check if player is alive
        self.alive: bool = True

        # Array of players to handle multi-player case
        self.players = players

        # Reset projectile state for all players carried over from previous level
        for player in players:
            player.projectile_shot = False
            player.projectiles = []

        # Create the boss enemy at the top center of the screen
        self.boss = Boss(0.5, 0.75, 3, 0.08)

        # Keep track of width and height for dynamic star size generation
        self.width = width
        self.height = height

        # Set initial enemy direction (To the right)
        self.enemy_dir = 1

        # Power up handler to manage power up spawning and collection
        self.power_up_handler = PowerUpHandler()

        # Music handler
        self.music = Music()

        # Keep track of player high score
        self.highscore = highscore

        # Multiplayer bool derived from number of players
        self.multiplayer = len(players) > 1

        # Preload boss music
        self.music.load(["assets/Music/boss_music"])

        # Play boss music in a continuous loop
        self.music.play("assets/Music/boss_music", loop=True)

        # Timer for shield power up duration
        self.shield_timer = 0

        # Cooldown period for shield power up in seconds
        self.shield_cooldown = 10

        # Timer for awarding bonus score over time
        self.score_timer = time.time()

        # Keep track of how long the player has been dead
        self.death_timer = None

        # Timer for tracking when the victory screen should appear
        self.victory_timer = None

        # Bool for tracking if an enemy has been hit
        self.hit = False

        # Variable for handling self.end_page
        self.end_page = None

        # Reuse star co-ordinates from previous level for visual continuity
        self.stars = stars

        # Bool to ensure score bonus is only awarded once
        self.score_bonus = False

    def check_distance(self, projectile1: Projectile, projectile2: Projectile) -> bool:
        # Calculate euclidean distance between two projectiles
        distance = math.hypot(
            projectile1.x - projectile2.x, projectile1.y - projectile2.y
        )

        # Return true if projectiles are close enough to be considered a collision
        return distance < 0.03

    def draw(self) -> None:
        # Clear the canvas
        stddraw.clear()

        # Draw a black background
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        # Draw all the stars
        for x, y, radius, colour in self.stars:
            probability = random.random()

            # Using probability to create a flickering effect for the stars
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        # Check if the boss is alive and the player has not died
        if not self.check_completion() and self.alive:
            # Smaller pen radius for line to determine where the enemies hit the player will die
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)

            # Create a dotted line where if the enemy hits this line the player dies
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            # Go through each player object
            for i, player in enumerate(self.players):
                # Different colors for each player
                if i % 2 == 0:
                    player.draw_spaceship(0.1, stddraw.WHITE)
                else:
                    player.draw_spaceship(0.1, stddraw.LIGHT_GRAY)

                # Update projectile co-ordinates
                player.move_projectiles()

                # Draw all the projectiles
                player.draw_projectiles()

                # Check for player controls
                player.control_player()

                # Check if player has run out of lives
                if player.lives <= 0:
                    self.alive = False
                    self.music.stop()
                    self.death_timer = time.time()

                # Check if player shoots
                if player.projectile_shot:
                    player.shoot(0.008)

                # Draw shield if active
                player.shield()

                # List to keep track of projectiles to remove
                projectile_to_remove = None

                for projectile in player.projectiles[:]:
                    # Check if a power up is hit by the projectile
                    power_up = self.power_up_handler.check_hit(projectile)

                    # Check if the boss is hit, reduce boss health and update score
                    if self.boss.is_hit_by_projectile(projectile):
                        self.boss.health -= 5
                        player.score += 100
                        projectile_to_remove = projectile
                        break
                    elif power_up != -1:
                        # Apply the corresponding power up effect
                        if power_up == 1:
                            # Shield power up
                            player.shield_timer = time.time()
                        elif power_up == 2:
                            # Bonus points power up
                            player.score += 500
                        elif power_up == 3:
                            # Extra life power up
                            player.lives += 1
                        break

                # Delete the projectile used to hit the boss or collect a power up
                if projectile_to_remove is not None:
                    player.projectiles.remove(projectile_to_remove)

                # check if player projectiles hit enemy projectiles
                # Lists of projectiles to remove from both sides after collision
                to_remove_player: list = []
                to_remove_boss: list = []

                # Check all combinations of player and boss projectiles for collisions
                for player_projectile in player.projectiles:
                    for enemy_projectile in self.boss.projectiles:
                        if self.check_distance(player_projectile, enemy_projectile):
                            to_remove_player.append(player_projectile)
                            to_remove_boss.append(enemy_projectile)

                # Remove collided projectiles from both player and boss projectile lists
                player.projectiles = [
                    projectile
                    for projectile in player.projectiles
                    if projectile not in to_remove_player
                ]
                self.boss.projectiles = [
                    projectile
                    for projectile in self.boss.projectiles
                    if projectile not in to_remove_boss
                ]

                # check boss projectiles hit player
                # Remove boss projectiles that have hit the player
                self.boss.projectiles = player.check_hit_projectile(
                    self.boss.projectiles
                )

                # Clean up projectiles that have left the screen
                player.clean_up()

            # boss movement and drawing
            # Handle boss movement
            self.enemy_dir = self.boss.move(self.enemy_dir, 0.002, 0.001, False)

            # Handle boss shooting
            self.boss.shoot()

            # Draw the boss
            self.boss.draw()

            # powerups
            # Update and draw all active power ups
            self.power_up_handler.update()
            self.power_up_handler.draw()

        # Player has died but boss is still alive - show end page
        elif not self.alive and self.boss.health > 0:
            if self.end_page is None:
                self.end_page = EndPage(
                    self.width, self.height, self.players, time.time(), self.highscore
                )
            self.end_page.draw()

        # Boss has been defeated - show victory screen
        elif self.boss.health <= 0:
            # Stop music to prevent audio clashes
            self.music.stop()

            # Record the time of victory for countdown timer
            if self.alive:
                self.victory_timer = time.time()

            # Award one-time score bonus for defeating the boss
            if not self.score_bonus:
                self.score_bonus = True
                for player in self.players:
                    player.score += 2000

            # Create victory page if it does not exist yet
            if self.end_page is None:
                self.end_page = Victory(
                    self.width, self.height, self.players, time.time(), self.highscore
                )

            # Draw the victory page
            self.end_page.draw()

            # Update that the player is dead
            self.alive = False

        # Draw scores and lives of the players
        if not self.multiplayer:
            stddraw.text(0.3, 0.9, f"Score: {self.players[0].score}")
            stddraw.text(0.6, 0.9, f"Lives: {self.players[0].lives}")
        else:
            stddraw.text(0.125, 0.9, f"Score: {self.players[0].score}")
            stddraw.text(0.4, 0.9, f"Lives: {self.players[0].lives}")
            stddraw.text(0.65, 0.9, f"Score: {self.players[1].score}")
            stddraw.text(0.9, 0.9, f"Lives: {self.players[1].lives}")
        stddraw.show(20)

        # Clean up boss projectiles that have left the screen
        self._clean_up()

    def _clean_up(self):
        # List to store only in-bounds boss projectiles
        copy_projectile_boss: list = []

        # Keep only projectiles that are still within the screen bounds
        for projectile in self.boss.projectiles:
            if 0 <= projectile.x <= 1 and 0 <= projectile.y <= 1:
                copy_projectile_boss.append(projectile)

        # Replace boss projectile list with the filtered list
        self.boss.projectiles = copy_projectile_boss

    def run(self):
        # Draw the level 3 page
        self.draw()

        # Array of bools of all keys pressed to handle escape
        keys = stddraw.getKeysPressed()

        # Check if escape is pressed to stop the game
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"

        # Check if r is pressed or timers have expired to restart the game
        if not self.alive and (
            keys[stddraw.K_r]
            or (not self.check_completion() and time.time() - self.death_timer > 5)
            or (self.check_completion() and time.time() - self.victory_timer > 15)
        ):
            self.end_page.stop_music()
            return "RESTART"

        # Default to continue game play state
        return "PLAY"

    def check_completion(self) -> bool:
        # Completion condition
        return self.boss.health <= 0
