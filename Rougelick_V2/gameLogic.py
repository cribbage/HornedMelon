#!/usr/bin/env python
import pygame, math, sys, random, os
from pygame.locals import *
from level import *
from globalVars import *


def createLevel(windowSize):
	levelSize = (1200, 600)
	levelPos = (0,0)
	lvl = level(levelSize)
	levelSurf = lvl.cleanSurf
	return lvl

def	update(lvl,dude,events,wallRects,levelSize):
	lvl.updateLevel()			
	playerUpdate(dude,events,wallRects,levelSize)
							
def playerUpdate(dude,events,wallRects,levelSize):
	dude.update(events,levelSize,wallRects)		
		
def blit(windowSurf,dude,lvl):
	pygame.draw.rect(lvl.cleanSurf,dude.color, dude.rect, 0)
	dude.drawFace(lvl.cleanSurf)
	for p in dude.particles:
		p.update(lvl.cleanSurf)
		if p.remove:
			dude.particles.remove(p)	
	windowSurf.blit(lvl.cleanSurf,lvl.pos)
	
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
				if a == x and b == y+TILESIZE[1]:#if the collision is to the left
					dude.rect.left = wallrect.right
				elif a == x+(TILESIZE[0]*2) and b ==y+TILESIZE[1]:#collision to the right
					dude.rect.right = wallrect.left
				elif b == y and a == x+TILESIZE[0] :#collision on top
					dude.rect.top = wallrect.bottom
				elif b == y+(TILESIZE[1]*2) and a == x+TILESIZE[0]:#collision on bottom
					dude.rect.bottom = wallrect.top
	dude.pos = dude.rect.center



