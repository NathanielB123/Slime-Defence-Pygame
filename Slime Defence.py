print("Loading... please wait. This may take a while.")
print("Please do not click on this window while the game is loading.")
import time  # Imports all libraries necessary for the game to run
import random
import math
import pygame
import ctypes
import _pickle
import os.path

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()  # Removes scaling done by Windows 10 on some monitors that can cause issues
ScreenRes = (1920,
             1080)  # Sets and stores the resolution of the window (right now only 1920 by 1080, meaning that monitors of other resolutions may have black bars or blurry visuals - for more explanation on why, see the comment a few lines down from this one)
Window = pygame.display.set_mode(ScreenRes,
                                 pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)  # Creates the display (DOUBLEBUF turns on v-sync to prevent tearing, HWSURFACE forces the use of VRAM if available instead of system RAM being used, leading to better performance)
pygame.mouse.set_cursor(*pygame.cursors.diamond)  # Makes the cursor a diamond for easier aiming and aesthetics
GameRes = [384, 216]
Tile = pygame.transform.scale(pygame.image.load("Images\Tile.png").convert_alpha(), (
    ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))  # Loads all the game's images
SpawnerTile = pygame.transform.scale(pygame.image.load("Images\SpawnerTile.png").convert_alpha(), (
    ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[
        1] * 24))  # ScreenRes over GameRes gets the ratio and therefore the amount the width or height of each image needs to be multiplied by to display correctly on other screens. In the game, resolution is kept at 1920 by 1080 because I experienced some odd bugs with other resolutions likely due to using DIV (//) rather than division. Ultimately, most monitors are 1920 by 1080 though and forcing the resolution on non-native monitors seemed to work well enough, and odd aspect ratios would likely end up stretching the images, so, in the end, I just kept it as it was and made 1920 by 1080 forced instead of allowing other resolutions.
