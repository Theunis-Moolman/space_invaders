from src.states.menu import MenuPage
from src.states.game import Level1, Level2, Level3

def main() -> None:
    width = 600
    height = 600
    Menu = MenuPage(width, height)
    state = "MENU"

    GamePage = Level1(width, height)

    while state != "ESCAPE":
        if state == "MENU":
            state = Menu.run()
        elif state == "PLAY":
            if GamePage.score == 20000 and not isinstance(GamePage, Level2):
                GamePage = Level2(width, height)
            if GamePage.score == 40000 and not isinstance(GamePage, Level3):
                GamePage = Level3(width, height)
            state = GamePage.run()

        elif state == "RESTART":
            GamePage = Level1(width, height)
            state = "PLAY"


if __name__ == "__main__":
    main()
