#!/usr/bin/env python
import pygame, math, sys, random, os
from pygame.locals import *
from level import *
from globalVars import *

def camera(pos,levelSize):
	rect = Rect ((0,0),WINDOWSIZE)
	rect.center = pos
	if rect.left < 0:
		rect.left = 0
	elif rect.right > levelSize[0]:
		rect.right = levelSize[0]	
	if rect.top < 0:
		rect.top = 0
	elif rect.bottom > levelSize[1]:
		rect.bottom = levelSize[1]
	return rect 
	
def createLevel(levelSize):
	lvl = level(levelSize)
	return lvl

def	update(lvl,dude,events):
	c = camera(dude.pos,lvl.levelSize)
	playerUpdate(dude,events,lvl.walls,lvl.levelSize,c)
	lvl.updateLevel(c)
	return c
							
def playerUpdate(dude,events,wallRects,levelSize,c):
	dude.update(events,levelSize,wallRects,c)		
		
def blit(windowSurf,dude,lvl,camera):
	dude.blit(lvl.cleanSurf,lvl.levelSize)
	windowSurf.blit(lvl.cleanSurf.subsurface(camera),(0,0))
	
def getInput(dude,lvl,events):
	for event in events:
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:	
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()											
								
def edgeCollision(dude,levelSize):
	if dude.rect.left < 0:
		dude.rect.left = 0
	elif dude.rect.right > levelSize[0]:
		dude.rect.right = levelSize[0]
	if dude.rect.top < 0:
		dude.rect.top = 0
	elif dude.rect.bottom > levelSize[1]:
		dude.rect.bottom = levelSize[1]
	dude.pos = dude.rect.center
					
def wallCollision(dude,wallRects):
	x = (dude.pos[0]-(dude.pos[0]%TILESIZE[0]))-TILESIZE[0]
	y = (dude.pos[1]-(dude.pos[1]%TILESIZE[1]))-TILESIZE[1]
	for a in range(x,x+(TILESIZE[0]*3),TILESIZE[0]):
		for b in range(y,y+(TILESIZE[1]*3),TILESIZE[1]):
			wallrect = Rect((a,b),TILESIZE)				
			if (a,b) in wallRects and dude.rect.colliderect(wallrect):
				if a == x:#if the collision is to the left
					dude.rect.left = wallrect.right
				elif a == x+(TILESIZE[0]*2):#collision to the right
					dude.rect.right = wallrect.left
				if b == y:#collision on top
					dude.rect.top = wallrect.bottom
				elif b == y+(TILESIZE[1]*2):#collision on bottom
					dude.rect.bottom = wallrect.top

				
	dude.pos = dude.rect.center



