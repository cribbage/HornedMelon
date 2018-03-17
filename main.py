#!/usr/bin/env python
#hello
import pygame, math, sys, random, os
from globalVars import *
from gameLogic import *
from tools import *
from enemy import *

def mainLoop(windowSurf,dude,fpsClock,lvl,enemies):
	while True:
		fpsNormalizer = normalizeFPS(fpsClock)
		events = pygame.event.get()
		getInput(events)
		windowSurf.fill((0,0,0))
		c = camera(dude.pos,lvl.levelSize)
		update(lvl,dude,events,c,enemies,fpsNormalizer)
		blit(windowSurf,dude,lvl,c,enemies)			
		pygame.display.set_caption("FPS: " +str(fpsClock.get_fps()))
		pygame.display.flip()
		fpsClock.tick(60)
						
def main():	
	pygame.init()
	fpsClock = pygame.time.Clock()
	resolution = pygame.display.Info()
	pygame.display.init()
	pygame.display.set_caption("FPS: " +str(fpsClock.get_fps()))	
	windowSurf = pygame.display.set_mode(WINDOWSIZE)
	levelSize = (2560,1280)
	level = createLevel(levelSize)
	dude = createPlayer(level.floors)
	enemies = createEnemies(level.floors,level.eCount)
	mainLoop(windowSurf,dude,fpsClock,level,enemies)
	
if __name__ == '__main__':
	main()
