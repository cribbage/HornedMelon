import pygame, math, sys, random, particles, enemy
from pygame.locals import *
from brickLayer import brick, brickLayer
from water import *
from save import *
from rug import Rug

class level:
	def __init__(self,levelSize, windowSize, rooms):
		self.levelSize = levelSize
		self.windowSize = windowSize
		self.surf = pygame.Surface(levelSize)
		self.waterSurf = waterLayer((100,96))
		self.rug = Rug((100,48))
		self.emptyCoords = []
		self.subSurfs = {}
		self.buildLevel(False)
		self.reloaded = False
		self.rooms = rooms
		self.time = 0
		self.data = (self.emptyCoords)

	def loadData(self):
		self.subSurfs = {}
		saveData = Save([],'levelData.txt')
		saveData.load(str)	
		self.data = saveData.data
		self.convertData()
		self.emptyCoords = self.data
		self.reloaded = True
		self.buildLevel(True)
	
	def convertData(self):
		tups = []
		for string in self.data:
			string.strip(" ")
			x = string.split(',')[0]
			y = string.split(',')[1]
			tups.append((int(x),int(y)))
		self.data = tups	
			
	def buildLevel(self, loading):
		self.drawFloor(loading,'empty',0,0,[],[],0,0,300)
		self.drawWater()
	
	def drawBrick(self,x,y,needFloorx,last,start):
		self.surf.blit(brickLayer((100,96)).surf,(x,y))
	#	self.surf.blit(self.rug.surf,(x,y+24))		
		if last =='full' and x in needFloorx:
			needFloorx.remove(x)		
		elif last == 'empty':
			last = 'full'
			start = x
		return(last,start,needFloorx)
	
	def skipTile(self,x,y,needFloorx,start,finish,last):
		self.emptyCoords.append((x,y))
		last ='empty'
		finsh = x 
		if finish <= start:
			nextX = start
		else:
			nextX = random.randrange(start,finish,100)
		needFloorx.append(nextX)
		return(last,finish,needFloorx)
		
	def drawFloor(self,loading,last,start,finish,needFloorx,needFloory,x,y,straight):
		while x <= self.levelSize[0] and y < self.levelSize[1]:	
			choice = random.randint(0,1)
			if loading:
				choice = 1
			if y == straight:
				choice =1
			if x in needFloorx or choice == 1:	
				last,start,needFloorx = self.drawBrick(x,y,needFloorx,last,start)										
			elif choice == 0:
				last,finish,needFloorx = self.skipTile(x,y,needFloorx,start,finish,last)
			x+=round(self.windowSize[0]*.083)
			if x == self.levelSize[0]:
				x =0
				y +=round(self.windowSize[1]*.16)
				
	def drawWater(self):
		for coords in self.emptyCoords:	
			self.subSurfs[coords] = Rect(coords,(100,96))				
			self.surf.blit(self.waterSurf.surfs[self.waterSurf.surfC],coords)
			
	def updateLevel(self,paused):
		if not paused:
			self.time += 1
			if self.time == 6:
				self.time = 0
				self.waterSurf.switchSurf()
				self.drawWater()

class Door:
	def __init__(self,surfSize):
		self.surf = pygame.Surface(surfSize).convert_alpha()	
		self.surf.fill((0,0,0,0))
		self.drawDoor()
		
	def drawDoor(self):
		pygame.draw.rect(self.surf, (139,69,19), (12,52,74,75),0)
		pygame.draw.ellipse(self.surf, (139,69,19), (12,12,75,75),0)
		pygame.draw.circle(self.surf, (255,215,0), (32,62), 6, 0)
		
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	levelSize = (2400, 1200)
	lvl = level(levelSize,windowSize,1)
	door = Door((100,96))
	
	time = 0
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
		windowSurf.fill((0,0,0))
		lvl.surf.blit(door.surf,(200,193))
		windowSurf.blit(lvl.surf,(0,0))
		
		lvl.updateLevel(time)
			
		time += 1
		if time > 6:
			time = 0		
		pygame.display.flip()
		fpsClock.tick(60)	
#test()
