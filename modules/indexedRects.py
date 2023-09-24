import pygame

class IndRect(pygame.Rect):
    def __init__(self, x : int, y : int, width : int, height : int, ind : int):
        super().__init__(x, y, width, height)
        self.ind = ind

"""
***INDEX TOC***
0 = Grass
1 = Water
2 = Next lvl
3 = Lava
4 = Floor
"""