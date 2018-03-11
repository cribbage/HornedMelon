import pygame, math, sys, random, time, random
from pygame.locals import *
class pathFinder:
	def __init__(self):
		self.pos = (200,480)
		self.startPos = self.pos
		self.pathPos = (0,0)
		self.walls = []
		self.goalPos = (400,0)
		self.makeWalls()
		self.surf = pygame.Surface((1200,600))
		self.surf.fill((255,255,255))
		self.rect = Rect(self.pos[0], self.pos[1], 100,96)
		self.xVel = 0
		self.yVel = 0
		self.drawSurf()		
		
	def makeWalls(self):
		x = 0
		y = 0
		i = 0
		while x<1200 and y < 600:
			yes = random.choice([True,False])
			if yes and (x,y) != self.pos and (x,y) != self.goalPos:
				self.walls.append((x,y))
			x+= 100
			if x >= 1200:
				x =0
				y += 96	
			i += 1	
	def drawSurf(self):
		self.surf.fill((255,255,255))
		pygame.draw.rect(self.surf,(0,255,0),self.rect,0)
		pygame.draw.rect(self.surf,(0,255,0),(self.goalPos[0],self.goalPos[1],100,96),0)
		x = 0
		y = 0
		while x <= 1200 and y <=600:
			pygame.draw.rect(self.surf,(0,0,0),(x,y,100,96),1)
			x+=100
			if x >= 1200:
				x=0
				y+=96
		for wall in self.walls:
			pygame.draw.rect(self.surf,(0,0,0),(wall[0],wall[1],100,96),0)
	def findPath(self,currentNode, parentNodes, traveledNodes, windowSurf, goingBack, forkNodes):
		x = int(math.ceil((currentNode[0]-100) / 100)) * 100
		y = int(math.ceil((currentNode[1]-96) / 96)) * 96	
		if len(parentNodes)!= 0:
			thisParent = parentNodes[len(parentNodes)-1]
		else:
			forkNodes.append(currentNode)
			thisParent = 0 
		if currentNode not in traveledNodes:
			parentNodes.append(currentNode)
			traveledNodes.append(currentNode)
		nodes = {}
		lowestF = 9999	
		diagonal = 1
		directions = 0	
		while x <= currentNode[0] + 200 and y <= currentNode[1]+96:	
			pygame.draw.rect(self.surf,(0,255,0),(currentNode[0],currentNode[1],100,96),0)
			windowSurf.fill((255,255,255))	
			windowSurf.blit(self.surf,(0,0))
			pygame.display.flip()
			
			if(x,y) not in self.walls and (x,y) != currentNode and (x,y) not in traveledNodes and (x,y) not in parentNodes and x >=0 and y>=0 and x < 1200 and y< 600 and diagonal == -1:
				pygame.draw.rect(self.surf,(random.randint(0,255),0,255),(x,y,100,96),6)
				directions += 1
				gX = self.goalPos[0] - x
				if gX < 0:
					gX *= -1
				gY = self.goalPos[1] - y
				if gY < 0:
					gY *= -1
				G = gX + gY								
				F = G
				if F not in nodes:
					nodes[F] = (x,y)
				if F < lowestF:
					lowestF = F
				
				
	#		if (x,y) in parentNodes and thisParent != (x,y) and (x,y) != currentNode and parentNodes.count(thisParent) == 2:
	#			parentNodes.remove((x,y))
	#			pygame.draw.rect(self.surf,(255,255,255),(x,y,100,96),0)
					
			x += 100
			if x >= currentNode[0]+200:
				x=currentNode[0]-100
				y += 96
			
			diagonal *= -1
		if directions >= 2:
			forkNodes.append(currentNode)
			print("FORK")
		if len(nodes) == 0:		
			if currentNode in forkNodes:
				forkNodes.remove(currentNode)
			currentNode = forkNodes[len(forkNodes)-1]
			if currentNode in parentNodes:				
				goingBack = True
				i = parentNodes.index(currentNode)			
			else:
				print(forkNodes)
				print(parentNodes)
				currentNode = self.startPos
			i = parentNodes.index(currentNode)		
			while i < len(parentNodes):
				pygame.draw.rect(self.surf,(255,255,255),(parentNodes[i][0],parentNodes[i][1],100,96),0)	
				parentNodes.remove(parentNodes[i])
		#	if thisParent != 0:
		#		 thisParent = parentNodes[i-1]
			#	 
				
				
		else:
			goingBack = False
			currentNode = nodes[lowestF]		
		
		if currentNode != self.goalPos:
			while True:	
				keysPressed = pygame.key.get_pressed()
				events = pygame.event.get()
				event = pygame.event.poll()
				for event in events:
					if event.type == QUIT:
						pygame.quit()
						sys.exit()
					if event.type == KEYDOWN:
						if event.key == K_SPACE:	
							self.path = parentNodes
						#	self.removeStragglers()						
							self.findPath(currentNode,parentNodes,traveledNodes,windowSurf,goingBack, forkNodes)						
		else:
			return		
	
	def findPath2(self,currentNode, parentNodes, traveledNodes, windowSurf, forkNode):
		x = int(math.ceil((currentNode[0]-50) / 50)) * 50
		y = int(math.ceil((currentNode[1]-50) / 50)) * 50
		if len(parentNodes) != 0:	
			thisParent = parentNodes.get(currentNode)
		traveledNodes.append(currentNode)
		nodes = {}
		lowestF = 9999	
		while x <= currentNode[0] + 100 and y <= currentNode[1]+50:	
			
			if(x,y) not in self.walls and (x,y) != currentNode and (x,y) not in traveledNodes and (x,y) not in parentNodes and x >=0 and y>=0 and x < 500 and y< 500:
				gX = self.goalPos[0] - x
				if gX < 0:
					gX *= -1
				gY = self.goalPos[1] - y
				if gY < 0:
					gY *= -1
				G = gX + gY								
				F = G
				if F in nodes:
					forkNode = nodes[F]
				nodes[F] = (x,y)
				if F < lowestF:
					lowestF = F
				
			x += 50
			if x >= currentNode[0]+100:
				x=currentNode[0]-50
				y += 50	
	#		if (x,y) in parentNodes and thisParent != (x,y) and (x,y) != currentNode:
	#			parentNodes.pop(parentNodes.get((x,y)))
	#			pygame.draw.rect(self.surf,(255,255,255),(x,y,50,50),0)
		if len(nodes) != 0:
			parentNodes[currentNode] = nodes[lowestF]
		if len(nodes) == 0:
			pygame.draw.rect(self.surf,(255,255,255),(currentNode[0],currentNode[1],50,50),0)
			parentNodes.pop(parentNodes.get(currentNode))
			parentNodes[currentNode] = thisParent		
		else:
			currentNode = nodes[lowestF]
				
		pygame.draw.rect(self.surf,(0,255,0),(currentNode[0],currentNode[1],50,50),0)
		windowSurf.fill((255,255,255))	
		windowSurf.blit(self.surf,(0,0))
		pygame.display.flip()	
		if currentNode != self.goalPos:
			while True:	
				keysPressed = pygame.key.get_pressed()
				events = pygame.event.get()
				event = pygame.event.poll()
				for event in events:
					if event.type == QUIT:
						pygame.quit()
						sys.exit()
					if event.type == KEYDOWN:
						if event.key == K_SPACE:
							self.findPath2(currentNode,parentNodes,traveledNodes,windowSurf, forkNode)						
		else:
			return	
	
	def removeStragglers(self):
		for node in self.path[1:]:
			if node[0] == self.path[self.path.index(node)-1][0] + 100 or node[1] == self.path[self.path.index(node)-1][1] + 100 or node[0] == self.path[self.path.index(node)-1][0] - 100 or node[1] == self.path[self.path.index(node)-1][1] - 100:
				pass
			else:
				self.path.remove(node)
					
	def update(self, windowSurf):
		self.drawSurf()
		self.findPath(self.pos,[],[], windowSurf, False, [])		
	#	self.findPath2(self.pos,{},[], windowSurf, 0)	
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	pf = pathFinder()
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pf.update(windowSurf)
		return
		windowSurf.fill((255,255,255))	
		windowSurf.blit(pf.surf,(0,0))
		pygame.display.flip()
		fpsClock.tick(60)	
while True:
	test()
