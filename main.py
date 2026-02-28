import stddraw
from src.states.menu import MenuPage

def main() -> None:
    Menu = MenuPage()
    state = "MENU"

    stddraw.setCanvasSize(1920, 1080)

    if state == "MENU":
        Menu.draw()
        Menu.run()

if __name__ == "__main__":
    main()
