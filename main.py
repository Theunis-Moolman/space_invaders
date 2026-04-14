from src.states.menu import MenuPage
from src.states.game import Level1, Level2, Level3
from src.states.transition import TransitionPage

def main() -> None:
    width = 600
    height = 600
    Menu = MenuPage(width, height)
    state = "MENU"
    # Sydwell did highscore text file
    with open('src/Stored/Highscore.txt', 'r') as f:
        line = f.read().strip()
    print(line)
    if line == "":
        highscore = 99999
    else:
        highscore = float(line)
    written:bool = False

    transitioned: bool = False

    level1_paragraph = "Enemies do not shoot back for now..."
    level2_paragraph = "Good luck! Enemies shoot back now! \n Look out for power ups\n You have 5 lives!\n Enemies reaching line = INSTANT DEATH"
    level3_paragraph = "Final boss reached! \n Hope you saved up lives..."

    while state != "ESCAPE":
        if state == "MENU":
            state = Menu.run()
        elif state == "PLAY":
            if not transitioned:
                written = False
                Transition = TransitionPage("Level 1", level1_paragraph, Menu.stars)
                Transition.draw()
                transitioned = True
                GamePage = Level1(width, height)
            else:
                if GamePage.score == 2500  and not isinstance(GamePage, Level2):
                    Transition = TransitionPage("Level 2", level2_paragraph, GamePage.stars)
                    Transition.draw()
                    GamePage = Level2(width, height, GamePage.stars)
                if isinstance(GamePage, Level2):
                    if len(GamePage.enemies.enemies) == 0:
                        Transition = TransitionPage("Level 3", level3_paragraph, GamePage.stars)
                        Transition.draw()
                        GamePage = Level3(width, height, GamePage.stars, GamePage.score, GamePage.lives)
                if isinstance(GamePage, Level3):
                    if GamePage.boss.health == 0:
                        ... #Add a winner screen!

                state = GamePage.run()
                if GamePage.dead and not written and GamePage.score > highscore:
                    highscore = GamePage.score
                    with open('src/Stored/Highscore.txt', 'w') as f:
                        f.write(str(highscore))
                    written = True


        elif state == "RESTART":
            transitioned = False
            state = "PLAY"


if __name__ == "__main__":
    main()
