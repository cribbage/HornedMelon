#!/usr/bin/env python
import pygame, math, sys, random
from pygame.locals import *
from globalVars import *
from brick import *
from water import *
from tools import *

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
		self.floors = []
		self.walls = []
		self.xWalls = {}
		self.wallDixct = {}
		self.moves = self.getMoves()
		self.buildLevel()
		self.cleanSurf = self.surf
		self.eCount = 50#amount of enemies
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
		up = (x,y-TILESIZE[1])
		down = (x,y+TILESIZE[1])
		left = (x-TILESIZE[0],y)
		right = (x+TILESIZE[0],y)
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
			self.floors.append(direction)								
		
	def drawWater(self,x=0,y=0):
		for x in range(0,self.levelSize[0],TILESIZE[0]):
			self.xWalls[x] = []
			for y in range(0,self.levelSize[1],TILESIZE[1]):
				if (x,y) not in self.floors:					
					self.surf.blit(self.waterSurf.surfs[self.waterSurf.surfC],(x,y))
					self.walls.append((x,y))
					self.xWalls[x].append((x,y))
	
	#goes through each tile to see if its empty and fills it with water		
	def redrawWater(self,camera):
		for wall in self.walls:
			rect = Rect(wall,TILESIZE)
			if inCamera(camera,rect):				
				self.surf.blit(self.waterSurf.surfs[self.waterSurf.surfC],wall)
							
	def updateLevel(self,camera,fpsn):
		self.cleanSurf = self.surf.copy()
		self.time += fpsn
		if self.time >= 6:
			self.time = 0
			self.waterSurf.switchSurf()
			self.redrawWater(camera)
		

