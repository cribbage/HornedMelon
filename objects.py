import pygame, math, sys, random, time, ScrollSpell
from pygame.locals import *
from ScrollSpell import *

class potion:
	def __init__(self,color, windowSize):
		windowSize = (1200,600)
		self.pos = (random.randint(0,2300),random.randint(0,1100))
		self.size = (round(windowSize[0]*.023),round(windowSize[1]*.046))
		self.surfSize = (round(windowSize[0]*.023),round(windowSize[1]*.046))
		self.surf = pygame.Surface((28,28)).convert_alpha()
		self.surf.fill((0,0,0,0))
		self.healingPower = random.randint(0,255)
		self.manaPower = random.randint(0,255)
		self.color = (self.healingPower,0,self.manaPower)
		self.triangle = ((0,self.surfSize[1]),(self.surfSize[0],self.surfSize[1]),(round(self.surfSize[0]/2),round(self.surfSize[1]/2)))
		self.erect = Rect(round(self.surfSize[0]*.21),round(self.surfSize[1]*.5),round(self.surfSize[0]*.21),round(self.surfSize[1]*.14))
		self.erect.center = self.triangle[2]
		self.scaleSurf = pygame.Surface((21,21)).convert_alpha()
		self.scaleSurf.fill((0,0,0,0))
		pygame.draw.polygon(self.surf, self.color,self.triangle,0)
		pygame.draw.polygon(self.surf, (0,0,0),self.triangle,1)
		pygame.draw.rect(self.surf,(141,179,245),self.erect,0)
		pygame.draw.rect(self.surf,(0,0,0),self.erect,1)
		self.rect = Rect(self.pos[0], self.pos[1],self.size[0], self.size[1])
		self.scale = pygame.transform.scale(self.surf, (21, 21),self.scaleSurf)
	
	def consume(self,player,hud,inventory,c,activeScrolls):
		if self.healingPower > self.manaPower:
			player.health += self.healingPower
			if player.health > player.mHealth:
				player.health = player.mHealth
		else:
			player.luck += self.manaPower
			if player.luck > player.mLuck:
				player.luck = player.mLuck
		player.stats = {'hp':str(player.health)+ "/" + str(player.mHealth), 'str':player.strg, 'agl':player.agl, 'def':player.dfen, 'MP':player.luck, 'hun':player.hunger, 'foc':player.foc}		
		hud.updateStats(player)
		inventory.removeItem('sounds/goodPotion2.wav')
		return activeScrolls
		
class scroll:
	def __init__(self,level,windowSize,pos):
		self.pos =(random.randint(0,2300),random.randint(0,1100))
		self.level = level
		self.size = (round(windowSize[0]*.023),round(windowSize[1]*.046))
		self.surf = pygame.Surface((28,28)).convert_alpha()	
		self.surf.fill((0,0,0,0))
		self.rect = Rect(self.pos[0], self.pos[1],self.size[0], self.size[1])
		self.scaleSurf = pygame.Surface((21,21)).convert_alpha()
		self.scaleSurf.fill((0,0,0,0))
		self.scale = pygame.transform.scale(self.surf, (21, 21),self.scaleSurf)
		self.draw()
		
	def draw(self):
		for x in range(0,28):
			for y in range(0,28):
				if random.choice((True,False)):
					pygame.draw.rect(self.surf,(random.randint(238,255),random.randint(218,255),random.randint(140,228)),(x,y,2,2),0)
	
	def consume(self,player,level,inventory,c,activeScrolls):
		inventory.removeItem('sounds/mystic.wav')
		activeScrolls.append(ScrollSpell((100,96),self.level,c.pos))
	#	return activeScrolls

class key:
	def __init__(self,windowSize,pos):
		self.pos = pos
		self.size = (round(windowSize[0]*.023),round(windowSize[1]*.046))
		self.surf = pygame.Surface((28,28)).convert_alpha()	
		self.surf.fill((0,0,0,0))
		self.rect = Rect(self.pos[0], self.pos[1],self.size[0], self.size[1])
		self.scaleSurf = pygame.Surface((21,21)).convert_alpha()
		self.scaleSurf.fill((0,0,0,0))
		self.scale = pygame.transform.scale(self.surf, (21, 21),self.scaleSurf)
		self.draw()	
	
	def draw(self):
		pygame.draw.circle(self.surf,(random.randint(235,255),random.randint(200,255),random.randint(0,210)),(5,9),4,2)
		for x in range(7,21):
			for y in range(7,9):
				pygame.draw.rect(self.surf,(random.randint(235,255),random.randint(200,255),random.randint(0,210)),(x,y,2,2),0)
		for x in (15,19):
			pygame.draw.rect(self.surf,(random.randint(235,255),random.randint(200,255),random.randint(0,210)),(x,9,2,4),0)	
	
	def consume(self,player,level,inventory,c,activeScrolls):
		pass
											
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	pot = potion((100,0,0),windowSize)
	scrl = scroll(1,windowSize,(100,200))
	k = key(windowSize,(100,300))
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		windowSurf.fill((100,100,100))
		windowSurf.blit(pot.surf,(100,100))
		windowSurf.blit(scrl.surf,(100,200))
		windowSurf.blit(k.surf,k.pos)
		pygame.display.flip()
		fpsClock.tick(60)	
#test()
