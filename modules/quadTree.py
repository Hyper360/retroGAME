import pygame
from modules.settings import *

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()

class QuadTree():
    # QUAD TREES FOR LOSERS
    MAX_OBJECTS = 4

    def __init__(self, boundary : pygame.Rect):
        self.boundary = boundary
        self.objects = []
        self.children = [None] * 4


    def insert(self, rect : pygame.Rect):
        if not self.boundary.colliderect(rect):
            return False

        if len(self.objects) < QuadTree.MAX_OBJECTS:
            self.objects.append(rect)
            return True

        if all(self.children):
            for child in self.children:
                child.insert(rect)

        if not any(self.children):
            self._split()
            self.insert(rect)

        return False

    def collision(self, rect : pygame.Rect):
        if not self.boundary.colliderect(rect):
            return 0

        if all(self.children):
            for child in self.children:
                result = child.collision(rect)
                if result is not 0:
                    return result

        for obj in self.objects:
            if obj.colliderect(rect):
                return obj.ind
        
        return 0

    def _split(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width // 2
        h = self.boundary.height // 2

        self.children[0] = QuadTree(pygame.Rect(x, y, w, h))
        self.children[1] = QuadTree(pygame.Rect(x + w, y, w, h))
        self.children[2] = QuadTree(pygame.Rect(x, y+h, w, h))
        self.children[3] = QuadTree(pygame.Rect(x+w, y+h, w, h))

    def draw(self):
        self.color = (255, 255, 255)
        for obj in self.objects:
            pygame.draw.rect(screen, self.color, obj, 2)
        
        if any(self.children):
            for child in self.children:
                child.draw()

        pygame.draw.rect(screen, (200, 0, 0), self.boundary, 2)

        