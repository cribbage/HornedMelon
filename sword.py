import pygame, math, sys, random, time, copy
from pygame.locals import *
from ants import *

class Sword:
	def __init__(self,sPoint,ePoint,damageNodes):
		self.sPoint = sPoint
		self.ePoint = ePoint
		self.damageNodes = damageNodes
		
	def moveSword(self,hat,axis1,axis2):
		self.sPoint = (hat[0],hat[1])			
		self.ePoint = (self.sPoint[0]+axis1*60,self.sPoint[1]+axis2*60)
	
	def drawSword(self,surf):
		pygame.draw.lines(surf, (255,255,255), False, (self.sPoint,self.ePoint), 10)
	
	def collisions(self,wielder,e,ants,levelPos, windowSize):
		x = -levelPos[0]
		y = -levelPos[1]
		if e.rect.collidepoint((self.ePoint[0]+x,self.ePoint[1]+y)):
			self.leaveMark(e,windowSize)
			self.damage(wielder,e)
			i = 1
			while i >0:
				ants.append(Ant(1,(self.ePoint[0]+x,self.ePoint[1]+y)))
				i -= 1	
	
	def damage(self,wielder,target):
		target.health -= wielder.strg
		target.hitTimer = 1
		if target.health <=0:
			target.alive = False
					
	def leaveMark(self,e,windowSize):
		x = (self.ePoint[0]/windowSize[0])*e.size[0]
		y = (self.ePoint[1]/windowSize[1])*e.size[1]
		pygame.draw.rect(e.surf,(random.randint(0,150),0,0),(int(x),int(y),random.randint(2,7),random.randint(2,7)))	
		
	def update(self,surf,hat,axis1,axis2):
		self.moveSword(hat,axis1,axis2)
		self.drawSword(surf)
		
def test():
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	p1 = (100,100)	
	p2 = (200,200)
	sword = Sword(p1,p2,3)
	attackRects = []
	while len(attackRects) < 20: 	
		attackRects.append(Rect(random.randint(0,1150),random.randint(0,550),50,50))
	r = 100
	b = 100
	g = 100
	
	grid = Grid()
	ants = []	
	pygame.joystick.init()
	controller = pygame.joystick.Joystick(0)
	controller.init()
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == JOYBUTTONDOWN:
				if event.button == 9:
					return
					
					
		
		
		
	
		windowSurf.fill((0,0,0))
		
		sword.update(windowSurf,controller.get_hat(0),controller.get_axis(2),controller.get_axis(3))
		
		for rect in attackRects:
			pygame.draw.rect(windowSurf,(r,g,b),rect,0)
			sword.collisions(rect,ants)
			r,g,b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
				
		
		for ant in ants:
			ant.update(grid)
			if ant.life <= 0:
				ants.remove(ant)
				
		windowSurf.blit(grid.surf,(0,0))
		
		pygame.display.flip()
		fpsClock.tick(60)
		
#while True:
#	test()
