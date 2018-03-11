import pygame, math, sys, random, particles, enemy, os
from Player import *
from enemy import *
from pygame.locals import *
from particles import Particle
from hud import *
from level import *
from cursor import *
from objects import *
from inventory import *
from infoBox import *
from sword import *
from ants import *
from save import *
from lightlayer import *

def createItems(windowSize,levelStuff):
	i = 0
	otions = []
	while i <= 20:
		otions.append(potion((random.randint(0,100),0,random.randint(0,100)),windowSize))
		otions.append(scroll(random.randint(0,5),windowSize,(random.randint(0,2300),random.randint(0,1100))))
		for obj in otions[i-1:]:
			isInWater(obj,levelStuff[2].subSurfs)
		i+=1
	return otions
				
def createEnemies(amount,levelStuff,windowSize):
	enemies = []
	for e in range(amount):
		enemies.append(enemy.enemy((random.randint(0,levelStuff[0][0]),random.randint(0,levelStuff[0][1])), levelStuff[2].subSurfs,windowSize))
		isInWater(enemies[e],levelStuff[2].subSurfs)
	return enemies
	
def createPlayer(windowSize,levelStuff):
	dude = player((windowSize[0]/2,round((windowSize[1]/2)-(windowSize[1]*.08))), levelStuff[2].subSurfs, windowSize)
	isInWater(dude,levelStuff[2].subSurfs)
	dude.ROR = (dude.pos[0] - round(windowSize[0]/2), dude.pos[1] - round((windowSize[1]/2)-(windowSize[1]*.08)))
	return dude
	
def createLevel(windowSize,MUSIC):
	levelSize = (2400, 1248)
	levelPos = (0,0)
	rooms = random.randint(3,12)
	lvl = level(levelSize,(1200, 600),rooms)
	levelSurf = lvl.surf
	levelSurf2 = pygame.Surface(levelSize)
	ll = lightLayer(windowSize)
	if ll.on:
		pygame.mixer.music.load('music/ambience.mp3')
	else:
		pygame.mixer.music.set_volume(0.8)
		pygame.mixer.music.load(random.choice(MUSIC))
	return [levelSize,levelPos,lvl,levelSurf,levelSurf2,ll]

def	update(paused,lvl,grid,dude,events,keysPressed,controller,levelSurf2
,windowSize,fireSound,fps,offset,size,maxLife,enemies,hudw,levelSize
,otions,invent,ants,c,windowSurf,infoB,sword,activeScrolls,BUTTONS,levelPos):
	lvl.updateLevel(paused)	
	levelSurf2.blit(lvl.surf,(0,0))		
	levelSurf2.blit(grid.surf,(0,0))
	playerUpdate(dude,events, keysPressed, lvl.subSurfs,controller.get_hat(0), (controller.get_axis(BUTTONS[8]),controller.get_axis(BUTTONS[9])), levelSurf2, windowSize, fireSound,fps,offset,size,maxLife,enemies,hudw,levelPos,levelSize,paused)
	nearItems(otions,dude, windowSize, levelSurf2, paused, invent)		
	bloodUpdate(ants,grid)
	nearEnemies(enemies,dude,levelSurf2, lvl.subSurfs, windowSize, paused, levelSize, c, windowSurf, levelPos, infoB, lvl.emptyCoords,sword,ants,hudw)
	scrlUpdate(paused,activeScrolls,levelSurf2,c,enemies,hudw,levelPos)	
		
def updatePauseMenu(pausem,MenuButton,windowSurf,c,paused,controller,BUTTONS):
	if paused:			
		updateCursor(c,controller,windowSurf,BUTTONS,paused)	
		pausem.play()		
		windowSurf.blit(MenuButton,(100,100))
		if c.rect.colliderect((100,100,100,100)) and c.clicked:
			pygame.mixer.music.stop()
			return True
		return False
				
def updateCursor(c,controller,windowSurf,BUTTONS,paused):
	cd = (controller.get_axis(BUTTONS[6]),controller.get_axis(BUTTONS[7]))
	if cd != (0,0) and paused:	
		c.update(cd,windowSurf)

