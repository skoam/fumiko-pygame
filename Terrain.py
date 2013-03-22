import  pygame
from pygame.locals import *
import master
# from GLOBAL_VARIABLES import *

class Terrain():
	# A Terrain is a List of pygame.rect objects and their fitting pygame.surface object.
	# There is a chipset loaded from a file with two rows:
	# The first one for the top edge of the Terrain
	# The second one for the fill

	Chipset = pygame.surface.Surface((0,0))
	BACKGROUND = pygame.surface.Surface((0,0))
	
	# The List of Tops contains Rectangles for the upper Line of the Terrain
	# for the Player and other Objects to collide with.
	# Average Length to fill the WINDOWWIDTH is 10
	List_of_Tops = []
	# Another List for the OFFSET of the TILES in List_of_Tops[]
	List_of_Offsets = []
	
	TILE_DICT = {}
	
	SIZE_ON_SCREEN = (0, 0)
	
	WINDOWWIDTH = 320
	WINDOWHEIGHT = 240
	
	# Some Variables for the Terrain
	
	Height = 120
	Position_Pointer = 0 # Used to move the Terrain depending on the X position of the player
	
	########### FUNCTIONS ###########
	
	def Make_Tileset(self, IMAGE_LIBRARY):
		Chipset_Length = self.Chipset.get_width() / 32 # Gets the amount of Tiles in the Chipset (32 x 32)
		for TILE in range(Chipset_Length - 1):
			# Adds two Elements to TILE_DICT
			self.TILE_DICT['Element_%s' % TILE] = self.Chipset.subsurface(32 * TILE, 0, 32, 32).convert_alpha()
			self.TILE_DICT['Element_%s_fill' % TILE] = self.Chipset.subsurface(32 * TILE, 32, 32, 32).convert()
		self.TILE_DICT['No_Element'] = IMAGE_LIBRARY['empty']
		
		# Scale the Surfaces to the Window Size:
		for Surface in self.TILE_DICT:
			self.TILE_DICT[Surface] = pygame.transform.scale(self.TILE_DICT[Surface], self.SIZE_ON_SCREEN)
	
	def Blit_To_Surface(self, SURFACE):
		# print ('Position_Pointer: %i' % self.Position_Pointer)
		# 1496, 16
		i = 0
		SIZE_X, SIZE_Y = self.SIZE_ON_SCREEN
		for TOP_TILE in self.List_of_Tops:
			if TOP_TILE == '1' and ((i * SIZE_X - self.Position_Pointer) < self.WINDOWWIDTH):
				X = i * SIZE_X
				Y = self.Height - self.List_of_Offsets[i]
				if (X + SIZE_X - self.Position_Pointer > 0):
					TILE_RECTANGLE = (X - self.Position_Pointer, Y, SIZE_X, SIZE_Y)
					SURFACE.blit(self.TILE_DICT['Element_0'], TILE_RECTANGLE)
					for u in range(1,6):
						TILE_RECTANGLE = (X - self.Position_Pointer, Y + u * SIZE_Y, SIZE_X, SIZE_Y)
						SURFACE.blit(self.TILE_DICT['Element_0_fill'], TILE_RECTANGLE)
				i += 1
			elif TOP_TILE == '2' and ((i * SIZE_X - self.Position_Pointer) < self.WINDOWWIDTH):
				X = i * SIZE_X
				Y = self.Height - self.List_of_Offsets[i]
				if (X + SIZE_X - self.Position_Pointer > 0):
					TILE_RECTANGLE = (X - self.Position_Pointer, Y, SIZE_X, SIZE_Y)
					SURFACE.blit(self.TILE_DICT['Element_1'], TILE_RECTANGLE)
					for u in range(1,6):
						TILE_RECTANGLE = (X - self.Position_Pointer, Y + u * SIZE_Y, SIZE_X, SIZE_Y)
						SURFACE.blit(self.TILE_DICT['Element_1_fill'], TILE_RECTANGLE)
				i += 1
			
			elif TOP_TILE == '0':
				X = i * SIZE_X
				Y = self.Height - self.List_of_Offsets[i]
				TILE_RECTANGLE = (X, Y, SIZE_X, SIZE_Y)
				SURFACE.blit(self.TILE_DICT['No_Element'], TILE_RECTANGLE)
				i += 1
				
	def adjust_offset(self, LIST_OF_OBJECTS):
		if self.Position_Pointer < 0:
			for OBJECT in LIST_OF_OBJECTS:
				OBJECT.X += self.Position_Pointer
			self.Position_Pointer = 0
		if self.Position_Pointer > ((len(self.List_of_Tops) * self.SIZE_ON_SCREEN[0]) - self.WINDOWWIDTH):
			for OBJECT in LIST_OF_OBJECTS:
				difference = self.Position_Pointer - ((len(self.List_of_Tops) * self.SIZE_ON_SCREEN[0]) - self.WINDOWWIDTH)
				OBJECT.X += difference
			self.Position_Pointer = ((len(self.List_of_Tops) * self.SIZE_ON_SCREEN[0]) - self.WINDOWWIDTH)
