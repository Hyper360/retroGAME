import pygame
import os
import pickle

from editorTileManager import TileManager
from mouseEditor import mouseEdit
from modules.settings import *

pygame.init()
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("Level Editor", "Level Editor")
clock = pygame.time.Clock()

levelsDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "levels")
spawnsDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spawns")
levelsList = [os.path.join(levelsDir, level) for level in os.listdir(levelsDir)]

TM = TileManager(screen)
ME = mouseEdit(screen, tileSize, ROWS, COLS)
ind = 0
fill = True

playerSpawn = []
enemySpawn = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                levelsList = [os.path.join(levelsDir, level) for level in os.listdir(levelsDir)]
                if all(TM.TILE_LAYOUT):
                    # Saving level
                    pickleOut = open(os.path.join(levelsDir, "level"+str(len(levelsList))),"wb")
                    pickle.dump(TM.TILE_LAYOUT, pickleOut)
                    pickleOut.close()

                    # Saving Spawn Pos
                    pickleOut = open(os.path.join(spawnsDir, "spawn"+str(len(levelsList))),"wb")
                    pickle.dump([playerSpawn, enemySpawn], pickleOut)
                    pickleOut.close()
                else:
                    print("Finish the level fool >:(")
            
            if event.key == pygame.K_f:
                fill = False if fill == True else True
            
            key = pygame.key.name(event.key)
            if str(key).isdigit():     
                ind = int(key) if str(key).isdigit() < len(TileManager.TILE_LIST) else ind

    screen.fill((230, 230, 230))
    TM.draw()
    ME.draw()


    if ME.getClick() != False:
        if fill == True:
            for i in range(ROWS):
                TM.changeRow(i, 0, TileManager.TILE_LIST[ind], COLS)

        if ind == 5:
            playerSpawn = [[ME.getClick()[0], ME.getClick()[1]]]
            
        if ind == 6:
            if enemySpawn.__contains__([ME.getClick()[0], ME.getClick()[1]]):
                pass
            else:
                enemySpawn.append([ME.getClick()[0], ME.getClick()[1]])

        else:
            TM.changeSingle(ME.getClick()[1], ME.getClick()[0], TileManager.TILE_LIST[ind]) 

    pygame.display.flip()
    clock.tick(60)
