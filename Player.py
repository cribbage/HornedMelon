import pygame, math, sys, random, particles, enemy, os
from pygame.locals import *
from save import *

class player:
	def __init__(self, pos, wallRects,windowSize):
		global BUTTONS
		BUTTONS = Save([],'controls.txt').load(int)
		self.pos = pos
		self.color = (111,0,0)
		self.windowSize = windowSize
		self.size =(random.randint(15,30), random.randint(15,30))
		self.ssp = random.randint(random.randint(0,11),random.randint(11,21))#starting skill points (spend them on skills)
		self.health = random.randint(10,25)#health
		self.mHealth = self.health#max health
		self.strg = random.randint(1,15)#strength(for swords)
		self.foc = random.randint(2,15)#focus(for magic)
		self.agl = random.randint(1,15)#agility(for bows)
		self.dfen = random.randint(1,15)#defence
		self.luck = random.randint(10,25)#luck(for finding items and affects enemy damage)
		self.mLuck = self.luck
		self.hunger = random.randint(10,35)#eat or pass out
		self.stats = {'hp':str(self.health)+ "/" + str(self.mHealth), 'str':self.strg, 'agl':self.agl, 'def':self.dfen, 'MP':self.luck, 'hun':self.hunger, 'foc':self.foc}
		self.mIntensity = random.randint(1,self.foc)#magic intensity
		self.x = 0#velocity
		self.y = 0#velocity
		self.mAttack = False
		self.rAttack = False
		self.sAttack = False
		self.direction = [0,0]
		self.particles = []
		self.atypes = ['magic', 'sword']
		self.atype = 'magic'
		self.alive = True
		self.quiver = []
		self.fired = []
		self.ROR = (self.pos[0] - round(windowSize[0]/2), self.pos[1] - round((windowSize[1]/2)-(windowSize[1]*.08)))
		self.data = (int(self.pos[0]//self.pos[0]),self.pos[1],self.size[0],self.size[1],self.health,self.mHealth,self.strg,self.foc,self.agl,self.dfen,self.luck,self.hunger,self.mIntensity)
		self.rect = Rect(self.pos[0], self.pos[1],self.size[0], self.size[1])
		self.stoned = random.choice([True, False])
		self.hitTimer = 0
		self.speed = 3
		
	def drawFace(self,surf,windowSize):
		if self.stoned:
			pygame.draw.circle(surf, (255,0,0), (int(windowSize[0]//2)+random.randint(0,5),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))+random.randint(0,5)), 3, 0)#LEFT EYE
			pygame.draw.circle(surf, (255,0,0), (int(windowSize[0]//2)+random.randint(self.size[0]-5,self.size[0]),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))+random.randint(0,5)), 3, 0)#RIGHT EYE
		else:
			pygame.draw.circle(surf, (255,255,255), (int(windowSize[0]//2)+random.randint(0,5),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))+random.randint(0,5)), 3, 0)#LEFT EYE
			pygame.draw.circle(surf, (255,255,255), (int(windowSize[0]//2)+random.randint(self.size[0]-5,self.size[0]),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))+random.randint(0,5)), 3, 0)#RIGHT EYE
		pygame.draw.circle(surf, (0,0,0), (int(windowSize[0]//2)+random.randint(0,5),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))+random.randint(0,5)), 2, 0)
		pygame.draw.circle(surf, (0,0,0), (int(windowSize[0]//2)+random.randint(self.size[0]-5,self.size[0]),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))+random.randint(0,5)), 2, 0)
		mouthStart = random.randint(-2,2)
		pygame.draw.arc(surf,(255,0,0), self.rect,-2,-1, 1)#MOUTH

	def collideItem(self,item, invent, itemlist):
		if item.rect.collidepoint(self.pos)or item.rect.collidepoint(((self.pos[0]+self.size[0]),self.pos[1])) or item.rect.collidepoint(((self.pos[0]+self.size[0]),(self.pos[1]+self.size[1]))) or item.rect.collidepoint((self.pos[0],(self.pos[1]+self.size[1]))):
			if not invent.full:		
				invent.addItem(item)		
				itemlist.remove(item)
				
	def loadData(self):
		saveData = Save([],'playerData.txt')
		saveData.load(int)	
		self.data = saveData.data
		print(self.data)
		self.fillData()
			
	def fillData(self):
		self.pos=(self.windowSize[0]/2,round((self.windowSize[1]/2)-(self.windowSize[1]*.08)))
		self.size =(self.data[2], self.data[3])
		self.health = self.data[4]#health
		self.mHealth = self.data[5]#max health
		self.strg = self.data[6]#strength(for swords)
		self.foc = self.data[7]#focus(for magic)
		self.agl = self.data[8]#agility(for bows)
		self.dfen = self.data[9]#defence
		self.luck = self.data[10]#luck(for finding items and affects enemy damage)
		self.hunger = self.data[11]#eat or pass out
		self.mIntensity = self.data[12]	
		self.stats = {'hp':str(self.health)+ "/" + str(self.mHealth), 'str':self.strg, 'agl':self.agl, 'def':self.dfen, 'MP':self.luck, 'hun':self.hunger, 'foc':self.foc}
				
	def move(self,dpad):
		self.x = dpad[0]*self.speed
		self.y = -dpad[1]*self.speed
	
	def getInput(self,event, fireSound):
		if event.type == JOYBUTTONDOWN:
			if event.button == BUTTONS[3]:
				if self.atype == 'magic':
					fireSound.play()
					self.mAttack = True	
				elif self.atype =='sword':
					self.sAttack = True
			elif event.button == BUTTONS[5]:
				if self.atypes.index(self.atype) >  0:
					self.atype = self.atypes[(self.atypes.index(self.atype))-1]
				else:
					self.atype = self.atypes[len(self.atypes)-1]	
		if event.type == JOYBUTTONUP:
			if event.button == BUTTONS[3]:	
				if self.atype == 'magic':
					fireSound.stop()
					self.mAttack = False		
				elif self.atype =='sword':
					self.sAttack = False	
		
	def update(self, events, keysPressed, wallRects, dpad, cAxis, surf, windowSize, fireSound,fps):		
	#	self.speed = (60//fps)*3					
		for event in events:
			self.move(dpad)
			self.getInput(event, fireSound)
		self.direction = (cAxis[0],cAxis[1])
		
		self.pos = (self.pos[0]+self.x, self.pos[1]+self.y)	
		self.rect = Rect(windowSize[0]/2,round((windowSize[1]/2)-(windowSize[1]*.08)),self.size[0], self.size[1])
