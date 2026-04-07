# Project Roadmap & Progress

### Project Progress: 39%
![Progress Bar](https://web.app)

### Features to be added:
- [ ] Background music in menu
- [ ] High score stored in a text file
- [ ] (Really difficult, but if needed: Enemy explosion effect)
- [ ] Sad music for game over
- [ ] Explosion effect for game over

> [!CAUTION]
> **TO FIX: (IMPORTANT TO DO FIRST BEFORE CONTINUING WITH FEATURES)**
> 
> - [ ] Enemy movements should first be left to right before the enemies descend
> 
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [ ] Add checks to see if the last enemy in a row is at the edge and then descend
> 
> - [ ] Turret should not shoot a laser. Should shoot a moving ball 
> 
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [ ] (Make a class for this maybe and then store array of objects in the spaceship class)
> 
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [ ] Make a function in gamestate class that iterates through objects comparing co-ordinates with x and y
> 
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [ ] is_enemy_hit has to be updated to use direct center-ordinates + radius of the moving ball to detect a hit
> 
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [ ] Make a function in spaceship class to draw all the bullets (Please use 0 to 1 scale)
> 
> - [ ] Game over should have an automatic restart too after a certain time
> 
> - [ ] (OPTIONAL SORT OF: CONVERT DRAW_SPACESHIP to 0 to 1 scale for better efficiency)

### TO DO: (Recommended by Sydwell)
- [ ] Levels to the game

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Level 1**: up to 15000 points with basic enemies (no shooting back)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Level 2**: Enemies + barriers (slower, but shooting back) - USE B FOR BLOCKING

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- up to 40000 points

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Player gets 5 lives

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Level 3**: Boss battle up to 60000 points

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Lives are transferred from level 2

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*(USE DIFFERENT CLASSES FOR EACH LEVEL IN GAME.PY)*

### Features completed:
- [x] Lives are added level 2
- [x] Music fixed
- [x] Different enemy images as levels increase
- [x] Enemies shooting back
- [x] Level 2 is partially completed (STILL NEED TO ADD BLOCKING)
- [x] Transition screen
- [x] Level 1 is completed
- [x] Restart
- [x] Score
- [x] Beam when enemy is shot
- [x] Basic gameplay
- [x] Shooting cooldown to prevent lag
