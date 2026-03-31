from src.states.menu import MenuPage
from src.states.game import GamePlay

def main() -> None:
    width = 500
    height = 500
    Menu = MenuPage(width, height)
    state = "MENU"

    GamePage = GamePlay(width, height)

    while state != "ESCAPE":
        if state == "MENU":
            state = Menu.run()
        elif state == "PLAY":
            state = GamePage.run()


if __name__ == "__main__":
    main()
