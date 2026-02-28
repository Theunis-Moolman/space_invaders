import stddraw
from src.states.menu import MenuPage

def main() -> None:
    Menu = MenuPage()
    state = "MENU"

    if state == "MENU":
        Menu.draw()
        Menu.run()

if __name__ == "__main__":
    main()
