#!/usr/bin/env python
import pygame, math, sys, random
from globalVars import *
from pygame.locals import *

def normalizeFPS(fpsClock):
	try:
		normalizer = FPS/fpsClock.get_fps()
	except:
		normalizer = 1	
	return normalizer

def inCamera(cam,rect):
	if rect.colliderect(cam):
		return True

def camera(pos,levelSize):
	rect = Rect ((0,0),WINDOWSIZE)
	rect.center = (pos[0]+random.randint(-5,5),pos[1]+random.randint(-5,5))
	if rect.left < 0:
		rect.left = 0
	elif rect.right > levelSize[0]:
		rect.right = levelSize[0]	
	if rect.top < 0:
		rect.top = 0
	elif rect.bottom > levelSize[1]:
		rect.bottom = levelSize[1]
	return rect 

def edgeCollision(dude,levelSize,didCollide=False):
	if dude.rect.left < 0:
		dude.rect.left = 0
		didCollide=True
	elif dude.rect.right > levelSize[0]:
		dude.rect.right = levelSize[0]
		didCollide=True
	if dude.rect.top < 0:
		dude.rect.top = 0
		didCollide=True
	elif dude.rect.bottom > levelSize[1]:
		dude.rect.bottom = levelSize[1]
		didCollide=True
	dude.pos = dude.rect.center
	return didCollide
					
def wallCollision(dude,wallRects,didCollide=False):
	x = round((dude.pos[0]-(dude.pos[0]%TILESIZE[0]))-TILESIZE[0])
	y = round((dude.pos[1]-(dude.pos[1]%TILESIZE[1]))-TILESIZE[1])
	for a in range(x,x+(TILESIZE[0]*3),TILESIZE[0]):
		for b in range(y,y+(TILESIZE[1]*3),TILESIZE[1]):
			wallrect = Rect((a,b),TILESIZE)				
			if (a,b) in wallRects and dude.rect.colliderect(wallrect):
				didCollide = True
				if a == x:#if the collision is to the left
					dude.rect.left = wallrect.right
				elif a == x+(TILESIZE[0]*2):#collision to the right
					dude.rect.right = wallrect.left
				if b == y:#collision on top
					dude.rect.top = wallrect.bottom
				elif b == y+(TILESIZE[1]*2):#collision on bottom
					dude.rect.bottom = wallrect.top				
	dude.pos = dude.rect.center
	return didCollide
	
def randomFloorPosition(floors):#returns random position for object placement
	pos = random.choice(floors)
	pos = (pos[0]+(TILESIZE[0]//2),pos[1]+(TILESIZE[1]//2))
	return pos
	
def getInput(events):
	for event in events:
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:	
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()											

def getDiffs(dx,dy,dist):
	xDiff = dx/dist
	yDiff = dy/dist
	return (xDiff,yDiff)

def getDistance(x1,y1,x2,y2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)
								
def slope(x1,y1,x2,y2):
	dx = x2 - x1
	dy = y2 - y1
	return (dx,dy)
	
