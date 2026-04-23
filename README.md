# Space Invaders


---

## How to Play

### Player 1
| Key | Action |
|-----|--------|
| `A` / `D` | Move left / right |
| `W` | Shoot |
| `Q` / `E` | Rotate turret angle |

### Player 2
| Key | Action |
|-----|--------|
| `J` / `L` | Move left / right |
| `I` | Shoot |
| `U` / `O` | Rotate turret angle |

### General
| Key | Action |
|-----|--------|
| `SPACE` | Start game |
| `R` | Restart after game over |
| `ESC` | Exit |
| `S` | Single player mode |
| `M` | Multiplayer mode |

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
Player bullets and boss projectiles can cancel each other out on contact.

### Animated Starfield Background
A randomised, twinkling star background is generated at the start of the game and persists across all levels for visual continuity.

### High Score Tracking
The game reads and displays the all-time high score on the main menu, stored locally in `src/Stored/Highscore.txt`.

### Sound Effects & Music
Background music and sound effects play during gameplay. Final boss features 1812 Tchaikonsky with the cannon sound extracted from the orchestra recording to add character to the game (Overdramatic for comedic purposes)

### Menu & End Screens & Victory screens
A styled main menu displays the high score and control instructions. The game over/Victory screen shows your final score, the player who won, options to restart or exit, and a 5-second auto-restart countdown.

### Multiplayer and singleplayer
During the menu state the player can choose between multi-player mode and single player mode. During the multiplayer mode each player's scores and lives are seperated. Winning condition is purely based on who has the highest score (So a player can choose to sabotage if they think their score is high enough at an instant). Each player also has seperate controls.

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
│   ├── states/
│   │   ├── game.py          # Level1, Level2, Level3 logic
│   │   ├── menu.py          # Main menu screen
│   │   ├── end.py           # Game over screen
│   │   ├── victory.py           # Game over screen
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
| Benjamin | 29139147 |

---

## Music Declaration

We declare that all music and sound effects used in this project are either original works or sourced from royalty-free / openly licensed libraries. The table below lists each audio asset and its origin.

| File | Source | URL |
|------|--------|---------------|
| `Music.wav` | [Source name here] | [Link or license here] |
| `Victory.wav` | [Source name here] | [Link or license here] |
| `shoot.wav` | Claude | claude.ai |
| `enemy_shoot.wav` | Claude | claude.ai |
| `Level1.wav` | degoose | https://freesound.org/people/degoose/sounds/580912/ |
| `Level2.wav` | Juhani Junkala | https://opengameart.org/content/5-chiptunes-action |
| `gameover.wav` | bevibeldesign (Freesound) | https://pixabay.com/sound-effects/film-special-effects-sucked-into-classroom-103774/ |
| `boss_music.wav` | Tchaikovsky (Audio Library) | https://www.youtube.com/watch?v=SylTHospNKM&list=RDSylTHospNKM&start_radio=1 |
---

## Image Declaration

We declare that all images and sprites used in this project are either original works or sourced from royalty-free / openly licensed libraries. The table below lists each image asset and its origin.

| File | Source | URL |
|------|--------|---------------|
| `Boss.png` | [Source name here] | [Link or license here] |
| `EnemyMissile.png` | [Source name here] | [Link or license here] |
| `Heart.png` | [Source name here] | [Link or license here] |
| `Projectile.png` | [Source name here] | [Link or license here] |
| `Shield.png` | [Source name here] | [Link or license here] |
| `Star.png` | [Source name here] | [Link or license here] |

