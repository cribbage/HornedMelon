import pygame, math, sys, random, time,particles
from pygame.locals import *

class ScrollSpell:
	def __init__(self,tileSize,level,pos):
		self.selectSize = tileSize #Size of selection rect
		self.size = (random.randint(10,25),random.randint(10,25))
		self.time = level*60
		self.level = level
		self.mAttack = random.randint(1,5)*level
		self.mIntensity = level
		self.usable = True 
		self.pos = pos
		self.rectSize = 1
		self.color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
		self.direction = (0,0)
		self.selRect = Rect(self.pos,self.selectSize)
		self.particles = []
		
	def zoomRect(self):#self.selRect closes in
		if self.rectSize < 48:
			self.rectSize += 1
		else:
			self.rectSize = 1
	
	def drawSelRect(self,pos,levelSurf):#Shows selection area
		x = pos[0] - (pos[0] % (self.selectSize[0]/self.rectSize)) 
		y = pos[1] - (pos[1] % (self.selectSize[1]/self.rectSize))
		a = self.selectSize[0]/self.rectSize
		b = self.selectSize[1]/self.rectSize
		self.selRect = Rect((x,y),(a,b))
		pygame.draw.rect(levelSurf,self.color,self.selRect,4)
		self.zoomRect() 
	
	def getDirection(self,pos):
		tileRect = Rect((pos[0] - (pos[0] % self.selectSize[0]),pos[1] - (pos[1] % (self.selectSize[1]))),self.selectSize)
		if self.selRect.center[0] > tileRect.center[0]:#aim left
			self.direction = (-1,0)
		else:#aim right
			self.direction = (1,0)
		if self.selRect.center[1] > tileRect.center[1]:#aim up
			self.direction = (self.direction[0],-1)
		else:#aim down
			self.direction = (self.direction[0],1)
	
	def placeSpell(self,pos,levelSurf):
		self.usable = False
		self.pos = pos
		self.getDirection(pos)
		
	def update(self,pos,levelSurf,click):
		self.drawSelRect(pos,levelSurf)
		if click:#CREATE SPELL
			self.placeSpell(pos,levelSurf)

		
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	scrl = ScrollSpell((100,100),1,(100,200))
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		windowSurf.fill((100,100,100))
		scrl.update(pygame.mouse.get_pos(),windowSurf,False)
		pygame.display.flip()
		fpsClock.tick(60)	
#test()
