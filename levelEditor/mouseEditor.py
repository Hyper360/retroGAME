import pygame

class mouseEdit():
    def __init__(self, screen, tileSize, ROWS, COLS):
        self.screen = screen
        self.tileSize = tileSize
    
    def getClick(self):
        mouseClick = pygame.mouse.get_pressed()[0]
        mousePos = pygame.mouse.get_pos()
        ROW = mousePos[1]//self.tileSize
        COL = mousePos[0]//self.tileSize

        if mouseClick:
            return (COL, ROW)
        
        return False

    def draw(self):
        mousePos = pygame.mouse.get_pos()
        ROW = mousePos[1]//self.tileSize
        COL = mousePos[0]//self.tileSize
        rect = pygame.Rect(COL * self.tileSize, ROW * self.tileSize, self.tileSize, self.tileSize)

        pygame.draw.rect(self.screen, (0, 200, 0), rect, 2)
    
    def update(self):
        self.getClick()
        self.draw()