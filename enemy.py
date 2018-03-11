import pygame, math, sys, random, particles
from pygame.locals import *
from pathfinderBU import pathFinder

class enemy:
	def __init__(self, pos, wallRects, windowSize):
		self.windowSize = windowSize#LEVELSIZE (TOO LAZY TO CHANGE RIGHT NOW)
		self.pos = pos
		self.size = (random.randint(10,30), random.randint(5,30))
		self.surf = pygame.Surface(self.size)
		self.burnSurf = pygame.Surface(self.size).convert_alpha()
		self.burnSurf.fill((0,0,0,0))
		self.rect = Rect(0, 0,self.size[0], self.size[1])
		pygame.draw.rect(self.surf,(111,111,0), self.rect, 0)
		self.health = random.randint(50,100)#health
		self.maxHealth = self.health
		self.strg = random.randint(1,15)#strength(for swords)
		self.foc = random.randint(2,8)#focus(for magic)
		self.agl = random.randint(1,15)#agility(for bows)
		self.dfen = random.randint(1,15)#defence
		self.mIntensity = random.randint(1,self.foc)#magic intensity
		self.mana = self.foc
		self.x = 0#velocity
		self.y = 0#velocity
		self.mAttack = False
		self.direction = [0,0]
		self.particles = []
		self.opp = 'x'
		self.alive = True
		self.steps = 30
		self.hitTimer = 0
		self.iB= 'none'
		self.bump = False
		self.first = self.getName("first.txt")
		self.last = self.getName("last.txt")
		self.path = []
		self.lastPos = self.pos
		
	def getName(self, nameFile):
		i = random.randint(0,20)
		f = open(nameFile, "r")
		name = ''
		while i > -1:
			name = f.readline()
			i-=1
		f.close()
		return str(name).rstrip()

	def drawHPI(self, surf):
		hpIndicator = Rect(self.rect.center[0]-50,self.pos[1]-15,round((self.health/self.maxHealth * 100)),10)
		negHPI = Rect(self.rect.center[0]-50,self.pos[1]-15,(100-(hpIndicator.right-hpIndicator.left)),10)	
		negHPI.topleft = hpIndicator.topright	
		pygame.draw.rect(surf,(0,150,0),hpIndicator,0)
		pygame.draw.rect(surf,(150,0,0),negHPI,0)
					
	def attack(self, playerPos):
		xDiff = self.rect.center[0] - playerPos[0]
		yDiff = self.rect.center[1] - playerPos[1]
		distance = ((self.rect.center[0] - playerPos[0])**2 + (self.rect.center[1] - playerPos[1])**2)**0.5
		if distance != 0:
			x = xDiff/distance
			y = yDiff/distance
			self.direction = (-x, -y)
	
	def isWaterBetween(self,wallRects,playerPos,xDiff,yDiff,levelPos):
		if playerPos[0] >= self.pos[0]:
			left = self.rect.right
		elif playerPos[0] < self.pos[0]:
			left = playerPos[0]
		if playerPos[1] >= self.pos[1]:
			top = self.rect.bottom
		elif playerPos[1] < self.pos[1]:
			top = playerPos[1]		
		checkRect = (left,top,xDiff,yDiff)
		x = int(math.ceil((self.pos[0]-200) / 100)) * 100
		y = int(math.ceil((self.pos[1]-100) / 96)) * 96	
		while x <= (self.pos[0] + 200) and y <= self.pos[1]+100:	
			if(x,y) in wallRects:		
				rect = Rect(x,y,100, 96)
				if rect.colliderect(checkRect):
					selfX = int(math.ceil((self.pos[0]-100) / 100)) * 100
					selfY = int(math.ceil((self.pos[1]-96) / 96)) * 96
					pX = int(math.ceil((playerPos[0]-100) / 100)) * 100
					pY = int(math.ceil((playerPos[1]-96) / 96)) * 96
					findPath = pathFinder((selfX,selfY),(pX,pY),wallRects)
					self.path = findPath.path
					print("PPATH:")
					print(self.path)									
			x+=100
			if x >= self.pos[0]+100:
				x = int(math.ceil((self.pos[0]-200) / 100)) * 100
				y+= 96
		
	def move(self, wallRects, playerPos, pathPos,levelPos):
		moves = [-2,0,2]
		self.x = moves[random.randint(-2,2)]
		self.y = moves[random.randint(-2,2)]
		xDiff = playerPos[0] - self.pos[0]
		yDiff = playerPos[1] - self.pos[1]
		if self.pos[0] > playerPos[0]:
			xDiff = self.pos[0] - playerPos[0]	
		if self.pos[1] > playerPos[1]:
			yDiff = self.pos[1] - playerPos[1]		
		pxDiff = pathPos[0] - self.pos[0]
		pyDiff = pathPos[1] - self.pos[1]
		if self.pos[0] > pathPos[0]:
			pxDiff = self.pos[0] - pathPos[0]	
		if self.pos[1] > playerPos[1]:
			pyDiff = self.pos[1] - pathPos[1]			
		
		if xDiff < 150 and yDiff< 150 and len(self.path) == 0:			
			self.isWaterBetween(wallRects,playerPos, xDiff, yDiff,levelPos)
			if playerPos[0] > self.pos[0]:
				self.x = 2
			elif playerPos[0] < self.pos[0]:
				self.x = -2
			if playerPos[1] > self.pos[1]:
				self.y = 2
			elif playerPos[1] < self.pos[1]:
				self.y = -2
				
		elif len(self.path) != 0:					
			if pathPos[0] > self.pos[0]:
				self.x = 2
			elif pathPos[0] < self.pos[0]:
				self.x = -2
			if pathPos[1] > self.pos[1]:
				self.y = 2
			elif pathPos[1] < self.pos[1]:
				self.y = -2
				
		if xDiff < 60 and xDiff >=0 and yDiff < 60 and yDiff >=0 and len(self.path) == 0:
			self.x=0
			self.y=0
		elif pxDiff < 40 and pxDiff >=0 and pyDiff < 40 and pyDiff >=0 and len(self.path) != 0:
			if len(self.path) == 1:
				self.path = []
			else:
				self.path.remove(self.path[0])	
					
		if self.mana > 0 and xDiff < 200 and yDiff < 200:
			self.mana -=35
			self.attack(playerPos)
			self.mAttack = True		
		else:
			self.mAttack = False
			
			if self.mana < self.foc:
				self.mana += 3
					
	def update(self, playerPos, surf, wallrects, windowSize, wallCoords,levelPos):
		if self.steps <= 0 and len(self.path) == 0:
			print("HOLY GOD")
			self.move(wallCoords, playerPos, (0,0),levelPos)
			self.steps = random.randint(1,30)
		elif len(self.path) != 0:
			point = self.path[0]
			self.move(wallCoords,playerPos,(point[0]+50, point[1]+48),levelPos)
		if self.pos == self.lastPos:
			self.path = []
		self.lastPos = self.pos	
		self.steps-=1	
		self.pos = (self.pos[0]+self.x, self.pos[1]+self.y)
		self.rect = Rect(self.pos[0], self.pos[1],self.size[0], self.size[1])
		self.surf.blit(self.burnSurf,(0,0))
		surf.blit(self.surf,self.pos)
		if self.hitTimer > 0:
			self.drawHPI(surf)
			self.hitTimer -= .01
