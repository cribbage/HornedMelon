import pygame, math, sys, random
from pygame.locals import *


class hud:
	def __init__(self,player, windowSize):
		self.windowSize = windowSize
		self.surf = pygame.Surface((windowSize[0],round(windowSize[1]*.167)))
		self.backGroundSurf = pygame.Surface((windowSize[0],round(windowSize[1]*.167)))
		self.color2 = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.font1 = pygame.font.Font('freesansbold.ttf', 20)	
		self.statFontObjs = []
		self.statFontObjsO = []
		self.prettyHud()
		self.updateStats(player)
				
	def prettyHud(self):
		rMin = random.randint(0,239)
		gMin = random.randint(0,239)
		bMin = random.randint(0,239)
		x=0
		y=0
		surfSize = pygame.Surface.get_size(self.surf)
		while x <= surfSize[0] and y < surfSize[1]:				
			pygame.draw.rect(self.backGroundSurf, (random.randint(rMin,rMin+16),random.randint(gMin,gMin+16),random.randint(bMin,bMin+16)), Rect(x,y,5, 5), 8)		
			x += 5
			if x >= surfSize[0] and y < surfSize[1]:
				x = 0
				y+= 5
					
	def drawStats(self):
		x=450
		y=10
		i=0
		for fontObj in self.statFontObjs:
			self.surf.blit(self.statFontObjsO[i],(x-1,y-1))
			self.surf.blit(fontObj,(x,y))
			i+=1
			x+=99
			if x >= 650:
				x=450
				y+=50	
		
	def drawHud(self):
		self.drawStats()
		pygame.draw.rect(self.surf, (0,0,0), Rect(0,0,self.windowSize[0], round(self.windowSize[1]*.83)), 3)			
		
	def updateStats(self,player):
		self.surf.blit(self.backGroundSurf,(0,0))
		self.statFontObjs = []
		self.statFontObjsO=[]
		for stat in player.stats:
			statFontObj = self.font1.render(str(stat) + ":" + str(player.stats[stat]) + " ",True,self.color2)
			self.statFontObjs.append(statFontObj)
			statFontObjO = self.font1.render(str(stat) + ":" + str(player.stats[stat]) + " ",True,(0,0,0))
			self.statFontObjsO.append(statFontObjO)
		self.drawHud()
