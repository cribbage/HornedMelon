import pygame, math, sys, random, time
from pygame.locals import *

class lightLayer:
	def __init__(self, windowSize):
		choices = [True, False]
		self.windowSize = windowSize
		self.on = random.choice(choices)
		if self.on:
			self.surf = pygame.Surface((windowSize)).convert_alpha()
			self.surf.fill((0,0,0,255))
			self.drawCircs()
		else:
			self.surf = pygame.Surface((0,0))
			
	def drawCircs(self):
		i = 255
		while i > 50:	
			pygame.draw.circle(self.surf, (0,0,0,i), (round(self.windowSize[0]/2),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))), i, 0)		
			i-=1
				
	def glow(self):
		i = 50
		if self.on:
			while i > 0:
				pygame.draw.circle(self.surf, (random.randint(150, 255),random.randint(150, 255),0,i), (round(self.windowSize[0]/2),round((self.windowSize[1]/2)-(self.windowSize[1]*.08))), i, 0)	
				i-=1	
