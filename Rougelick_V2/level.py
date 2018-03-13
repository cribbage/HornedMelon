#!/usr/bin/env python
import pygame, math, sys, random
from pygame.locals import *
from globalVars import *
from brick import *
from water import *

"""
This file handles level creation and animated tiles. The level is built
by a simple automata, so every tile is reachable.
"""

class level:
	#Initializing builds the level
	def __init__(self,levelSize):
		self.pos = (0,0)
		self.levelSize = levelSize
		self.windowSize = WINDOWSIZE
		self.surf = pygame.Surface(levelSize)
		self.waterSurf = waterTile(TILESIZE)
		self.filledCoords = []
		self.walls = []
		self.moves = self.getMoves()
		self.buildLevel()
		self.cleanSurf = self.surf
		self.time = 0
		
	#determines how many moves the automata will make	
	def getMoves(self):
		x = self.levelSize[0]//TILESIZE[0]
		y = self.levelSize[1]//TILESIZE[1]
		return (x*y)*2
			
	def buildLevel(self):
		self.drawFloor()
		self.drawWater()
	
	#draws brick tile to level
	def drawBrick(self,x,y):
		self.surf.blit(BrickTile(TILESIZE).surf,(x,y))	
		return
	
	#gets next direction for automata, makes sure it stays within the level
	def getDirection(self,x,y):
		up = (x,y-100)
		down = (x,y+100)
		left = (x-100,y)
		right = (x+100,y)
		direction = random.choice([up,down,left,right])
		while direction[0] < 0 or direction[1] < 0 or direction[0] >= self.levelSize[0] or direction[1] >= self.levelSize[1]:
			direction = random.choice([up,down,left,right])	
		return direction	
		
	#creates level using simple automata
	def drawFloor(self):	
		x=self.levelSize[0]//2
		y=self.levelSize[1]//2
		for z in range(self.moves,0,-1):
			direction = self.getDirection(x,y)
			x,y = direction		
			self.drawBrick(x,y)						
			self.filledCoords.append(direction)								
		
	
	#goes through each tile to see if its empty and fills it with water		
	def drawWater(self,x=0,y=0):
		for x in range(0,self.levelSize[0],TILESIZE[0]):
			for y in range(0,self.levelSize[1],TILESIZE[1]):
				if (x,y) not in self.filledCoords:					
					self.surf.blit(self.waterSurf.surfs[self.waterSurf.surfC],(x,y))
					self.walls.append((x,y))
					
	def updateLevel(self):
		self.cleanSurf = self.surf.copy()
		self.time += 1
		if self.time == 6:
			self.time = 0
			self.waterSurf.switchSurf()
			self.drawWater()


		
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	

	windowSurf = pygame.display.set_mode(WINDOWSIZE)
	
	levelSize = (1200, 600)
	lvl = level(levelSize)
	
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				lvl = level(levelSize)
		windowSurf.fill((0,0,0))
		windowSurf.blit(lvl.surf,lvl.pos)
		
		lvl.updateLevel()
					
		pygame.display.flip()
		fpsClock.tick(60)	
#test()