import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from modules.entity import Entity
from modules.settings import *

class Enemy(Entity):
    def __init__(self, screen : pygame.Surface, row : int, col : int, imagePath : str, speed : int, grid : list):
        super().__init__(screen, row, col, imagePath, speed)
        self.direction = pygame.math.Vector2(0, 0)
        self.grid = Grid(width=COLS, height=ROWS, matrix=grid)
        self.pos = self.rect.center

        self.path = []
        self.collisionRects = []
    
    def emptyPath(self):
        self.path = []

    def getCoord(self):
        col = self.rect.centerx // tileSize
        row = self.rect.centery // tileSize

        return (col, row)

    def createPath(self, endCoord : tuple):
        startX, startY = self.getCoord()
        start = self.grid.node(startX, startY)

        col = endCoord[0]
        row = endCoord[1]
        end = self.grid.node(col, row)

        finder = AStarFinder()
        self.path,_ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        
        self.setPath(self.path)
    
    def createCollisionRects(self):
        if self.path:
            self.collisionRects = []
            for point in self.path:
                x, y = point
                x = (x * tileSize) + tileSize//2
                y = (y * tileSize) + tileSize//2
                rect = pygame.Rect(x-2, y-2, 4, 4)
                self.collisionRects.append(rect)
    
    def getDirection(self):
        if len(self.collisionRects) > 1:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collisionRects[1].center)
            self.direction = (end-start).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []
            self.collisionRects = []
    
    def checkCollision(self):
        if len(self.collisionRects) > 1:
            for rect in self.collisionRects:
                if rect.collidepoint(self.pos):
                    del self.collisionRects[1]
                    self.getDirection()
        else:
            self.emptyPath()
            self.collisionRects = []

    def update(self):
        self.pos += self.direction * self.speed
        self.checkCollision()
        self.rect.center = self.pos
        
        self.draw()

    def setPath(self, path):
        self.path = path
        self.createCollisionRects()
        self.getDirection()
    