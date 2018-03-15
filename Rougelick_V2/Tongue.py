#!/usr/bin/env python
import pygame, math, sys, random, time, copy
from pygame.locals import *
from tools import *

class Tongue:
	def __init__(self,startPoint,length):
		self.sPoint = startPoint
		self.ePoint = 0
		self.length = length
		
	def moveTongue(self,mPos):
		direction = self.getDirection(mPos[0],mPos[1])			
		self.ePoint = (self.sPoint[0]+direction[0],self.sPoint[1]+direction[1])
	
	def drawTongue(self,surf):
		pygame.draw.lines(surf, (255,182,193), False, (self.sPoint,self.ePoint), 5)
	
	def getDirection(self,xDest,yDest):
		dx,dy = slope(self.sPoint[0],self.sPoint[1],xDest,yDest)
		dist = getDistance(self.sPoint[0],self.sPoint[1],xDest,yDest)
		if dist > self.length:
			diffs = getDiffs(dx,dy,dist)			
			xDiff = diffs[0]*self.length
			yDiff = diffs[1]*self.length
		else:
			xDiff = dx
			yDiff = dy
		return (xDiff,yDiff)
			
	def update(self,sPoint,mPos):
		self.sPoint = sPoint
		self.moveTongue(mPos)
		
		


