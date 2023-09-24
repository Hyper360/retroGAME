import pygame
from modules.settings import *

class Entity():
    def __init__(self, screen, row, col, imagePath, speed):
        self.screen = screen
        self.x = row * tileSize
        self.y = col * tileSize
        self.image = pygame.transform.scale(pygame.image.load(imagePath), (tileSize, tileSize))
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, tileSize, tileSize)
    
    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))