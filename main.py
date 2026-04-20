from src.states.menu import MenuPage
from src.states.game import Level1, Level2, Level3
from src.states.transition import TransitionPage
from src.Music.music import Music

def main() -> None:
    """
    Main function that ties everything together
    Handles displaying a high score
    Uses a finite state machine to run the game in a continuous loop
    Args:
        None

    Returns:
        None

    Author: Theunis, Ben and Sydwell
    """
    width = 600
    height = 600
    Menu = MenuPage(width, height)
    state = "MENU"

    with open('src/Stored/Highscore.txt', 'r') as f:
        line = f.read().strip()
    if line == "":
        highscore = 0
    else:
        highscore = float(line)
    written:bool = False

    transitioned: bool = False

    level1_paragraph = "Enemies do not shoot back for now..."
    level2_paragraph = "Good luck! Enemies shoot back now! \n Look out for power ups\n You have 5 lives!\n Enemies reaching line = INSTANT DEATH"
    level3_paragraph = "Final boss reached! \n Hope you saved up lives..."

    music = Music()
    music.load(['assets/Music/Music'])
    music.play('assets/Music/Music', loop = True)

    while state != "ESCAPE":
        if state == "MENU":
            state = Menu.run()
        elif state == "PLAY":
            if not transitioned:
                music.stop() 
                written = False
                Transition = TransitionPage("Level 1", level1_paragraph, Menu.stars)
                Transition.draw()
                transitioned = True
                GamePage = Level1(width, height)
            else:
                if GamePage.check_completion()  and isinstance(GamePage, Level1):
                    Transition = TransitionPage("Level 2", level2_paragraph, GamePage.stars)
                    Transition.draw()
                    GamePage = Level2(width, height, GamePage.stars)
                elif GamePage.check_completion() and isinstance(GamePage, Level2):
                    Transition = TransitionPage("Level 3", level3_paragraph, GamePage.stars)
                    Transition.draw()
                    GamePage = Level3(width, height, GamePage.stars, GamePage.score, GamePage.lives)
                elif GamePage.check_completion() and isinstance(GamePage, Level3):
                    ... #Add winner screen
                    if GamePage.score > highscore and not written:
                        highscore = GamePage.score
                        with open('src/Stored/Highscore.txt', 'w') as f:
                            f.write(str(highscore))
                        written = True

                state = GamePage.run()
                if not GamePage.alive and not written and GamePage.score > highscore:
                    highscore = GamePage.score
                    with open('src/Stored/Highscore.txt', 'w') as f:
                        f.write(str(highscore))
                    written = True


        elif state == "RESTART":
            transitioned = False
            state = "PLAY"


if __name__ == "__main__":
    main()
