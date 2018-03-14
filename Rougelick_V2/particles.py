#!/usr/bin/env python
import pygame, math, sys, random
from pygame.locals import *
from globalVars import *
from math import*

class Particle:
	
	def __init__(self,size, pos, maxLife, xDest, yDest,speed):
		self.size = random.randint(2,size)
		self.pos = pos
		self.maxLife = maxLife
		self.direction = self.getDirection(xDest,yDest)
		self.xVel = self.direction[0]*speed
		self.yVel = self.direction[1]*speed
		self.remove = False
			
	def getDirection(self,xDest,yDest):
		dx = xDest - self.pos[0]
		dy = yDest - self.pos[1]
		dist = math.sqrt((xDest-self.pos[0])**2 + (yDest-self.pos[1])**2)
		if dist == 0:
			dist = 0.1
		xDiff = dx/dist
		yDiff = dy/dist
		return (xDiff,yDiff)
		
	def move(self):
		self.maxLife -= 1		
		if self.maxLife > 1:
			self.pos = (self.pos[0]+round(self.xVel), (self.pos[1]+round(self.yVel)))
		else:
			self.remove = True
	
	def collideWall(self,levelSize):
		if self.pos[0]-self.size <= 0:
			self.xVel = -self.xVel			
		if self.pos[1]-self.size <= 0:
			self.yVel = -self.yVel			
		if self.pos[0]+self.size >=levelSize[0]:
			self.xVel = -self.xVel		
		if self.pos[1]+self.size >= levelSize[1]:
			self.yVel = -self.yVel		
											
	def update(self,surf,levelSize):
		self.move()
		self.collideWall(levelSize)		
		self.cir = pygame.draw.circle(surf, (random.randint(233, 255),random.randint(0, 165),0), self.pos, self.size, 0)#LAVA
		


