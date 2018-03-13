import pygame, math, sys, random, time
from pygame.locals import *

"""
This file is an animated water tile. It is created similarly to the brick,
but it only draws small solid squares, and it draws them to several textures.
In order to animate it, you have to call switchSurf. There is a 6 frame
timer in the Level file which controls that, at this point.

Probably should make this class into a general animator for tiles, but 
only animating water for now, and maybe forever.
"""

		
class waterTile:
	#create the four surfaces
	def __init__(self, surfSize):
		self.surfSize = surfSize
		self.surf = pygame.Surface(surfSize)
		self.surf2 = pygame.Surface(surfSize)
		self.surf3 = pygame.Surface(surfSize)
		self.surfs = [self.surf, self.surf2, self.surf3]
		self.surfC = 0
		self.drawWater()
	
	#animate	
	def switchSurf(self):
		self.surfC +=1
		if self.surfC > 2:
			self.surfC = 0
	
	#create random water pattern for each surface
	def drawWater(self):	
		for surf in self.surfs:
			x=0
			y=0
			while x <= self.surfSize[0] and y < self.surfSize[1]:				
				pygame.draw.rect(surf, (random.randint(0,100),random.randint(0,100),255), Rect(x,y,2,2), 0)						
				x += 2
				if x >= self.surfSize[0] and y < self.surfSize[1]:
					x = 0
					y+= 2
	
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	water = waterTile((100,100))
	
	time = 0
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
		windowSurf.fill((0,0,0))
		
		x=0
		y=0
		
		#same tile repeated across the screen demonstrating seemlessness
		while x < 1200 and y <600:
			windowSurf.blit(water.surfs[water.surfC],(x,y))
			x+=100
			if x == 1200:
				x = 0
				y+=100

		
		if time == 6:
			water.switchSurf()

		time += 1
		if time > 6:
			time = 0		
		pygame.display.flip()
		fpsClock.tick(60)	
#test()
