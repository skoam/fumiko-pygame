import pygame
from pygame.locals import *

def Player_and_Terrain(Player, TILE_POINTER, Terrain):
	SIZE_X, SIZE_Y = Terrain.SIZE_ON_SCREEN
	X = TILE_POINTER * SIZE_X
	Y = Terrain.Height - Terrain.List_of_Offsets[TILE_POINTER]
	TILE_RECTANGLE = pygame.Rect(X - Terrain.Position_Pointer, Y, SIZE_X, SIZE_Y * 6)
	
	#if TILE_RECTANGLE.colliderect((Player.build_rectangle_with_offset(0, 0, 0, 2))):
	#	return True
	if TILE_RECTANGLE.collidepoint((Player.X + Player.Width / 6, Player.Y + Player.Height / 1.5)) or TILE_RECTANGLE.collidepoint((Player.X + Player.Width - Player.Width / 6, Player.Y + Player.Height / 1.5)):
		return 'Stop'
	if TILE_RECTANGLE.collidepoint((Player.X + Player.Width / 8, Player.Y + Player.Height / 2)) or TILE_RECTANGLE.collidepoint((Player.X + Player.Width - Player.Width / 8, Player.Y + Player.Height / 2)):
		return 'Stop'
	
	if TILE_RECTANGLE.collidepoint((Player.X + Player.Width / 4, Player.Y + Player.Height)) or TILE_RECTANGLE.collidepoint((Player.X + Player.Width - Player.Width / 4, Player.Y + Player.Height)):
		return True
		
	if TILE_RECTANGLE.collidepoint((Player.X + Player.Width / 2, Player.Y + Player.Height)):
		return True
	return False
	
def Object_and_Terrain(Object, TILE_POINTER, Terrain):
	SIZE_X, SIZE_Y = Terrain.SIZE_ON_SCREEN
	X = TILE_POINTER * SIZE_X
	Y = Terrain.Height - Terrain.List_of_Offsets[TILE_POINTER]
	TILE_RECTANGLE = pygame.Rect(X - Terrain.Position_Pointer, Y, SIZE_X, SIZE_Y * 6)
	
	if TILE_RECTANGLE.colliderect((Object.X + Object.Width / 4, Object.Y, Object.Width / 2, Object.Height)):
		return True
	return False
