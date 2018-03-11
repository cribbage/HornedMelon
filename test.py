import pygame, math, sys, random
from pygame.locals import *

class brick:
	def __init__(self, brickMin, brickMax, step, width):
		self.brickSurfs = []
		self.brickMin = brickMin
		self.brickMax = brickMax
		self.step = step
		self.width = width
		self.makeBricks()
		
	def makeBricks(self):		
		i = self.brickMin
		index = 0
		while i <= self.brickMax:
			bRect = Rect(0, 0,i, self.width)
			self.brickSurfs.append(pygame.Surface((i,self.width)))
			self.makeiRects(index)
			pygame.draw.rect(self.brickSurfs[index], (0,0,0), bRect, 3)
			
			i += self.step
			index += 1
			
	def makeiRects(self,i):
		x=0
		y=0
		surfSize = pygame.Surface.get_size(self.brickSurfs[i])
		while x <= surfSize[0] and y < surfSize[1]:
				
			pygame.draw.rect(self.brickSurfs[i], (random.randint(50,66),random.randint(50,66),random.randint(54,66)), Rect(x,y,5, self.width), 3)		
			x += 5
			if x >= surfSize[0] and y < surfSize[1]:
				x = 0
				y+= 5


			
class brickLayer:
	def __init__(self, surfSize):
		self.pos = (0,0)	
		self.surfSize = surfSize
		self.surf =  pygame.Surface(surfSize).convert()
		self.surf.set_colorkey((1,0,0))
		self.surf.fill((1,0,0))
		self.bricks = brick(15,40,5,20)
		while self.pos[0] <= self.surfSize[0] and self.pos[1] < self.surfSize[1]:
			self.drawRect()
		
	def drawRect(self):
		bRect = random.choice(self.bricks.brickSurfs)
		self.surf.blit(bRect,self.pos)
		self.movePos(pygame.Surface.get_size(bRect))
	
	def movePos(self, surfSize):
		xPos = self.pos[0]+surfSize[0]
		yPos = self.pos[1]
		if xPos > self.surfSize[0]:			
			xPos = 0
			yPos += 20
			
		self.rectLength = random.randrange(15,40,5)
		self.rectWidth = 20
		
		self.pos = (xPos, yPos)	
			
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	floor = brickLayer((1200,600))
	
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
		windowSurf.fill((0,150,0))
		
		windowSurf.blit(floor.surf,(0,0))

					
		pygame.display.flip()
		fpsClock.tick(60)	
		
test()

