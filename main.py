from src.states.menu import MenuPage
from src.states.game import Level1, Level2, Level3
from src.states.transition import TransitionPage

def main() -> None:
    width = 600
    height = 600
    Menu = MenuPage(width, height)
    state = "MENU"
    transitioned: bool = False

    level1_paragraph = "Enemies do not shoot back for now..."
    level2_paragraph = "Good luck! Enemies shoot back now! \n USE B FOR BLOCKING\n You have 5 lives!\n Enemies reaching line = INSTANT DEATH"
    level3_paragraph = "Final boss reached! \n Hope you saved up lives..."

    while state != "ESCAPE":
        if state == "MENU":
            state = Menu.run()
        elif state == "PLAY":
            if not transitioned:
                Transition = TransitionPage("Level 1", level1_paragraph, Menu.stars)
                Transition.draw()
                transitioned = True
                GamePage = Level1(width, height)
            else:
                if GamePage.score >= 15000 and not isinstance(GamePage, Level2):
                    Transition = TransitionPage("Level 2", level2_paragraph, GamePage.stars)
                    Transition.draw()
                    GamePage = Level2(width, height, GamePage.stars)
                if GamePage.score >= 40000 and not isinstance(GamePage, Level3):
                    Transition = TransitionPage("Level 3", level3_paragraph, GamePage.stars)
                    Transition.draw()
                    GamePage = Level3(width, height, GamePage.stars)
                state = GamePage.run()

        elif state == "RESTART":
            transitioned = False
            state = "PLAY"


if __name__ == "__main__":
    main()