Wall = pygame.transform.scale(pygame.image.load("Images\Wall.png").convert_alpha(),
                              (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
Rock = pygame.transform.scale(pygame.image.load("Images\Rock.png").convert_alpha(),
                              (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
MetalWall = pygame.transform.scale(pygame.image.load("Images\WallMetal.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
Trap = pygame.transform.scale(pygame.image.load("Images\Trap.png").convert_alpha(),
                              (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
Turret = pygame.transform.scale(pygame.image.load("Images\SlimeTurret.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
Chest = pygame.transform.scale(pygame.image.load("Images\Chest.png").convert_alpha(),
                               (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
OpenChest = pygame.transform.scale(pygame.image.load("Images\ChestOpen.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
Slime = pygame.transform.scale(pygame.image.load("Images\Slime.png").convert_alpha(),
                               (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
BobbySlime = pygame.transform.scale(pygame.image.load("Images\Bobby.png").convert_alpha(),
                                    (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
BigSlime = pygame.transform.scale(pygame.image.load("Images\BigSlime.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 48, ScreenRes[1] // GameRes[1] * 48))
BigSlimeDamaged = pygame.transform.scale(pygame.image.load("Images\BigSlimeDamaged.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 48, ScreenRes[1] // GameRes[1] * 48))
LongJumpSlime = pygame.transform.scale(pygame.image.load("Images\LongJumpSlime.png").convert_alpha(),
                                       (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
ShootingSlime = pygame.transform.scale(pygame.image.load("Images\ShootingSlime.png").convert_alpha(),
                                       (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
ProjectileWhite = pygame.transform.scale(pygame.image.load("Images\SlimeProjectileWhite.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
ProjectileBlack = pygame.transform.scale(pygame.image.load("Images\SlimeProjectileBlack.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
Arrow = pygame.transform.scale(pygame.image.load("Images\ArrowWhite.png").convert_alpha(),
                               (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
Shadow = pygame.transform.scale(pygame.image.load("Images\Shadow.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
ChestMarker = pygame.transform.scale(pygame.image.load("Images\ChestMarker.png").convert_alpha(),
                                     (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
BigShadow = pygame.transform.scale(pygame.image.load("Images\BigShadow.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 48, ScreenRes[1] // GameRes[1] * 48))
Background = pygame.transform.scale(pygame.image.load("Images\Background.png").convert_alpha(), (
    ScreenRes[0] // GameRes[0] * ScreenRes[0], ScreenRes[1] // GameRes[1] * ScreenRes[1]))
Credits = pygame.transform.scale(pygame.image.load("Images\Credits.png").convert_alpha(),
                                 (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216))
Instructions = pygame.transform.scale(pygame.image.load("Images\Instructions.png").convert_alpha(),
                                      (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216))
GameOverScreen = pygame.transform.scale(pygame.image.load("Images\GameOver.png").convert_alpha(),
                                        (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216))
Hints = [pygame.transform.scale(pygame.image.load("Images\HelpText.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint1.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint2.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint3.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint4.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint5.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint6.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint7.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint8.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint9.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint10.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint11.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint12.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
         pygame.transform.scale(pygame.image.load("Images\Hint13.png").convert_alpha(),
                                (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216))]
MenuScreens = [pygame.transform.scale(pygame.image.load("Images\Menu1.png").convert_alpha(),
                                      (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
               pygame.transform.scale(pygame.image.load("Images\Menu2.png").convert_alpha(),
                                      (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
               pygame.transform.scale(pygame.image.load("Images\Menu3.png").convert_alpha(),
                                      (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
               pygame.transform.scale(pygame.image.load("Images\Menu4.png").convert_alpha(),
                                      (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
               pygame.transform.scale(pygame.image.load("Images\Menu5.png").convert_alpha(),
                                      (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216))]
SettingScreen = pygame.transform.scale(pygame.image.load("Images\Settings.png").convert_alpha(),
                                       (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216))
SelectedSettings = [pygame.transform.scale(pygame.image.load("Images\SoundsOn.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\SoundsOff.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\MusicOn.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\MusicOff.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\DifficultyEasySelected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\DifficultyMediumSelected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\DifficultyHardSelected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\MapSizeSmallSelected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\MapSizeMediumSelected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\MapSizeLargeSelected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\MapSizeHugeSelected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\GameSpeed0.5Selected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\GameSpeed1Selected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\GameSpeed2Selected.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\SmallModeOn.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    pygame.transform.scale(pygame.image.load("Images\SmallModeOff.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216))]
ActiveSettings = [pygame.transform.scale(pygame.image.load("Images\SoundsActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\MusicActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\DifficultyEasyActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\DifficultyMediumActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\DifficultyHardActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\MapSizeSmallActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\MapSizeMediumActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\MapSizeLargeActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\MapSizeHugeActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\GameSpeed0.5Active.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\GameSpeed1Active.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\GameSpeed2Active.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                  pygame.transform.scale(pygame.image.load("Images\SmallModeActive.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216))]
Hero = [pygame.transform.scale(pygame.image.load("Images\Archer1.png").convert_alpha(),
                               (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
        pygame.transform.scale(pygame.image.load("Images\Archer2.png").convert_alpha(),
                               (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
        pygame.transform.scale(pygame.image.load("Images\Archer1.png").convert_alpha(),
                               (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
        pygame.transform.scale(pygame.image.load("Images\Archer3.png").convert_alpha(),
                               (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))]
Bow = [pygame.transform.scale(pygame.image.load("Images\Bow1.png").convert_alpha(),
                              (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
       pygame.transform.scale(pygame.image.load("Images\Bow4.png").convert_alpha(),
                              (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
       pygame.transform.scale(pygame.image.load("Images\Bow3.png").convert_alpha(),
                              (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
       pygame.transform.scale(pygame.image.load("Images\Bow2.png").convert_alpha(),
                              (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
       pygame.transform.scale(pygame.image.load("Images\Bow5.png").convert_alpha(),
                              (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))]
ArrowShoot = pygame.mixer.Sound("Sounds\ArrowShoot.wav")  # Loads the game's sounds
EnemyHit = pygame.mixer.Sound("Sounds\EnemyHit.wav")
SlimeJump = pygame.mixer.Sound("Sounds\SlimeJump.wav")
Music = pygame.mixer.Sound("Sounds\MusicIdea1.wav")
pygame.mixer.set_num_channels(
    10)  # Sets the number of different sounds that can be played simultaneously to 10 (can be higher but 10 seems a decent number for now)


def InitNavGrid(Grid, NavGrid, x, y, CharPos, FrameTime,
                Settings):  # Function for converting the list Grid which has information on what each tile is into a mostly-empty new list, NavGrid, which will be used for the enemy's pathfinding
    while y < len(Grid):
        if x == len(Grid[0]):
            x = 0
            NavGrid.append([])
        while x < len(Grid[0]):
            if Grid[y][x] == "C" or (CharPos[0] // 24 == x and CharPos[
                1] // 24 == y):  # Chests or the player's position are given the value 100, meaning tiles up to 100 tiles away from them will be given values and the enemies will be able to path-find from them
                NavGrid[y].append(100)
            elif Grid[y][x] == "W" or Grid[y][x] == "M" or Grid[y][x] == "R" or Grid[y][
                x] == "P":  # Walls, metal walls, rocks and turrets are given the value -1 making sure the enemies will never jump onto those tiles
                NavGrid[y].append(-1)
            else:
                NavGrid[y].append(
                    0)  # Any other tiles are given the value 0 but will likely be changed to higher values after NavGridConstruct finishes
            x += 1
        y += 1
        if (time.time() - FrameTime) > Settings[
            4]:  # To avoid major lag spikes, the function saves its current progress by returning the x and y values it reached as well as the half-finished NavGrid if the time taken for it exceeds the value for the amount of time each frame should take
            return NavGrid, x, y
    return (NavGrid, x,
            y)  # The finished NavGrid is returned along with the x and y values it reached so Main() knows it has finished


def NavGridConstruct(NavGrid, Temp, FrameTime,
                     Settings):  # Function for making each empty tile in the NavGrid have a value assigned to it representing how close it is to the chest or the player
    i = Temp
    Done = 0
    while Done == 0:
        Done = 1
        for y in range(0, len(NavGrid)):
            for x in range(0, len(NavGrid[y])):
                if NavGrid[y][x] == i:
                    Done = 0  # If a tile has been found with the value of the value of the tiles being looked at, the function has not finished checking and so Done is set to 1
                    for Coord in [(1, 0), (-1, 0), (0, -1), (0,
                                                             1)]:  # Tiles above, below and to the right and left of the tile being looked at are assigned the value of the tile being looked at subtract 1 so each tile further away from the objectives has a lower and lower value
                        try:  # Try... except; because the code definitely works and the only errors are from checking tiles on the grid that do not exist (past the boundaries). Try except prevents these errors from crashing the program and is easier to implement than a check for if the tile being looked at is outside the Grid but ends up having the exact same effect.
                            if NavGrid[y + Coord[1]][x + Coord[0]] == 0:
                                NavGrid[y + Coord[1]][x + Coord[0]] = i - 1
                        except IndexError:
                            pass
        if i > 1:
            i -= 1
        else:
            return ([NavGrid, i,
                     Done])  # If the function has started looking at tiles with a value of 1, the function has finished and the finished NavGrid is returned
        if time.time() - FrameTime > Settings[
            4] and not i == Temp:  # To avoid major lag spikes, the function saves its current progress by returning the half-finished NavGrid and values saving its progress if the time taken for it exceeds the value for the amount of time each frame should take
            return [NavGrid, i, Done]
    return ([NavGrid, i,
             Done])  # If there are no tiles with the value of the value of tiles being checked, the functions has finished and the finished NavGrid is returned


def GridGen(Settings):  # Function for generating a basic grid of tiles with a chest, enemy spawn zone, walls and rocks
    Grid = []
    XLength = Settings[3]  # Settings[3] contains the value for the width and height of the map
    YLength = Settings[3]
    for i in range(0, YLength):
        Grid.append([])
        for i2 in range(0, XLength):
            RandomNum = -1
            if i == YLength // 2 and i2 == XLength // 2:  # Key: C: Chest W: Slime Wall S: Enemy Spawn Area E: Empty M: Metal Wall T: Slime Trap V: Rock P: Turret O: Open Chest
                Grid[i] += "C"
            elif i == 0 or i == YLength - 1 or i2 == 0 or i2 == XLength - 1:
                Grid[i] += "M"
            elif i == 1 or i == YLength - 2 or i2 == 1 or i2 == XLength - 2:
                Grid[i] += "S"
            else:
                RandomNum = random.randint(0,
                                           12)  # If a metal wall, chest or spawn zone does not need to be placed on a particular tile, it is an empty tile and has a chance to have a rock placed on it
            if RandomNum == 12:
                if not (i + 1, i2) == (XLength // 2, YLength // 2) and not (i, i2 + 1) == (
                        XLength // 2, YLength // 2) and not (i - 1, i2) == (XLength // 2, YLength // 2) and not (i,
                                                                                                                 i2 - 1) == (
                                                                                                                        XLength // 2,
                                                                                                                        YLength // 2):  # Prevents walls from spawning right next to the chest
                    Grid[i] += "R"
                elif not RandomNum == -1:
                    Grid[i] += "E"
            elif not RandomNum == -1:
                Grid[i] += "E"
    return Grid  # Returns the Grid of tiles


def EnemyTick(Grid, NavGrid, EnemyList, CharPos, BowInfo, UpdateNeeded, EnemySpawnData, CamPos, Settings, GameTicks,
              Score):  # Function for handling the enemies' AI and movement as well as arrows shot by the bow
    GameOver = [0, "Nothing",
                "Nothing"]  # GameOver is set to 0 at the start so if it is not changed then the player must be still alive
    ToKill = []  # Creates the list of enemies that should be removed from the list after the main part of the function has finished
    if EnemySpawnData[
        1] == 0:  # Handles enemy spawning if a wave needs to spawn (EnemySpawnData[1] is the countdown timer to spawning)
        if EnemySpawnData[2] // 24 == EnemySpawnData[
            2] / 24:  # Makes it so every 24 frames more enemies are spawned if need be
            EnemySpawnData[2] += 1
            BigSlimes = 0
            for Enemy in EnemyList:
                if Enemy[0] == "BigSlime":
                    BigSlimes += 1
            if random.randint(0, 6) == 0:
                EnemyList.append(
                    ["LongJumpSlime", random.choice((1, len(Grid[0]) - 2)), random.randint(1, len(Grid) - 2),
                     "Still"])  # Spawns slimes on the vertical or horizontal rows of the map
            elif random.randint(0, 6) == 0:
                EnemyList.append(
                    ["LongJumpSlime", random.randint(1, len(Grid[0]) - 2), random.choice((1, len(Grid) - 2)), "Still"])
            elif random.randint(0, 9) == 0:
                EnemyList.append(
                    ["ShootingSlime", random.choice((1, len(Grid[0]) - 2)), random.randint(1, len(Grid) - 2), "Still"])
            elif random.randint(0, 9) == 0:
                EnemyList.append(
                    ["ShootingSlime", random.randint(1, len(Grid[0]) - 2), random.choice((1, len(Grid) - 2)), "Still"])
            elif random.randint(0, 12) == 0 and BigSlimes < round(EnemySpawnData[0] * Settings[2] * 0.1):
                EnemyList.append(
                    ["BigSlime", random.choice((1, len(Grid[0]) - 3)), random.randint(1, len(Grid) - 3), "Still2"])
            elif random.randint(0, 12) == 0 and BigSlimes < round(EnemySpawnData[0] * Settings[2] * 0.1):
                EnemyList.append(
                    ["BigSlime", random.randint(1, len(Grid[0]) - 3), random.choice((0, len(Grid) - 3)), "Still2"])
            elif random.randint(0, 48) == 0:
                EnemyList.append(
                    ["BobbySlime", random.choice((1, len(Grid[0]) - 2)), random.randint(1, len(Grid) - 2), "Still"])
            elif random.randint(0, 48) == 0:
                EnemyList.append(
                    ["BobbySlime", random.choice((1, len(Grid[0]) - 2)), random.randint(1, len(Grid) - 2), "Still"])
            else:
                EnemyList.append(["BasicSlime", random.choice((1, len(Grid[0]) - 2)), random.randint(1, len(Grid) - 2),
                                  "Still"])  # Or spawns two basic slimes one on the horizontal and one on the vertical rows
                EnemyList.append(
                    ["BasicSlime", random.randint(1, len(Grid[0]) - 2), random.choice((1, len(Grid) - 2)), "Still"])
        elif round(EnemySpawnData[2] / 24) < Settings[2] * (EnemySpawnData[
                                                                0] + 1):  # If more enemies need to be spawned, the amount is increased (Settings[2] is the difficulty)
            EnemySpawnData[2] += 1
        else:  # If the wave has ended, countdown to the next wave begins
            EnemySpawnData[0] += 1  # EnemySpawnData[0] is the number of the wave the player has reached so far
            EnemySpawnData[1] = 480
            EnemySpawnData[2] = 0
            Score += 20
            # WIP feature
            # if EnemySpawnData[0]/RandomNum==EnemySpawnData[0]//RandomNum: #Every so often, the chest is opened and a new chest spawns
            # for y in range(0,len(Grid)):
            # for x in range(0,len(Grid[0])):
            # if Grid[y][x]=="C":
            # ChestPos=(x,y)
            # Grid[y][x]="O"
            # while not ChestPos=="Done":
            # y=random.randint(0,len(Grid)-1)
            # x=random.randint(0,len(Grid[0])-1)
            # if Grid[y][x]=="E" and not NavGrid[y][x]==0 and not (x,y)==ChestPos:
            # Grid[y][x]="C"
            # UpdateNeeded=1
            # EnemyList=[]
            # ChestPos="Done"
    else:
        EnemySpawnData[1] -= 1  # If a wave is not being spawned, the countdown timer to  the next wave is reduced
    if BowInfo[
        1] == 12:  # If the bow is ready to shoot an arrow, an arrow is spawned at the player's tile heading in the direction they are aiming
        if Settings[0] == 1:
            ArrowShoot.play()
        if BowInfo[0] == "Right":
            EnemyList.append(
                ["Arrow", int(round((CharPos[0] + 18) / 24) * 24), int(round(CharPos[1] // 24) * 24), [12, 0]])
        elif BowInfo[0] == "Left":
            EnemyList.append(
                ["Arrow", int(round((CharPos[0] - 6) / 24) * 24), int(round(CharPos[1] // 24) * 24), [-12, 0]])
        elif BowInfo[0] == "Up":
            EnemyList.append(["Arrow", int(round(CharPos[0] / 24) * 24), int(round((CharPos[1]) // 24) * 24), [0, -12]])
        else:
            EnemyList.append(
                ["Arrow", int(round(CharPos[0] / 24) * 24), int(round((CharPos[1] + 24) // 24) * 24), [0, 12]])
        BowInfo[1] -= 1
    elif BowInfo[1] > 0:  # Increases the frame of animation for the bow if it is being fired
        BowInfo[1] -= 1
    for y in range(0, len(Grid)):  # Code for turrets shooting
        for x in range(0, len(Grid[0])):
            if Grid[y][x] == "P":
                if GameTicks // 192 == GameTicks / 192:  # Will make the turret shoot every 48 frames, cycling through directions up, right, down and left
                    EnemyList.append(["FriendProjectile", x * 24 + 18, y * 24, [6, 0]])
                    if Settings[0] == 1 and y * 24 - CamPos[1] < GameRes[1] // 2 and x * 24 - CamPos[0] < GameRes[
                        0] // 2 and y * 24 - CamPos[1] > GameRes[1] // 2 * -1 - 24 and x * 24 - CamPos[0] > GameRes[
                        0] // 2 * -1 - 24:
                        ArrowShoot.play()
                elif (GameTicks + 48) // 192 == (GameTicks + 48) / 192:
                    EnemyList.append(["FriendProjectile", x * 24, y * 24, [0, -6]])
                    if Settings[0] == 1 and y * 24 - CamPos[1] < GameRes[1] // 2 and x * 24 - CamPos[0] < GameRes[
                        0] // 2 and y * 24 - CamPos[1] > GameRes[1] // 2 * -1 - 24 and x * 24 - CamPos[0] > GameRes[
                        0] // 2 * -1 - 24:
                        ArrowShoot.play()
                elif Settings[0] == 1 and (GameTicks + 96) // 192 == (GameTicks + 96) / 192:
                    EnemyList.append(["FriendProjectile", x * 24 - 6, y * 24, [-6, 0]])
                    if y * 24 - CamPos[1] < GameRes[1] // 2 and x * 24 - CamPos[0] < GameRes[0] // 2 and y * 24 - \
                            CamPos[1] > GameRes[1] // 2 * -1 - 24 and x * 24 - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                        ArrowShoot.play()
                elif Settings[0] == 1 and (GameTicks + 144) // 192 == (GameTicks + 144) / 192:
                    EnemyList.append(["FriendProjectile", x * 24, y * 24 + 24, [0, 6]])
                    if Settings[0] == 1 and y * 24 - CamPos[1] < GameRes[1] // 2 and x * 24 - CamPos[0] < GameRes[
                        0] // 2 and y * 24 - CamPos[1] > GameRes[1] // 2 * -1 - 24 and x * 24 - CamPos[0] > GameRes[
                        0] // 2 * -1 - 24:
                        ArrowShoot.play()
    for i in range(0, len(EnemyList)):  # Updates the status of every enemy (or arrow) currently alive
        if EnemyList[i][0] == "BasicSlime":  # Code for if the enemy is a basic green slime
            if EnemyList[i][3] == "Still":  # If the slime is still, the countdown to jumping starts
                EnemyList[i][3] = "WindUp"
                EnemyList[i].append(0)
            elif EnemyList[i][3] == "Jumping":
                if EnemyList[i][4] == 24:  # If the slime has finished jumping, the slime's position is moved
                    EnemyList[i][3] = "Still"
                    EnemyList[i][1] += EnemyList[i][5][0]
                    EnemyList[i][2] += EnemyList[i][5][1]
                    EnemyList[i].pop()
                    EnemyList[i].pop()
                    if CharPos[0] // 24 == EnemyList[i][1] and CharPos[1] // 24 == EnemyList[i][
                        2]:  # Checks for if the slime has jumped on the player or the chest and it is game over
                        GameOver[0] = 1
                        GameOver[1] = "BasicSlime"
                        GameOver[2] = "Hero"
                    elif Grid[EnemyList[i][2]][EnemyList[i][1]] == "C":
                        GameOver[0] = 1
                        GameOver[1] = "BasicSlime"
                        GameOver[2] = "Chest"
                    elif Grid[EnemyList[i][2]][
                        EnemyList[i][1]] == "T":  # Checks if the slime has jumped on a trap and should be killed
                        if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                            1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                            1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[
                            0] // 2 * -1 - 24:  # Check for if the slime is on screen (otherwise the sound should not be played)
                            EnemyHit.play()  # Plays the sound effect for the enemy being hit
                        Grid[EnemyList[i][2]][EnemyList[i][
                            1]] = "E"  # Being trapped doesn't spawn a wall - intentional mechanic rather than oversight :P Traps not making the enemy spawn their associated tile on death increases gameplay tactics and opportunities
                        ToKill.append(i)
                else:
                    EnemyList[i][4] += 1  # If the slime is still jumping, the amount they have jumped is increased
            elif EnemyList[i][3] == "WindUp" and EnemyList[i][
                4] == 48:  # If the slime is ready to jump, the tile to which they should is decided
                EnemyList[i].pop()
                EnemyList[i][3] = "Jumping"
                EnemyList[i].append(1)
                Moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
                random.shuffle(Moves)  # Randomises order in which moves will be checked resulting in random movement
                Moved = 0
                for TempMove in Moves:
                    try:  # Try... except; because the code definitely works and the only errors are from checking tiles on the grid that do not exist (past the boundaries). Try except removes these errors from crashing the program and is easier to implement than a check for if the tile being looked at is outside the Grid
                        if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] > \
                                NavGrid[EnemyList[i][2]][
                                    EnemyList[i][
                                        1]]:  # If the value of the tile for how close it is to the chest or the player is higher than the slimes current tile it is on, the slime picks that option
                            EnemyList[i].append(TempMove)
                            Moved = 1
                    except IndexError:
                        pass
                    if Moved == 1:  # No other options are checked if one move found is good
                        break
                if Moved == 0:  # If the slime does not pick a move, it is likely blocked off from the player and objective and so becomes a big slime to be able to destroy the blocking walls if the amount spawned already is not too high or moves randomly if not
                    BigSlimes = 0
                    for Enemy in EnemyList:
                        if Enemy[0] == "BigSlime":
                            BigSlimes += 1
                    if BigSlimes < round(EnemySpawnData[0] * Settings[
                        2] * 0.1):  # Settings[2] is the difficulty, EnemySpawnData[0] is the wave the player has reached, both are taken into account to decide if the slime should turn into a giant one
                        EnemyList[i][0] = "BigSlime"
                        EnemyList[i][3] = "Growing"
                        EnemyList[i][4] = 24
                    else:  # The slime picks a random move, even if it does not benefit it, if enough big slimes have already spawned
                        for TempMove in Moves:
                            try:  # Already explained above why this is used
                                if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] > -1:
                                    EnemyList[i].append(TempMove)
                                    Moved = 1
                            except IndexError:
                                pass
                            if Moved == 1:
                                break
                if Moved == 1:  # Not ELIF - moved can be set to 1 in above if statement and the random move still needs to be checked for potential enemy collisions
                    for i2 in range(0, len(
                            EnemyList)):  # Checks every enemy to see if they are either jumping to, or at, the tile the slime is planning to jump to
                        if not i2 == i and EnemyList[i2][1] == EnemyList[i][1] + TempMove[0] and EnemyList[i2][2] == \
                                EnemyList[i][2] + TempMove[1] and (
                                EnemyList[i2][0] == "BasicSlime" or EnemyList[i2][0] == "LongJumpSlime" or
                                EnemyList[i2][0] == "ShootingSlime" or EnemyList[i2][0] == "BobbySlime") and (
                                EnemyList[i2][3] == "Still" or EnemyList[i2][3] == "WindUp"):
                            EnemyList[i].pop()
                            EnemyList[i][3] = "Still"
                            EnemyList[i].pop()
                            break
                        elif (EnemyList[i2][0] == "BasicSlime" or EnemyList[i2][0] == "LongJumpSlime" or EnemyList[i2][
                            0] == "ShootingSlime" or EnemyList[i2][0] == "BobbySlime") and EnemyList[i2][
                            3] == "Jumping" and not i2 == i and EnemyList[i2][1] + EnemyList[i2][5][0] == EnemyList[i][
                            1] + TempMove[0] and EnemyList[i2][2] + EnemyList[i2][5][1] == EnemyList[i][2] + TempMove[
                            1]:
                            EnemyList[i].pop()
                            EnemyList[i][3] = "Still"
                            EnemyList[i].pop()
                            break
                    if Settings[0] == 1 and EnemyList[i][3] == "Jumping" and EnemyList[i][2] * 24 - CamPos[1] < GameRes[
                        1] // 2 and EnemyList[i][1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - \
                            CamPos[1] > GameRes[1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[
                        0] // 2 * -1 - 24:
                        SlimeJump.play()  # If the enemy is on the screen, the sound effect for the enemy jumping is played
                elif not EnemyList[i][
                             0] == "BigSlime":  # If the slime has not moved or turned into a big slime, its state is set back to Still for another WindUp
                    EnemyList[i][3] = "Still"
                    EnemyList[i].pop()
            else:
                EnemyList[i][4] += 1  # If the enemy is winding up to a jump, the timer until it jumps is decreased
                for i2 in range(0, len(EnemyList)):
                    if EnemyList[i2][0] == "Arrow" or EnemyList[i2][
                        0] == "FriendProjectile":  # Collisions with arrows are checked to see if the slime should be killed
                        if EnemyList[i2][1] // 24 == EnemyList[i][1] and EnemyList[i2][2] // 24 == EnemyList[i][2]:
                            if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                                1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                                1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                                EnemyHit.play()
                            if EnemyList[i2][
                                0] == "Arrow":  # Projectiles from turrets should not create the associated tile for that slime
                                Grid[EnemyList[i][2]][EnemyList[i][1]] = "W"
                            NavGrid[EnemyList[i][2]][EnemyList[i][1]] = "-1"
                            ToKill.append(i)
                            ToKill.append(i2)
                            UpdateNeeded = 1
        elif EnemyList[i][
            0] == "LongJumpSlime":  # Very similar to basic slime, look above for comments on code that is not commented here
            if EnemyList[i][3] == "Still":
                EnemyList[i][3] = "WindUp"
                EnemyList[i].append(0)
            elif EnemyList[i][3] == "Jumping":
                if EnemyList[i][4] == 24:
                    EnemyList[i][3] = "Still"
                    EnemyList[i][1] += EnemyList[i][5][0]
                    EnemyList[i][2] += EnemyList[i][5][1]
                    EnemyList[i].pop()
                    EnemyList[i].pop()
                    if CharPos[0] // 24 == EnemyList[i][1] and CharPos[1] // 24 == EnemyList[i][2]:
                        GameOver[0] = 1
                        GameOver[1] = "LongJumpSlime"
                        GameOver[2] = "Hero"
                    elif Grid[EnemyList[i][2]][EnemyList[i][1]] == "C":
                        GameOver[0] = 1
                        GameOver[1] = "LongJumpSlime"
                        GameOver[2] = "Chest"
                    elif Grid[EnemyList[i][2]][EnemyList[i][1]] == "T":
                        if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                            1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                            1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                            EnemyHit.play()
                        Grid[EnemyList[i][2]][EnemyList[i][
                            1]] = "E"  # Trap is not replaced to avoid ability to infinitely kill long-jumping enemies by abusing their AI. Intentional mechanic, not an oversight :P
                        ToKill.append(i)
                else:
                    EnemyList[i][4] += 1
            elif EnemyList[i][3] == "WindUp" and EnemyList[i][4] == 48:
                EnemyList[i].pop()
                EnemyList[i][3] = "Jumping"
                EnemyList[i].append(1)
                Moves = [(2, 0), (-2, 0), (0, -2), (0, 2)]  # Allows the slime to jump 2 blocks as well as 1
                random.shuffle(Moves)
                Moves2 = [(1, 0), (-1, 0), (0, -1),
                          (0, 1)]  # Makes slime able to also jump 1 block, but with lower priority
                random.shuffle(Moves2)
                Moves = Moves + Moves2
                Moved = 0
                for TempMove in Moves:
                    try:
                        if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] > \
                                NavGrid[EnemyList[i][2]][
                                    EnemyList[i][
                                        1]]:  # Will not always pick the best possible option, as NavGrid is not specific for the double jump slime and it does not check how much better each tile is to its current, but adds more consistency in movement as it will aways follow similar paths to the basic slimes, just sometimes skipping sections
                            EnemyList[i].append(TempMove)
                            Moved = 1
                    except IndexError:
                        pass
                    if Moved == 1:
                        break
                if Moved == 0:
                    for TempMove in Moves:
                        try:
                            if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] > -1:
                                EnemyList[i].append(TempMove)
                                Moved = 1
                        except IndexError:
                            pass
                        if Moved == 1:
                            break
                if Moved == 1:
                    for i2 in range(0, len(EnemyList)):
                        if not i2 == i and EnemyList[i2][1] == EnemyList[i][1] + TempMove[0] and EnemyList[i2][2] == \
                                EnemyList[i][2] + TempMove[1] and (
                                EnemyList[i2][0] == "BasicSlime" or EnemyList[i2][0] == "LongJumpSlime" or
                                EnemyList[i2][0] == "ShootingSlime" or EnemyList[i2][0] == "BobbySlime") and (
                                EnemyList[i2][3] == "Still" or EnemyList[i2][3] == "WindUp"):
                            EnemyList[i].pop()
                            EnemyList[i][3] = "Still"
                            EnemyList[i].pop()
                        elif (EnemyList[i2][0] == "BasicSlime" or EnemyList[i2][0] == "LongJumpSlime" or EnemyList[i2][
                            0] == "ShootingSlime" or EnemyList[i2][0] == "BobbySlime") and EnemyList[i2][
                            3] == "Jumping" and not i2 == i:
                            if EnemyList[i2][1] + EnemyList[i2][5][0] == EnemyList[i][1] + TempMove[0] and \
                                    EnemyList[i2][
                                        2] + EnemyList[i2][5][1] == EnemyList[i][2] + TempMove[1]:
                                EnemyList[i].pop()
                                EnemyList[i][3] = "Still"
                                EnemyList[i].pop()
                    if Settings[0] == 1 and EnemyList[i][3] == "Jumping" and EnemyList[i][2] * 24 - CamPos[1] < GameRes[
                        1] // 2 and EnemyList[i][1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - \
                            CamPos[1] > GameRes[1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[
                        0] // 2 * -1 - 24:
                        SlimeJump.play()
                else:
                    EnemyList[i][3] = "Still"
                    EnemyList[i].pop()
            else:
                EnemyList[i][4] += 1
                for i2 in range(0, len(EnemyList)):
                    if EnemyList[i2][0] == "Arrow" or EnemyList[i2][0] == "FriendProjectile":
                        if EnemyList[i2][1] // 24 == EnemyList[i][1] and EnemyList[i2][2] // 24 == EnemyList[i][2]:
                            if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                                1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                                1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                                EnemyHit.play()
                            if EnemyList[i2][
                                0] == "Arrow":  # Projectiles from turrets should not create the associated tile for that slime
                                Grid[EnemyList[i][2]][EnemyList[i][1]] = "T"
                            NavGrid[EnemyList[i][2]][EnemyList[i][1]] = "-1"
                            ToKill.append(i)
                            ToKill.append(i2)
                            UpdateNeeded = 1
        elif EnemyList[i][
            0] == "ShootingSlime":  # Very similar to basic slime, look above for comments on code that is not commented here
            if EnemyList[i][3] == "Still":
                EnemyList[i][3] = "WindUp"
                EnemyList[i].append(0)
            elif EnemyList[i][3] == "Jumping":
                if EnemyList[i][4] == 24:
                    EnemyList[i][3] = "Still"
                    EnemyList[i][1] += EnemyList[i][5][0]
                    EnemyList[i][2] += EnemyList[i][5][1]
                    EnemyList[i].pop()
                    EnemyList[i].pop()
                    if CharPos[0] // 24 == EnemyList[i][1] and CharPos[1] // 24 == EnemyList[i][2]:
                        GameOver[0] = 1
                        GameOver[1] = "ShootingSlime"
                        GameOver[2] = "Hero"
                    elif Grid[EnemyList[i][2]][EnemyList[i][1]] == "C":
                        GameOver[0] = 1
                        GameOver[1] = "ShootingSlime"
                        GameOver[2] = "Chest"
                    elif Grid[EnemyList[i][2]][EnemyList[i][1]] == "T":
                        if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                            1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                            1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                            EnemyHit.play()
                        Grid[EnemyList[i][2]][EnemyList[i][1]] = "E"
                        ToKill.append(i)
                    else:  # Will only shoot if it is not game over and the slime has not jumped into a trap
                        if (EnemyList[i][1] + EnemyList[i][2]) // 4 == (EnemyList[i][1] + EnemyList[i][
                            2]) / 4:  # Will mean that projectiles are shot in a semi-random but predictable direction and it will change each time the slime moves
                            EnemyList.append(["EnemyProjectile", EnemyList[i][1] * 24, EnemyList[i][2] * 24, [4, 0]])
                        elif (EnemyList[i][1] + EnemyList[i][2] + 1) // 4 == (
                                EnemyList[i][1] + EnemyList[i][2] + 1) / 4:
                            EnemyList.append(["EnemyProjectile", EnemyList[i][1] * 24, EnemyList[i][2] * 24, [0, 4]])
                        elif (EnemyList[i][1] + EnemyList[i][2] + 2) // 4 == (
                                EnemyList[i][1] + EnemyList[i][2] + 2) / 4:
                            EnemyList.append(["EnemyProjectile", EnemyList[i][1] * 24, EnemyList[i][2] * 24, [-4, 0]])
                        else:
                            EnemyList.append(["EnemyProjectile", EnemyList[i][1] * 24, EnemyList[i][2] * 24, [0, -4]])
                        if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                            1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                            1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                            ArrowShoot.play()
                else:
                    EnemyList[i][4] += 1
            elif EnemyList[i][3] == "WindUp" and EnemyList[i][4] == 48:
                EnemyList[i].pop()
                EnemyList[i][3] = "Jumping"
                EnemyList[i].append(1)
                Moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
                random.shuffle(Moves)
                Moved = 0
                for TempMove in Moves:
                    try:
                        if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] > \
                                NavGrid[EnemyList[i][2]][
                                    EnemyList[i][1]]:
                            EnemyList[i].append(TempMove)
                            Moved = 1
                    except IndexError:
                        pass
                    if Moved == 1:
                        break
                if Moved == 0:
                    for TempMove in Moves:
                        try:
                            if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] > -1:
                                EnemyList[i].append(TempMove)
                                Moved = 1
                        except IndexError:
                            pass
                        if Moved == 1:
                            break
                if Moved == 1:
                    for i2 in range(0, len(EnemyList)):
                        if not i2 == i and EnemyList[i2][1] == EnemyList[i][1] + TempMove[0] and EnemyList[i2][2] == \
                                EnemyList[i][2] + TempMove[1] and (
                                EnemyList[i2][0] == "BasicSlime" or EnemyList[i2][0] == "LongJumpSlime" or
                                EnemyList[i2][0] == "ShootingSlime") and (
                                EnemyList[i2][3] == "Still" or EnemyList[i2][3] == "WindUp"):
                            EnemyList[i].pop()
                            EnemyList[i][3] = "Still"
                            EnemyList[i].pop()
                        elif (EnemyList[i2][0] == "BasicSlime" or EnemyList[i2][0] == "LongJumpSlime" or EnemyList[i2][
                            0] == "ShootingSlime" or EnemyList[i2][0] == "BobbySlime") and EnemyList[i2][
                            3] == "Jumping" and not i2 == i:
                            if EnemyList[i2][1] + EnemyList[i2][5][0] == EnemyList[i][1] + TempMove[0] and \
                                    EnemyList[i2][
                                        2] + EnemyList[i2][5][1] == EnemyList[i][2] + TempMove[1]:
                                EnemyList[i].pop()
                                EnemyList[i][3] = "Still"
                                EnemyList[i].pop()
                    if Settings[0] == 1 and EnemyList[i][3] == "Jumping" and EnemyList[i][2] * 24 - CamPos[1] < GameRes[
                        1] // 2 and EnemyList[i][1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - \
                            CamPos[1] > GameRes[1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[
                        0] // 2 * -1 - 24:
                        SlimeJump.play()
                else:
                    EnemyList[i][3] = "Still"
                    EnemyList[i].pop()
            else:
                EnemyList[i][4] += 1
                for i2 in range(0, len(EnemyList)):
                    if EnemyList[i2][0] == "Arrow" or EnemyList[i2][0] == "FriendProjectile":
                        if EnemyList[i2][1] // 24 == EnemyList[i][1] and EnemyList[i2][2] // 24 == EnemyList[i][2]:
                            if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                                1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                                1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                                EnemyHit.play()
                            if EnemyList[i2][
                                0] == "Arrow":  # Projectiles from turrets should not create the associated tile for that slime
                                Grid[EnemyList[i][2]][EnemyList[i][1]] = "P"
                            NavGrid[EnemyList[i][2]][EnemyList[i][1]] = "-1"
                            ToKill.append(i)
                            ToKill.append(i2)
                            UpdateNeeded = 1
        elif EnemyList[i][
            0] == "BigSlime":  # Similar to other slimes, look above for comments on code that is not commented here
            if EnemyList[i][3][
               :-1] == "Still":  # [:-1] is used to get all the characters excluding the final one and [-1] is used to get the final character as for the big slime, the state is saved as <State><Health>. For example: "Jumping2" meaning the slime is jumping and its health is 2
                EnemyList[i][3] = "WindUp" + EnemyList[i][3][-1]
                EnemyList[i].append(0)
            elif EnemyList[i][3] == "Growing":
                if EnemyList[i][
                    4] == 48:  # If the slime has finished growing, the slime's state is set to still with 2 health and the area around the slime is cleared if walls or traps are present
                    EnemyList[i][3] = "Still2"
                    EnemyList[i].pop()
                    if Grid[EnemyList[i][2]][EnemyList[i][1]] == "W" or Grid[EnemyList[i][2] + 1][
                        EnemyList[i][1]] == "W" or Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] == "W" or \
                            Grid[EnemyList[i][2]][EnemyList[i][1] + 1] == "W" or Grid[EnemyList[i][2]][
                        EnemyList[i][1]] == "R" or Grid[EnemyList[i][2] + 1][EnemyList[i][1]] == "R" or \
                            Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] == "R" or Grid[EnemyList[i][2]][
                        EnemyList[i][1] + 1] == "R" or Grid[EnemyList[i][2]][EnemyList[i][1]] == "T" or \
                            Grid[EnemyList[i][2] + 1][EnemyList[i][1]] == "T" or Grid[EnemyList[i][2] + 1][
                        EnemyList[i][1] + 1] == "T" or Grid[EnemyList[i][2]][EnemyList[i][1] + 1] == "T" or \
                            Grid[EnemyList[i][2]][EnemyList[i][1]] == "P" or Grid[EnemyList[i][2] + 1][
                        EnemyList[i][1]] == "P" or Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] == "P" or \
                            Grid[EnemyList[i][2]][EnemyList[i][1] + 1] == "P":
                        Grid[EnemyList[i][2]][EnemyList[i][1]] = "E"
                        Grid[EnemyList[i][2] + 1][EnemyList[i][1]] = "E"
                        Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] = "E"
                        Grid[EnemyList[i][2]][EnemyList[i][1] + 1] = "E"
                        UpdateNeeded = 1
                else:
                    EnemyList[i][4] += 1
            elif EnemyList[i][3][:-1] == "Jumping":
                if EnemyList[i][4] == 24:
                    EnemyList[i][3] = "Still" + EnemyList[i][3][-1]
                    EnemyList[i][1] += EnemyList[i][5][0]
                    EnemyList[i][2] += EnemyList[i][5][1]
                    EnemyList[i].pop()
                    EnemyList[i].pop()
                    if (CharPos[0] // 24 == EnemyList[i][1] and CharPos[1] // 24 == EnemyList[i][2]) or (
                            CharPos[0] // 24 == EnemyList[i][1] + 1 and CharPos[1] // 24 == EnemyList[i][2]) or (
                            CharPos[0] // 24 == EnemyList[i][1] + 1 and CharPos[1] // 24 == EnemyList[i][2] + 1) or (
                            CharPos[0] // 24 == EnemyList[i][1] and CharPos[1] // 24 == EnemyList[i][2] + 1):
                        GameOver[0] = 1
                        GameOver[1] = "BigSlime"
                        GameOver[2] = "Hero"
                    elif Grid[EnemyList[i][2]][EnemyList[i][1]] == "C" or Grid[EnemyList[i][2] + 1][
                        EnemyList[i][1]] == "C" or Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] == "C" or \
                            Grid[EnemyList[i][2]][EnemyList[i][1] + 1] == "C":
                        GameOver[0] = 1
                        GameOver[1] = "BigSlime"
                        GameOver[2] = "Chest"
                    elif Grid[EnemyList[i][2]][EnemyList[i][1]] == "W" or Grid[EnemyList[i][2] + 1][
                        EnemyList[i][1]] == "W" or Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] == "W" or \
                            Grid[EnemyList[i][2]][EnemyList[i][1] + 1] == "W" or Grid[EnemyList[i][2]][
                        EnemyList[i][1]] == "R" or Grid[EnemyList[i][2] + 1][EnemyList[i][1]] == "R" or \
                            Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] == "R" or Grid[EnemyList[i][2]][
                        EnemyList[i][1] + 1] == "R" or Grid[EnemyList[i][2]][EnemyList[i][1]] == "T" or \
                            Grid[EnemyList[i][2] + 1][EnemyList[i][1]] == "T" or Grid[EnemyList[i][2] + 1][
                        EnemyList[i][1] + 1] == "T" or Grid[EnemyList[i][2]][EnemyList[i][1] + 1] == "T" or \
                            Grid[EnemyList[i][2]][EnemyList[i][1]] == "P" or Grid[EnemyList[i][2] + 1][
                        EnemyList[i][1]] == "P" or Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] == "P" or \
                            Grid[EnemyList[i][2]][EnemyList[i][1] + 1] == "P":
                        Grid[EnemyList[i][2]][EnemyList[i][
                            1]] = "E"  # Big slime destroys traps or walls where it lands after jumping if they are present
                        Grid[EnemyList[i][2] + 1][EnemyList[i][1]] = "E"
                        Grid[EnemyList[i][2] + 1][EnemyList[i][1] + 1] = "E"
                        Grid[EnemyList[i][2]][EnemyList[i][1] + 1] = "E"
                        UpdateNeeded = 1
                else:
                    EnemyList[i][4] += 1
            elif EnemyList[i][3][:-1] == "WindUp" and EnemyList[i][
                4] == 48:  # The big slime always jumps towards the chest making it important that the player stays nearby to defend it at all times
                EnemyList[i].pop()
                EnemyList[i][3] = "Jumping" + EnemyList[i][3][-1]
                EnemyList[i].append(1)
                EnemyList[i].append([int(
                    round((len(Grid[0]) // 2 - EnemyList[i][1]) / abs(len(Grid[0]) // 2 - EnemyList[i][1] + 0.01))),
                    int(round((len(Grid) // 2 - EnemyList[i][2]) / abs(len(Grid) // 2 - EnemyList[i][
                        2] + 0.01)))])  # Add 0.01 to avoid ever dividing by 0
                if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][1] * 24 - \
                        CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] + 24 > GameRes[
                    1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] + 24 > GameRes[0] // 2 * -1 - 24:
                    SlimeJump.play()
            else:
                EnemyList[i][4] += 1
                for i2 in range(0, len(EnemyList)):
                    if EnemyList[i2][0] == "Arrow" or EnemyList[i2][0] == "FriendProjectile":
                        if (EnemyList[i2][1] // 24 == EnemyList[i][1] and EnemyList[i2][2] // 24 == EnemyList[i][
                            2]) or (EnemyList[i2][1] // 24 == EnemyList[i][1] + 1 and EnemyList[i2][2] // 24 ==
                                    EnemyList[i][2]) or (
                                EnemyList[i2][1] // 24 == EnemyList[i][1] + 1 and EnemyList[i2][2] // 24 ==
                                EnemyList[i][2] + 1) or (
                                EnemyList[i2][1] // 24 == EnemyList[i][1] and EnemyList[i2][2] // 24 == EnemyList[i][
                            2] + 1):
                            if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                                1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] + 24 > \
                                    GameRes[1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] + 24 > GameRes[
                                0] // 2 * -1 - 24:
                                EnemyHit.play()
                            if int(EnemyList[i][3][-1]) < 2:  # If the Big Slime has 1 health, the arrow kill it
                                ToKill.append(i)
                                ToKill.append(i2)
                            else:
                                EnemyList[i][3] = EnemyList[i][3][:-1] + str(
                                    (int(EnemyList[i][3][-1]) - 1))  # Otherwise, the Big Slime's health is reduced by 1
                                ToKill.append(i2)
        elif EnemyList[i][0] == "BobbySlime":  # Code for if the enemy is a basic green slime
            if EnemyList[i][3] == "Still":  # If the slime is still, the countdown to jumping starts
                EnemyList[i][3] = "WindUp"
                EnemyList[i].append(0)
            elif EnemyList[i][3] == "Jumping":
                if EnemyList[i][4] == 24:  # If the slime has finished jumping, the slime's position is moved
                    EnemyList[i][3] = "Still"
                    EnemyList[i][1] += EnemyList[i][5][0]
                    EnemyList[i][2] += EnemyList[i][5][1]
                    EnemyList[i].pop()
                    EnemyList[i].pop()
                    if CharPos[0] // 24 == EnemyList[i][1] and CharPos[1] // 24 == EnemyList[i][
                        2]:  # Checks for if the slime has jumped on the player or the chest and it is game over
                        GameOver[0] = 1
                        GameOver[1] = "BasicSlime"
                        GameOver[2] = "Hero"
                    elif Grid[EnemyList[i][2]][EnemyList[i][1]] == "C":
                        GameOver[0] = 1
                        GameOver[1] = "BasicSlime"
                        GameOver[2] = "Chest"
                    elif Grid[EnemyList[i][2]][
                        EnemyList[i][1]] == "T":  # Checks if the slime has jumped on a trap and should be killed
                        if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                            1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                            1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[
                            0] // 2 * -1 - 24:  # Check for if the slime is on screen (otherwise the sound should not be played)
                            EnemyHit.play()  # Plays the sound effect for the enemy being hit
                        Grid[EnemyList[i][2]][EnemyList[i][
                            1]] = "E"  # Being trapped doesn't spawn a wall - intentional mechanic rather than oversight :P Traps not making the enemy spawn their associated tile on death increases gameplay tactics and opportunities
                        ToKill.append(i)
                else:
                    EnemyList[i][4] += 2  # If the slime is still jumping, the amount they have jumped is increased
            elif EnemyList[i][3] == "WindUp" and EnemyList[i][
                4] == 24:  # If the slime is ready to jump, the tile to which they should is decided
                EnemyList[i].pop()
                EnemyList[i][3] = "Jumping"
                EnemyList[i].append(0)
                Moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
                random.shuffle(Moves)  # Randomises order in which moves will be checked resulting in random movement
                Moved = 0
                for TempMove in Moves:
                    try:  # Try... except; because the code definitely works and the only errors are from checking tiles on the grid that do not exist (past the boundaries). Try except removes these errors from crashing the program and is easier to implement than a check for if the tile being looked at is outside the Grid
                        if NavGrid[EnemyList[i][2]][EnemyList[i][1]] < 90 + random.randint(-3, 3):
                            if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] > \
                                    NavGrid[EnemyList[i][2]][
                                        EnemyList[i][
                                            1]]:  # If the value of the tile for how close it is to the chest or the player is higher than the slimes current tile it is on, the slime picks that option
                                EnemyList[i].append(TempMove)
                                Moved = 1
                        elif NavGrid[EnemyList[i][2]][EnemyList[i][1]] > 95 + random.randint(-3, 3):
                            if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] < \
                                    NavGrid[EnemyList[i][2]][
                                        EnemyList[i][1]] and not NavGrid[EnemyList[i][2] + TempMove[1]][
                                                                     EnemyList[i][1] + TempMove[
                                                                         0]] == -1:  # If the value of the tile for how close it is to the chest or the player is higher than the slimes current tile it is on, the slime picks that option
                                EnemyList[i].append(TempMove)
                                Moved = 1
                    except IndexError:
                        pass
                    if Moved == 1:  # No other options are checked if one move found is good
                        break
                if Moved == 0:  # If the slime does not pick a move, it is likely blocked off from the player and objective and so becomes a big slime to be able to destroy the blocking walls if the amount spawned already is not too high or moves randomly if not
                    for TempMove in Moves:
                        try:  # Already explained above why this is used
                            if NavGrid[EnemyList[i][2] + TempMove[1]][EnemyList[i][1] + TempMove[0]] > -1:
                                EnemyList[i].append(TempMove)
                                Moved = 1
                        except IndexError:
                            pass
                        if Moved == 1:
                            break
                if Moved == 1:  # Not ELIF - moved can be set to 1 in above if statement and the random move still needs to be checked for potential enemy collisions
                    for i2 in range(0, len(
                            EnemyList)):  # Checks every enemy to see if they are either jumping to, or at, the tile the slime is planning to jump to
                        if not i2 == i and EnemyList[i2][1] == EnemyList[i][1] + TempMove[0] and EnemyList[i2][2] == \
                                EnemyList[i][2] + TempMove[1] and (
                                EnemyList[i2][0] == "BasicSlime" or EnemyList[i2][0] == "LongJumpSlime" or
                                EnemyList[i2][0] == "ShootingSlime" or EnemyList[i2][0] == "BobbySlime") and (
                                EnemyList[i2][3] == "Still" or EnemyList[i2][3] == "WindUp"):
                            EnemyList[i].pop()
                            EnemyList[i][3] = "Still"
                            EnemyList[i].pop()
                            break
                        elif (EnemyList[i2][0] == "BasicSlime" or EnemyList[i2][0] == "LongJumpSlime" or EnemyList[i2][
                            0] == "ShootingSlime" or EnemyList[i2][0] == "BobbySlime") and EnemyList[i2][
                            3] == "Jumping" and not i2 == i and EnemyList[i2][1] + EnemyList[i2][5][0] == EnemyList[i][
                            1] + TempMove[0] and EnemyList[i2][2] + EnemyList[i2][5][1] == EnemyList[i][2] + TempMove[
                            1]:
                            EnemyList[i].pop()
                            EnemyList[i][3] = "Still"
                            EnemyList[i].pop()
                            break
                    if Settings[0] == 1 and EnemyList[i][3] == "Jumping" and EnemyList[i][2] * 24 - CamPos[1] < GameRes[
                        1] // 2 and EnemyList[i][1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - \
                            CamPos[1] > GameRes[1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[
                        0] // 2 * -1 - 24:
                        SlimeJump.play()  # If the enemy is on the screen, the sound effect for the enemy jumping is played
                elif not EnemyList[i][
                             0] == "BigSlime":  # If the slime has not moved or turned into a big slime, its state is set back to Still for another WindUp
                    EnemyList[i][3] = "Still"
                    EnemyList[i].pop()
            else:
                EnemyList[i][4] += 1  # If the enemy is winding up to a jump, the timer until it jumps is decreased
                for i2 in range(0, len(EnemyList)):
                    if EnemyList[i2][0] == "Arrow" or EnemyList[i2][
                        0] == "FriendProjectile":  # Collisions with arrows are checked to see if the slime should be killed
                        if EnemyList[i2][1] // 24 == EnemyList[i][1] and EnemyList[i2][2] // 24 == EnemyList[i][2]:
                            if Settings[0] == 1 and EnemyList[i][2] * 24 - CamPos[1] < GameRes[1] // 2 and EnemyList[i][
                                1] * 24 - CamPos[0] < GameRes[0] // 2 and EnemyList[i][2] * 24 - CamPos[1] > GameRes[
                                1] // 2 * -1 - 24 and EnemyList[i][1] * 24 - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                                EnemyHit.play()
                            if EnemyList[i2][
                                0] == "Arrow":  # Projectiles from turrets should not create the associated tile for that slime
                                ToKill.append(i)
                                ToKill.append(i2)
                                UpdateNeeded = 1
        elif EnemyList[i][0] == "Arrow" or EnemyList[i][
            0] == "FriendProjectile":  # If the enemy is an arrow, its position is moved by its speed stored in EnemyList[i][3]. If it moves into a wall, it is removed
            try:  # Already explained above why this is used
                if not (Grid[(EnemyList[i][2] + EnemyList[i][3][1]) // 24][
                            (EnemyList[i][1] + EnemyList[i][3][0]) // 24] == "W" or
                        Grid[(EnemyList[i][2] + EnemyList[i][3][1]) // 24][
                            (EnemyList[i][1] + EnemyList[i][3][0]) // 24] == "S" or
                        Grid[(EnemyList[i][2] + EnemyList[i][3][1]) // 24][
                            (EnemyList[i][1] + EnemyList[i][3][0]) // 24] == "R" or
                        Grid[(EnemyList[i][2] + EnemyList[i][3][1]) // 24][
                            (EnemyList[i][1] + EnemyList[i][3][0]) // 24] == "P"):
                    EnemyList[i][1] += EnemyList[i][3][0]
                    EnemyList[i][2] += EnemyList[i][3][1]
                else:
                    ToKill.append(i)
            except IndexError:
                pass
        elif EnemyList[i][0] == "EnemyProjectile":  # Similar to code for arrows
            try:
                if not (Grid[(EnemyList[i][2] + EnemyList[i][3][1]) // 24][
                            (EnemyList[i][1] + EnemyList[i][3][0]) // 24] == "W" or
                        Grid[(EnemyList[i][2] + EnemyList[i][3][1]) // 24][
                            (EnemyList[i][1] + EnemyList[i][3][0]) // 24] == "S" or
                        Grid[(EnemyList[i][2] + EnemyList[i][3][1]) // 24][
                            (EnemyList[i][1] + EnemyList[i][3][0]) // 24] == "R" or
                        Grid[(EnemyList[i][2] + EnemyList[i][3][1]) // 24][
                            (EnemyList[i][1] + EnemyList[i][3][0]) // 24] == "P"):
                    EnemyList[i][1] += EnemyList[i][3][0]
                    EnemyList[i][2] += EnemyList[i][3][1]
                    if EnemyList[i][1] // 24 == CharPos[0] // 24 and EnemyList[i][2] // 24 == CharPos[1] // 24:
                        GameOver[0] = 1
                        GameOver[1] = "ShootingSlime"
                        GameOver[2] = "Hero"
                else:
                    ToKill.append(i)
            except IndexError:
                pass
        else:
            pass
    if len(ToKill) > 0:
        ToKill.sort(
            reverse=True)  # List of enemies to be removed is sorted backwards to make it so one enemy being removed will not affect the position of others
        LastEnemy = -1  # LastEnemy variable is initially set to a value that no enemy can possibly be numbered at but is used so enemies killed by multiple things are not removed twice, resulting in another, wrong enemy being removed as well
        for Enemy in ToKill:
            if not Enemy == LastEnemy:
                if EnemyList[Enemy][0] == "BasicSlime":
                    Score += 10
                elif EnemyList[Enemy][0] == "LongJumpSlime" or EnemyList[Enemy][0] == "ShootingSlime":
                    Score += 20
                elif EnemyList[Enemy][0] == "BigSlime":
                    Score += 30
                elif EnemyList[Enemy][0] == "BobbySlime":
                    Score += 100
                EnemyList.pop(Enemy)
                LastEnemy = Enemy
    return (EnemyList, GameOver, BowInfo, UpdateNeeded, Grid, EnemySpawnData, NavGrid,
            Score)  # Returns the varibles that could have been modified and need to be saved


def Display(Grid, EnemyList, CharPos, CamPos, Movement, BowInfo,
            GameTicks):  # Function to display everything on the screen during the game
    Window.blit(Background, (0,
                             0))  # Clears the screen so everything can be displayed on top properly and there are no visual bugs when looking past the edge of the map
    ChestOnScreen = 0
    for y in range(0, len(Grid)):  # Displays all the tiles in view of the player
        for x in range(0, len(Grid[y])):
            if GameRes[1] // 2 > y * 24 - CamPos[1] > GameRes[1] // 2 * -1 - 24 and GameRes[0] // 2 > x * 24 - CamPos[
                0] > GameRes[0] // 2 * -1 - 24:
                if Grid[y][x] == "W":
                    Window.blit(Wall, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                       (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                elif Grid[y][x] == "M":
                    Window.blit(MetalWall, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                            (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                elif Grid[y][x] == "R":
                    Window.blit(Rock, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                       (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                elif Grid[y][x] == "T":
                    Window.blit(Trap, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                       (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                elif Grid[y][x] == "P":
                    Window.blit(Turret, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                         (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                elif Grid[y][x] == "C":
                    Window.blit(Chest, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                        (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                    ChestOnScreen = 1
                elif Grid[y][x] == "O":
                    Window.blit(OpenChest, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                            (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                elif Grid[y][x] == "S":
                    Window.blit(SpawnerTile, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                              (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                else:
                    Window.blit(Tile, ((x * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                       (y * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
    for Enemy in EnemyList:  # Displays shadows of jumping enemies and arrows
        if Enemy[0] == "BasicSlime" or Enemy[0] == "LongJumpSlime" or Enemy[0] == "ShootingSlime" or Enemy[
            0] == "BobbySlime":
            if Enemy[3] == "Jumping":
                if Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + 12 - (abs(Enemy[4] - 12)) < GameRes[
                    1] // 2 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + 12 - (abs(Enemy[4] - 12)) < \
                        GameRes[0] // 2 and Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + 12 - (
                        abs(Enemy[4] - 12)) > GameRes[1] // 2 * -1 - 24 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - \
                        CamPos[
                            0] + 12 - (abs(Enemy[4] - 12)) > GameRes[0] // 2 * -1 - 24:
                    Window.blit(pygame.transform.scale(Shadow, (ScreenRes[0] // GameRes[0] * abs(Enemy[4] - 12) * 2,
                                                                ScreenRes[1] // GameRes[1] * abs(Enemy[4] - 12) * 2)), (
                                    (Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + (GameRes[0] // 2) + 12 - (
                                        abs(Enemy[4] - 12))) * (ScreenRes[0] // GameRes[0]), (
                                            Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + (
                                            GameRes[1] // 2) + 12 - (abs(Enemy[4] - 12))) * (
                                            ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "BigSlime":
            if Enemy[3][:-1] == "Jumping":
                if Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] - (abs(Enemy[4] * 2 - 24)) < GameRes[1] // 2 and \
                        Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] - (abs(Enemy[4] * 2 - 24)) < GameRes[
                    0] // 2 and Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + 48 - (
                        abs(Enemy[4] * 2 - 24)) + 24 > GameRes[1] // 2 * -1 - 24 and Enemy[1] * 24 + (
                        Enemy[5][0] * Enemy[4]) - \
                        CamPos[0] + 48 - (abs(Enemy[4] * 2 - 24)) + 24 > GameRes[0] // 2 * -1 - 24:
                    Window.blit(pygame.transform.scale(BigShadow, (ScreenRes[0] // GameRes[0] * abs(Enemy[4] - 12) * 4,
                                                                   ScreenRes[1] // GameRes[1] * abs(
                                                                       Enemy[4] - 12) * 4)), ((Enemy[1] * 24 + (
                            Enemy[5][0] * Enemy[4]) - CamPos[0] + (GameRes[0] // 2) + 24 - (abs(
                        Enemy[4] * 2 - 24))) * (ScreenRes[0] // GameRes[0]), (Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) -
                                                                              CamPos[1] + (GameRes[1] // 2) + 24 - (
                                                                                  abs(Enemy[4] * 2 - 24))) * (ScreenRes[
                                                                                                                  1] //
                                                                                                              GameRes[
                                                                                                                  1])))
        elif Enemy[0] == "Arrow":
            if Enemy[2] - CamPos[1] < GameRes[1] // 2 and Enemy[1] - CamPos[0] < GameRes[0] // 2 and Enemy[2] - CamPos[
                1] > GameRes[1] // 2 * -1 - 24 and Enemy[1] - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                if Enemy[3][
                    0] > 0:  # The list stored at Enemy[3] represents the x and y speed of the arrow and therefore the direction it is travelling in so the program knows whether to flip or rotate it
                    ChangedArrow = Arrow  # ChangedArrow is used instead of just Arrow inside the .flip or .rotate to make the lines less overly long and the program more readable
                elif Enemy[3][0] < 0:
                    ChangedArrow = pygame.transform.flip(Arrow, True, False)
                elif Enemy[3][1] < 0:
                    ChangedArrow = pygame.transform.rotate(Arrow, 90)
                else:
                    ChangedArrow = pygame.transform.rotate(Arrow, -90)
                Window.blit(ChangedArrow, ((Enemy[1] - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                           (Enemy[2] - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "EnemyProjectile":
            if Enemy[2] - CamPos[1] < GameRes[1] // 2 and Enemy[1] - CamPos[0] < GameRes[0] // 2 and Enemy[2] - CamPos[
                1] > GameRes[1] // 2 * -1 - 24 and Enemy[1] - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                Window.blit(ProjectileBlack, ((Enemy[1] - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                              (Enemy[2] - CamPos[1] + (GameRes[1] // 2)) * (
                                                      ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "FriendProjectile":
            if Enemy[2] - CamPos[1] < GameRes[1] // 2 and Enemy[1] - CamPos[0] < GameRes[0] // 2 and Enemy[2] - CamPos[
                1] > GameRes[1] // 2 * -1 - 24 and Enemy[1] - CamPos[0] > GameRes[0] // 2 * -1 - 24:
                Window.blit(ProjectileWhite, ((Enemy[1] - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                              (Enemy[2] - CamPos[1] + (GameRes[1] // 2)) * (
                                                      ScreenRes[1] // GameRes[1])))
    for Enemy in EnemyList:  # Displays all the enemies that are still
        if Enemy[0] == "BasicSlime":
            if Enemy[3] == "Still" or Enemy[3] == "WindUp":
                if \
                        GameRes[1] // 2 > Enemy[2] * 24 - CamPos[1] > GameRes[1] // 2 * -1 - 24 and GameRes[0] // 2 > \
                                Enemy[
                                    1] * 24 - CamPos[0] > GameRes[
                            0] // 2 * -1 - 24:
                    Window.blit(Slime, ((Enemy[1] * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                        (Enemy[2] * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "LongJumpSlime":
            if Enemy[3] == "Still" or Enemy[3] == "WindUp":
                if GameRes[1] // 2 * -1 - 24 < Enemy[2] * 24 - CamPos[1] < GameRes[1] // 2 < \
                        GameRes[0] // 2 and Enemy[1] * 24 - CamPos[0] > GameRes[
                    0] // 2 * -1 - 24:
                    Window.blit(LongJumpSlime, (
                        (Enemy[1] * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                        (Enemy[2] * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "ShootingSlime":
            if Enemy[3] == "Still" or Enemy[3] == "WindUp":
                if \
                        GameRes[1] // 2 > Enemy[2] * 24 - CamPos[1] > GameRes[1] // 2 * -1 - 24 and GameRes[0] // 2 > \
                                Enemy[
                                    1] * 24 - CamPos[0] > GameRes[
                            0] // 2 * -1 - 24:
                    Window.blit(ShootingSlime, (
                        (Enemy[1] * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                        (Enemy[2] * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "BobbySlime":
            if Enemy[3] == "Still" or Enemy[3] == "WindUp":
                if \
                        GameRes[1] // 2 > Enemy[2] * 24 - CamPos[1] > GameRes[1] // 2 * -1 - 24 and GameRes[0] // 2 > \
                                Enemy[
                                    1] * 24 - CamPos[0] > GameRes[
                            0] // 2 * -1 - 24:
                    Window.blit(BobbySlime, (
                        (Enemy[1] * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                        (Enemy[2] * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "BigSlime":
            if Enemy[3][:-1] == "Still" or Enemy[3][:-1] == "WindUp":
                if Enemy[2] * 24 - CamPos[1] < GameRes[1] // 2 and Enemy[1] * 24 - CamPos[0] < GameRes[0] // 2 and \
                        Enemy[2] * 24 - CamPos[1] + 24 > GameRes[1] // 2 * -1 - 24 and Enemy[1] * 24 - CamPos[0] + 24 > \
                        GameRes[0] // 2 * -1 - 24:
                    if Enemy[3][-1] == "2":
                        Window.blit(BigSlime, (
                            (Enemy[1] * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                            (Enemy[2] * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
                    else:
                        Window.blit(BigSlimeDamaged, (
                            (Enemy[1] * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                            (Enemy[2] * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
            elif Enemy[3] == "Growing":
                if Enemy[2] * 24 - CamPos[1] < GameRes[1] // 2 and Enemy[1] * 24 - CamPos[0] < GameRes[0] // 2 and \
                        Enemy[2] * 24 - CamPos[1] + 24 > GameRes[1] // 2 * -1 - 24 and Enemy[1] * 24 - CamPos[0] + 24 > \
                        GameRes[0] // 2 * -1 - 24:
                    Window.blit(pygame.transform.scale(Slime, (
                        ScreenRes[0] // GameRes[0] * Enemy[4], ScreenRes[1] // GameRes[1] * Enemy[4])), (
                                    (Enemy[1] * 24 - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                    (Enemy[2] * 24 - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
    ChangedHero = []  # Displays the character and the bow
    if BowInfo[
        0] == "Right":  # BowFramePicker() is a tiny function that is called to get, without extra lines of code being needed here, which frame of animation the bow is on
        Window.blit(Bow[BowFramePicker(BowInfo)], (
            (CharPos[0] - CamPos[0] + (GameRes[0] // 2) + 18) * (ScreenRes[0] // GameRes[0]),
            (CharPos[1] - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
        for Frame in Hero:
            ChangedHero.append(Frame)
    elif BowInfo[0] == "Left":
        Window.blit(pygame.transform.flip(Bow[BowFramePicker(BowInfo)], True, False), (
            (CharPos[0] - CamPos[0] + (GameRes[0] // 2) - 18) * (ScreenRes[0] // GameRes[0]),
            (CharPos[1] - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
        for Frame in Hero:
            ChangedHero.append(pygame.transform.flip(Frame, True, False))
    elif BowInfo[0] == "Up":
        Window.blit(pygame.transform.rotate(Bow[BowFramePicker(BowInfo)], 90), (
            (CharPos[0] - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
            (CharPos[1] - CamPos[1] + (GameRes[1] // 2) - 24) * (ScreenRes[1] // GameRes[1])))
        for Frame in Hero:
            ChangedHero.append(Frame)
    else:
        Window.blit(pygame.transform.rotate(Bow[BowFramePicker(BowInfo)], -90), (
            (CharPos[0] - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
            (CharPos[1] - CamPos[1] + (GameRes[1] // 2) + 24) * (ScreenRes[1] // GameRes[1])))
        for Frame in Hero:
            ChangedHero.append(Frame)
    if not Movement[0] == 0:
        Window.blit(ChangedHero[abs(Movement[0] // 6) - 1], (
            (CharPos[0] - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
            (CharPos[1] - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
    elif not Movement[1] == 0:
        Window.blit(ChangedHero[abs(Movement[1] // 6) - 1], (
            (CharPos[0] - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
            (CharPos[1] - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
    else:
        Window.blit(ChangedHero[3], ((CharPos[0] - CamPos[0] + (GameRes[0] // 2)) * (ScreenRes[0] // GameRes[0]),
                                     (CharPos[1] - CamPos[1] + (GameRes[1] // 2)) * (ScreenRes[1] // GameRes[1])))
    for Enemy in EnemyList:  # Slimes that are jumping are finally displayed; seperately, to make them always layer on top of stationary enemies or the player
        if Enemy[0] == "BasicSlime":
            if Enemy[3] == "Jumping":
                if Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 < GameRes[
                    1] // 2 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] < GameRes[0] // 2 and Enemy[
                    2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 > GameRes[
                    1] // 2 * -1 - 24 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] > GameRes[
                    0] // 2 * -1 - 24:
                    Window.blit(Slime, ((Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + (GameRes[0] // 2)) * (
                            ScreenRes[0] // GameRes[0]), (Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + (
                            GameRes[1] // 2) + ((Enemy[4] - 12) ** 2) / 5 - 28) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "LongJumpSlime":
            if Enemy[3] == "Jumping":
                if Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 < GameRes[
                    1] // 2 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] < GameRes[0] // 2 and Enemy[
                    2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 > GameRes[
                    1] // 2 * -1 - 24 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] > GameRes[
                    0] // 2 * -1 - 24:
                    Window.blit(LongJumpSlime, (
                        (Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + (GameRes[0] // 2)) * (
                                ScreenRes[0] // GameRes[0]), (
                                Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + (GameRes[1] // 2) + (
                                (Enemy[4] - 12) ** 2) / 5 - 28) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "ShootingSlime":
            if Enemy[3] == "Jumping":
                if Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 < GameRes[
                    1] // 2 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] < GameRes[0] // 2 and Enemy[
                    2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 > GameRes[
                    1] // 2 * -1 - 24 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] > GameRes[
                    0] // 2 * -1 - 24:
                    Window.blit(ShootingSlime, (
                        (Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + (GameRes[0] // 2)) * (
                                ScreenRes[0] // GameRes[0]), (
                                Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + (GameRes[1] // 2) + (
                                (Enemy[4] - 12) ** 2) / 5 - 28) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "BobbySlime":
            if Enemy[3] == "Jumping":
                if Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 < GameRes[
                    1] // 2 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] < GameRes[0] // 2 and Enemy[
                    2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 > GameRes[
                    1] // 2 * -1 - 24 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] > GameRes[
                    0] // 2 * -1 - 24:
                    Window.blit(BobbySlime, (
                        (Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + (GameRes[0] // 2)) * (
                                ScreenRes[0] // GameRes[0]), (
                                Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + (GameRes[1] // 2) + (
                                (Enemy[4] - 12) ** 2) / 5 - 28) * (ScreenRes[1] // GameRes[1])))
        elif Enemy[0] == "BigSlime":
            if Enemy[3][:-1] == "Jumping":
                if Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 28 < GameRes[
                    1] // 2 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] < GameRes[0] // 2 and Enemy[
                    2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + ((Enemy[4] - 12) ** 2) / 5 - 4 > GameRes[
                    1] // 2 * -1 - 24 and Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + 24 > GameRes[
                    0] // 2 * -1 - 24:
                    if Enemy[3][-1] == "2":
                        Window.blit(BigSlime, (
                            (Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + (GameRes[0] // 2)) * (
                                    ScreenRes[0] // GameRes[0]), (
                                    Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + (GameRes[1] // 2) + (
                                    (Enemy[4] - 12) ** 2) / 5 - 28) * (ScreenRes[1] // GameRes[1])))
                    else:
                        Window.blit(BigSlimeDamaged, (
                            (Enemy[1] * 24 + (Enemy[5][0] * Enemy[4]) - CamPos[0] + (GameRes[0] // 2)) * (
                                    ScreenRes[0] // GameRes[0]), (
                                    Enemy[2] * 24 + (Enemy[5][1] * Enemy[4]) - CamPos[1] + (GameRes[1] // 2) + (
                                    (Enemy[4] - 12) ** 2) / 5 - 28) * (ScreenRes[1] // GameRes[1])))
    if ChestOnScreen == 0:  # For displaying the icon showing where the chest is
        for y in range(0, len(Grid)):  # Checks the position of the chest and saves it in the variable "ChestPos"
            for x in range(0, len(Grid[0])):
                if Grid[y][x] == "C":
                    ChestPos = (x * 24, y * 24)
        if math.degrees(math.atan(abs(ChestPos[0] - CamPos[0]) / abs(ChestPos[1] - CamPos[1]))) > math.degrees(
                math.atan(ScreenRes[0] / ScreenRes[
                    1])):  # Checks if the marker needs to point in the vertical or horizontal axis by working out the angle from the camera to the chest
            if ChestPos[0] > CamPos[0]:  # Checks if the chest is to the right or left of the player
                Window.blit(pygame.transform.rotate(ChestMarker, -90), (
                    (GameRes[0] - 24 - abs(int(math.sin(GameTicks / 30) * 8))) * (ScreenRes[0] // GameRes[0]),
                    (min(max((ChestPos[1] - CamPos[1] + GameRes[1] // 2), -1), GameRes[1] - 23)) * (
                            ScreenRes[1] // GameRes[1])))
            else:  # abs(int(math.sin(GameTicks/30)*8)) is used to add a slight bobbing effect making the icon more interesting, GameTicks goes up every frame so sin(GameTicks) will always go up and down
                Window.blit(pygame.transform.rotate(ChestMarker, 90), (
                    abs(int(math.sin(GameTicks / 30) * 8)) * (ScreenRes[0] // GameRes[0]),
                    (min(max((ChestPos[1] - CamPos[1] + GameRes[1] // 2), -1), GameRes[1] - 23)) * (
                            ScreenRes[1] // GameRes[1])))
        else:
            if ChestPos[1] > CamPos[1]:  # Checks if the chest is above or below the player
                Window.blit(pygame.transform.rotate(ChestMarker, 180), (
                    (min(max((ChestPos[0] - CamPos[0] + GameRes[0] // 2), -1), GameRes[0] - 23)) * (
                            ScreenRes[0] // GameRes[0]),
                    (GameRes[1] - 24 - abs(int(math.sin(GameTicks / 30) * 8))) * (ScreenRes[1] // GameRes[1])))
            else:
                Window.blit(pygame.transform.rotate(ChestMarker, 0), (
                    (min(max((ChestPos[0] - CamPos[0] + GameRes[0] // 2), -1), GameRes[0] - 23)) * (
                            ScreenRes[0] // GameRes[0]),
                    abs(int(math.sin(GameTicks / 30) * 8)) * (ScreenRes[1] // GameRes[1])))
    pygame.display.update()  # The screen is finally updated so the new frame with all the images blit-ed can be shown to the player


def Move(Grid, EnemyList, CamPos, CharPos, Movement, UpdateNeeded, BowInfo,
         GameOver):  # Function to manage the movement of the player
    InputKeys = pygame.key.get_pressed()
    if InputKeys[pygame.K_p]:  # Very simple way to pause the game if required
        while InputKeys[pygame.K_p]:
            InputKeys = pygame.key.get_pressed()
            pygame.event.get()
        while not InputKeys[pygame.K_p]:
            InputKeys = pygame.key.get_pressed()
            pygame.event.get()
        while InputKeys[pygame.K_p]:
            InputKeys = pygame.key.get_pressed()
            pygame.event.get()
    if Movement[0] == 0 and Movement[
        1] == 0:  # If the player is not moving, check keyboard inputs and if there are walls in the way of where the player wants to move to see if they should start moving
        try:  ##Already explained above why this is used
            if InputKeys[pygame.K_w] and not (
                    Grid[(CharPos[1] // 24) - 1][CharPos[0] // 24] == "W" or Grid[(CharPos[1] // 24) - 1][
                CharPos[0] // 24] == "S" or Grid[(CharPos[1] // 24) - 1][CharPos[0] // 24] == "M" or
                    Grid[(CharPos[1] // 24) - 1][CharPos[0] // 24] == "R" or Grid[(CharPos[1] // 24) - 1][
                        CharPos[0] // 24] == "P"):
                Movement[1] -= 24
                for i in range(0, len(EnemyList)):
                    if EnemyList[i][1] == CharPos[0] // 24 and EnemyList[i][2] == (CharPos[1] // 24) - 1 and (
                            EnemyList[i][0] == "BasicSlime" or EnemyList[i][0] == "LongJumpSlime" or EnemyList[i][
                        0] == "ShootingSlime" or EnemyList[i][0] == "BobbySlime") and (
                            EnemyList[i][3] == "Still" or EnemyList[i][3] == "WindUp"):
                        Movement[1] = 0
            elif InputKeys[pygame.K_s] and not (
                    Grid[(CharPos[1] // 24) + 1][CharPos[0] // 24] == "W" or Grid[(CharPos[1] // 24) + 1][
                CharPos[0] // 24] == "S" or Grid[(CharPos[1] // 24) + 1][CharPos[0] // 24] == "M" or
                    Grid[(CharPos[1] // 24) + 1][CharPos[0] // 24] == "R" or Grid[(CharPos[1] // 24) + 1][
                        CharPos[0] // 24] == "P"):
                Movement[1] += 24
                for i in range(0, len(EnemyList)):
                    if EnemyList[i][1] == CharPos[0] // 24 and EnemyList[i][2] == (CharPos[1] // 24) + 1 and (
                            EnemyList[i][0] == "BasicSlime" or EnemyList[i][0] == "LongJumpSlime" or EnemyList[i][
                        0] == "ShootingSlime" or EnemyList[i][0] == "BobbySlime") and (
                            EnemyList[i][3] == "Still" or EnemyList[i][3] == "WindUp"):
                        Movement[1] = 0
            elif InputKeys[pygame.K_a] and not (
                    Grid[CharPos[1] // 24][(CharPos[0] // 24) - 1] == "W" or Grid[(CharPos[1] // 24)][
                CharPos[0] // 24 - 1] == "S" or Grid[(CharPos[1] // 24)][CharPos[0] // 24 - 1] == "M" or
                    Grid[(CharPos[1] // 24)][CharPos[0] // 24 - 1] == "R" or Grid[(CharPos[1] // 24)][
                        CharPos[0] // 24 - 1] == "P"):
                Movement[0] -= 24
                for i in range(0, len(EnemyList)):
                    if EnemyList[i][1] == (CharPos[0] // 24) - 1 and EnemyList[i][2] == CharPos[1] // 24 and (
                            EnemyList[i][0] == "BasicSlime" or EnemyList[i][0] == "LongJumpSlime" or EnemyList[i][
                        0] == "ShootingSlime" or EnemyList[i][0] == "BobbySlime") and (
                            EnemyList[i][3] == "Still" or EnemyList[i][3] == "WindUp"):
                        Movement[0] = 0
            elif InputKeys[pygame.K_d] and not (
                    Grid[CharPos[1] // 24][(CharPos[0] // 24) + 1] == "W" or Grid[(CharPos[1] // 24)][
                CharPos[0] // 24 + 1] == "S" or Grid[(CharPos[1] // 24)][CharPos[0] // 24 + 1] == "M" or
                    Grid[(CharPos[1] // 24)][CharPos[0] // 24 + 1] == "R" or Grid[(CharPos[1] // 24)][
                        CharPos[0] // 24 + 1] == "P"):
                Movement[0] += 24
                for i in range(0, len(EnemyList)):
                    if EnemyList[i][1] == (CharPos[0] // 24) + 1 and EnemyList[i][2] == CharPos[1] // 24 and (
                            EnemyList[i][0] == "BasicSlime" or EnemyList[i][0] == "LongJumpSlime" or EnemyList[i][
                        0] == "ShootingSlime" or EnemyList[i][0] == "BobbySlime") and (
                            EnemyList[i][3] == "Still" or EnemyList[i][3] == "WindUp"):
                        Movement[0] = 0
        except IndexError:
            pass
        if Grid[CharPos[1] // 24][CharPos[0] // 24] == "T":  # If the player moves onto a trap, it is game over
            GameOver[0] = 1
            GameOver[
                1] = "Trapped"  # GameOver[1] (and [2]) store how the player died so it can be said on the death screen
    else:  # Could be if not(Movement[0]==0 and Movement[1]==0): to make movement less stop-starty but the game is grid based so IMO it feels better for movement not completely smooth
        UpdateNeeded = 1  # The player has moved so the NavGrid of how close each tile is to either the player or the chest needs to be updated
        if Movement[0] > 0:  # Moves the player and reduced the amount they need to further move by if necessary
            CharPos[0] += 4
            Movement[0] -= 4
        elif Movement[0] < 0:
            CharPos[0] -= 4
            Movement[0] += 4
        if Movement[1] > 0:
            CharPos[1] += 4
            Movement[1] -= 4
        elif Movement[1] < 0:
            CharPos[1] -= 4
            Movement[1] += 4
    MouseX, MouseY = pygame.mouse.get_pos()  # Gets the position of the mouse pointer on the screen
    MouseX = MouseX // (ScreenRes[1] // GameRes[
        1])  # Changes the variable to store the position of the mouse pointer in in the resolution of the game (384 by 216) not 1920 by 1080 or any other screen resolution in use
    MouseY = MouseY // (ScreenRes[1] // GameRes[1])
    CamPos[0] += ((CharPos[0] * 1.5 + (MouseX + CamPos[0] - (GameRes[0] // 2)) * 0.5) / 2 - CamPos[
        0]) / 10 + 1.2  # Moves the camera smoothly to show the player but also move slightly towards the mouse so it is possible to look around by aiming
    CamPos[1] += ((CharPos[1] * 1.5 + (MouseY + CamPos[1] - (GameRes[1] // 2)) * 0.5) / 2 - CamPos[1]) / 10 + 1.2
    if not (InputKeys[pygame.K_UP] or InputKeys[pygame.K_DOWN] or InputKeys[pygame.K_LEFT] or InputKeys[
        pygame.K_RIGHT]):
        if abs(MouseX - (CharPos[0] - CamPos[0] + (GameRes[0] // 2))) > abs(MouseY - (CharPos[1] - CamPos[1] + (
                GameRes[
                    1] // 2))):  # Code to check the direction the player should be facing based of the co-ordinates of the mouse pointer in relation to the player by finding which difference (the x or y one) is greater and if it is negative or positive
            if MouseX > GameRes[0] / 2:
                BowInfo[0] = "Right"
            else:
                BowInfo[0] = "Left"
        else:
            if MouseY < GameRes[1] / 2:
                BowInfo[0] = "Up"
            else:
                BowInfo[0] = "Down"
    else:
        if InputKeys[pygame.K_RIGHT]:
            BowInfo[0] = "Right"
        elif InputKeys[pygame.K_LEFT]:
            BowInfo[0] = "Left"
        elif InputKeys[pygame.K_UP]:
            BowInfo[0] = "Up"
        else:
            BowInfo[0] = "Down"
    InputMouseKeys = pygame.mouse.get_pressed()  # The mouse buttons currently pressed are checked and saved
    if (InputMouseKeys[0] or InputKeys[pygame.K_UP] or InputKeys[pygame.K_DOWN] or InputKeys[pygame.K_LEFT] or
        InputKeys[pygame.K_RIGHT]) and BowInfo[
        1] == 0:  # InputMouseKeys[0] is left click, the button used to shoot an arrow
        BowInfo[1] = 24  # The timer until an arrow is fired is set to 24
    return CamPos, CharPos, Movement, UpdateNeeded, BowInfo, GameOver  # The player's position, the position of the camera, the player's movement, if an update to the NavGrid is needed, information of the direction the player is aiming and the frame of animation for the bow and whether the player has died (by stepping into a trap) are returned


def BowFramePicker(
        BowInfo):  # Tiny function to work out the frame of animation for the bow to avoid extra if-elses with extremely long lines of code in the Display() function
    if 12 > BowInfo[1] > 0:
        return 4  # If the bow has been fired, the frame of animation showing the bow empty is returned
    else:
        return max(0, BowInfo[
            1] - 12) // 4  # Otherwise, the frame of animation is returned for either (if the bow is being fired and therefore BowInfo[1] is greater than 12) the frame of animation for pulling back the arrow or just (if the bow is not being fired and therefore BowInfo[1] is 0) the image of the bow string not being pulled back


def AdjustGlobals(Settings):  # Function to simply adjust all images to be smaller for small mode to work properly
    # Global is used to make the following variables editable and changes them permanently
    if Settings[5] == 1:  # No need to reset to 384 by 216 if small mode is not active as it will already have been done
        global GameRes
        GameRes = [1920, 1080]
    global Tile
    global SpawnerTile
    global Wall
    global Rock
    global MetalWall
    global Trap
    global Turret
    global Chest
    global OpenChest
    global Slime
    global BobbySlime
    global BigSlime
    global BigSlimeDamaged
    global LongJumpSlime
    global ShootingSlime
    global Arrow
    global ProjectileWhite
    global ProjectileBlack
    global Shadow
    global ChestMarker
    global BigShadow
    global Background
    global Hero
    global Bow
    Tile = pygame.transform.scale(pygame.image.load("Images\Tile.png").convert_alpha(), (
        ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))  # Loads all the game's images
    SpawnerTile = pygame.transform.scale(pygame.image.load("Images\SpawnerTile.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Wall = pygame.transform.scale(pygame.image.load("Images\Wall.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Rock = pygame.transform.scale(pygame.image.load("Images\Rock.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    MetalWall = pygame.transform.scale(pygame.image.load("Images\WallMetal.png").convert_alpha(),
                                       (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Trap = pygame.transform.scale(pygame.image.load("Images\Trap.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Turret = pygame.transform.scale(pygame.image.load("Images\SlimeTurret.png").convert_alpha(),
                                    (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Chest = pygame.transform.scale(pygame.image.load("Images\Chest.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    OpenChest = pygame.transform.scale(pygame.image.load("Images\ChestOpen.png").convert_alpha(),
                                       (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Slime = pygame.transform.scale(pygame.image.load("Images\Slime.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    BobbySlime = pygame.transform.scale(pygame.image.load("Images\Bobby.png").convert_alpha(),
                                        (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    BigSlime = pygame.transform.scale(pygame.image.load("Images\BigSlime.png").convert_alpha(),
                                      (ScreenRes[0] // GameRes[0] * 48, ScreenRes[1] // GameRes[1] * 48))
    BigSlimeDamaged = pygame.transform.scale(pygame.image.load("Images\BigSlimeDamaged.png").convert_alpha(),
                                             (ScreenRes[0] // GameRes[0] * 48, ScreenRes[1] // GameRes[1] * 48))
    LongJumpSlime = pygame.transform.scale(pygame.image.load("Images\LongJumpSlime.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    ShootingSlime = pygame.transform.scale(pygame.image.load("Images\ShootingSlime.png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Arrow = pygame.transform.scale(pygame.image.load("Images\ArrowWhite.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    ProjectileWhite = pygame.transform.scale(pygame.image.load("Images\SlimeProjectileWhite.png").convert_alpha(),
                                             (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    ProjectileBlack = pygame.transform.scale(pygame.image.load("Images\SlimeProjectileBlack.png").convert_alpha(),
                                             (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Arrow = pygame.transform.scale(pygame.image.load("Images\ArrowWhite.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    Shadow = pygame.transform.scale(pygame.image.load("Images\Shadow.png").convert_alpha(),
                                    (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    ChestMarker = pygame.transform.scale(pygame.image.load("Images\ChestMarker.png").convert_alpha(),
                                         (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))
    BigShadow = pygame.transform.scale(pygame.image.load("Images\BigShadow.png").convert_alpha(),
                                       (ScreenRes[0] // GameRes[0] * 48, ScreenRes[1] // GameRes[1] * 48))
    Background = pygame.transform.scale(pygame.image.load("Images\Background.png").convert_alpha(), (
        ScreenRes[0] // GameRes[0] * ScreenRes[0], ScreenRes[1] // GameRes[1] * ScreenRes[1]))
    Hero = [pygame.transform.scale(pygame.image.load("Images\Archer1.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
            pygame.transform.scale(pygame.image.load("Images\Archer2.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
            pygame.transform.scale(pygame.image.load("Images\Archer1.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
            pygame.transform.scale(pygame.image.load("Images\Archer3.png").convert_alpha(),
                                   (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))]
    Bow = [pygame.transform.scale(pygame.image.load("Images\Bow1.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
           pygame.transform.scale(pygame.image.load("Images\Bow4.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
           pygame.transform.scale(pygame.image.load("Images\Bow3.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
           pygame.transform.scale(pygame.image.load("Images\Bow2.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24)),
           pygame.transform.scale(pygame.image.load("Images\Bow5.png").convert_alpha(),
                                  (ScreenRes[0] // GameRes[0] * 24, ScreenRes[1] // GameRes[1] * 24))]


def DisplaySettings(Settings,
                    SettingActive):  # Function to display which settings in the settings window have been selected and which ones are actively being hovered over
    Window.blit(SelectedSettings[1 - Settings[0]], (0,
                                                    0))  # SelectedSettings[0] and [1] are the images for sound being on or off, so 1-whether sound is on or off is the image needed
    Window.blit(SelectedSettings[3 - Settings[1]], (0, 0))  # Similar to the above line but for music being on or off
    if Settings[
        2] == 1:  # For each setting after, if it has been selected, the image for it being outlined in yellow showing it as selected is displayed
        Window.blit(SelectedSettings[4], (0, 0))
    elif Settings[2] == 2:
        Window.blit(SelectedSettings[5], (0, 0))
    elif Settings[2] == 3:
        Window.blit(SelectedSettings[6], (0, 0))
    if Settings[3] == 15:
        Window.blit(SelectedSettings[7], (0, 0))
    elif Settings[3] == 25:
        Window.blit(SelectedSettings[8], (0, 0))
    elif Settings[3] == 35:
        Window.blit(SelectedSettings[9], (0, 0))
    elif Settings[3] == 45:
        Window.blit(SelectedSettings[10], (0, 0))
    if Settings[4] == 1 / 15:
        Window.blit(SelectedSettings[11], (0, 0))
    elif Settings[4] == 1 / 30:
        Window.blit(SelectedSettings[12], (0, 0))
    elif Settings[4] == 1 / 60:
        Window.blit(SelectedSettings[13], (0, 0))
    Window.blit(SelectedSettings[15 - Settings[5]],
                (0, 0))  # Same as the above lines for sound and music but for "Small Mode" being on or off
    Window.blit(ActiveSettings[SettingActive], (0,
                                                0))  # Finally, the setting currently highlighted by the player is displayed, on top of any other outlines to make it clear


def Menu(Settings, MusicLoopTime,
         LastHint):  # Function for displaying parts of the main menu and all the options that can be selected other than the game itself
    if LastHint == -1:
        Hint = 0  # On first game played, the hint telling the user to use WASD, SPACE and ESC is displayed
    else:
        Hint = random.randint(1, 13)
        while Hint == LastHint:
            Hint = random.randint(1, 13)
    OptionActive = 0  # OptionActive is used to store what option the player currently has highlighted
    InputKeys = pygame.key.get_pressed()
    while not (
            InputKeys[pygame.K_SPACE] and OptionActive == 0):  # Runs until the option for playing the game is selected
        InputKeys = pygame.key.get_pressed()
        Window.blit(MenuScreens[OptionActive], (0, 0))
        Window.blit(Hints[Hint], (0, 0))
        pygame.event.get()
        pygame.display.update()
        time.sleep(0.0001)
        if InputKeys[pygame.K_w] or InputKeys[
            pygame.K_a]:  # Changes the option selected if the player presses the WASD keys
            if OptionActive > 0:
                OptionActive -= 1
            else:
                OptionActive = 4
            while InputKeys[pygame.K_w] or InputKeys[
                pygame.K_a]:  # Second while loop to make it so the option selected will only increase by one until the player releases and then presses the button again
                InputKeys = pygame.key.get_pressed()
                Window.blit(MenuScreens[OptionActive], (0, 0))
                Window.blit(Hints[Hint], (0, 0))
                pygame.event.get()
                pygame.display.update()
                time.sleep(0.0001)
        elif InputKeys[pygame.K_s] or InputKeys[pygame.K_d]:
            if OptionActive < 4:
                OptionActive += 1
            else:
                OptionActive = 0
            while InputKeys[pygame.K_s] or InputKeys[pygame.K_d]:
                InputKeys = pygame.key.get_pressed()
                Window.blit(MenuScreens[OptionActive], (0, 0))
                Window.blit(Hints[Hint], (0, 0))
                pygame.event.get()
                pygame.display.update()
                time.sleep(0.0001)
        elif InputKeys[
            pygame.K_SPACE]:  # Runs the code for if the user selects an option except for OptionActive=0 which is for play and is handled by the while loop
            if OptionActive == 1:
                while not InputKeys[pygame.K_ESCAPE]:  # For displaying the credits
                    InputKeys = pygame.key.get_pressed()
                    Window.blit(Credits, (0, 0))
                    Window.blit(Hints[Hint], (0, 0))
                    pygame.event.get()
                    pygame.display.update()
                    time.sleep(0.0001)
            elif OptionActive == 2:
                SettingActive = 0
                while not InputKeys[pygame.K_ESCAPE]:  # For displaying the settings screen
                    while InputKeys[pygame.K_SPACE]:
                        InputKeys = pygame.key.get_pressed()
                        Window.blit(SettingScreen, (0, 0))
                        DisplaySettings(Settings, SettingActive)
                        Window.blit(Hints[Hint], (0, 0))
                        pygame.event.get()
                        pygame.display.update()
                        time.sleep(0.0001)
                    InputKeys = pygame.key.get_pressed()
                    Window.blit(SettingScreen, (0, 0))
                    DisplaySettings(Settings, SettingActive)
                    Window.blit(Hints[Hint], (0, 0))
                    pygame.event.get()
                    pygame.display.update()
                    time.sleep(0.0001)
                    if InputKeys[pygame.K_w] or InputKeys[
                        pygame.K_a]:  # Similar to above code for display but instead of different images for each setting in the setting screen being highlighted, the highlighting is shown with DisplaySettings()
                        if SettingActive > 0:
                            SettingActive -= 1
                        else:
                            SettingActive = 12
                        while InputKeys[pygame.K_w] or InputKeys[pygame.K_a]:
                            InputKeys = pygame.key.get_pressed()
                            Window.blit(SettingScreen, (0, 0))
                            DisplaySettings(Settings, SettingActive)
                            Window.blit(Hints[Hint], (0, 0))
                            pygame.event.get()
                            pygame.display.update()
                            time.sleep(0.0001)
                    elif InputKeys[pygame.K_s] or InputKeys[pygame.K_d]:
                        if SettingActive < 12:
                            SettingActive += 1
                        else:
                            SettingActive = 0
                        while InputKeys[pygame.K_s] or InputKeys[pygame.K_d]:
                            InputKeys = pygame.key.get_pressed()
                            Window.blit(SettingScreen, (0, 0))
                            DisplaySettings(Settings, SettingActive)
                            Window.blit(Hints[Hint], (0, 0))
                            pygame.event.get()
                            pygame.display.update()
                            time.sleep(0.0001)
                    elif InputKeys[pygame.K_SPACE]:  # For if the user selects a setting to change
                        if SettingActive == 0:
                            Settings[0] = 1 - Settings[
                                0]  # Sound is on or off so selecting it should reverse the value, 1, or 0 so 1-1 or 0 makes the opposite
                        elif SettingActive == 1:
                            pygame.mixer.stop()
                            Settings[1] = 1 - Settings[1]  # Same as above but for toggling off and on music
                            if Settings[1] == 1:
                                Music.play()
                                MusicLoopTime = time.time()
                        elif SettingActive == 2:  # Difficulty is stored as either 1 2 or 3
                            Settings[2] = 1
                        elif SettingActive == 3:
                            Settings[2] = 2
                        elif SettingActive == 4:
                            Settings[2] = 3
                        elif SettingActive == 5:  # Map size is stored as how long the length and width will be, 15, 25, 35 or 45
                            Settings[3] = 15
                        elif SettingActive == 6:
                            Settings[3] = 25
                        elif SettingActive == 7:
                            Settings[3] = 35
                        elif SettingActive == 8:
                            Settings[3] = 45
                        elif SettingActive == 9:  # Game speed is stored as how long the program waits until it reruns the main game loop 1/15 results in 15 frames per second, 1/30 results in 30, 1/60 results in 60 meaning. 30 is intended so 15 halfs the speed and 60 doubles it. The reason frame rate is tied to game speed instead of adjusting the values for how fast everything moves is so slower computers can try and run on half speed and gain some consistency in performance and experience better AI behaviour if the computer is too slow to handle 30 fps
                            Settings[4] = 1 / 15
                        elif SettingActive == 10:
                            Settings[4] = 1 / 30
                        elif SettingActive == 11:
                            Settings[4] = 1 / 60
                        elif SettingActive == 12:  # Same as code for music and sounds
                            Settings[5] = 1 - Settings[5]
                        while InputKeys[
                            pygame.K_SPACE]:  # While loop to stop toggle-able options from being instantly toggled on and off
                            InputKeys = pygame.key.get_pressed()
                            Window.blit(SettingScreen, (0, 0))
                            DisplaySettings(Settings, SettingActive)
                            Window.blit(Hints[Hint], (0, 0))
                            pygame.event.get()
                            pygame.display.update()
                            time.sleep(0.0001)
                _pickle.dump(Settings, open("Settings.cfg", "wb"))  # Writes to file saving settings
            elif OptionActive == 3:  # Code to display instructions if that option is selected
                while InputKeys[pygame.K_SPACE] or not InputKeys[pygame.K_ESCAPE]:
                    InputKeys = pygame.key.get_pressed()
                    Window.blit(Instructions, (0, 0))
                    Window.blit(Hints[Hint], (0, 0))
                    pygame.event.get()
                    pygame.display.update()
                    time.sleep(0.0001)
            elif OptionActive == 4:  # If the option for quitting is selected, the program exits
                pygame.display.quit()
                pygame.quit()
                exit()
    return Settings, MusicLoopTime, Hint


def Main(LastHint):  # The main function to initialise many of the variable and call other functions
    if os.path.exists("Settings.cfg"):  # Tests if settings file has been created
        Settings = _pickle.load(open("Settings.cfg", "rb"))  # If so settings are taken from that file
    else:
        Settings = [1, 1, 1, 25, 1 / 30, 0]  # If not settings are set to default
    if Settings[1] == 1:  # Settings[1] is whether music should be played or not
        Music.play()
    MusicLoopTime = time.time()
    Settings, MusicLoopTime, LastHint = Menu(Settings, MusicLoopTime, LastHint)
    AdjustGlobals(
        Settings)  # Used to, if small mode has been toggled on or off since the game has last been played, change the size of all game assets to make it display properly
    Grid = GridGen(Settings)
    EnemyList = []
    CharPos = [(len(Grid[0]) // 2) * 24, (len(
        Grid) // 2) * 24]  # Half the length of the grid excluding remainders or decimals, as the length will always be odd, is the center tile where the player and camera should start at
    CamPos = [(len(Grid[0]) // 2) * 24, (len(Grid) // 2) * 24]
    Movement = [0,
                24]  # Starts the player moving downwards showing how movement looks and giving a small - almost intro-like animation at the start of the game
    Score = 0
    NavGrid = [[]]
    NavX = 0  # NavX and NavY are used to store the co-ordinates InitNavGrid has reached so far
    NavY = 0
    while NavX < len(Grid) or NavY < len(Grid[0]):
        FrameTime = time.time()
        NavGrid, NavX, NavY = InitNavGrid(Grid, NavGrid, NavX, NavY, CharPos, FrameTime, Settings)
        pygame.event.get()  # Stops the game from timing out if the process takes a long time
    Results = [NavGrid, 100, 0]
    while Results[2] == 0 and Results[
        1] > 2:  # Results[2] is whether it has finished and Results[1] is the current value of tiles being checked (below 2 tiles nearby are no longer assigned values so NavGridConstruct has completed
        FrameTime = time.time()
        Results = NavGridConstruct(Results[0], Results[1], FrameTime, Settings)
        pygame.event.get()
    NavGrid = Results[0]
    GameOver = [0, "Nothing",
                "Nothing"]  # GameOver[0] is whether the player has lost, GameOver[1] and [2] store how the player died so it can be shown on the death screen
    NewNavGrid = NavGrid  # NewNavGrid is used to store new grids of how close each tile is to the player or chest while they are being generated without the code for the AI crashing due to their current NavGrid being ovewritten
    BowInfo = ["Right",
               0]  # BowInfo[0] is the direction the player and bow are facing; BowInfo[1] stores the timer for arrows being shot and the cooldown until the next one can be (24=bow starts firing, 12=arrow is shot)
    EnemySpawnData = [1, 0,
                      0]  # Used to store information for how many enemies will spawn and when they will, explained in more detail in the function EnemyTick()
    GameTicks = 0  # Variable used to store how long the game has gone on for
    while GameOver[0] == 0:  # The main game loop
        FrameTime = time.time()
        UpdateNeeded = 0  # Variable to store whether the NavGrid needs updating (the player has moved, a wall has been created/destroyed etc)
        Display(Grid, EnemyList, CharPos, CamPos, Movement, BowInfo,
                GameTicks)  # Function to display all assets on the screen while the game is being played
        EnemyList, GameOver, BowInfo, UpdateNeeded, Grid, EnemySpawnData, NavGrid, Score = EnemyTick(Grid, NavGrid,
                                                                                                     EnemyList, CharPos,
                                                                                                     BowInfo,
                                                                                                     UpdateNeeded,
                                                                                                     EnemySpawnData,
                                                                                                     CamPos, Settings,
                                                                                                     GameTicks,
                                                                                                     Score)  # Function to update enemy's statuses, positions as well as the arrows shot by the bow
        CamPos, CharPos, Movement, UpdateNeeded, BowInfo, GameOver = Move(Grid, EnemyList, CamPos, CharPos, Movement,
                                                                          UpdateNeeded, BowInfo,
                                                                          GameOver)  # Function for getting keypresses and moving the player
        if UpdateNeeded == 1 and NavGrid == NewNavGrid:  # If an update is required for the grid of how close each tile is to the chest or player, the variables storing InitNavGrid's progress are reset to 0 so it will be called
            NavX = 0
            NavY = 0
            NewNavGrid = [[]]
        if NavX < len(Grid) or NavY < len(Grid[0]):
            NewNavGrid, NavX, NavY = InitNavGrid(Grid, NewNavGrid, NavX, NavY, CharPos, FrameTime, Settings)
            Results = [NewNavGrid, 100,
                       0]  # Results[1] and Results[0] are reset so NavGridConstruct is called to finish the NavGrid
        elif Results[2] == 0 and Results[1] > 2:
            Results = NavGridConstruct(Results[0], Results[1], FrameTime, Settings)
            NewNavGrid = Results[0]
        else:
            NavGrid = NewNavGrid
        pygame.event.get()  # Makes the game not time-out
        if time.time() - FrameTime < Settings[
            4] - 0.01:  # If the frame completes before the targeted time (default around 32 milliseconds) then time.sleep() is used to pause the program to force the framerate to stay consistent (-0.01 is used because very rarely, the if statement can take long enough to computer that by the time it finishes, the time has increased and now Settings[4]-(time.time()-FrameTime) is negative causing a crash
            time.sleep(Settings[4] - (time.time() - FrameTime))
        else:
            pass
        GameTicks += 1
        if Settings[1] == 1 and time.time() - MusicLoopTime > 260:
            Music.play()
            MusicLoopTime = time.time()
    pygame.mixer.stop()  # Code for if the player has died
    global GameRes  # Used to reset GameRes if it was changed by small mode being active
    GameRes = [384, 216]
    InputKeys = pygame.key.get_pressed()
    Score = int(Score * ((1 / 30) / Settings[4]) * Settings[2])  # Modifies score based on game speed and difficulty
    Score = str(
        Score)  # Converts score to a string so it does not need to be converted later again and again inside the while loop
    while not InputKeys[pygame.K_SPACE] and not InputKeys[
        pygame.K_ESCAPE]:  # Will show the death screen until the player presses space or escape
        InputKeys = pygame.key.get_pressed()
        Window.blit(GameOverScreen, (0, 0))
        Window.blit(pygame.transform.scale(pygame.image.load("Images\GameOver" + GameOver[1] + ".png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)), (0,
                                                                                                                   0))  # GameOver[1] and [2] store how the player died so images relating to their death are displayed
        if GameOver[2] == "Chest":
            Window.blit(pygame.transform.scale(pygame.image.load("Images\GameOver" + "Chest" + ".png").convert_alpha(),
                                               (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                        (0, 0))
        for Digit in range(0, len(Score)):
            Window.blit(
                pygame.transform.scale(pygame.image.load("Images\Score" + Score[Digit] + ".png").convert_alpha(),
                                       (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                (Digit * 12 * (ScreenRes[1] // GameRes[1]), 0))
        pygame.event.get()
        pygame.display.update()
        time.sleep(0.0001)
    while InputKeys[pygame.K_SPACE] or InputKeys[
        pygame.K_ESCAPE]:  # Second while to avoid the main menu instantly showing with spacebar pressed and play being selected resulting in the player being unable to navigate the main menu after dying if they wanted to
        InputKeys = pygame.key.get_pressed()
        Window.blit(GameOverScreen, (0, 0))
        Window.blit(pygame.transform.scale(pygame.image.load("Images\GameOver" + GameOver[1] + ".png").convert_alpha(),
                                           (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                    (0, 0))
        if GameOver[2] == "Chest":
            Window.blit(pygame.transform.scale(pygame.image.load("Images\GameOver" + "Chest" + ".png").convert_alpha(),
                                               (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                        (0, 0))
        for Digit in range(0, len(Score)):
            Window.blit(
                pygame.transform.scale(pygame.image.load("Images\Score" + Score[Digit] + ".png").convert_alpha(),
                                       (ScreenRes[0] // GameRes[0] * 384, ScreenRes[1] // GameRes[1] * 216)),
                (Digit * 12 * (ScreenRes[1] // GameRes[1]), 0))
        pygame.event.get()
        pygame.display.update()
        time.sleep(0.0001)
    Main(LastHint)  # Restarts the game


Main(-1)
