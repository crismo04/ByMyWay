"""
Cristian Molina
Game of Life. John Horton Conway
This is my ineficient (and quickly done) code for this game
Thanks to dot CSV for the inspiration
"""

import pygame
import numpy as np
import time

pygame.init()

widht, heigth = 700, 700
screen = pygame.display.set_mode((widht, heigth))

bg = 25, 25, 25
screen.fill(bg)

nCellsX, nCellsY = 100, 100
dimCW = widht / nCellsX
dimCH = heigth / nCellsY

gameRun = False

# matrix for the cells, (0 = no cell, 1 = cell)
gameState = np.zeros((nCellsX, nCellsY))

while 1:
    # save the old state, thus all changes happens at the same time
    newGameState = np.copy(gameState)

    # clean the old screen and sleep a bit the view
    screen.fill(bg)

    # search input events
    inEv = pygame.event.get()
    for event in inEv:
        if event.type == pygame.KEYDOWN:
            gameRun = not gameRun

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            cellX, cellY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[cellX, cellY] = not newGameState[cellX, cellY]

    for y in range(0, nCellsX):
        for x in range(0, nCellsY):

            if gameRun:

                # sum of neighbour cells in toroid form
                nNeigh = gameState[(x - 1) % nCellsX, (y - 1) % nCellsY] + \
                         gameState[(x - 1) % nCellsX, y % nCellsY] + \
                         gameState[(x - 1) % nCellsX, (y + 1) % nCellsY] + \
                         gameState[x % nCellsX, (y - 1) % nCellsY] + \
                         gameState[x % nCellsX, (y + 1) % nCellsY] + \
                         gameState[(x + 1) % nCellsX, (y - 1) % nCellsY] + \
                         gameState[(x + 1) % nCellsX, y % nCellsY] + \
                         gameState[(x + 1) % nCellsX, (y + 1) % nCellsY]

                # rules: #1, if you have 3 neighbour, revive
                if gameState[x, y] == 0 and nNeigh == 3:
                    newGameState[x, y] = 1
                # 2, if you have more tah 3 neighbour or less tha 2, die
                elif gameState[x, y] == 1 and (nNeigh < 2 or nNeigh > 3):
                    newGameState[x, y] = 0

            # polygon for each cell
            poly = [(x * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (x * dimCW, (y + 1) * dimCH)]

            # draw each cell
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (225, 225, 225), poly, 0)

    # update the display and the gamestate
    gameState = np.copy(newGameState)
    pygame.display.flip()
