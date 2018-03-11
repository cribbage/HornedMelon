import pygame, math, sys, random, particles, enemy, os
from GameLogic import *
from Player import *
from enemy import *
from pygame.locals import *
from particles import Particle
from hud import *
from level import *
from lightlayer import *
from cursor import *
from objects import *
from inventory import *
from infoBox import *
from save import *
from sword import *
from ants import *
from StartMenu import *
from ScrollSpell import *

MUSIC = ('music/runnin.mp3', 'music/party.mp3','music/murkin.mp3')
PAUSEMUSIC = ('music/pausemusic.wav')

	
					
def start(windowSize,controller,loading,windowSurf):	
	size = 6
	maxLife = 20
	offset = 10
	PM = 0
	pausem = pygame.mixer.Sound(PAUSEMUSIC[0])
	fireSound = pygame.mixer.Sound('sounds/fire.wav')
	resolution = pygame.display.Info()
	levelStuff = createLevel(windowSize,MUSIC)
	pygame.mixer.music.play(-1)
	dude = createPlayer(windowSize,levelStuff)
	sword = Sword(dude.pos,dude.ROR,2)
	levelStuff[1] = (levelStuff[1][0] - dude.ROR[0], levelStuff[1][1] - dude.ROR[1])
	enemies = createEnemies(250,levelStuff,windowSize)
	hudw = hud(dude, windowSize)
	c = cursor(windowSize)
	infoB = 'none'
	paused = False
	invent = inventory((round(windowSize[0]*.75),round(windowSize[1]*.83)), windowSize) 
	infoBoxes = {}
	currentBox = 'none'
	otion = potion((100,0,0),windowSize)
	otion2 = potion((0,0,100),windowSize) 
	pots = (otion,otion2)
	otions = createItems(windowSize,levelStuff)
	grid = Grid()
	MenuButton = menuButton()
	ants = []
	activeScrolls = []
	if loading:
		load(dude,levelStuff[2],levelPos,hudw,fireSound,windowSize)
		
	mainLoop(windowSize,controller,windowSurf,MenuButton,fireSound,levelStuff[0],levelStuff[1],levelStuff[2],levelStuff[3],levelStuff[5],dude,sword,enemies,hudw,size,offset,maxLife,c,infoB,paused,invent,infoBoxes,currentBox,otion,otion2,pots,otions,activeScrolls,grid,ants,PM,pausem,levelStuff[4],BUTTONS,fpsClock)

while True:
	global BUTTONS
	BUTTONS = Save([],'controls.txt').load(int)
	pygame.init()
	fpsClock = pygame.time.Clock()
	resolution = pygame.display.Info()
	pygame.display.init()
	pygame.display.set_caption("FPS: " +str(fpsClock.get_fps()))
	pygame.mixer.pre_init(22050, 16, 2, 8096)
	pygame.mixer.set_num_channels(2)
	windowSize = (1200,600)
	windowSize = (resolution.current_w, resolution.current_h)
	windowSurf = pygame.display.set_mode(windowSize,FULLSCREEN)
	controller = pygame.joystick.Joystick(0)
	controller.init()
	while True:
		loading = StartMenu(windowSize,windowSurf,controller,fpsClock,BUTTONS)
		start(windowSize,controller,loading.loading,windowSurf)
