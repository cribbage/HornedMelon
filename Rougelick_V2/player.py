#!/usr/bin/env python
import pygame, math, sys, random, os
from pygame.locals import *
from globalVars import *
from gameLogic import *
from particles import Particle

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
		self.magicIntensity = 5
		self.magicSpread = 	25
		self.magicLife = 25
		self.magicSpeed = 8
		self.particles = []
		self.mbd = False
		
	def drawFace(self,surf):
		pygame.draw.circle(surf, (255,255,255), self.rect.topleft, 3, 0)#LEFT EYE
		pygame.draw.circle(surf, (255,255,255), self.rect.topright, 3, 0)#RIGHT EYE
		pygame.draw.circle(surf, (0,0,0), (self.rect.topleft[0]+random.randint(-2,2),self.rect.topleft[1]+random.randint(-2,2)), 2, 0)#left pupil
		pygame.draw.circle(surf, (0,0,0), (self.rect.topright[0]+random.randint(-2,2),self.rect.topright[1]+random.randint(-2,2)), 2, 0)#right pupil
		mouthStart = random.randint(-2,2)
		pygame.draw.arc(surf,(255,0,0), self.rect,-2,-1, 1)#MOUTH
	
	def move(self,xVel,yVel,levelSize,wallRects):
		self.pos = (self.pos[0]+xVel,self.pos[1]+yVel)
		self.rect.center = self.pos
		edgeCollision(self,levelSize)
		wallCollision(self,wallRects)
	
	def magic(self):
		for i in range(self.magicIntensity):
			xOffset = random.randint(-self.magicSpread,self.magicSpread)
			yOffset = random.randint(-self.magicSpread,self.magicSpread)
			mousePos = pygame.mouse.get_pos()
			startPos = ((self.pos[0] + xOffset), (self.pos[1] + yOffset))
			newP = Particle(8, startPos, self.magicLife, mousePos[0], mousePos[1],self.magicSpeed)
			self.particles.append(newP)
					
	def getInput(self,events,levelSize,wallRects):
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
		self.move(self.x,self.y,levelSize,wallRects)				
		if self.mbd:
			self.magic()
			
	def update(self,events,levelSize,wallRects):					
		self.getInput(events,levelSize,wallRects)
	
		
		
