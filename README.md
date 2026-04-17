# Space Invaders


---

## How to Play

| Key | Action |
|-----|--------|
| `←` / `→` | Move left / right |
| `↑` | Shoot |
| `A` / `D` | Rotate turret angle |
| `SPACE` | Start game |
| `R` | Restart after game over |
| `ESC` | Exit |

---

## Additional Features

### Three Unique Levels
The game progresses across three levels, each with increasing difficulty. Level 2 carries your score forward, and Level 3 carries both your score and remaining lives into the final boss battle.

### Enemies Shoot Back (Level 2)
In Level 2, enemies fire laser beams downward at the player. The shoot frequency scales with your score, making the game progressively harder the better you do. A wind-up animation warns you before the shot fires.

### Power-Ups (Levels 2 & 3)
Power-ups drift across the screen and are collected by shooting them. There are three types:

- **Shield** — Activates a temporary barrier above the player that blocks incoming enemy fire for 10 seconds.
- **Star** — Instantly awards 500 bonus points.
- **Heart** — Grants an extra life.

### Lives System (Levels 2 & 3)
Players start Level 2 with 5 lives. Taking a hit from an enemy laser costs one life, and the game only ends when all lives are lost.

### Boss Battle (Level 3)
The final level features a giant boss enemy with 100 HP and a health bar displayed at the top of the screen. The boss moves side to side and fires a spread of 5 projectiles in a fan pattern at random intervals.

### Projectile Collision (Level 3)
Player bullets and boss projectiles can cancel each other out on contact, adding a layer of strategy to the final battle.

### Animated Starfield Background
A randomised, twinkling star background is generated at the start of the game and persists across all levels for visual continuity.

### High Score Tracking
The game reads and displays the all-time high score on the main menu, stored locally in `src/Stored/Highscore.txt`.

### Sound Effects & Music
Background music and sound effects play during gameplay, including distinct sounds for player shooting and enemy firing.

### Menu & End Screens
A styled main menu displays the high score and control instructions. The game over screen shows your final score, options to restart or exit, and a 5-second auto-restart countdown.

---

## Project Structure

```
space_invaders/
├── main.py                  # Entry point
├── src/
│   ├── Game/
│   │   ├── spaceship.py     # Player & Projectile classes
│   │   ├── enemies.py       # Enemy, Boss & Enemies handler
│   │   ├── powerups.py      # PowerUp & PowerUpHandler classes
│   │   └── controls.py      # Keyboard input handling
│   ├── states/
│   │   ├── game.py          # Level1, Level2, Level3 logic
│   │   ├── menu.py          # Main menu screen
│   │   ├── end.py           # Game over screen
│   │   └── transition.py    # Level transition screen
│   ├── Music/
│   │   └── music.py         # Audio handler
│   └── Stored/
│       └── Highscore.txt    # Persistent high score
└── assets/
    ├── images/              # Sprites (Boss, Shield, Heart, etc.)
    └── Music/               # WAV audio files
```

---


## Authors

| Name | Student Number |
|------|---------------|
| Sydwell | XXXXXXX |
| Theunis | 28904516 |

---

## Music Declaration

We declare that all music and sound effects used in this project are either original works or sourced from royalty-free / openly licensed libraries. The table below lists each audio asset and its origin.

| File | Source | License / URL |
|------|--------|---------------|
| `Music.wav` | [Source name here] | [Link or license here] |
| `Defeat.wav` | [Source name here] | [Link or license here] |
| `Victory.wav` | [Source name here] | [Link or license here] |
| `shoot.wav` | [Claude] | [claude.ai] |
| `enemy_shoot.wav` | [Claude] | [claude.ai] |

---

## Image Declaration

We declare that all images and sprites used in this project are either original works or sourced from royalty-free / openly licensed libraries. The table below lists each image asset and its origin.

| File | Source | License / URL |
|------|--------|---------------|
| `Boss.png` | [Source name here] | [Link or license here] |
| `EnemyMissile.png` | [Source name here] | [Link or license here] |
| `Heart.png` | [Source name here] | [Link or license here] |
| `Logo.png` | [Source name here] | [Link or license here] |
| `Projectile.png` | [Source name here] | [Link or license here] |
| `Shield.png` | [Source name here] | [Link or license here] |
| `Star.png` | [Source name here] | [Link or license here] |
