import pygame, GLOBAL_VARIABLES
from pygame.locals import *
from GLOBAL_VARIABLES import *

class Object():
	X = 0
	Y = 0
	Width = 32 # determined by the charset
	Height = 32 # determined by the charset
	Weight = 10 * (float(WINDOWHEIGHT / 600))# Basic Weight of Objects scaled to the resolution
	
	Rect = pygame.Rect(0,0,0,0)
	Sprite = pygame.Surface((0,0))
	
	WIDTH_ON_SCREEN = Width * (WINDOWWIDTH / 320)
	HEIGHT_ON_SCREEN = Height * (WINDOWHEIGHT / 240)
	
	moveDown = False
	moveLeft = False
	moveRight = False
	moveUp = False
	
	def build_rectangle(self):
		Rectangle = pygame.Rect(self.X, self.Y, self.Width, self.Height)
		return Rectangle
	
	def draw(self, surface):
		self.Rect = self.build_rectangle()
		surface.blit(self.Sprite, self.Rect)
		return surface

	def Move(self, Level):
		if self.moveDown:
			self.Y += self.Weight