def scrlUpdate(paused,activeScrolls,levelSurf2,c,enemies,hudw,levelPos):
	if paused:
		for scrol in activeScrolls:
			if scrol.usable:
				scrol.update((c.pos[0]-levelPos[0],c.pos[1]-levelPos[1]),levelSurf2,c.clicked)

	if not paused:				
		for scrol in activeScrolls:
			if not scrol.usable:
				if scrol.time !=0:
					createMagic(scrol,10,6,20)
					magicUpdate(scrol,levelSurf2,enemies,hudw,levelPos)
					scrol.time -=1
				else:
					activeScrolls.remove(scrol)	

def bloodUpdate(ants,grid):
	for ant in ants:
		ant.update(grid)
		if ant.life <= 0:
			ants.remove(ant)
			
def playerUpdate(dude,events,keysPressed,subSurfs,controllerHat,aim
,levelSurf2,windowSize,fireSound,fps,offset,size,maxLife,enemies,hudw
,levelPos,levelSize,paused):
	if not paused:
		dude.update(events, keysPressed, subSurfs,controllerHat, aim, levelSurf2, windowSize, fireSound,fps)		
		wallCollisions(dude, subSurfs,levelSurf2)
		edgeCollision(dude,levelSize)		
		createMagic(dude,offset,size,maxLife)
		magicUpdate(dude,levelSurf2,enemies,hudw,levelPos)	

def blit(levelSurf2,levelPos,ll,windowSurf,dude,hudw,invent,paused
,windowSize,otion,otion2,c,activeScrolls,sword,controller,BUTTONS):	
	windowSurf.blit(levelSurf2,(levelPos[0],levelPos[1]))
	if ll.on:		
		windowSurf.blit(ll.surf,(0,0))
	pygame.draw.rect(windowSurf,dude.color, dude.rect, 0)
	dude.drawFace(windowSurf, windowSize)
	windowSurf.blit(hudw.surf,(0,round(windowSize[1]*.83)))	
	invent.update(random.choice([otion,otion2]),c,windowSurf,dude,hudw,activeScrolls)
	windowSurf.blit(invent.surf,invent.pos)	
	if dude.sAttack:
		sword.update(windowSurf,dude.rect.center,controller.get_axis(BUTTONS[8]),controller.get_axis(BUTTONS[9]))
	
def save(dude,lvl,invent):
	Save(dude.data,'playerData.txt').save()
	Save(lvl.data,'levelData.txt').save()
	Save(invent.data,'inventoryData.txt').save()
	Save(invent.itemData,'itemData.txt').save()		

def load(dude,lvl,levelPos,hudw,fireSound,windowSize):
	dude.mAttack = False	
	fireSound.stop()
	lvl.loadData()
	dude.ROR = (0,0)
	dude.loadData()
	isInWater(dude,lvl.subSurfs)
	dude.ROR = (dude.pos[0] - round(windowSize[0]/2), dude.pos[1] - round((windowSize[1]/2)-(windowSize[1]*.08)))
	levelPos = (0- dude.ROR[0], 0- dude.ROR[1])	
	hudw.updateStats(dude)
	
def getInput(fireSound,dude,lvl,invent,hudw,pausem,paused,c,BUTTONS,events,keysPressed,event,windowSize,levelPos):

	for event in events:
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:	
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()											
			elif event.key == K_m:
				save(dude,lvl,invent)			
			elif event.key == K_l:
				load(dude,lvl,levelPos,hudw,fireSound,windowSize)					
		elif event.type == JOYBUTTONDOWN:
			if event.button == BUTTONS[4]:
				paused = not paused
				if paused:
					pygame.mixer.music.pause()
					fireSound.stop()
					dude.mAttack = False	
				elif not paused:
					pausem.stop()
					pygame.mixer.music.unpause()					
			if paused:									
				if event.button == BUTTONS[1]:
					c.clicked = True
				elif event.button == BUTTONS[0]:
					if c.speed < 16:
						c.speed +=4
				elif event.button == BUTTONS[2]:
					if c.speed >4:
						c.speed -=4
		elif event.type == JOYBUTTONUP:
			if event.button == BUTTONS[1]:
				c.clicked = False
	return paused
					
def menuButton():
	menuButton = pygame.font.Font('freesansbold.ttf', 30).render('MENU', True, (255,255,255))
	menuButton.get_rect(topleft=(0,0))
	return menuButton
	
