import pygame
from pygame.locals import *

class Object():
	def __init__(self):
		self.X = 0
		self.Y = 0
		self.Width = 32 # determined by the charset
		self.Height = 32 # determined by the charset
		self.Weight = 10 # Basic Weight of Objects
	
		self.Rect = pygame.Rect(0,0,0,0)
		self.Sprite = pygame.Surface((0,0))
	
		self.moveDown = False
		self.moveLeft = False
		self.moveRight = False
		self.moveUp = False
	
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
	
