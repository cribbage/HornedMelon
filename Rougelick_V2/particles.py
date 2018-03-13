#!/usr/bin/env python
import pygame, math, sys, random
from pygame.locals import *
from globalVars import *
from math import*

def displayValues(size, maxLife, intensity, gravity, maxVel, offset, particles,fps, windowSurf):
	font = pygame.font.Font('freesansbold.ttf', 25)	
	size = font.render("(q,w) SIZE = " + str(size), True, (255,255,255))
	maxlife = font.render("(a,s) MAXLIFE = " + str(maxLife),True,(255,255,255))
	intensity = font.render("(z,x) INTENSITY = " + str(intensity), True, (255,255,255))
	gravity = font.render("(e,r) GRAVITY = " + str(gravity), True, (255,255,255))
	maxvel = font.render("(d,f) MAXVEL = " + str(maxVel), True, (255,255,255))
	offsetval = font.render("(c,v) OFFSET = " + str(offset), True, (255,255,255))
	pAmount = font.render("(t) PARTICLES = " + str(len(particles)), True, (255,255,255))
	fps = font.render("FPS = " + str(fps), True, (255,255,255))

	values = [size,maxlife,intensity, gravity, maxvel, offsetval, pAmount,fps]
	
	y = 0	
	for value in values:
		value.get_rect(topleft=(0,0))
		windowSurf.blit(value, (0, y))
		y += 25

class Particle:
	
	def __init__(self,size, pos, maxLife, xDest, yDest,speed):
		self.size = random.randint(2,size)
		self.pos = pos
		self.maxLife = maxLife
		angle = self.getAngle(xDest,yDest)
		self.xVel = angle[0]*speed
		self.yVel = angle[1]*speed
		self.remove = False
		
		
	def getAngle(self,xDest,yDest):
		dx = xDest - self.pos[0]
		dy = yDest - self.pos[1]
		dist = math.sqrt((xDest-self.pos[0])**2 + (yDest-self.pos[1])**2)
		xDiff = dx/dist
		yDiff = dy/dist
		return (xDiff,yDiff)
		
	def move(self):
		self.maxLife -= 1		
		if self.maxLife > 1:
			self.pos = (self.pos[0]+round(self.xVel), (self.pos[1]+round(self.yVel)))
		else:
			self.remove = True
	
	def collideWall(self):
		if self.pos[0]-self.size <= 0:
			self.xVel = -self.xVel			
		if self.pos[1]-self.size <= 0:
			self.yVel = -self.yVel			
		if self.pos[0]+self.size >=WINDOWSIZE[0]:
			self.xVel = -self.xVel		
		if self.pos[1]+self.size >= WINDOWSIZE[1]:
			self.yVel = -self.yVel		
											
	def update(self,surf):
		self.move()
		self.collideWall()		
		self.cir = pygame.draw.circle(surf, (random.randint(233, 255),random.randint(0, 165),0), self.pos, self.size, 0)#LAVA
		
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	windowSurf = pygame.display.set_mode(WINDOWSIZE)
	size = 12
	maxLife = 26
	intensity = 1
	gravity = 1
	maxVel = 5
	offset = 10
	
	particles = []
	
	mbd = False
	
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				mbd = True
			if event.type == MOUSEBUTTONUP:
				mbd = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_t:
					particles = [] 
				if event.key == K_w:
					size += 1
				if event.key == K_q:
					if size > 0:
						size -= 1	
				if event.key == K_s:
					maxLife += 1
				if event.key == K_a:
					maxLife -= 1
				if event.key == K_x:
					intensity += 1
				if event.key == K_z:
					intensity -= 1	
				if event.key == K_r:
					gravity += 1
				if event.key == K_e:
					gravity -= 1
				if event.key == K_f:
					maxVel += 1
				if event.key == K_d:
					maxVel -= 1	
				if event.key == K_v:
					offset += 1
				if event.key == K_c:
					if offset > 0:
						offset -= 1
								
		if mbd:
			i = intensity
			
			while i > 0:
				xOffset = random.randint(-offset,offset)
				yOffset = random.randint(-offset,offset)
				mousePos = pygame.mouse.get_pos()
				newPPos = ((mousePos[0] + xOffset), (mousePos[1] + yOffset))
				newP = Particle(size, newPPos, maxLife, maxVel, gravity)	
				particles.append(newP)
				i -= 1
				
		windowSurf.fill((0,0,0))
		
		for p in particles:
			p.update(gravity, windowSurf, maxVel)	
			
			if p.remove:
				particles.remove(p)
					
		displayValues(size, maxLife, intensity, gravity, maxVel, offset, particles,fpsClock.get_fps(),windowSurf)
					
		pygame.display.flip()
		fpsClock.tick(60)

#test()