def nearEnemies(enemies,dude,surf,wallRects,windowSize,paused,levelSize
,cursor,windowSurf,levelPos,iB,emptyCoords,sword,ants,hud):
	for e in enemies:
		if e.alive:
			if e.pos[0] >= dude.pos[0]:
				if e.pos[0] - dude.pos[0] < windowSize[0]/2:
					goochX = True 
				else:
					goochX = False
			elif dude.pos[0] > e.pos[0]:
				if dude.pos[0] - e.pos[0] < windowSize[0]/2:
					goochX = True
				else:
					goochX = False
			if e.pos[1] >= dude.pos[1]:
				if e.pos[1] - dude.pos[1] < windowSize[1]/2:
					goochY = True 
				else:
					goochY = False
			elif dude.pos[1] > e.pos[1]:
				if dude.pos[1] - e.pos[1] < windowSize[1]/2:
					goochY = True
				else:
					goochY = False
			if goochX and goochY and not paused:
				if e.iB != 'none':
					e.iB = 'none'
				e.update(dude.pos,surf, wallRects,windowSize, emptyCoords,levelPos)
				edgeCollision(e,levelSize)
				createMagic(e,10,6,20)
				magicUpdate(e,surf,[dude],hud,levelPos)
				wallCollisions(e,wallRects,surf)
				if dude.sAttack:
					sword.collisions(dude,e,ants,levelPos,windowSize)
			#	for c in e.path:
			#		rect = (c[0],c[1],100,96)
			#		pygame.draw.rect(surf,(0,0,200),rect,0)
			elif paused:
				surf.blit(e.surf,e.pos)
				if e.rect.collidepoint((cursor.pos[0] + (-levelPos[0]), cursor.pos[1] +(-levelPos[1]))):
					iB = showInfo(iB,e, surf,cursor,levelPos, windowSize, levelSize)								
					return
		else:
			deathSound = 'sounds/deathsound'+str(random.randint(1,5))+'.wav'
			pygame.mixer.Sound(deathSound).play()
			enemies.remove(e)	
			
def showInfo(iB,e,surf,cursor,levelPos,windowSize,levelSize):
	if e.iB == 'none':
		i = infoBox((e.first + " " + e.last),('HP: '+str(e.health) +"/ " + str(e.maxHealth),'Strg: ' + str(e.strg),'Foc: ' + str(e.foc),'Dfen: ' + str(e.dfen)))
		e.iB = i.surf
	x = (cursor.pos[0] + (-levelPos[0]))
	y =(cursor.pos[1] + (-levelPos[1]))
	if cursor.pos[0] > windowSize[0]/2:
		x -= 100
	if cursor.pos[1] > windowSize[1]/2:
		y -= 100
	surf.blit(e.iB,(x,y))
	
def magicUpdate(character,surf,targets,hud,levelPos):	
	for p in character.particles:
		p.update(character.direction[0], surf, character.direction[1], targets,character.particles,hud,levelPos)	
		if p.remove and p in character.particles:
			character.particles.remove(p)

def createMagic(dude,offset,size,maxLife):
	if dude.mAttack:
		i = dude.mIntensity	
		while i > 0:
			xOffset = random.randint(-offset,offset)
			yOffset = random.randint(-offset,offset)
			newPPos = ((round(dude.pos[0]+(dude.size[0]/2)) + xOffset), (round(dude.pos[1]+(dude.size[1]/2)) + yOffset))
			newP = Particle(size, newPPos, maxLife, dude.direction[0], dude.direction[1])	
			dude.particles.append(newP)
			i -= 1

def edgeCollision(dude,levelSize):
	if dude.pos[0] <= 0 or dude.pos[0] >= levelSize[0]-dude.size[0]:
		dude.pos = (dude.pos[0] +(-dude.x), dude.pos[1])
		dude.x = 0
	if dude.pos[1] <= 0 or dude.pos[1] >= levelSize[1]-dude.size[1]:
		dude.pos = (dude.pos[0] ), dude.pos[1]+(-dude.y)
		dude.y = 0				
		
def nearItems(items,dude, windowSize, levelSurf, paused, invent):
	for i in items:	
		if i.pos[0] >= dude.pos[0]:
			if i.pos[0] - dude.pos[0] < windowSize[0]/2:
				goochX = True 
			else:
				goochX = False
		elif dude.pos[0] > i.pos[0]:
			if dude.pos[0] - i.pos[0] < windowSize[0]/2:
				goochX = True
			else:
				goochX = False
		if i.pos[1] >= dude.pos[1]:
			if i.pos[1] - dude.pos[1] < windowSize[1]/2:
				goochY = True 
			else:
				goochY = False
		elif dude.pos[1] > i.pos[1]:
			if dude.pos[1] - i.pos[1] < windowSize[1]/2:
				goochY = True
			else:
				goochY = False
		if goochX and goochY:
			levelSurf.blit(i.surf,i.pos)
			dude.collideItem(i,invent,items)
			
