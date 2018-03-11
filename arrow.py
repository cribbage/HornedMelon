import pygame, math, sys, random
from pygame.locals import *

class Arrow:
	def __init__(self,pos):
		self.oPos = pos
		self.pos = pos			
		self.triangle = ((self.pos[0]-30,self.pos[1]), (self.pos[0]-10,self.pos[1]-10), (self.pos[0]-10,self.pos[1]+10))
		self.lastD = 'right'
		self.charge = 0
		self.charging = False
		self.fired = False
		self.direction = (0,0)
		self.mFrames = 130
		
	def draw(self, surf):
		pygame.draw.polygon(surf, (100,0,0),self.triangle,0)
		
	def aim(self, direction):		
		direction = (round(direction[0]), round(direction[1]))
		self.direction = direction
		
		if direction == (1,0) or self.lastD == 'right':
			self.triangle = ((self.pos[0]+30,self.pos[1]), (self.pos[0]+10,self.pos[1]-10), (self.pos[0]+10,self.pos[1]+10))
			self.lastD = 'right'
		if direction == (1,1) or self.lastD == 'bottomRight':
			self.triangle = ((self.pos[0]+23,self.pos[1]+23), (self.pos[0]+15,self.pos[1]), (self.pos[0],self.pos[1]+15))
			self.lastD = 'bottomRight'
		if direction == (1,-1) or self.lastD == 'topRight':
			self.triangle = ((self.pos[0]+23,self.pos[1]-23), (self.pos[0]+15,self.pos[1]), (self.pos[0],self.pos[1]-15))
			self.lastD = 'topRight'
		if direction == (-1,0) or self.lastD == 'left':
			self.triangle = ((self.pos[0]-30,self.pos[1]), (self.pos[0]-10,self.pos[1]-10), (self.pos[0]-10,self.pos[1]+10))
			self.lastD = 'left'
		if direction == (-1,-1) or self.lastD == 'bottomLeft':
			self.triangle = ((self.pos[0]-23,self.pos[1]-23), (self.pos[0]-15,self.pos[1]), (self.pos[0],self.pos[1]-15))
			self.lastD = 'bottomLeft'
		if direction == (-1,1) or self.lastD == 'topLeft':
			self.triangle = ((self.pos[0]-23,self.pos[1]+23), (self.pos[0]-15,self.pos[1]), (self.pos[0],self.pos[1]+15))
			self.lastD = 'topLeft'
		if direction == (0,1) or self.lastD == 'down':
			self.triangle = ((self.pos[0],self.pos[1]+30), (self.pos[0]-10,self.pos[1]+10), (self.pos[0]+10,self.pos[1]+10))
			self.lastD = 'down'
		if direction == (0,-1) or self.lastD == 'up':
			self.triangle = ((self.pos[0],self.pos[1]-30), (self.pos[0]-10,self.pos[1]-10), (self.pos[0]+10,self.pos[1]-10))
			self.lastD = 'up'
	
	def move(self):
		self.pos = (self.pos[0]+round(self.direction[0]*8), self.pos[1]+round(self.direction[1]*8))
		
		if self.direction == (1,0):
			self.triangle = ((self.pos[0]+30,self.pos[1]), (self.pos[0]+10,self.pos[1]-10), (self.pos[0]+10,self.pos[1]+10))
		
		if self.direction == (1,1):
			self.triangle = ((self.pos[0]+23,self.pos[1]+23), (self.pos[0]+15,self.pos[1]), (self.pos[0],self.pos[1]+15))
		
		if self.direction == (1,-1):
			self.triangle = ((self.pos[0]+23,self.pos[1]-23), (self.pos[0]+15,self.pos[1]), (self.pos[0],self.pos[1]-15))
			
		if self.direction == (-1,0):
			self.triangle = ((self.pos[0]-30,self.pos[1]), (self.pos[0]-10,self.pos[1]-10), (self.pos[0]-10,self.pos[1]+10))
			
		if self.direction == (-1,-1):
			self.triangle = ((self.pos[0]-23,self.pos[1]-23), (self.pos[0]-15,self.pos[1]), (self.pos[0],self.pos[1]-15))
			
		if self.direction == (-1,1):
			self.triangle = ((self.pos[0]-23,self.pos[1]+23), (self.pos[0]-15,self.pos[1]), (self.pos[0],self.pos[1]+15))
			
		if self.direction == (0,1):
			self.triangle = ((self.pos[0],self.pos[1]+30), (self.pos[0]-10,self.pos[1]+10), (self.pos[0]+10,self.pos[1]+10))
			
		if self.direction == (0,-1):
			self.triangle = ((self.pos[0],self.pos[1]-30), (self.pos[0]-10,self.pos[1]-10), (self.pos[0]+10,self.pos[1]-10))
			
	def update(self,surf,direction):
		if not self.fired:
			self.aim(direction)
			if self.charging:
				self.charge +=.01
		if self.fired:
			if self.direction == (0,0):
				self.fired = False		
			self.move()
			self.mFrames -=1
			if self.mFrames <= 0:
				self.pos = self.oPos
				self.mFrames = 130 
				self.fired = False
			
		self.draw(surf)
		
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	quiver = []
	fired = []
	i=5
	while i > 0:
		quiver.append(Arrow((600,250)))
		i-=1
		
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
			if event.type == JOYBUTTONDOWN:
				if event.button == 7 and len(quiver) > 1:
					quiver[0].charging = True
					
			if event.type == JOYBUTTONUP:
				if event.button == 7 and len(quiver) > 1:
					quiver[0].fired = True
					fired.append(quiver.pop(0))	
					
		xAx = controller.get_axis(2)
		yAx = controller.get_axis(3)
		
		print(quiver[0].charge)
		
		windowSurf.fill((0,0,0))

		for a in quiver:
			a.update(windowSurf,(xAx,yAx))
		for a in fired:
			a.update(windowSurf,(xAx,yAx))
			if not a.fired:
				a.charging = False
				a.charge = 0
				a.pos = quiver[0].pos
				quiver.append(fired.pop(0))
		pygame.display.flip()
		fpsClock.tick(60)	
#test()

