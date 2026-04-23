from src.states.menu import MenuPageSingle, MenuPageMulti
from src.states.game import Level1, Level2, Level3
from src.states.transition import TransitionPage
from src.Music.music import Music
import stddraw


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
    stddraw.setCanvasSize(width, height)
    state = "MENU"

    with open("src/Stored/Highscore.txt", "r") as f:
        line = f.read().strip()
    if line == "":
        highscore = 0
    else:
        highscore = int(line)
    multiplayer: bool = False
    Menu = MenuPageSingle(width, height, highscore)

    transitioned: bool = False

    level1_paragraph = "Enemies do not shoot back for now..."
    level2_paragraph = "Good luck! Enemies shoot back now! \n Look out for power ups\n You have 5 lives!\n Enemies reaching line = INSTANT DEATH"
    level3_paragraph = "Final boss reached! \n Hope you saved up lives..."

    music = Music()
    music.load(["assets/Music/Music"])
    music.play("assets/Music/Music", loop=True)

    while state != "ESCAPE":
        if state == "MENU":
            state = Menu.run()
        elif state == "SINGLE":
            multiplayer = False
            Transition = TransitionPage("1 PLAYER", "Activated", Menu.stars)
            Transition.draw()
            Menu = MenuPageSingle(width, height, highscore)
            state = Menu.run()
        elif state == "MULTI":
            multiplayer = True
            Transition = TransitionPage("2 PLAYER", "Activated", Menu.stars)
            Transition.draw()
            Menu = MenuPageMulti(width, height, highscore)
            state = Menu.run()
        elif state == "PLAY":
            if not transitioned:
                music.stop()
                Transition = TransitionPage("Level 1", level1_paragraph, Menu.stars)
                Transition.draw()
                transitioned = True
                GamePage = Level1(width, height, multiplayer, highscore)
            else:
                if GamePage.check_completion() and isinstance(GamePage, Level1):
                    Transition = TransitionPage(
                        "Level 2", level2_paragraph, GamePage.stars
                    )
                    Transition.draw()
                    GamePage = Level2(
                        width,
                        height,
                        GamePage.stars,
                        multiplayer,
                        GamePage.players,
                        highscore,
                    )
                elif GamePage.check_completion() and isinstance(GamePage, Level2):
                    Transition = TransitionPage(
                        "Level 3", level3_paragraph, GamePage.stars
                    )
                    Transition.draw()
                    GamePage = Level3(
                        width, height, GamePage.stars, GamePage.players, highscore
                    )

                state = GamePage.run()

        elif state == "RESTART":
            transitioned = False
            state = "PLAY"


if __name__ == "__main__":
    main()
