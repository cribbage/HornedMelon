import pygame, random, time, random,copy,gc
from pygame.locals import *
from save import *
NOTES= ['sounds/a.wav','sounds/b.wav','sounds/c.wav','sounds/d.wav','sounds/e.wav','sounds/f.wav','sounds/g.wav']
class StartMenu:
	def __init__(self,windowSize,windowSurf,controller,fpsClock,buttons):
		self.surf = windowSurf
		self.opSurf = pygame.Surface((windowSize[0]//4,windowSize[1]//3))
		self.options = ['New Game','Load Game','Options','Quit']
		self.selectSound = pygame.mixer.Sound('sounds/select.wav')
		self.selectionSound = pygame.mixer.Sound('sounds/selection.wav')
		self.loadSound = pygame.mixer.Sound('sounds/load.wav')
		self.newSound = pygame.mixer.Sound('sounds/newgame.wav')
		self.selection = 0
		self.buttons = buttons
		self.r,self.g,self.b = (random.randint(0,125),random.randint(125,255)),(random.randint(0,125),random.randint(125,255)),(random.randint(0,125),random.randint(125,255))
		self.font = pygame.font.Font('freesansbold.ttf', 20)
		self.lastHat = 0
		self.rect = Rect(random.randint(0,windowSize[0]),random.randint(0,windowSize[1]),random.randint(2,50),random.randint(2,50))
		self.hLine = ((0,0),(windowSize[0],0))
		self.vLine = ((0,0),(0,windowSize[1]))
		self.lineSpeed= self.getLineSpeeds()
		self.loading = self.showMenu(windowSize,controller,fpsClock)
	
	def getLineSpeeds(self):
		if self.rect.center[0] > self.rect.center[1]:
			return (1,self.rect.center[1]/self.rect.center[0])
		elif self.rect.center[0] < self.rect.center[1]:
			return (self.rect.center[0]/self.rect.center[1],1)
		else:
			return (0,0)
		
	def showOptions(self,windowSize):
		self.opSurf.fill((20,20,20))
		ng = self.font.render(self.options[0], True, (255,255,255))
		lg = self.font.render(self.options[1], True, (255,255,255))
		op = self.font.render(self.options[2], True, (255,255,255))
		q =  self.font.render(self.options[3], True, (255,255,255))
		
		fontObjs = [ng,lg,op,q]
		x=0
		y=0
		for obj in fontObjs:
			if fontObjs.index(obj) == self.selection:
				self.opSurf.blit(obj,(windowSize[0]//24,y))
			else:
				self.opSurf.blit(obj,(x,y))
			y+=50
		
		self.surf.blit(self.opSurf,(windowSize[0]//12,windowSize[1]//6))
			
	def getSelection(self,controller):
		if controller.get_hat(0)[1] != self.lastHat:
			if controller.get_hat(0)[1] != 0:
				self.selectSound.play()
			self.selection -= controller.get_hat(0)[1]
			self.lastHat = controller.get_hat(0)[1]
			if self.selection >= 4:
				self.selection = 0
			elif self.selection <= -1 :
				self.selection = 3				
	
	def rectifyBackground(self,windowSize):	
		pygame.draw.rect(self.surf,(random.randint(self.r[0],self.r[1]),random.randint(self.g[0],self.g[1]),random.randint(self.b[0],self.b[1])),self.rect,0)
		pygame.draw.lines(self.surf, (random.randint(self.r[0],self.r[1]),random.randint(self.g[0],self.g[1]),random.randint(self.b[0],self.b[1])), False, self.hLine, 1)	
		pygame.draw.lines(self.surf, (random.randint(self.r[0],self.r[1]),random.randint(self.g[0],self.g[1]),random.randint(self.b[0],self.b[1])), False, self.vLine, 1)
		if self.hLine[0][1] != self.rect.center[1]:
			self.hLine = ((0,self.hLine[0][1]+self.lineSpeed[1]),(windowSize[0],self.hLine[0][1]+self.lineSpeed[1]))
		if self.vLine[0][0] != self.rect.center[0]:
			self.vLine = ((self.vLine[0][0]+self.lineSpeed[0],0),(self.vLine[0][0]+self.lineSpeed[0],windowSize[1]))		

		if self.hLine[0][1] == self.rect.center[1] or self.vLine[0][0] == self.rect.center[0]:
			self.r,self.g,self.b = (random.randint(0,125),random.randint(125,255)),(random.randint(0,125),random.randint(125,255)),(random.randint(0,125),random.randint(125,255))
			self.rect = Rect(random.randint(0,windowSize[0]),random.randint(0,windowSize[1]),random.randint(2,50),random.randint(2,50))
			self.hLine = ((0,0),(windowSize[0],0))
			self.vLine = ((0,0),(0,windowSize[1]))	
			self.lineSpeed = self.getLineSpeeds()
			
	def showMenu(self,windowSize,controller,fpsClock):	
		while True:	
			note = pygame.mixer.Sound('a.wav')
			keysPressed = pygame.key.get_pressed()
			events = pygame.event.get()
			event = pygame.event.poll()
			for event in events:
				if event.type == QUIT:
					pygame.quit()
					sys.exit()	
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						return
				elif event.type == JOYBUTTONDOWN:
					if event.button == self.buttons[1]:
						if self.options[self.selection] == 'New Game':
							note.stop()
							self.newSound.play()						
							return False
						elif self.options[self.selection] == 'Load Game':
							note.stop()
							self.loadSound.play()
							return True
						elif self.options[self.selection] == 'Options':
							self.selectionSound.play()
							OptionMenu(windowSize,self.surf,controller,fpsClock,self.buttons)
						elif self.options[self.selection] == 'Quit':
							pygame.quit()
							sys.exit()		
			self.rectifyBackground(windowSize)
			note = pygame.mixer.Sound(NOTES[random.randint(0,6)])
			note.play()
			self.getSelection(controller)
			
			self.showOptions(windowSize)
								
			pygame.display.flip()
			fpsClock.tick(60)

class OptionMenu:
	def __init__(self,windowSize,windowSurf,controller,fpsClock,buttons):
		self.surf = windowSurf
		self.opSurf = pygame.Surface((windowSize[0]//2,windowSize[1]//2))
		self.options = {'Triangle':buttons[0],'X':buttons[1],'Square':buttons[2],'R1':buttons[3],'Start':buttons[4],'Select':buttons[5],'LSH':buttons[6],'LSV':buttons[7],'RSH':buttons[8],'RSV':buttons[9],'Return':25}
		self.selection = 0
		self.buttons = buttons
		self.r,self.g,self.b = (random.randint(0,125),random.randint(125,255)),(random.randint(0,125),random.randint(125,255)),(random.randint(0,125),random.randint(125,255))
		self.font = pygame.font.Font('freesansbold.ttf', 20)
		self.lastHat = 0
		self.selectSound = pygame.mixer.Sound('sounds/select.wav')
		self.selectionSound = pygame.mixer.Sound('sounds/selection.wav')
		self.showMenu(windowSize,controller,fpsClock)
	
	def showOptions(self,windowSize):
		self.opSurf.fill((20,20,20))
		t = self.font.render('Triangle/Y:  ' + str(self.options['Triangle']), True, (255,255,255))
		x = self.font.render('Select:   ' + str(self.options['X']), True, (255,255,255))
		sq = self.font.render('Square/X:  ' + str(self.options['Square']), True, (255,255,255))
		r = self.font.render('Attack:  ' + str(self.options['R1']), True, (255,255,255))
		s = self.font.render('Start:  ' + str(self.options['Start']), True, (255,255,255))
		sel = self.font.render('Select:  ' + str(self.options['Select']), True, (255,255,255))
		lsh = self.font.render('Left Stick Horizontal:  ' + str(self.options['LSH']), True, (255,255,255))
		lsv = self.font.render('Left Stick Vertical:  ' + str(self.options['LSV']), True, (255,255,255))
		rsh = self.font.render('Right Stick Horizontal:  ' + str(self.options['RSH']), True, (255,255,255))
		rsv = self.font.render('Right Stick Vertical:  ' + str(self.options['RSV']), True, (255,255,255))
		re = self.font.render('Return', True,(255,255,255))
		
		fontObjs = [t,x,sq,r,s,sel,lsh,lsv,rsh,rsv,re]
		x=0
		y=0
		for obj in fontObjs:
			if fontObjs.index(obj) == self.selection:
				self.opSurf.blit(obj,(x+windowSize[0]//24,y))
			else:
				self.opSurf.blit(obj,(x,y))
			y+=windowSize[1]//12
			if y >= self.opSurf.get_size()[1]:
				y = 0
				x += windowSize[0]//4
		
		self.surf.blit(self.opSurf,(windowSize[0]//12,windowSize[1]//6))
			
	def getSelection(self,controller):
		if controller.get_hat(0)[1] != self.lastHat:
			if controller.get_hat(0)[1] != 0:
				self.selectSound.play()
			self.selection -= controller.get_hat(0)[1]
			self.lastHat = controller.get_hat(0)[1]
			if self.selection >= 11:
				self.selection = 0
			elif self.selection <= -1 :
				self.selection = 10				
	
	def rectifyBackground(self,windowSize):
		i = 10
		while i > 0:
			pygame.draw.rect(self.surf,(random.randint(self.r[0],self.r[1]),random.randint(self.g[0],self.g[1]),random.randint(self.b[0],self.b[1])),(random.randint(0,windowSize[0]),random.randint(0,windowSize[1]),random.randint(2,50),random.randint(2,50)),0)
			i-=1
	def changeButtons(self,event):
		if self.selection == 0:
			self.buttons[0] = event.button
			self.options['Triangle'] = self.buttons[0]
		elif self.selection == 1:
			self.buttons[1] = event.button
			self.options['X'] = self.buttons[1]
		elif self.selection == 2:
			self.buttons[2] = event.button
			self.options['Square'] = self.buttons[2]
		elif self.selection == 3:
			self.buttons[3] = event.button
			self.options['R1'] = self.buttons[3]
		elif self.selection == 4:
			self.buttons[4] = event.button	
			self.options['Start'] = self.buttons[4]				
		elif self.selection == 5:
			self.buttons[5] = event.button	
			self.options['Select'] = self.buttons[5]	
	
	def changeAxes(self,controller):
		axes = controller.get_numaxes()
		for i in range(axes):
			axis = controller.get_axis(i)	
			if axis > 0.05 and axis <= 1 or axis < -0.05 and axis >= -1:
				self.selectionSound.play()
				if self.selection == 6:
					self.buttons[6] = i
					self.options['LSH'] = self.buttons[6]	
				elif self.selection == 7:
					self.buttons[7] = i
					self.options['LSV'] = self.buttons[7]	
				elif self.selection == 8:
					self.buttons[8] = i
					self.options['RSH'] = self.buttons[8]	
				elif self.selection == 9:
					self.buttons[9] = i		
					self.options['RSV'] = self.buttons[9]	
					
	def showMenu(self,windowSize,controller,fpsClock):		
		while True:	
			keysPressed = pygame.key.get_pressed()
			events = pygame.event.get()
			event = pygame.event.poll()
			for event in events:
				if event.type == QUIT:
					pygame.quit()
					sys.exit()	
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						return
				elif event.type == JOYBUTTONDOWN:
					self.selectionSound.play()
					if event.button == self.buttons[1]:
						if self.selection == 10:	
							self.surf.fill((0,0,0))	
							Save(self.buttons,'controls.txt').save()				
							return
					self.changeButtons(event)
					
			self.changeAxes(controller)	
					
			self.rectifyBackground(windowSize)
			
			self.getSelection(controller)
			
			self.showOptions(windowSize)
								
			pygame.display.flip()
			fpsClock.tick(60)
