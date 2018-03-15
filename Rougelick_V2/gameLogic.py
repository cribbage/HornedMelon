#!/usr/bin/env python
import pygame, math, sys, random, os
from pygame.locals import *
from level import *
from globalVars import *
from player import *
from tools import *
from enemy import *


###---Initialization--###


def createLevel(levelSize):
	lvl = level(levelSize)
	return lvl

def createPlayer(floors):
	pos = randomFloorPosition(floors)
	dude = player(pos)
	dude.rect.center = pos
	return dude

def createEnemy(floors):
	pos = randomFloorPosition(floors)
	enemy = Enemy(pos)
	return enemy

def createEnemies(floors,eNum):
	enemies = []
	for x in range(eNum):
		enemies.append(createEnemy(floors))
	return enemies


###---Running---###


"""Enemy Logic"""

def updateEnemy(enemy,walls,levelSize,fpsn):
	enemy.update(walls,levelSize,fpsn)

def updateEnemies(enemies,walls,levelSize,xWalls,fpsn):
	for enemy in enemies:
		enemy.update(walls,levelSize,xWalls,fpsn)

def blitEnemy(enemy,surf):
	enemy.blit(surf)
	
def blitEnemies(enemies,surf,c):
	for enemy in enemies:
		if inCamera(c,enemy.rect):
			blitEnemy(enemy,surf)

"""Player Logic"""

def updatePlayer(dude,events,wallRects,levelSize,c,fpsn):
	dude.update(events,levelSize,wallRects,c,fpsn)	

def blitPlayer(dude,surf,size,fpsn):
	dude.blit(surf,size,fpsn)

"""General Logic"""

def	update(lvl,dude,events,c,enemies,fpsn):
	updatePlayer(dude,events,lvl.walls,lvl.levelSize,c,fpsn)
	updateEnemies(enemies,lvl.walls,lvl.levelSize,lvl.xWalls,fpsn)
	lvl.updateLevel(c,fpsn)
									
def blit(windowSurf,dude,lvl,camera,enemies,fpsn):
	blitPlayer(dude,lvl.cleanSurf,lvl.levelSize,fpsn)
	blitEnemies(enemies,lvl.cleanSurf,camera)
	windowSurf.blit(lvl.cleanSurf.subsurface(camera),(0,0))
	




