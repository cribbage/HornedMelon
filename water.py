import pygame, math, sys, random, time
from pygame.locals import *
		
class waterLayer:
	def __init__(self, surfSize):
		self.surf = pygame.Surface(surfSize)
		self.surf2 = pygame.Surface(surfSize)
		self.surf3 = pygame.Surface(surfSize)
		self.surfs = [self.surf, self.surf2, self.surf3]
		self.surfC = 0
		self.liq = random.choice(('water','lava'))
		self.drawWater()
		
	def switchSurf(self):
		self.surfC +=1
		if self.surfC > 2:
			self.surfC = 0
	
	def drawWater(self):	
		for surf in self.surfs:
			x=0
			y=0
			surfSize = pygame.Surface.get_size(surf)
			while x <= surfSize[0] and y < surfSize[1]:	
				if self.liq == 'water':				
					pygame.draw.rect(surf, (random.randint(0,100),random.randint(0,100),255), Rect(x,y,2,2), 0)		
				elif self.liq == 'lava':
					pygame.draw.rect(surf, random.choice(((random.randint(233, 255),random.randint(0, 165),0), (0,0,0))), Rect(x,y,2,2) ,0)
				x += 2
				if x >= surfSize[0] and y < surfSize[1]:
					x = 0
					y+= 2
	
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	water = waterLayer((300,150))
	
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
		while x < 1200 and y <600:
			windowSurf.blit(water.surfs[water.surfC],(x,y))
			x+=300
			if x == 1200:
				x = 0
				y+=150

		
		if time == 6:
			water.switchSurf()

		time += 1
		if time > 6:
			time = 0		
		pygame.display.flip()
		fpsClock.tick(60)	
#test()
