from modules.mainImports import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption("An Apple A Day...")
    clock = pygame.time.Clock()
    pygame.mixer.music.load("music/TheFloorIsLava.mp3")
    pygame.mixer.music.play(-1)
    scanLines = pygame.image.load("assets/scanLines.png")
    scanLines.set_alpha(100)

    QT = QuadTree(pygame.Rect(0, 0, screenW, screenH))
    TM = TileManager(screen, QT)
    MC = MusicController(os.path.join(os.path.dirname(__file__), "music"))
    MC.addMusicToLvl(0, "Eat.mp3")
    MC.addMusicToLvl(1, "FastEater.mp3")
    MC.addMusicToLvl(2, "StillFollowingMe.mp3")
    MC.addMusicToLvl(3, "TheFloorIsLava.mp3")
    MC.addMusicToLvl(4, "SomewhereInTheMaze.mp3")
    MC.addMusicToLvl(5, "lost.mp3")
    MC.addMusicToLvl(6, "amen.mp3")
    hurtTimer = Timer(1000)
    damageTimer = Timer(500)

    levelInd = 0
    TM.loadTileLayout(open(levels[levelInd], "rb"))
    enemyList = []
    enemyList.append(Enemy(screen, enemyCmds[levelInd][0], enemyCmds[levelInd][1], "assets/doctor.png", 4, TM.returnMatrix()))
    player = Player(screen, playerCmds[levelInd][0], playerCmds[levelInd][1], "assets/player.png", tileSize//2)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        screen.fill((255, 255, 255))
        curTime = pygame.time.get_ticks()

        TM.draw()
        player.update(QT, curTime)
        damageTimer.update(curTime)

        # Hurt Timer
        hurtTimer.update(curTime)
        if hurtTimer.signal == True:
            player.HB.deduct_health(5)
            hurtTimer.reset(curTime)

        # Check if the player touched the level tile
        if player.ind == 2:
            QT = QuadTree(pygame.Rect(0, 0, screenW, screenH))
            TM = TileManager(screen, QT)
            levelInd += 1
            TM.loadTileLayout(open(levels[levelInd], "rb"))
            MC.changeLvl(levelInd)
            enemyList.clear()
            if levelInd > 3:
                for i in range(len(enemyCmds[levelInd])):
                    enemyList.append(Enemy(screen, enemyCmds[levelInd][i][0], enemyCmds[levelInd][i][1], "assets/doctor.png", 4, TM.returnMatrix()))
                player = Player(screen, playerCmds[levelInd][0][0], playerCmds[levelInd][0][1], "assets/player.png", tileSize//2)
            else:         
                enemyList.append(Enemy(screen, enemyCmds[levelInd][1], enemyCmds[levelInd][1], "assets/doctor.png", 4, TM.returnMatrix()))
                player = Player(screen, playerCmds[levelInd][0], playerCmds[levelInd][1], "assets/player.png", tileSize//2)

        # Enemy stuff
        for enemy in enemyList:
            enemy.update()
            enemy.draw()
            if player.moving == True:
                enemy.createPath((player.rect.centerx//tileSize, player.rect.centery//tileSize))

        # Check if player rectangle collides with any of the enemies
        if damageTimer.signal:
            for enemy in enemyList:
                if player.rect.colliderect(enemy.rect):
                    player.HB.deduct_health(10)
                    damageTimer.reset(curTime)

        screen.blit(scanLines, (0,0))
        pygame.display.flip()
        clock.tick(60)
        

