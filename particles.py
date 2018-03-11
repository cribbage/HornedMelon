import pygame, math, sys, random
from pygame.locals import *
from enemy import *
from Player import *
from hud import*

pygame.display.init()
resolution = pygame.display.Info()
WINDOWSIZE = (2400, 1248)

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
	
	def __init__(self,size, pos, maxLife, maxVel, gravity):
		self.size = random.randint(0,size)
		self.pos = pos
		self.maxLife = maxLife
		self.xVel = 0
		self.yVel = 0	
		self.remove = False
		self.fired = False
		
	def move(self, gravity, velocity):
		self.maxLife -= 1		
		if self.maxLife > 1:
			self.yVel += velocity
			self.xVel += gravity
			if self.yVel != 0 or self.xVel != 0:
				self.fired = True
			self.pos = (self.pos[0]+round(self.xVel), (self.pos[1]+round(self.yVel)))
		else:
			self.remove = True
	
	def collideWall(self):
		if self.pos[0]-self.size <= 0:
	#		self.pos = (0,self.pos[1])
			self.xVel = -self.xVel
			
		if self.pos[1]-self.size <= 0:
	#		self.pos = (self.pos[0],0)
			self.yVel = -self.yVel	
			
		if self.pos[0]+self.size >=WINDOWSIZE[0]:
	#		self.pos = (WINDOWSIZE[0],self.pos[1])
			self.xVel = -self.xVel
			
		if self.pos[1]+self.size >= WINDOWSIZE[1]:
	#		self.pos = (self.pos[0],WINDOWSIZE[1])
			self.yVel = -self.yVel	
			
			
	def collideTarget(self,targets,pList,hud,levelPos):
		for target in targets:
			if type(target) == player:
				x = -levelPos[0]
				y = -levelPos[1]
				rect = Rect((0,0),target.size)
				rect.center = (target.rect.center[0]+x,target.rect.center[1]+y)	
				if rect.collidepoint(self.pos):
					if self in pList:
						pList.remove(self)
						target.stats = {'hp':str(target.health)+ "/" + str(target.mHealth), 'str':target.strg, 'agl':target.agl, 'def':target.dfen, 'MP':target.luck, 'hun':target.hunger, 'foc':target.foc}
						hud.updateStats(target)
					target.health -= 1	
			elif target.rect.collidepoint(self.pos):
				if self in pList:
					pList.remove(self)
				target.health -= 1
				target.hitTimer = 1
				
	#				pygame.draw.rect(target.surf,(random.randint(233, 255),random.randint(0, 165),0), (0,0,target.size[0],target.size[1]))
				burn = Rect((random.randint(5,target.size[0])-5,random.randint(5,target.size[1])-5, random.randint(0,5),random.randint(0,5)))
				pygame.draw.rect(target.burnSurf,(0,0,0),burn,0)
			
					
				#	target.surf.blit(burn,(random.randint(5,target.size[0])-5,random.randint(5,target.size[1])-5))
			if target.health <=0:
				target.alive = False
											
	def update(self,gravity, windowSurf, maxVel, targets,pList,hud,levelPos):
		self.move(gravity, maxVel)
		self.collideWall()
		if (gravity,maxVel) == (0,0) or (gravity,maxVel) == (-3.0517578125e-05,-3.0517578125e-05) :
			self.fired = False
		if self.fired:
			self.collideTarget(targets,pList,hud,levelPos)
	#	self.cir = pygame.draw.circle(windowSurf, (0,120,150), self.pos, self.size, 0)
	#	self.cir = pygame.draw.circle(windowSurf, (random.randint(self.rMin, self.rMin+155),random.randint(self.gMin, self.gMin+55),random.randint(self.bMin, self.bMin+105)), self.pos, self.size, 0)
	#	self.cir = pygame.draw.circle(windowSurf, (0,random.randint(100, 150),random.randint(110, 160)), self.pos, self.size, 0)#WATER
		self.cir = pygame.draw.circle(windowSurf, (random.randint(233, 255),random.randint(0, 165),0), self.pos, self.size, 0)#LAVA
		
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
		
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
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

