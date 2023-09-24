import pickle
import os
# Level Loading
levelsDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "levels")
levels = [os.path.join(levelsDir, level) for level in os.listdir(levelsDir)]


# Spawn Position
enemyCmds = {
}
playerCmds = {
}
    
spawnDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spawns")
spawnList = [os.path.join(spawnDir, level) for level in os.listdir(spawnDir)]

for i in range(len(spawnList)):
    spawn = pickle.load(open(spawnList[i], "rb"))
    enemyCmds[i] = spawn[1]
    playerCmds[i] = spawn[0]
