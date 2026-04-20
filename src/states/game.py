import stddraw
from src.Game.enemies import Enemies, Boss
from src.Game.spaceship import Player, Projectile
import random
from color import Color
from src.Game.controls import controls
from src.Game.powerups import PowerUpHandler
from src.states.end import EndPage
import time
from src.Music.music import Music
import math

class Level1:
    """
    Level 1 with players not shooting back at all
    Basic space invaders type game play

    Args:
        width: width of the game window
        height: height of the game window


    Author: Sydwell and Theunis
    """
    def __init__(self, width: int, height: int):
        self.score: int = 0
        self.alive: bool = True
        self.iteration_num: int = 0
        self.player = Player(0, -0.85, 0.2, 0, 0, 90)
        self.enemies = Enemies()
        self.width = width
        self.height = height
        self.enemy_speed = 0.001
        self.enemy_dir = 1

        self.projectile_shot: bool = False
        self.projectile_dx = 0
        self.projectile_dy = 0

        self.enemies.create_enemies(1, 5, 5)
        self.cooldown_timer = time.time()
        self.death_timer = 0

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

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.5, 0.9, f"Score: {self.score}")

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)
        if not self.enemies.check_death():
            self.player.draw_spaceship(0.1, stddraw.WHITE, False)
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            self.enemy_dir = self.enemies.enemy_update(self.enemy_dir, self.enemy_speed, self.enemy_speed * 12, False)
            self.enemies.draw_enemies()
            self.player.move_projectiles()
            self.player.draw_projectiles()

            if self.projectile_shot and (time.time() - self.cooldown_timer) > 0.8:
                self.cooldown_timer = time.time()
                self.player.shoot(0.008)

            for projectile in self.player.projectiles:
                if self.enemies.check_hit(projectile):
                    self.score += 100
                    self.enemy_speed += 0.00008
                    self.player.projectiles.remove(projectile)
                    break

            self.projectile_shot = False
        else:
            if self.alive:
                self.death_timer = time.time()
                print(self.death_timer)
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.score, time.time())
            self.end_page.draw()
            self.alive = False
        stddraw.show(20)

        self._clean_up()

    def _clean_up(self):
        copy_projectile: list = []
        for projectile in self.player.projectiles:
            if 0 <= projectile.x <= 1 and 0 <= projectile.y <= 1:
                copy_projectile.append(projectile)

        self.player.projectiles = copy_projectile

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        self.projectile_shot = controls(self.player, keys)
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and (keys[stddraw.K_r] or time.time() - self.death_timer > 5):
            return "RESTART"

        return "PLAY"

    def check_completion(self):
        return self.score == 2500
        

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
    def __init__(self, width: int, height: int, stars: list):
        self.score: int = 2500
        self.alive: bool = True
        self.iteration_num: int = 0
        self.player = Player(0, -0.85, 0.08, 0, 0, 90)
        self.enemies = Enemies()
        self.width = width
        self.height = height
        self.enemy_speed = 0.001
        self.block = False
        self.lives = 5
        self.music = Music()
        self.music.load(["assets/Music/enemy_shoot", "assets/Music/shoot"])
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
        self.cooldown_timer = time.time()
        self.block_cooldown = time.time()
        self.death_timer = 0
        self.hit = False

        self.stars = stars

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.3, 0.9, f"Score: {self.score}")
        stddraw.text(0.6, 0.9, f"Lives: {self.lives}")

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        if not self.enemies.check_death() and self.lives > 0:
            self.player.draw_spaceship(0.1, stddraw.WHITE, False)
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
                self.hit = False

                random_enemy = self.enemies.shoot()
                if random_enemy is not None and random_enemy not in self.enemies_shooting:
                    self.enemies_shooting.append(random_enemy)

            self.shoot_countdown -= 1
            if self.shoot_countdown == 20:
                self.music.play("assets/Music/enemy_shoot")


            # player shooting
            if self.projectile_shot and (time.time() - self.cooldown_timer) > 0.8:
                self.cooldown_timer = time.time()
                self.player.shoot(0.008)
                self.projectile_shot = False

            # check hits every frame
            for projectile in self.player.projectiles[:]:
                power_up = self.power_up_handler.check_hit(projectile)
                if self.enemies.check_hit(projectile):
                    self.score += 100
                    self.enemy_speed += 0.00008
                    self.player.projectiles.remove(projectile)
                    break
                elif power_up != -1:
                    if power_up == 1:

                        self.shield_timer = time.time()
                    elif power_up == 2:
                        self.score += 500
                    elif power_up == 3:
                        self.lives += 1

            self.enemies_shooting = [enemy for enemy in self.enemies_shooting if enemy in self.enemies.enemies]
            for enemy in self.enemies_shooting:
                if 20 < self.shoot_countdown < 60:
                    for i in range(100):
                        stddraw.filledCircle(enemy.x, enemy.y - i / 100, 0.002)

                if 0 < self.shoot_countdown <= 20:
                    stddraw.setPenColor(stddraw.RED)
                    stddraw.setPenRadius(0.003)
                    if time.time() - self.shield_timer > self.shield_cooldown:
                        stddraw.line(enemy.x, enemy.y, enemy.x, 0)
                        if (self.player.x + 1) / 2 - self.player.radius <= enemy.x <= (
                                self.player.x + 1) / 2 + self.player.radius:
                            if not self.hit:
                                self.lives -= 1
                            self.hit = True
                    else:
                        if (self.player.x + 1) / 2 - self.player.radius <= enemy.x <= (
                                self.player.x + 1) / 2 + self.player.radius:
                            stddraw.line(enemy.x, enemy.y, enemy.x, (self.player.y + 1)/2 + self.player.radius + 0.07)
                        else:
                            stddraw.line(enemy.x, enemy.y, enemy.x, 0)


            if time.time() - self.shield_timer < self.shield_cooldown:
                stddraw.setPenColor(stddraw.WHITE)
                x = (self.player.x + 1)/2
                y = (self.player.y + 1)/2
                stddraw.filledRectangle(x - self.player.radius, y + self.player.radius + 0.07, self.player.radius * 2, 0.02)
            self.player.move_projectiles()
            self.player.draw_projectiles()

        else:
            if self.alive:
                self.death_timer = time.time()
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.score, time.time())
            self.end_page.draw()
            self.alive = False
        self._clean_up()
        stddraw.show(20)

    def _clean_up(self):
        copy_projectile: list = []
        for projectile in self.player.projectiles:
            if 0 <= projectile.x <= 1 and 0 <= projectile.y <= 1:
                copy_projectile.append(projectile)

        self.player.projectiles = copy_projectile

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        self.projectile_shot = controls(self.player, keys)
        self.block = keys[stddraw.K_b]
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and (keys[stddraw.K_r] or time.time() - self.death_timer > 5):
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
    def __init__(self, width: int, height: int, stars: list, score: int, lives: int):
        self.score: int = score
        self.alive: bool = True
        self.player = Player(0, -0.85, 0.2, 0, 0, 90)
        self.boss = Boss(0.5, 0.75, 3, 0.08)
        self.width = width
        self.height = height
        self.lives = lives
        self.enemy_dir = 1
        self.power_up_handler = PowerUpHandler()

        self.shield_timer = 0
        self.shield_cooldown = 10

        self.projectile_shot: bool = False
        self.cooldown_timer = time.time()
        self.death_timer = 0
        self.hit = False

        self.end_page = None
        self.stars = stars

    def check_distance(self, projectile1: Projectile, projectile2: Projectile) -> bool:
        distance = math.hypot(projectile1.x - projectile2.x, projectile1.y - projectile2.y)

        return distance < 0.03

    def draw(self) -> None:
        stddraw.clear()
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledRectangle(0, 0, 1, 1)

        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.3, 0.9, f"Score: {self.score}")
        stddraw.text(0.6, 0.9, f"Lives: {self.lives}")

        for x, y, radius, colour in self.stars:
            probability = random.random()
            if probability < 0.99:
                stddraw.setPenColor(colour)
                stddraw.filledCircle(x, y, radius)

        if not self.check_completion() and self.lives > 0:
            self.player.draw_spaceship(0.1, stddraw.WHITE, False)
            stddraw.setPenRadius(0.001)
            stddraw.setPenColor(stddraw.WHITE)
            for i in range(100):
                x = i / 100
                stddraw.filledCircle(x, 0.205, 0.002)

            # boss movement and drawing
            self.enemy_dir = self.boss.move(self.enemy_dir, 0.002, 0.001, False)
            self.boss.shoot()
            self.boss.draw()

            # powerups
            self.power_up_handler.update()
            self.power_up_handler.draw()

            # player shooting
            if self.projectile_shot and (time.time() - self.cooldown_timer) > 0.8:
                self.cooldown_timer = time.time()
                self.player.shoot(0.008)
                self.projectile_shot = False

            # check player projectile hits boss
            for projectile in self.player.projectiles[:]:
                power_up = self.power_up_handler.check_hit(projectile)
                if self.boss.is_hit_by_projectile(projectile):
                    self.boss.health -= 5
                    self.score += 100
                    self.player.projectiles.remove(projectile)
                    break
                elif power_up != -1:
                    if power_up == 1:
                        self.shield_timer = time.time()
                    elif power_up == 2:
                        self.score += 500
                    elif power_up == 3:
                        self.lives += 1

            #check if player projectiles hit enemy projectiles

            to_remove_player: list = []
            to_remove_boss: list = []
            for player_projectile in self.player.projectiles:
                for enemy_projectile in self.boss.projectiles:
                    if self.check_distance(player_projectile, enemy_projectile):
                        to_remove_player.append(player_projectile)
                        to_remove_boss.append(enemy_projectile)

            self.player.projectiles = [projectile for projectile in self.player.projectiles if projectile not in to_remove_player]
            self.boss.projectiles = [projectile for projectile in self.boss.projectiles if
                                       projectile not in to_remove_boss]
            # check boss projectiles hit player
            for projectile in self.boss.projectiles:
                player_x = (self.player.x + 1) / 2
                player_y = (self.player.y + 1) / 2
                if math.hypot(projectile.x - player_x, projectile.y - player_y) < self.player.radius * 0.7:
                    if time.time() - self.shield_timer < self.shield_cooldown:
                        self.shield_timer = 0
                    else:
                        self.lives -= 1
                    self.boss.projectiles.remove(projectile)
                    break

            # draw shield
            if time.time() - self.shield_timer < self.shield_cooldown:
                stddraw.setPenColor(stddraw.WHITE)
                x = (self.player.x + 1) / 2
                y = (self.player.y + 1) / 2
                stddraw.filledRectangle(x - self.player.radius, y + self.player.radius + 0.07, self.player.radius * 2, 0.02)

            self.player.move_projectiles()
            self.player.draw_projectiles()

        elif self.lives < 0:
            if self.alive:
                self.death_timer = time.time()
            if self.end_page is None:
                self.end_page = EndPage(self.width, self.height, self.score, time.time())
            self.end_page.draw()
            self.alive = False

        stddraw.show(20)
        self._clean_up()

    def _clean_up(self):
        copy_projectile_player: list = []
        for projectile in self.player.projectiles:
            if 0 <= projectile.x <= 1 and 0 <= projectile.y <= 1:
                copy_projectile_player.append(projectile)

        self.player.projectiles = copy_projectile_player

        copy_projectile_boss: list = []
        for projectile in self.boss.projectiles:
            if 0 <= projectile.x <= 1 and 0 <= projectile.y <= 1:
                copy_projectile_boss.append(projectile)

        self.boss.projectiles = copy_projectile_boss

    def run(self):
        self.draw()
        keys = stddraw.getKeysPressed()
        self.projectile_shot = controls(self.player, keys)
        if keys[stddraw.K_ESCAPE]:
            return "ESCAPE"
        if not self.alive and (keys[stddraw.K_r] or time.time() - self.death_timer > 5):
            return "RESTART"

        return "PLAY"

    def check_completion(self) -> bool:
        return self.boss.health <= 0