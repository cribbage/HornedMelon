import pygame, math, sys, random, time, random
from pygame.locals import *

class Node:
	def __init__(self,pos,endGoal,startPos,parent,parentDist):
		self.pos = pos
		self.parent = parent
		self.parentDist = parentDist
		self.sD = self.getDistance(startPos,pos)
		self.eD = self.getDistance(endGoal,pos)
		self.F = (parentDist + self.sD) + self.eD
	
	def changeParent(self,newParent,newParentDist):
		self.parent = newParent
		self.F = (newParentDist + self.sD) + self.eD
			
	def getDistance(self,gD,sP):
		fX = gD[0] - sP[0]
		if fX < 0 :
			fX *=-1
		fY = gD[1] - sP[1]
		if fY < 0 :
			fY *=-1
		return(fX+fY)
		
class pathFinder:
	def __init__(self):
		self.pos = (random.randrange(0,1100,100),random.randrange(0,500,96))
		self.startPos = self.pos
		self.pathPos = (0,0)		
		self.goalPos = (random.randrange(0,1100,100),random.randrange(0,500,96))
		self.startNode = Node(self.pos,self.goalPos,self.startPos,[],0)
		self.walls = []
		self.makeWalls()
		self.path = []
		self.openList = [self.startNode]
		self.closedList = []
		self.nodes = {}
		self.endNode = self.startNode
		self.gotPath = False
		s = time.time()
		self.path = self.findPath()		
		e = time.time() - s
		print("PATHFINDING TOOK: ",e," SECONDS.")
		
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
				
	def findPath(self):
		while not self.gotPath:
			i = 0
			if i == len(self.openList):
				return []
			while i < len(self.openList):			
				self.findNextChildren(self.openList[i])
				i+=1
		print(self.startPos,self.goalPos)
		if self.endNode != self.startPos:
			return self.getPath(self.endNode,[])
		else:
			return []
	
	def createPriority(self,node,comparison):
		if node.F < comparison:
			self.priorityPaths = [node]
			
	def getPath(self,thisNode,path):
		path.insert(0,thisNode.pos)
		if thisNode != self.startNode:
			self.getPath(thisNode.parent,path)		
		return(path)
		
	def findNextChildren(self,currentNode):
		print(currentNode.pos)
		if currentNode not in self.closedList:
			self.openList.remove(currentNode)
			self.closedList.append(currentNode.pos)
		diagonal = 1
		x = int(math.ceil((currentNode.pos[0]-100) / 100)) * 100
		y = int(math.ceil((currentNode.pos[1]-96) / 96)) * 96				
		lowestF = 9999		
		while x <= currentNode.pos[0] + 200 and y <= currentNode.pos[1]+96:	
			if (x,y) not in self.walls and (x,y) == self.goalPos and diagonal != 1 :
				self.gotPath = True
				self.endNode = Node((x,y),self.goalPos,self.startPos,currentNode,currentNode.eD)
				return
				
			elif (x,y) in self.nodes and self.nodes[(x,y)] in self.openList and (x,y) not in self.walls and diagonal != 1:
				openIndex = self.openList.index(self.nodes[(x,y)])
				compareNode = self.openList[openIndex]
				if currentNode.F  >  compareNode.parent.F :		
					currentNode.changeParent(compareNode.parent,compareNode.parent.eD)
					
			elif (x,y) not in self.nodes and (x,y) not in self.walls and diagonal != 1 and x >= 0 and y >=0 and x <=1100 and y <=500:
				n = Node((x,y),self.goalPos,self.startPos,currentNode,currentNode.eD)
				self.nodes[(x,y)] = n			
				self.openList.append(n)
								
			x += 100
			if x >= currentNode.pos[0]+200:
				x=currentNode.pos[0]-100
				y += 96			
			diagonal *= -1
		
		

def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	pf = pathFinder()
	print(pf.path)
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
					return
		windowSurf.fill((255,255,255))
		
		for wall in pf.walls:
			pygame.draw.rect(windowSurf,(0,0,0),(wall[0],wall[1],100,96),0)
		for coord in pf.path:
			pygame.draw.rect(windowSurf,(255,0,0),(coord[0],coord[1],100,96),0)
		pygame.draw.rect(windowSurf,(0,255,0),(pf.startPos[0],pf.startPos[1],100,96),0)
		pygame.draw.rect(windowSurf,(0,255,255),(pf.goalPos[0],pf.goalPos[1],100,96),0)
		
		pygame.display.flip()
		fpsClock.tick(60)
		
while True:
	test()
