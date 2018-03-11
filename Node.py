import pygame, math, sys, random, time, random
from pygame.locals import *

class Node:
	def __init__(self,pos,endGoal,startPos,parent):
		self.pos = pos
		self.parent = parent 
		self.sD = self.getDistance(startPos,pos)
		self.eD = self.getDistance(endGoal,pos)
		self.F = (self.parent.sd + self.sD) + self.eD
			
	def getDistance(self,gD,sP):
		fX = eD[0] - sP[0]
		if fX < 0 :
			fX *=1
		fY = eD[1] - sP[1]
		if fY < 0 :
			fY *=1
		return(fX+fY)
