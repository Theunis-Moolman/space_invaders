import stdaudio
import threading
import time


class Music:
    """
    Music handler that handles loading audio files, playing music in threads to prevent lag, and generating sound

    Args:
        None

    Author: Sydwell, Ben and Theunis
    """

    def __init__(self):
        self.sounds = {}

        # Thread variable to determine if it should play
        self._playing = True

        # Thread variable to determine if the audio should loop
        self._loop = False

        # Current sample to prevent clashing
        self._current_sample = None

        # Current sfx sample to prevent clashing
        self._sfx_samples = None

        # Cooldown to prevent sfx overwrite
        self.sfx_cooldown = 0

        # Music main thread
        self.thread = threading.Thread(target=self._play, daemon=True)
        self.thread.start()

    def load(self, titles):
        # Load title into list to prevent lag due to loading files over and over again
        for title in titles:
            self.sounds[title] = stdaudio.read(title)

    def _play(self):
        i = 0

        # Main thread that runs continuously while playing is true
        while self._playing:

            # Check if sfx sample is not none
            if self._sfx_samples is not None:

                # Prevent clashing
                sfx = self._sfx_samples

                # Remove from queue so that it plays once
                self._sfx_samples = None

                # Play sample in batches (From earlier from audio clashes)
                for j in range(0, len(sfx), 4096):
                    # Play batch
                    stdaudio.playSamples(sfx[j : j + 4096])
                #
                if self._current_sample:

                    i = (i + len(sfx)) % len(self._current_sample)

            # Prevent clashing
            sample = self._current_sample

            # Check if sample is not none to prevent indexing errors
            if sample is not None:
                stdaudio.playSamples(sample[i : i + 4096])
                # Move to next batch
                i += 4096

                # Check if end of file is reached
                if i >= len(sample):
                    # Reset to start if looping
                    if self._loop:
                        i = 0
                    # Else destroy sample
                    else:
                        self._current_sample = None
                        i = 0
            else:
                time.sleep(0.1)  # Prevent the CPU from suffering due to spinning

    def play(self, title, loop=False, sfx=False):
        # Play sfx
        if sfx:
            if time.time() - self.sfx_cooldown > 2:
                self.sfx_cooldown = time.time()
                self._sfx_samples = self.sounds[title]
        # Play music
        else:
            self._loop = loop
            self._current_sample = self.sounds[title]
            i = 0

    # Stop the current sample and remove looping
    def stop(self):
        self._current_sample = None
        self._loop = False
