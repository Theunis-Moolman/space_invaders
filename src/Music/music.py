import stdaudio
import math
import threading


class Music:
    """
    Music handler that handles loading audio files, playing music in threads to prevent lag, and generating sound

    Args:
        None

    Author: Sydwell, Ben and Theunis
    """

    def __init__(self):
        self.sounds = {}
        self._playing = False

    def load(self, titles):
        for title in titles:
            self.sounds[title] = stdaudio.read(title)

    def play(self, title, loop=False):
        self._playing = True
        samples = self.sounds[title]

        def _play():
            while self._playing:
                for i in range(0, len(samples), 4096):
                    if not self._playing:
                        return
                    else:
                        stdaudio.playSamples(samples[i : i + 4096])
                if not loop:
                    break

        thread = threading.Thread(target=_play, daemon=True)
        thread.start()

    def stop(self):
        self._playing = False
