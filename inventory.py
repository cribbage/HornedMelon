import pygame, math, sys, random, time, copy
from pygame.locals import *
#from objects import potion
#from cursor import cursor

class inventory:
	def __init__(self,pos, windowSize):
		self.pos = pos
		self.surfSize = (round(windowSize[0])*.24,round(windowSize[1]*.16))
		self.rect = Rect(self.pos,self.surfSize)
		self.surf = pygame.Surface(self.surfSize)
		self.items = []
		self.slotSize = (round(windowSize[0]*.026),round(windowSize[1]*.053))
		self.nextEmpty = (0,0)
		self.inventory = {}
		self.full = False
		self.selection = 0
		self.sSelection = 0
		self.data = self.inventory
		self.itemData = []
		
	def addItem(self,item):
		pygame.mixer.Sound('sounds/pickUpItem.wav').play()
		self.inventory[self.nextEmpty] = item
		self.nextEmpty = (self.nextEmpty[0]+self.slotSize[0],self.nextEmpty[1])		
		while self.nextEmpty in self.inventory and type(self.inventory[self.nextEmpty]) != pygame.Surface:
			self.nextEmpty = (self.nextEmpty[0]+self.slotSize[0],self.nextEmpty[1])		
		if self.nextEmpty[0] > (self.surfSize[0] - self.slotSize[0]):
			self.nextEmpty = (0,self.nextEmpty[1]+self.slotSize[1])
			if self.nextEmpty[1] > self.surfSize[1] - self.slotSize[1]:
				self.full = True
		self.itemData.append(item)
		
	def findNextEmpty(self):
		for c in self.inventory:
			if type(self.inventory[c]) == pygame.Surface:
				self.nextEmpty = c
				return
		
	def drawInventory(self):
		self.surf.fill((0,0,0))
		for coord in self.inventory:
			if type(self.inventory[coord]) != pygame.Surface:
				self.surf.blit(self.inventory[coord].surf,coord)
		
	def selected(self,cursor,surf):#Get selection and draw rectangle around selection
		x = (((cursor.pos[0]-self.pos[0])//self.slotSize[0])*self.slotSize[0])
		y = (((cursor.pos[1]-self.pos[1])//self.slotSize[1])*self.slotSize[1])
		pygame.draw.rect(self.surf,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),((x,y),self.slotSize),1)
		self.selection = (x,y)
	
	def moveItem(self,cursor,surf):
		self.surf.blit(self.inventory[self.selection].surf,(cursor.pos[0]-self.pos[0],cursor.pos[1]-self.pos[1]))
	
	def selectSpot(self, cursor):
		x = (((cursor.pos[0]-self.pos[0])//self.slotSize[0])*self.slotSize[0])
		y = (((cursor.pos[1]-self.pos[1])//self.slotSize[1])*self.slotSize[1])
		pygame.draw.rect(self.surf,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),((x,y),self.slotSize),1)
		self.sSelection = (x,y)
		if self.sSelection in self.inventory:
			self.items = [copy.copy(self.inventory[self.selection]),copy.copy(self.inventory[self.sSelection])]
		else:
			empty = pygame.Surface(self.slotSize)
			self.inventory[(self.sSelection)] = empty
	
	def replaceItem(self,cursor):		
		if cursor.rect.colliderect(self.rect) and self.sSelection != pygame.Surface:
			pygame.mixer.Sound('sounds/switchItem.wav').play()
			self.inventory[(self.sSelection)] = self.items[0]
			self.inventory[(self.selection)] = self.items[1]
		elif cursor.rect.colliderect(self.rect) and self.sSelection == pygame.Surface:
			pygame.mixer.Sound('sounds/switchItem.wav').play()
			self.mextEmpty = self.sSelection
			self.inventory[(self.selection)] = self.items[1]
		elif not cursor.rect.colliderect(self.rect):
			self.removeItem('sounds/dropItem.wav')
		self.items = []
	
	def removeItem(self,s):
		pygame.mixer.Sound(s).play()
		empty = pygame.Surface(self.slotSize)
		self.inventory[(self.selection)] = empty
					
	def update(self,item,cursor,surf,player,hud,activeScrolls):
		self.drawInventory()
		self.findNextEmpty()
		if not cursor.clicked:
			if len(self.items) != 0:
				if self.selection != self.sSelection:
					self.replaceItem(cursor)
				else:
					self.inventory[self.selection].consume(player,hud,self,cursor,activeScrolls)
					self.items = []
				#	return activeScrolls
			self.selected(cursor,surf)
		if cursor.clicked and self.rect.collidepoint(cursor.pos) and self.selection in self.inventory and type(self.inventory[self.selection]) != pygame.Surface:
			self.moveItem(cursor,surf)
			self.selectSpot(cursor)
			
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	c = cursor()
	pot = inventory((100,100))
	otion = potion((100,0,0))
	otion2 = potion((0,0,100))
	potions = (otion,otion2)
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
				if event.button == 2:
					c.clicked = True
			if event.type == JOYBUTTONUP:
				if event.button == 2:
					c.clicked = False
		
			
		windowSurf.fill((100,100,100))
		pot.update(random.choice(potions),c,windowSurf)	
		windowSurf.blit(pot.surf,pot.pos)
		cd = (controller.get_axis(0),controller.get_axis(1))	
		if cd != (0,0):
			c.update(cd,windowSurf)
		pygame.display.flip()
		fpsClock.tick(60)	
#test()
