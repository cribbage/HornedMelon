#!/usr/bin/env python
import pygame, math, sys, random
from pygame.locals import *
from tools import *

class Enemy:
	def __init__(self, pos):
		self.pos = pos
		self.size = (random.randrange(8,24,4), random.randrange(8,24,4))
		self.rect = Rect(0, 0,self.size[0], self.size[1])
		self.rect.center = self.pos
		self.color = (150,150,150)
		self.speed = 2
		self.x = 0#velocity
		self.y = 0#velocity
		self.dest = (0,0)
		self.destDist = 0
		self.moveAngle = 0
		self.pickDestination()
		self.getDirection()
		self.moveTimer = 720
		self.lSpots = [x for x in range(TILESIZE[0]-(self.size[0]//2)-1,TILESIZE[0]+1)]
		self.tSpots = [x for x in range(TILESIZE[1]-(self.size[1]//2)-1,TILESIZE[1]+1)]
		self.lSpots.append(0)
		self.tSpots.append(0)
		self.rSpots = [x for x in range(0,(self.size[0]//2)+1)]
		self.bSpots = [x for x in range(0,(self.size[1]//2)+1)]
		self.rSpots.append(TILESIZE[0])
		self.bSpots.append(TILESIZE[1])
		
	def blit(self,surf):
		pygame.draw.rect(surf,self.color,self.rect,0)
		self.drawFace(surf)
		
	def getDirection(self):
		xDest,yDest = self.dest
		dx,dy = slope(self.pos[0],self.pos[1],xDest,yDest)
		xDiff,yDiff = getDiffs(dx,dy,self.destDist)
		self.x = xDiff*self.speed
		self.y = yDiff*self.speed
		
	def pickDestination(self):
		self.angle = random.randint(0,360)
		self.destDist = random.randrange(10,100)
		xAngle = math.cos(self.angle)
		yAngle = math.sin(self.angle)
		self.dest = (round(self.pos[0] + xAngle*self.destDist),round(self.pos[1] + yAngle*self.destDist))
	
	def move(self,fpsn):		
		self.pos = (round(self.pos[0]+(self.x*fpsn)),round(self.pos[1]+(self.y*fpsn)))	
		self.rect.center = self.pos	
	
	def drawFace(self,surf):
		pygame.draw.circle(surf, (255,255,255), self.rect.topleft, 3, 0)#LEFT EYE
		pygame.draw.circle(surf, (255,255,255), self.rect.topright, 3, 0)#RIGHT EYE
		pygame.draw.circle(surf, (0,0,0), (self.rect.topleft[0]+round(self.x),self.rect.topleft[1]+round(self.y)), 2, 0)#left pupil
		pygame.draw.circle(surf, (0,0,0), (self.rect.topright[0]+round(self.x),self.rect.topright[1]+round(self.y)), 2, 0)#right pupil
		pygame.draw.arc(surf,(255,0,0), self.rect,-2,-1, 1)#MOUTH
	
	def nearEdge(self,walls,xWalls,levelSize):#checks which side is outside of current tile, checks if the side is in a wall
		currTilex = self.pos[0]-(self.pos[0]%TILESIZE[0])
		currTiley = self.pos[1]-(self.pos[1]%TILESIZE[1])
		xl = self.rect.left-(self.rect.left%TILESIZE[0])
		xr = self.rect.right-(self.rect.right%TILESIZE[0])
		yt = self.rect.top-(self.rect.top%TILESIZE[1])
		yb = self.rect.bottom-(self.rect.bottom%TILESIZE[1])	
		collision = False	
		if xl != currTilex:
			x = round((self.pos[0]-(self.pos[0]%TILESIZE[0]))-TILESIZE[0])
			y = round((self.pos[1]-(self.pos[1]%TILESIZE[1]))) 
			if (x,y) in xWalls[x]:
				collision = True
				self.rect.left = currTilex			
		if xr != currTilex and not xr >= levelSize[0]:
			x = round((self.pos[0]-(self.pos[0]%TILESIZE[0])+TILESIZE[0]))
			y = round((self.pos[1]-(self.pos[1]%TILESIZE[1]))) 
			if (x,y) in xWalls[x]:
				collision = True
				self.rect.right = currTilex+(TILESIZE[0]-1)			
		if yt != currTiley:
			x = round((self.pos[0]-(self.pos[0]%TILESIZE[0])))
			y = round((self.pos[1]-(self.pos[1]%TILESIZE[1]))-TILESIZE[0]) 
			if (x,y) in xWalls[x]:
				collision = True
				self.rect.top = currTiley			
		if yb != currTiley and not yb >= levelSize[1]:
			x = round((self.pos[0]-(self.pos[0]%TILESIZE[0])))
			y = round((self.pos[1]-(self.pos[1]%TILESIZE[1]))+TILESIZE[0]) 
			if (x,y) in xWalls[x]:
				collision = True
				self.rect.bottom = currTiley+TILESIZE[1]			
		self.pos = self.rect.center	
		return collision
				
	def update(self,wallRects,levelSize,xWalls,fpsn):
		self.move(fpsn)
		ec = edgeCollision(self,levelSize)
		wc = self.nearEdge(wallRects,xWalls,levelSize)
		
		if self.rect.collidepoint(self.dest) or wc or ec:
			self.pickDestination()
			self.getDirection()
