#!/usr/bin/env python
import pygame, math, sys, random, os
from globalVars import *
from gameLogic import *
from player import*

def createPlayer(windowSize,level):
	startPos = random.choice(level.filledCoords)
	startPos = (startPos[0]+(TILESIZE[0]//2),startPos[1]+(TILESIZE[1]//2))
	dude = player(startPos)
	dude.rect.center = startPos
	return dude
	

def mainLoop(windowSurf,dude,fpsClock,lvl):
	while True:
		events = pygame.event.get()
		windowSurf.fill((0,0,0))
		update(lvl,dude,events,lvl.walls,lvl.levelSize)
	#	print(dude.pos)
		blit(windowSurf,dude,lvl)		
		#lvl.pos = (lvl.pos[0]-dude.pos[0], lvl.pos[1]-dude.pos[1])		
		pygame.display.set_caption("FPS: " +str(fpsClock.get_fps()))
		pygame.display.flip()
		fpsClock.tick(60)
						
def start(windowSurf):
	print("building level...")		
	level = createLevel(windowSize)
	print("creating player...")
	dude = createPlayer(windowSize,level)
	print("starting main loop...")
	mainLoop(windowSurf,dude,fpsClock,level)

while True:
	print("initializing pygame...")
	pygame.init()
	fpsClock = pygame.time.Clock()
	resolution = pygame.display.Info()
	pygame.display.init()
	pygame.display.set_caption("FPS: " +str(fpsClock.get_fps()))	
	windowSize = (1200,600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	while True:
		print("preparing main loop...")
		start(windowSurf)
		

