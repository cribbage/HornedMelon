#!/usr/bin/env python
#hello
import pygame, math, sys, random
from pygame.locals import *
from globalVars import *
""" 
This file is for filling surfaces with brick textures. It creates bricks of
six different lengths and randomly places them onto a surface with a 
unique configuration of six uniquely colored bricks. 
Can either be used to create a whole background, or tiles.
"""

class Bricks:
	#create this object and self.surfs will be a list of brick surfaces
	def __init__(self,minLen=TILESIZE[0]*.15,maxLen=TILESIZE[0]*.40,step=TILESIZE[0]*.05,width=TILESIZE[1]*.20):
		self.surfs = []
		self.minLen = minLen #minimum length of bricks
		self.maxLen = maxLen #maximum length of bricks
		self.step = step #increment of length
		self.width = width
		self.makeBricks()
	
	#calls makeBrickSurface for each length of brick and appends it to self.surfs	
	def makeBricks(self):		
		i = self.minLen 
		while i <= self.maxLen: 		
			self.surfs.append(self.makeBrickSurface(i))		
			i += self.step 
	
	#creates the brick surface	
	def makeBrickSurface(self,i): 
		bSurf = pygame.Surface((round(i),round(self.width))) 		
		bSurf = self.fillBrick(i,bSurf)		
		return bSurf 
	
	#fills the brick surface, first the colorful 5x5 rects, then a black border
	def fillBrick(self,i,bSurf,x=0,y=0):
		surfSize = pygame.Surface.get_size(bSurf)	
		while x <= surfSize[0] and y < surfSize[1]:	
			color = (random.randint(50,66),random.randint(50,66),random.randint(54,66))
			rect = Rect(x,y,5, self.width)
			pygame.draw.rect(bSurf, color, rect, 3) 	
			x += 5
			if x >= surfSize[0] and y < surfSize[1]:
				x = 0
				y+= 5
		pygame.draw.rect(bSurf, (0,0,0), (0, 0,i, self.width), 2) 
		return bSurf
			
class BrickTile:
	#Places bricks neatly into a tile defined by tileSize 
	def __init__(self, tileSize):
		self.pos = (0,0)	
		self.tileSize = tileSize
		self.surf =  pygame.Surface(tileSize).convert()
		self.surf.set_colorkey((1,0,0))
		self.surf.fill((1,0,0))
		self.bricks = Bricks()
		self.placeBricks()
		
	def placeBricks(self):	
		while self.pos[0] <= self.tileSize[0] and self.pos[1] < self.tileSize[1]:
			self.drawBrick()
			self.movePos(pygame.Surface.get_size(self.bRect))
			
	#chooses random brick, draws to tile
	def drawBrick(self):
		self.bRect = random.choice(self.bricks.surfs)
		self.surf.blit(self.bRect,self.pos)
		
	#move to next brick position
	def movePos(self, brickSize):
		xPos = self.pos[0]+brickSize[0]
		yPos = self.pos[1]
		if xPos > self.tileSize[0]:			
			xPos = 0
			yPos += TILESIZE[1]*.2	
		self.pos = (xPos, yPos)	
			
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)	
	floor = BrickTile((1200,600))
	
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
		windowSurf.fill((0,150,0))		
		windowSurf.blit(floor.surf,(0,0))					
		pygame.display.flip()
		fpsClock.tick(60)	
	
#test()
