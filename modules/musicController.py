import pygame
import os

class MusicController():
    def __init__(self, pathToMusic):
        self.Levels = {
            0 : "",
            1 : "",
            2 : "",
            3 : "",
            3 : ""
        }
        self.pathToMusic = pathToMusic
        self.music = [os.path.join(pathToMusic, music) for music in os.listdir(pathToMusic)]
        self.curLvlInd = 0
    
    def changeLvl(self, lvlInd):
        self.curLvlInd = lvlInd
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        self.playMusic()
    
    def playMusic(self):
        pygame.mixer.music.load(self.Levels[self.curLvlInd])
        pygame.mixer.music.play()

    def addMusicToLvl(self, lvlIndex : int, musicName : str):
        self.Levels[lvlIndex] = self.music[self.music.index(os.path.join(self.pathToMusic, musicName))]
