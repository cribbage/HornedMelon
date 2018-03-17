#!/usr/bin/env python
#hello
import pygame, math, sys, random, os
from pygame.locals import *
from globalVars import *
from particles import Particle
from Tongue import Tongue
from tools import *

class player:
	def __init__(self, pos):		
		self.pos = pos
		self.color = (111,0,0)
		self.size =(random.randint(15,30), random.randint(15,30))	
		self.rect = Rect((0,0),self.size)
		self.rect.center = pos
		self.speed = 3
		self.x = 0#velocity
		self.y = 0#velocity
		self.tongueLength = 60
		self.tongue = Tongue(self.pos,self.tongueLength)
		self.magicIntensity = 5
		self.magicSpread = 	12
		self.magicLife = 25
		self.magicSpeed = 8
		self.particles = []
		self.attackMode = "magic"
		self.mbd = False
		
	def drawFace(self,surf):
		pygame.draw.circle(surf, (255,255,255), self.rect.topleft, 3, 0)#LEFT EYE
		pygame.draw.circle(surf, (255,255,255), self.rect.topright, 3, 0)#RIGHT EYE
		pygame.draw.circle(surf, (0,0,0), (self.rect.topleft[0]+random.randint(-2,2),self.rect.topleft[1]+random.randint(-2,2)), 2, 0)#left pupil
		pygame.draw.circle(surf, (0,0,0), (self.rect.topright[0]+random.randint(-2,2),self.rect.topright[1]+random.randint(-2,2)), 2, 0)#right pupil
		mouthStart = random.randint(-2,2)
		pygame.draw.arc(surf,(255,0,0), self.rect,-2,-1, 1)#MOUTH
	
	def move(self,xVel,yVel,levelSize,wallRects,fpsn):
		self.pos = (self.pos[0]+round(xVel*fpsn),self.pos[1]+round(yVel*fpsn))
		self.rect.center = self.pos
		edgeCollision(self,levelSize)
		wallCollision(self,wallRects)
	
	def magic(self,x,y,fpsn):#mouse position is relative to window, not level, so add cameras topleft positon to the mouse position
		for i in range(self.magicIntensity):
			xOffset = random.randint(-self.magicSpread,self.magicSpread)
			yOffset = random.randint(-self.magicSpread,self.magicSpread)
			mousePos = pygame.mouse.get_pos()
			startPos = ((self.pos[0] + xOffset), (self.pos[1] + yOffset)) 
			newP = Particle(4, startPos, self.magicLife, mousePos[0]+xOffset+x, mousePos[1]+yOffset+y,self.magicSpeed,fpsn)
			self.particles.append(newP)
	
	def updateTongue(self,camera):
		mousePos = pygame.mouse.get_pos()
		realMousePos = (mousePos[0]+camera[0],mousePos[1]+camera[1])
		self.tongue.update((self.rect.midbottom[0],self.rect.midbottom[1]-3),realMousePos)
		
	def getInput(self,events,levelSize,wallRects,camera,fpsn):
		for event in events:
			if event.type == KEYDOWN:				
				if event.key == K_d:
					self.x += self.speed
				if event.key == K_a:
					self.x -= self.speed
				if event.key == K_w:
					self.y -= self.speed	
				if event.key == K_s:
					self.y += self.speed
				if event.key == K_1:
					self.attackMode = "magic"
				if event.key == K_2:
					self.attackMode = "tongue"	
			elif event.type == KEYUP:
				if event.key == K_d:					
					self.x -= self.speed
				if event.key == K_a:				
					self.x += self.speed
				if event.key == K_w:
					self.y += self.speed	
				if event.key == K_s:
					self.y -= self.speed
			if event.type == MOUSEBUTTONDOWN:				
				self.mbd = True
			if event.type == MOUSEBUTTONUP:
				self.mbd = False	
		self.move(self.x,self.y,levelSize,wallRects,fpsn)				
		if self.mbd:
			if self.attackMode == "magic":
				self.magic(camera.topleft[0],camera.topleft[1],fpsn)
			elif self.attackMode == "tongue":
				self.updateTongue(camera.topleft)
	
	def blit(self,surf):
		pygame.draw.rect(surf,self.color,self.rect,0)
		self.drawFace(surf)
		if self.mbd and self.attackMode == "tongue":
			self.tongue.drawTongue(surf)
					
	def update(self,events,levelSize,wallRects,camera,fpsn):					
		self.getInput(events,levelSize,wallRects,camera,fpsn)
	
		
		
