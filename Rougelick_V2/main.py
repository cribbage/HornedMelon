#!/usr/bin/env python
import pygame, math, sys, random, os
from globalVars import *
from gameLogic import *
from player import*

def createPlayer(level):
	startPos = random.choice(level.filledCoords)
	startPos = (startPos[0]+(TILESIZE[0]//2),startPos[1]+(TILESIZE[1]//2))
	dude = player(startPos)
	dude.rect.center = startPos
	return dude
	
def mainLoop(windowSurf,dude,fpsClock,lvl):
	while True:
		events = pygame.event.get()
		windowSurf.fill((0,0,0))
		camera = update(lvl,dude,events)
		blit(windowSurf,dude,lvl,camera)			
		pygame.display.set_caption("FPS: " +str(fpsClock.get_fps()))
		pygame.display.flip()
		fpsClock.tick(60)
						
def start(windowSurf,levelSize):	
	level = createLevel(levelSize)
	dude = createPlayer(level)
	mainLoop(windowSurf,dude,fpsClock,level)

while True:
	pygame.init()
	fpsClock = pygame.time.Clock()
	resolution = pygame.display.Info()
	pygame.display.init()
	pygame.display.set_caption("FPS: " +str(fpsClock.get_fps()))	
	windowSize = (1200,600)
	windowSurf = pygame.display.set_mode(windowSize)
	levelSize = (2400,2400)
	start(windowSurf,levelSize)
		

