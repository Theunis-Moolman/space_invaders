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
        self.score: int = 0
        self.alive: bool = True
        self.iteration_num: int = 0
        self.players = []
        self.highscore = highscore
        self.multiplayer: bool = multiplayer
        if multiplayer:
            self.players.append(Player(0.1, -0.85, 0.2, 0, 0, 90, 1))
            self.players.append(Player(0.9, -0.85, 0.2, 0, 0, 90, 2))
        else:
            self.players.append(Player(0.1, -0.85, 0.2, 0, 0, 90, 1))
        self.enemies = Enemies()
        self.width = width
        self.height = height
        self.enemy_speed = 0.001
        self.enemy_dir = 1

        self.projectile_shot: bool = False
        self.projectile_dx = 0
        self.projectile_dy = 0

        self.projectile_shot: bool = False
        self.projectile_dx = 0
        self.projectile_dy = 0

        self.enemies.create_enemies(1, 5, 5)
        self.cooldown_timers = [time.time(), time.time()]
        self.death_timer = 0

        self.music = Music()
        self.music.load(["assets/Music/level1"])
        self.music.play("assets/Music/level1", loop=True)

        self.end_page = None

        self.stars = []

        for i in range(600):
            rand_x = random.random()
            rand_y = random.random()
            radius = random.random() * min(self.width, self.height) / 500000
            #

            colour = Color(random.randrange(130, 220), random.randrange(130, 220), 255)
            self.stars.append((rand_x, rand_y, radius, colour))

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)
        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)
        if not self.enemies.check_death():
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            for i, player in enumerate(self.players):
                if i % 2 == 0:
                    player.draw_spaceship(0.1, stddraw.WHITE)
                else:
                    player.draw_spaceship(0.1, stddraw.LIGHT_GRAY)
                projectiles_to_remove = None
                for projectile in player.projectiles:
                    if self.enemies.check_hit(projectile):
                        player.score += 100
                        self.enemy_speed += 0.00008
                        projectiles_to_remove = projectile
                        break
                if projectiles_to_remove is not None:
                    player.projectiles.remove(projectiles_to_remove)

                player.move_projectiles()
                player.draw_projectiles()
                player.control_player()

                if player.projectile_shot:
                    player.shoot(0.008)

                player.clean_up()

            self.enemy_dir = self.enemies.enemy_update(self.enemy_dir, self.enemy_speed, self.enemy_speed * 12, False)
            self.enemies.draw_enemies()
        else:
            if self.alive:
                self.music.stop()
                self.death_timer = time.time()
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.players, time.time(), self.highscore)
            self.end_page.draw()
            self.alive = False
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

        if self.check_completion():
            self.music.stop()

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and (keys[stddraw.K_r] or time.time() - self.death_timer > 5):
            self.end_page.stop_music()
            return "RESTART"

        return "PLAY"

    def check_completion(self):
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
    def __init__(self, width: int, height: int, stars: list, multiplayer: bool, players, highscore: int):
        self.alive: bool = True
        self.iteration_num: int = 0
        self.players = players
        self.highscore = highscore
        self.enemies = Enemies()
        self.width = width
        self.height = height
        self.multiplayer = multiplayer
        self.enemy_speed = 0.001
        self.block = False
        self.music = Music()
        self.music.load(["assets/Music/enemy_shoot", "assets/Music/level2"])
        self.music.play("assets/Music/level2", loop=True)
        self.shoot_countdown = -1
        self.enemies_shooting = []
        self.enemy_dir = 1
        self.power_up_handler = PowerUpHandler()

        self.shield_timer = 0
        self.shield_cooldown = 10

        self.end_page = None

        self.projectile_shot: bool = False
        self.projectile_dx = 0
        self.projectile_dy = 0

        self.enemies.create_enemies(2, 5, 5)
        self.cooldown_timers = [time.time(), time.time()]
        self.block_cooldown = time.time()
        self.death_timer = 0
        self.hit = False

        self.stars = stars

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        if not self.enemies.check_death() and self.alive:
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            self.enemy_dir = self.enemies.enemy_update(self.enemy_dir, self.enemy_speed, self.enemy_speed * 12, False)
            self.enemies.draw_enemies()
            self.power_up_handler.update()
            self.power_up_handler.draw()

            # enemy shooting logic
            if random.randint(0, 120) == 1 and self.shoot_countdown < 0 and len(self.enemies.enemies) > 0:
                self.shoot_countdown = 60
                for player in self.players:
                    player.hit = False

                random_enemy = self.enemies.shoot()
                if random_enemy is not None and random_enemy not in self.enemies_shooting:
                    self.enemies_shooting.append(random_enemy)

            self.shoot_countdown -= 1
            if self.shoot_countdown == 20:
                self.music.play("assets/Music/enemy_shoot")

            self.enemies_shooting = [enemy for enemy in self.enemies_shooting if enemy in self.enemies.enemies]
            for i, player in enumerate(self.players):
                if i % 2 == 0:
                    player.draw_spaceship(0.1, stddraw.WHITE)
                else:
                    player.draw_spaceship(0.1, stddraw.LIGHT_GRAY)

                player.move_projectiles()
                player.draw_projectiles()
                player.control_player()

                if player.projectile_shot:
                   player.shoot(0.008)

                player.clean_up()

                # check hits every frame
                projectile_to_remove = None
                for projectile in player.projectiles[:]:
                    power_up = self.power_up_handler.check_hit(projectile)
                    if self.enemies.check_hit(projectile):
                        player.score += 100
                        self.enemy_speed += 0.00008
                        projectile_to_remove = projectile
                        break
                    elif power_up != -1:
                        if power_up == 1:
                            player.shield_timer = time.time()
                        elif power_up == 2:
                            player.score += 500
                        elif power_up == 3:
                            player.lives += 1
                        break
                if projectile_to_remove is not None:
                    player.projectiles.remove(projectile_to_remove)
                player.shield()
                if 0 < self.shoot_countdown <= 20:
                    for enemy in self.enemies_shooting:
                            stddraw.setPenColor(stddraw.RED)
                            stddraw.setPenRadius(0.003)
                            stddraw.line(enemy.x, enemy.y, enemy.x, 0)
                            if player.check_hit_laser(enemy):
                                stddraw.line(enemy.x, enemy.y, enemy.x, (player.y + 1)/2 + player.radius + 0.07)
                            else:
                                stddraw.line(enemy.x, enemy.y, enemy.x, 0)
                if player.lives <= 0:
                    self.alive = False
                    self.music.stop()
                    self.death_timer = time.time()
            for enemy in self.enemies_shooting:
                if 20 < self.shoot_countdown < 60:
                    for i in range(100):
                        stddraw.filledCircle(enemy.x, enemy.y - i / 100, 0.002)
            if self.check_completion():
                self.music.stop()

        else:
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.players, time.time(), self.highscore)
            self.end_page.draw()
            self.alive = False

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
        self.draw()
        keys = stddraw.getKeysPressed()
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and (keys[stddraw.K_r] or time.time() - self.death_timer > 5):
            self.end_page.stop_music()
            return "RESTART"

        return "PLAY"

    def check_completion(self):
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
    def __init__(self, width: int, height: int, stars: list, players: list[Player], highscore: int):
        self.alive: bool = True
        self.players = players
        self.boss = Boss(0.5, 0.75, 3, 0.08)
        self.width = width
        self.height = height
        self.enemy_dir = 1
        self.power_up_handler = PowerUpHandler()
        self.music = Music()
        self.highscore = highscore
        self.multiplayer = len(players) > 1

        self.music.load(["assets/Music/boss_music"])
        self.music.play("assets/Music/boss_music", loop=True)

        self.shield_timer = 0
        self.shield_cooldown = 10

        self.score_timer = time.time()

        self.projectile_shot: bool = False
        self.cooldown_timer = time.time()
        self.death_timer = None
        self.victory_timer = None
        self.hit = False

        self.end_page = None
        self.stars = stars
        self.score_bonus = False

    def check_distance(self, projectile1: Projectile, projectile2: Projectile) -> bool:
        distance = math.hypot(projectile1.x - projectile2.x, projectile1.y - projectile2.y)

        return distance < 0.03

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        if not self.check_completion() and self.alive:
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            for i, player in enumerate(self.players):
                if i % 2 == 0:
                    player.draw_spaceship(0.1, stddraw.WHITE)
                else:
                    player.draw_spaceship(0.1, stddraw.LIGHT_GRAY)

                player.move_projectiles()
                player.draw_projectiles()
                player.control_player()

                if player.lives <= 0:
                    self.alive = False
                    self.music.stop()
                    self.death_timer = time.time()


                if player.projectile_shot:
                    player.shoot(0.008)


                projectile_to_remove = None

                for projectile in player.projectiles[:]:
                    power_up = self.power_up_handler.check_hit(projectile)
                    if self.boss.is_hit_by_projectile(projectile):
                        self.boss.health -= 5
                        player.score += 100
                        projectile_to_remove = projectile
                        break
                    elif power_up != -1:
                        if power_up == 1:
                            player.shield_timer = time.time()
                        elif power_up == 2:
                            player.score += 500
                        elif power_up == 3:
                            player.lives += 1
                        break
                if projectile_to_remove is not None:
                    player.projectiles.remove(projectile_to_remove)

                # check if player projectiles hit enemy projectiles

                to_remove_player: list = []
                to_remove_boss: list = []
                for player_projectile in player.projectiles:
                    for enemy_projectile in self.boss.projectiles:
                        if self.check_distance(player_projectile, enemy_projectile):
                            to_remove_player.append(player_projectile)
                            to_remove_boss.append(enemy_projectile)

                player.projectiles = [projectile for projectile in player.projectiles if
                                           projectile not in to_remove_player]
                self.boss.projectiles = [projectile for projectile in self.boss.projectiles if
                                         projectile not in to_remove_boss]
                # check boss projectiles hit player
                self.boss.projectiles = player.check_hit_projectile(self.boss.projectiles)

                player.clean_up()

            # boss movement and drawing
            self.enemy_dir = self.boss.move(self.enemy_dir, 0.002, 0.001, False)
            self.boss.shoot()
            self.boss.draw()

            # powerups
            self.power_up_handler.update()
            self.power_up_handler.draw()

        elif not self.alive and self.boss.health > 0:
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.players, time.time(), self.highscore)
            self.end_page.draw()
        elif self.boss.health <= 0:
            self.music.stop()
            if self.alive:
                self.victory_timer = time.time()
            if not self.score_bonus:
                self.score_bonus = True
                for player in self.players:
                    player.score += 2000
            if self.end_page is None:
                self.end_page = Victory(self.width, self.height, self.players, time.time(), self.highscore)
            self.end_page.draw()
            self.alive = False

        if not self.multiplayer:
            stddraw.text(0.3, 0.9, f"Score: {self.players[0].score}")
            stddraw.text(0.6, 0.9, f"Lives: {self.players[0].lives}")
        else:
            stddraw.text(0.125, 0.9, f"Score: {self.players[0].score}")
            stddraw.text(0.4, 0.9, f"Lives: {self.players[0].lives}")
            stddraw.text(0.65, 0.9, f"Score: {self.players[1].score}")
            stddraw.text(0.9, 0.9, f"Lives: {self.players[1].lives}")
        stddraw.show(20)
        self._clean_up()

    def _clean_up(self):
        copy_projectile_boss: list = []
        for projectile in self.boss.projectiles:
            if 0 <= projectile.x <= 1 and 0 <= projectile.y <= 1:
                copy_projectile_boss.append(projectile)

        self.boss.projectiles = copy_projectile_boss

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and (keys[stddraw.K_r] or (not self.check_completion() and time.time() - self.death_timer > 5) or (self.check_completion() and time.time() - self.victory_timer > 15)):
            self.end_page.stop_music()
            return "RESTART"

        return "PLAY"

    def check_completion(self) -> bool:
        return self.boss.health <= 0