def wallCollisions(self,wallRects,surf):
	x = int(math.ceil((self.pos[0]-200) / 100)) * 100
	y = int(math.ceil((self.pos[1]-96) / 96)) * 96	
	while x <= (self.pos[0] + 200) and y <= (self.pos[1]+100):	
		if(x,y) in wallRects.keys():		
			rect = Rect(x,y,100, 96)
			if rect.collidepoint(self.pos) or rect.collidepoint(((self.pos[0]+self.size[0]),self.pos[1])) or rect.collidepoint(((self.pos[0]+self.size[0]),(self.pos[1]+self.size[1]))) or rect.collidepoint((self.pos[0],(self.pos[1]+self.size[1]))):	
				if self.pos[0]+self.size[0]> rect.left and self.pos[0] < rect.left or self.pos[0]+self.size[0]> rect.right and self.pos[0] < rect.right:
					self.pos = (self.pos[0]+(-self.x),self.pos[1])
					self.x = 0						
				if self.pos[1]+self.size[1]> rect.top and self.pos[1] < rect.top or self.pos[1]+self.size[1]> rect.bottom and self.pos[1] < rect.bottom:
					self.pos = (self.pos[0],self.pos[1]+(-self.y))
					self.y = 0							
		x+=100
		if x >= self.pos[0]+100:
			x = int(math.ceil((self.pos[0]-200) / 100)) * 100
			y+= 96

def isInWater(self,wallRects):
	x = int(math.ceil((self.pos[0]-200) / 100)) * 100
	y = int(math.ceil((self.pos[1]-100) / 96)) * 96	
	while x <= (self.pos[0] + 200) and y <= self.pos[1]+100:	
		if(x,y) in wallRects.keys():
			rect = Rect(x,y,100, 96)
			if rect.collidepoint(self.pos) or rect.collidepoint(((self.pos[0]+self.size[0]),self.pos[1])) or rect.collidepoint(((self.pos[0]+self.size[0]),(self.pos[1]+self.size[1]))) or rect.collidepoint((self.pos[0],(self.pos[1]+self.size[1]))):	
				self.pos = (random.randint(600,2300), random.randint(250,1100))
				self.rect = Rect(self.pos[0], self.pos[1],self.size[0], self.size[1])
				isInWater(self, wallRects)
		x+=100
		if x >= self.pos[0]+100:
			x = int(math.ceil((self.pos[0]-200) / 100)) * 100
			y+= 96

def mainLoop(windowSize,controller,windowSurf,MenuButton,fireSound,
levelSize,levelPos,lvl,levelSurf,ll,dude,sword,enemies,hudw,size,offset,
maxLife,c,infoB,paused,invent,infoBoxes,currentBox,otion,otion2,pots,
otions,activeScrolls,grid,ants,PM,pausem,levelSurf2,BUTTONS,fpsClock):
	while True:
		events = pygame.event.get()
		keysPressed = pygame.key.get_pressed() 
		event = pygame.event.poll()
		paused = getInput(fireSound,dude,lvl,invent,hudw,pausem,paused,c,BUTTONS,events,keysPressed,event,windowSize,levelPos)					
		windowSurf.fill((0,0,0))
		update(paused,lvl,grid,dude,events,keysPressed,controller,levelSurf2,windowSize,fireSound,fpsClock.get_fps(),offset,size,maxLife,enemies,hudw,levelSize,otions,invent,ants,c,windowSurf,infoB,sword,activeScrolls,BUTTONS,levelPos)		
		blit(levelSurf2,levelPos,ll,windowSurf,dude,hudw,invent,paused,windowSize,otion,otion2,c,activeScrolls,sword,controller,BUTTONS)
		if not paused:
			levelPos = (levelPos[0]-dude.x, levelPos[1]-dude.y)
		if updatePauseMenu(pausem,MenuButton,windowSurf,c,paused,controller,BUTTONS):
			return			
		pygame.display.set_caption("FPS: " +str(fpsClock.get_fps()))
		pygame.display.flip()
		fpsClock.tick(60)
