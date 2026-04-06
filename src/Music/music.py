import stdaudio
import math
import threading


class Music:
    def __init__(self):
        self.sounds = {}

    def load(self, titles):
        for title in titles:
            self.sounds[title] = stdaudio.read(title)

    def play(self, title):
        thread = threading.Thread(target=stdaudio.playSamples, args=(self.sounds[title],), daemon=True)
        thread.start()

    def sound(self, pitch, rate):
        SAMPLE_RATE = rate  # Standard audio sample rate
        duration = 0.2       # 200 milliseconds
        frequency = pitch
        samples = []
        for i in range(int(SAMPLE_RATE * duration)):
            t = i / SAMPLE_RATE
        # Volume decays over time
            volume = 1.0 - (t / duration)  
        # Frequency slides down slightly for effect
            freq = frequency * (1.0 - 0.3 * t / duration)  
            sample = volume * math.sin(2 * math.pi * freq * t)
            samples.append(sample)
    
        #stdaudio.playSamples(samples)


