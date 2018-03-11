import pygame, math, sys, random, time, copy
from pygame.locals import *

class Shield:
	def __init__(self):
		self.size = (random.randint(50,80),random.randint(50,80))
		self.surf = pygame.Surface(self.size)
		self.rect = self.surf.get_rect()
		self.start = 1
		self.end = 2
		self.shield = pygame.draw.arc(self.surf, (100,0,0), self.rect, self.start, self.end, 5)

	def spin(self,direction):
		self.start += direction[0]*.05
		self.end += direction[0]*.05
		self.shield = pygame.draw.arc(self.surf, (random.randint(0,255),0,0), self.rect, self.start, self.end, 2)
		print(self.start,self.end)
	def update(self,direction):
		self.surf.fill((0,100,0))
		self.spin(direction)
		
		
def test():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	windowSize = (1200, 600)
	windowSurf = pygame.display.set_mode(windowSize)
	
	s = shield()
	controller = pygame.joystick.Joystick(0)
	controller.init()
	
	while True:	
		keysPressed = pygame.key.get_pressed()
		events = pygame.event.get()
		event = pygame.event.poll()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
		windowSurf.fill((0,0,0))
		
		s.update((-controller.get_axis(2),controller.get_axis(3)))
		
		windowSurf.blit(s.surf,(300,200))
		
		
		
		pygame.display.flip()
		fpsClock.tick(60)	
test()
