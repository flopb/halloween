import pygame
from time import sleep


class SoundManager():
    def __init__(self):
        self.path = 'assets/sounds/'
        pygame.init()
        pygame.mixer.init()
        self.effects = {}

    def playSong(self, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loops=0, start=30)

    def stopSong(self, fadeout_ms = 0):
        if fadeout_ms == 0:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.fadeout(fadeout_ms)

    def playFX(self, FX_name: str, loops=1, maxtime=0, fade_ms=0):
        effect = self.effects.get(FX_name)
        if effect is None:
            self.effects[FX_name] = pygame.mixer.Sound('assets/sounds/' + str(FX_name) + '.wav')

        self.effects[FX_name].play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)

        return self.effects[FX_name]
