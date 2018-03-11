import pygame, math, sys, random, time, random,copy,gc
from save import Save
from pygame.locals import *
pygame.init()
resolution = pygame.display.Info()
WINDOWSIZE = (1200,600)
MENUSIZE = (round(WINDOWSIZE[0]*.25),WINDOWSIZE[1])
ANTSIZE = (2,2)
NODESIZE = (2,2)
GRIDSIZE = (2400,1248)
ANTS = 25
ORIGINSIZE = (1,1)
ORIGINCENTER = (GRIDSIZE[0]//2,GRIDSIZE[1]//2)
OFFSET =3
GREEN = (0,255,0)
BLOOD = []
PULSERATE = 15
PULSECYCLES = 3
ENDFLOWTIME = PULSECYCLES*PULSERATE
FLOWS = 1

while len(BLOOD) < 30:
	shade = (random.randint(0,255),0,0)
	if shade not in BLOOD:
		BLOOD.append(shade)		
BLACK = (0,0,0)
RED = (45,0,0)
BLUE = (0,0,255)
GRAY = (50,50,50)



class Menu:
	def __init__(self):
		self.surf = pygame.Surface(MENUSIZE)
		self.font = pygame.font.Font('freesansbold.ttf', 20)	
		self.statFontObjs = []
		self.statFontObjsO = []
		self.grids = {}
		self.displayValues()
			
	def displayValues(self):
		self.surf.fill(GRAY)
		nodeSize = self.font.render("NODE_SIZE = " + str(NODESIZE), True, (255,255,255))
		gridSize = self.font.render("GRID_SIZE = " + str(GRIDSIZE), True, (255,255,255))
		ants = self.font.render("ANTS = " + str(ANTS), True, (255,255,255))
		offset = self.font.render("OFFSET = " + str(OFFSET), True, (255,255,255))
		pulseRate = self.font.render("PULSE_RATE = " + str(PULSERATE), True, (255,255,255))
		pulseCycles = self.font.render("PULSE_CYLCES = " + str(PULSECYCLES), True, (255,255,255))
		originSize = self.font.render("ORIGIN = " + str(ORIGINSIZE), True, (255,255,255))
		flows = self.font.render("FLOWS = " + str(FLOWS), True, (255,255,255))
		values = [nodeSize,gridSize,ants,offset,pulseRate,pulseCycles,originSize,flows]
		
		y = 0	
		for value in values:
			value.get_rect(topleft=(0,0))
			self.surf.blit(value, (0, y))
			y += 75

class Node:
	def __init__(self,pos):
		self.pos = pos
		self.color = BLACK
		
class Grid:
	def __init__(self):
		self.surf = pygame.Surface(GRIDSIZE).convert_alpha()
		self.surf.set_colorkey((0,0,0,0))
		self.surf.fill((0,0,0,0))
		self.nodes = {}
				
	def redrawNode(self,coords,c):
		self.nodes[coords].color = c
		pygame.draw.rect(self.surf,self.nodes[coords].color,(coords[0],coords[1],NODESIZE[0],NODESIZE[1]),0)

class Ant:
	def __init__(self,option,originArea):
		self.originArea = originArea
		self.option = 1
		if self.option == 1:
			self.pos = (random.randrange(int(self.originArea[0])-ORIGINSIZE[0],int(self.originArea[0])+ORIGINSIZE[0],5),random.randrange(int(self.originArea[1])-ORIGINSIZE[1],int(self.originArea[1])+ORIGINSIZE[1],5))
		elif self.option == 0: 			
			self.pos = (random.randrange(0,GRIDSIZE[0]-NODESIZE[0],5),random.randrange(0,GRIDSIZE[0]-NODESIZE[0],5))
		self.color = random.choice([RED,BLUE])
		self.rect =(self.pos[0],self.pos[1],ANTSIZE[0],ANTSIZE[1])
		self.lastColor = BLACK
		self.blood = 0
		self.direction = 'whey'
		self.rMove = ['UP','LEFT','DOWN','RIGHT']
		self.bMove = ['DOWN','LEFT','UP','RIGHT']
		self.movement = 0
		self.pulse = PULSERATE
		self.life = ENDFLOWTIME
		
	def pulsate(self):
		if self.pulse == 0:
			if self.option == 1:
				self.pos = self.pos = (random.randrange(int(self.originArea[0])-ORIGINSIZE[0],int(self.originArea[0])+ORIGINSIZE[0],5),random.randrange(int(self.originArea[1])-ORIGINSIZE[1],int(self.originArea[1])+ORIGINSIZE[1],5))
			elif self.option == 0: 			
				self.pos = (random.randrange(0,GRIDSIZE[0]-NODESIZE[0],5),random.randrange(0,GRIDSIZE[0]-NODESIZE[0],5))
			self.pulse = PULSERATE + 1
		self.pulse -= 1
		self.life -= 1
		
	def drawAnt(self,surface):
		self.rect =(self.pos[0],self.pos[1],ANTSIZE[0],ANTSIZE[1])
		pygame.draw.rect(surface,self.color,self.rect,0)
		
	def getDirection(self,grid):
		try:
			if grid.nodes[self.pos] not in grid.nodes:
				pass
		except:
			grid.nodes[self.pos] = Node(self.pos)
		
		if grid.nodes[self.pos].color != self.lastColor:
			if self.color == RED and self.movement == 3:
				if grid.nodes[self.pos].color == BLACK or grid.nodes[self.pos].color == BLUE:
					self.direction = 'LEFT'
				else:
					self.direction = 'RIGHT'
		
			elif self.color == BLUE and self.movement == 3:
				if grid.nodes[self.pos].color == BLACK or grid.nodes[self.pos].color == BLUE:
					self.direction = 'RIGHT'
				else:
					self.direction = 'LEFT'
			self.movement = 0
		else:
			if self.color == RED:
				self.direction = self.rMove[self.movement]
			else:
				self.direction = self.bMove[self.movement]
				
		self.lastColor = grid.nodes[self.pos].color
		
		if grid.nodes[self.pos].color == BLACK or grid.nodes[self.pos].color == RED:
			grid.redrawNode(self.pos,(random.randint(0, 150),0,0))

		else:
			grid.redrawNode(self.pos,RED)
		self.movement +=1
		if self.movement > 3:
			self.movement = 0	
				
	def move(self):
		if self.direction == 'RIGHT':
			self.pos = (self.pos[0]+(NODESIZE[0]*random.randint(1,OFFSET)),self.pos[1])
			if self.pos[0] >= GRIDSIZE[0]:
				self.pos = (0,self.pos[1])
				self.blood += 1
		elif self.direction == 'UP':	
			self.pos = (self.pos[0],self.pos[1]-(NODESIZE[1]*random.randint(1,OFFSET)))
			if self.pos[1] <= 0:
				self.blood += 1
				self.pos = (self.pos[0],GRIDSIZE[1] - (NODESIZE[1]*random.randint(1,OFFSET)))
					
		elif self.direction == 'LEFT':
			self.pos = (self.pos[0] - (NODESIZE[0]*random.randint(1,OFFSET)),self.pos[1])
			if self.pos[0] <= 0:
				self.blood += 1
				self.pos = (GRIDSIZE[0] - (NODESIZE[0]*random.randint(1,OFFSET)),self.pos[1])
		elif self.direction == 'DOWN':	
			self.pos = (self.pos[0],self.pos[1]+(NODESIZE[1]*random.randint(1,OFFSET)))
			if self.pos[1] >= GRIDSIZE[1]:
				self.blood += 1
				self.pos = (self.pos[0],0)
		if self.blood >= len(BLOOD)-1:
			self.blood = 0
	
	
	def update(self,grid):
		self.getDirection(grid)
		self.move()
		self.pulsate()
	#	self.drawAnt(grid.surf)


def test(choice,grid,ants,i,windowSurf,fpsClock,menu):
	global NODESIZE,ANTS,GRIDSIZE,OFFSET,PULSERATE,PULSECYCLES,ENDFLOWTIME,ORIGINSIZE,FLOWS
	
	while i >0:
		ants.append(Ant(choice,ORIGINCENTER))
		i -= 1
	
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				FLOWS += 1
				menu.displayValues()
				mInput = pygame.mouse.get_pos()
				i = ANTS
				while i >0:
					ants.append(Ant(choice,(mInput[0]-300,mInput[1])))
					i -= 1		
			if event.type == KEYDOWN:				
				if event.key == K_q:
					if NODESIZE[0] > 1:
						NODESIZE = (NODESIZE[0]-1,NODESIZE[1]-1)
						menu.displayValues()
				if event.key == K_w:
					NODESIZE = (NODESIZE[0]+1,NODESIZE[1]+1)
					menu.displayValues()
				if event.key == K_a:
					if PULSECYCLES > 1:
						PULSECYCLES -= 1						
						menu.displayValues()
						ENDFLOWTIME = PULSECYCLES*PULSERATE
				if event.key == K_s:
					PULSECYCLES += 1
					ENDFLOWTIME = PULSECYCLES*PULSERATE
					menu.displayValues()		
				if event.key == K_z:
					if ANTS> 1:
						ANTS -= 1						
						menu.displayValues()
				if event.key == K_x:
					ANTS += 1
					menu.displayValues()			
				if event.key == K_e:
					if OFFSET> 1:
						OFFSET -= 1						
						menu.displayValues()
				if event.key == K_r:
					OFFSET += 1
					menu.displayValues()
				if event.key == K_c:
					if PULSERATE> 1:
						PULSERATE -= 1						
						menu.displayValues()
				if event.key == K_v:
					PULSERATE += 1
					menu.displayValues()
				if event.key == K_t:
					if ORIGINSIZE[0]> 1:
						ORIGINSIZE = (ORIGINSIZE[0]-1,ORIGINSIZE[1])						
						menu.displayValues()
				if event.key == K_y:
					ORIGINSIZE = (ORIGINSIZE[0]+1,ORIGINSIZE[1])	
					menu.displayValues()
				if event.key == K_g:
					if ORIGINSIZE[1]> 1:
						ORIGINSIZE = (ORIGINSIZE[0],ORIGINSIZE[1]-1)						
						menu.displayValues()
				if event.key == K_h:
					ORIGINSIZE = (ORIGINSIZE[0],ORIGINSIZE[1]+1)	
					menu.displayValues()
				if event.key == K_SPACE:
					
					grid.nodes = {}
					
					ants = []
					return 
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
					
		windowSurf.fill((0,0,0))

		for ant in ants:
			ant.update(grid)
			if ant.life <= 0:
				ants.remove(ant)
				
		windowSurf.blit(grid.surf,(MENUSIZE[0],0))
		
		windowSurf.blit(menu.surf,(0,0))
		pygame.display.flip()
		fpsClock.tick(60)
		
#fpsClock = pygame.time.Clock()
#windowSurf = pygame.display.set_mode(WINDOWSIZE)	

#while True:		
#	FLOWS = 1
#	test(random.choice((0,1)),Grid(),[],ANTS,windowSurf,fpsClock,Menu())
