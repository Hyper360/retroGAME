import pygame
from modules.entity import Entity
from modules.settings import *
from modules.quadTree import QuadTree
from modules.timer import Timer
from modules.healthbar import HealthBar

class Player(Entity):
    def __init__(self, screen, row, col, imageDir, speed):
        super().__init__(screen, row, col, imageDir, speed)
        self.moveFree = [[1, 1],
                     [1, 1]] # Index 0 if for vertical movement, Index 1 is for horizontal movement
        self.ind = 0
        self.timer = Timer(50)
        self.HB = HealthBar(screen, (self.rect.x, self.rect.top), 100, self.rect.width, 5, "You", True, "assets/Dragon_Fire.ttf")
        self.moving = False
    
    def move(self, curTime : int):
        key = pygame.key.get_pressed()
        if self.timer.signal == True:
            if key[pygame.K_w]:
                self.y -= self.speed if self.moveFree[0][0] == 1 else 0
                self.moving = True if self.moveFree[0][0] else False
            elif key[pygame.K_s]:
                self.y += self.speed if self.moveFree[0][1] == 1 else 0
                self.moving = True if self.moveFree[0][1] else False
            elif key[pygame.K_a]:
                self.x -= self.speed if self.moveFree[1][0] == 1 else 0
                self.moving = True if self.moveFree[1][0] else False
            elif key[pygame.K_d]:
                self.x += self.speed if self.moveFree[1][1] == 1 else 0
                self.moving = True if self.moveFree[1][1] else False
            self.timer.reset(curTime) if self.moving else 0
        else:
            self.moving = False
        
        self.rect = pygame.Rect(self.x, self.y, tileSize, tileSize)
    
    def checkMoveFree(self, qt : QuadTree):
        up = pygame.Rect(self.x, self.y - self.speed, tileSize, tileSize)
        down = pygame.Rect(self.x, self.y + self.speed, tileSize, tileSize)
        left = pygame.Rect(self.x - self.speed, self.y, tileSize, tileSize)
        right = pygame.Rect(self.x + self.speed, self.y, tileSize, tileSize)

        # For each direction we adjust the "moveFree" according to the availability of space
        
        self.moveFree[0][0] = self.blockResponse(up, qt)

        self.moveFree[0][1] = self.blockResponse(down, qt)

        self.moveFree[1][0] = self.blockResponse(left, qt)

        self.moveFree[1][1] = self.blockResponse(right, qt)

        self.ind = qt.collision(self.rect)
        
        if self.rect.left - self.speed < 0:
            self.moveFree[1][0] = 0
        if self.rect.right + self.speed > screenW:
            self.moveFree[1][1] = 0
        if self.rect.top - self.speed < 0:
            self.moveFree[0][0] = 0
        if self.rect.bottom + self.speed > screenH:
            self.moveFree[0][1] = 0

        return 0
    def blockResponse(self, rect : pygame.Rect, qt : QuadTree):
        match qt.collision(rect):
            case 0:
                return 1
            case 1:
                return 0
            case 2:
                return 1
            case 3:
                return 0
            case 4:
                return 1
            case _:
                return 1


    def update(self, qt : QuadTree, curTime : int):
        self.checkMoveFree(qt)
        self.move(curTime)
        self.draw()
        self.HB.changePos(self.rect.x, self.rect.top-20)
        self.HB.draw()
        self.timer.update(curTime)
            