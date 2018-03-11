import pygame, math, sys, random, time
from pygame.locals import *

class cursor:
	def __init__(self, windowSize):
		self.windowSize = windowSize
		self.pos = ((windowSize[0]/2,round((windowSize[1]/2)-(windowSize[1]*.08))))
		self.size = 5
		self.rect = Rect(self.pos,(self.size,self.size))
		self.color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
		self.clicked = False
		self.x = 0
		self.y = 0
		self.speed = 4
		
	def move(self,direction):
		self.x = round(direction[0]*self.speed)
		self.y = round(direction[1]*self.speed)
		self.pos = (self.pos[0]+self.x, self.pos[1]+self.y)
		self.rect.topleft = self.pos
		if self.pos[0] >= self.windowSize[0]:
			self.pos = (self.windowSize[0],self.pos[1])
		elif self.pos[0] <= 0:
			self.pos = (0,self.pos[1])
		if self.pos[1] >= self.windowSize[1]:
			self.pos = (self.pos[0],self.windowSize[1])
		elif self.pos[1] <= 0:
			self.pos = (self.pos[0],0)
			
	def update(self,direction,surf):
		self.move(direction)
		pygame.draw.rect(surf,self.color, self.rect, 0)
