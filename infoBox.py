import pygame, math, sys, random, time, copy
from pygame.locals import *

class infoBox:
	def __init__(self, objType,stats):# AND THE LORD SAID: "ALL SHALL BE STRINGED" AND ALL WERE STRINGS
		self.stats = stats 
		self.surf = pygame.Surface((100,100))
		self.font = pygame.font.Font('freesansbold.ttf', 10)	
		self.objType = self.font.render(objType,True,(255,50,255))
		self.objType.get_rect(topleft=(0,0))	
		self.drawInfo()
		
	def drawInfo(self):
		self.surf.blit(self.objType,(5,0))
		y= 15
		for stat in self.stats:
			fontObj = self.font.render(stat,True,(random.randint(0,255),255,255))
			fontObj.get_rect(topleft=(0,0))
			self.surf.blit(fontObj, (0, y))
			
			y += 15
		

