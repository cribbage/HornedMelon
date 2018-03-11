import pygame, math, sys, random, time
from pygame.locals import *

class LightLayer:
	def __init__(self, windowSize):
		choices = [True, False]
		self.windowSize = windowSize
		self.on = random.choice(choices)
		self.surf = pygame.Surface((windowSize)).convert_alpha()
		self.surf.fill((0,0,0,255))
		self.drawCircs()
			
	def drawCircs(self):
		i = 255
		while i > 50:	
			pygame.draw.circle(self.surf, (0,0,0,i), (round(self.windowSize[0]/2),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))), i, 0)		
			i-=1
				
	def glow(self):
		i = 50
		if self.on:
			while i > 0:
				pygame.draw.circle(self.surf, (random.randint(150, 255),random.randint(150, 255),0,i), (round(self.windowSize[0]/2),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))), i, 0)	
				i-=1	

class LightEmitter:
	def __init__(self,pos,size,surf):
		self.size = size
		self.pos = pos
		self.litPlaces = []
		self.drawRects(surf)
		
	def drawRects(self,surf):
		n = 1
		for i in range(self.size,self.size*6,6):
			for x in range(self.pos[0]-(self.size)*n,self.pos[0]+self.size*n,(self.size)):
				for y in range(self.pos[1]-(self.size)*n,self.pos[1]+self.size*n,(self.size)):
					if(x,y) not in self.litPlaces and random.choice((True,False)):
						pygame.draw.rect(surf, (0,0,0,255-i),(x,y,self.size,self.size),0)		
						self.litPlaces.append((x,y))
			n+=1
		pygame.draw.rect(surf,(100,0,0),((self.pos[0],self.pos[1]),(self.size,self.size)),0)	
		
	#def update(self,surf,pos):
	#	self.drawRects(surf,pos)
		
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	ll = LightLayer((1200,600))
	le = LightEmitter((600,300),6,ll.surf)
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		windowSurf.fill((100,100,100))
		windowSurf.blit(ll.surf,(0,0))
		pygame.display.flip()
		fpsClock.tick(60)	
#test()
