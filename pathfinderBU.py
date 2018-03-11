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
	def __init__(self,enemyPos, playerPos, walls):
		self.pos = enemyPos
		self.startPos = self.pos
		self.pathPos = (0,0)		
		self.goalPos = playerPos
		self.startNode = Node(self.pos,self.goalPos,self.startPos,[],0)
		self.walls = walls
		self.openList = [self.startNode]
		self.closedList = []
		self.endNode = self.startNode
		self.gotPath = False
		self.nodes = {}
		self.path = self.findPath()		
				
	def findPath(self):
		q = 0
		while not self.gotPath and q < 500:
			i = 0
			while i < len(self.openList):			
				self.findNextChildren(self.openList[i])
				i+=1
			q+=1
		if self.endNode != self.startPos:
			return self.getPath(self.endNode,[])
		else:
			return []
			
	def getPath(self,thisNode,path):
		path.insert(0,thisNode.pos)
		if thisNode != self.startNode:
			self.getPath(thisNode.parent,path)		
		return(path)
		
	def findNextChildren(self,currentNode):
		if currentNode not in self.closedList:
			self.openList.remove(currentNode)
			self.closedList.append(currentNode.pos)
		diagonal = 1
		x = int(math.ceil((currentNode.pos[0]-100) / 100)) * 100
		y = int(math.ceil((currentNode.pos[1]-96) / 96)) * 96
									
		while x <= currentNode.pos[0] + 200 and y <= currentNode.pos[1]+96:	
			if (x,y) not in self.walls and (x,y) == self.goalPos and diagonal != 1:
				self.gotPath = True
				self.endNode = Node((x,y),self.goalPos,self.startPos,currentNode,currentNode.eD)
				return
				
			elif (x,y) in self.nodes and self.nodes[(x,y)] in self.openList and diagonal != 1:
				openIndex = self.openList.index(self.nodes[(x,y)])
				compareNode = self.openList[openIndex]
				if currentNode.eD  <  compareNode.parentDist :					
					compareNode.changeParent(currentNode,currentNode.eD)
					
			elif (x,y) not in self.nodes and (x,y) not in self.walls and diagonal != 1 and x >= 0 and y >=0 and x <=2300 and y <=1100:
				n = Node((x,y),self.goalPos,self.startPos,currentNode,currentNode.eD)
				self.nodes[(x,y)] = n
				self.openList.append(n)	
			
			x += 100
			if x >= currentNode.pos[0]+200:
				x=currentNode.pos[0]-100
				y += 96			
			diagonal *= -1
		


