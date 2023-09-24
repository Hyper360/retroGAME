import pygame
import pickle
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from modules.indexedRects import IndRect
from modules.settings import *
from modules.quadTree import QuadTree

class Tile():
    def __init__(self, screen : pygame.Surface, x : int, y : int, imagePath : str, objType : int = 0):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(imagePath).convert_alpha(), (tileSize, tileSize))
        self.ind = objType
        if objType != 0:
            self.Rect = IndRect(self.x, self.y, tileSize, tileSize, objType)
            
    
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

class TileManager():
    GRID = [[None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,]

    TILE_LAYOUT = [[None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,
            [None] * 18,]
    
    GRASS = "assets/grass.png"
    WATER = "assets/water.png"
    LEVEL = "assets/nextLevel.png"
    LAVA = "assets/lava.png"
    BLOCK = "assets/border.png"
    PSPAWN = "assets/pSpawn.png"
    ESPAWN = "assets/eSpawn.png"
    
    TILE_LIST = [GRASS, WATER, LEVEL, LAVA, BLOCK, PSPAWN, ESPAWN]
    def __init__(self, screen : pygame.Surface, quadTree : QuadTree = None):
        self.screen = screen
        self.quadTree = quadTree
    
    def changeRow(self, row : int, col : int, TMpath : str, end : int = 1):
        for i in range(col, end):
            self.changeSingle(row, i, TMpath)

    def changeCol(self, row : int, col : int, TMpath : str, end : int = 1):
        for i in range(row, end):
            self.changeSingle(i, col, TMpath)
    
    def changeSingle(self, row : int, col : int, TMpath : str):
        if TMpath.find("water") >= 0:
            self.GRID[row][col] = Tile(self.screen, col * tileSize, row * tileSize, TMpath, objType=1)
            self.TILE_LAYOUT[row][col] = 1
        elif TMpath.find("Level") >= 0:
            self.GRID[row][col] = Tile(self.screen, col * tileSize, row * tileSize, TMpath, objType=2)
            self.TILE_LAYOUT[row][col] = 2
        elif TMpath.find("lava") >= 0:
            self.GRID[row][col] = Tile(self.screen, col * tileSize, row * tileSize, TMpath, objType=3)
            self.TILE_LAYOUT[row][col] = 3
        elif TMpath.find("bord") >= 0:
            self.GRID[row][col] = Tile(self.screen, col * tileSize, row * tileSize, TMpath, objType=4)
            self.TILE_LAYOUT[row][col] = 4
        elif TMpath.find("pSpawn") >= 0:
            self.GRID[row][col] = Tile(self.screen, col * tileSize, row * tileSize, TMpath, objType=5)
        elif TMpath.find("eSpawn") >= 0:
            self.GRID[row][col] = Tile(self.screen, col * tileSize, row * tileSize, TMpath, objType=5)
        else:
            self.GRID[row][col] = Tile(self.screen, col * tileSize, row * tileSize, TMpath)
            self.TILE_LAYOUT[row][col] = 0

    def loadTileLayout(self, tileLayout : str):
        tileLayout = pickle.load(tileLayout)
        for r in range(len(tileLayout)):
            for c in range(len(tileLayout[r])):
                type = tileLayout[r][c]
                self.GRID[r][c] = Tile(self.screen, c * tileSize, r * tileSize, self.TILE_LIST[type], objType=type)

    def draw(self):

        if any(self.GRID):
            for x in range(len(self.GRID)):
                for y in range(len(self.GRID[x])):
                    tile = self.GRID[x][y]

                    if tile != None:
                        tile.draw()