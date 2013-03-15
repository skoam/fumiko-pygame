import pygame
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FULLSCREEN = False

IMAGE_LIBRARY =	{	'Fumiko': pygame.image.load("Fumiko.png"),
					'empty': pygame.image.load("charempty.png"),
					'Chipset_1': pygame.image.load("Chipset_1.png"),
					'BG_1': pygame.image.load("BG_2.jpg"),
					'Object_Rock': pygame.image.load("rock_smaller.png"),
					'Object_Grass': pygame.image.load("grass.png"),
					'Boss_A': pygame.image.load("mons6.png")
				}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

bgColor = GRAY

PLAYER_LIST = []
LIST_OF_OBJECTS = []
