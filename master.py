import sys, time, pygame, player, GLOBAL_VARIABLES, Terrain, random, Object, copy
import collision_detection, gravity
from pygame.locals import *
from player import *
from GLOBAL_VARIABLES import *
from collision_detection import *
from gravity import *
from Terrain import *
from Object import *

# Basic Imports

def main():
	# Global Variables
	global DISPLAYSURF, FPSCLOCK
	
	# Initialize the Things
	pygame.init()
	
	if FULLSCREEN == False:
		# Set to Windowed Mode
		DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	else:
		# Set to Full Screen
		DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
	
	# Set the Window Title
	pygame.display.set_caption('Destiny of Goddess')
	
	# Creating a Clock Object to adjust the framerate to be FPS
	FPSCLOCK = pygame.time.Clock() 
	
	# Converting these Images will make the drawing much faster
	IMAGE_LIBRARY['Boss_A'] = IMAGE_LIBRARY['Boss_A'].convert_alpha()
	IMAGE_LIBRARY['empty'] = IMAGE_LIBRARY['empty'].convert_alpha()
	IMAGE_LIBRARY['Object_Rock'] = IMAGE_LIBRARY['Object_Rock'].convert_alpha()
	IMAGE_LIBRARY['Object_Grass'] = IMAGE_LIBRARY['Object_Grass'].convert_alpha()
	IMAGE_LIBRARY['Fumiko'] = IMAGE_LIBRARY['Fumiko'].convert_alpha()
	IMAGE_LIBRARY['BG_1'] = IMAGE_LIBRARY['BG_1'].convert()
	
	# These two can be used to adjust values to the Screenheight and width.
	# For example it is used for the Terrain.List_of_Offsets to keep the velocity
	scale_X = int(WINDOWWIDTH / 320)
	scale_Y = int(WINDOWHEIGHT / 240)
	
	################### MAP_GENERATOR #############
	
	# Initialize class Terrain()
	Level1 = Terrain()
	# The average height of the Terrain
	Level1.Height = WINDOWHEIGHT - WINDOWHEIGHT / 2
	# load some sprites for the Terrain
	Level1.Chipset = IMAGE_LIBRARY['Chipset_1']
	Level1.BACKGROUND = IMAGE_LIBRARY['BG_1']
	Level1.BACKGROUND = pygame.transform.scale(Level1.BACKGROUND, (WINDOWWIDTH, WINDOWHEIGHT))
	
	# Here the actual Map is created. It is build from a list of Number representing the tile-type and
	# another number for the offset this tile has. It's generated randomly or (better) made by hand.
	
	#Level1.List_of_Tops = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
	#Level1.List_of_Offsets = [0, 0, 0, -5, 5, 10, 10, 10, 40, 5, 0, -20, -10, -15, -20, -25]
	
	for i in range(30):
		Level1.List_of_Tops.append('2')
		
	for i in range(1, len(Level1.List_of_Tops) + 1):
		Level1.List_of_Offsets.append(random.randrange(0, 20, 5))
	Level1.List_of_Offsets.append(Level1.List_of_Offsets[len(Level1.List_of_Tops)-1])
	for i in range(len(Level1.List_of_Offsets)):
		Level1.List_of_Offsets[i] *= scale_Y # scaling
	
	# This function creates the actual subsprites from the chipset!
	Level1.Make_Tileset()
	
	################### PLAYER ##################
	
	# Initializing the class
	Fumiko = Player()
	
	# Player Name
	Fumiko.Name = "Fumiko"
	
	# Positioning
	Fumiko.X = 20
	Fumiko.Y = 20
	Fumiko.Height = 32
	Fumiko.Width = 24
	
	# Loading the sprite
	Fumiko.Charset = IMAGE_LIBRARY['Fumiko']
	
	# cutting out the frames from the charset and saving them in a Dictionary
	Fumiko.Frame_Dict['Right_A'] = Fumiko.Charset.subsurface((Fumiko.build_frame(0, 32)))
	Fumiko.Frame_Dict['Right_N'] = Fumiko.Charset.subsurface((Fumiko.build_frame(24, 32)))
	Fumiko.Frame_Dict['Right_B'] = Fumiko.Charset.subsurface((Fumiko.build_frame(48, 32)))
	Fumiko.Frame_Dict['Left_A'] = Fumiko.Charset.subsurface((Fumiko.build_frame(0, 96)))
	Fumiko.Frame_Dict['Left_N'] = Fumiko.Charset.subsurface((Fumiko.build_frame(24, 96)))
	Fumiko.Frame_Dict['Left_B'] = Fumiko.Charset.subsurface((Fumiko.build_frame(48, 96)))
	Fumiko.Frame_Dict['runRight_A'] = Fumiko.Charset.subsurface((Fumiko.build_frame(72, 32)))
	Fumiko.Frame_Dict['runRight_N'] = Fumiko.Charset.subsurface((Fumiko.build_frame(96, 32)))
	Fumiko.Frame_Dict['runRight_B'] = Fumiko.Charset.subsurface((Fumiko.build_frame(120, 32)))
	Fumiko.Frame_Dict['runLeft_A'] = Fumiko.Charset.subsurface((Fumiko.build_frame(72, 96)))
	Fumiko.Frame_Dict['runLeft_N'] = Fumiko.Charset.subsurface((Fumiko.build_frame(96, 96)))
	Fumiko.Frame_Dict['runLeft_B'] = Fumiko.Charset.subsurface((Fumiko.build_frame(120, 96)))
	Fumiko.Frame_Dict['Jump_After_R'] = Fumiko.Charset.subsurface((Fumiko.build_frame(240, 32)))
	Fumiko.Frame_Dict['Jump_After_L'] = pygame.transform.flip(Fumiko.Frame_Dict['Jump_After_R'], True, False)
	Fumiko.Frame_Dict['Jump_Before_R'] = Fumiko.Charset.subsurface((Fumiko.build_frame(384, 96)))
	Fumiko.Frame_Dict['Jump_Before_L'] = pygame.transform.flip(Fumiko.Frame_Dict['Jump_Before_R'], True, False)
	
	# scaling the images
	for Frame in Fumiko.Frame_Dict:
		Fumiko.Frame_Dict[Frame] = pygame.transform.scale(Fumiko.get_frame(Frame), (Fumiko.WIDTH_ON_SCREEN, Fumiko.HEIGHT_ON_SCREEN))
		
	# creating the animations
	# These lists are sequences used by Player.update_frame()
	# The pointers are for sequencing
	Fumiko.Animations['moveRight'] = ['Right_B', 'Right_N', 'Right_A', 'Right_N']
	Fumiko.Animations['moveLeft'] = ['Left_B', 'Left_N', 'Left_A', 'Left_N']
	Fumiko.Animations['runRight'] = ['runRight_N', 'runRight_A', 'runRight_N', 'runRight_B']
	Fumiko.Animations['runLeft'] = ['runLeft_N', 'runLeft_A', 'runLeft_N', 'runLeft_B']
	
	Fumiko.Animations['moveRight_pointer'] = 0
	Fumiko.Animations['moveLeft_pointer'] = 0
	Fumiko.Animations['runRight_pointer'] = 0
	Fumiko.Animations['runLeft_pointer'] = 0
	
	# calculating the weight in dependency of WINDOWHEIGHT
	Fumiko.Weight = 10 * (float(WINDOWHEIGHT) / 600)

	# Starting Frame
	Fumiko.currentFrame = 'Right_N'
	Fumiko.Facing = 'Right'
	
	# Gameplay values
	Fumiko.Health = 10
	Fumiko.Mana = 6
	
	# Starting State
	Fumiko.set_state('Waiting')
	
	# Adding the Player to a List of Players
	PLAYER_LIST.append(Fumiko)

	currentPlayer = Fumiko # Setting Fumiko as the controllable Player
	
	################## OBJECTS #####################
	
	# A bigger Object
	
	Monster = Object()
	Monster.X = WINDOWWIDTH / 2 + WINDOWWIDTH / 8
	Monster.Sprite = IMAGE_LIBRARY['Boss_A']
	Monster.Width = int(Monster.Sprite.get_width() * scale_X)
	Monster.Height = int(Monster.Sprite.get_height() * scale_Y)
	Monster.Sprite = pygame.transform.scale(Monster.Sprite, (Monster.Width, Monster.Height))
	Monster.Rect = Monster.build_rectangle()
	
	# A bunch of Rocks
	
	Rock = Object()
	Rock.X = WINDOWWIDTH / 2 # Position on the Screen for the Object to appear
	Rock.Y = 0  # Position on the Screen for the Object to appear
	Rock.Sprite = IMAGE_LIBRARY['Object_Rock']
	Rock.Width = int(Rock.Width * scale_X) # Setting the Width and Height to a proper Screen Size
	Rock.Height = int(Rock.Height * scale_Y) # Setting the Width and Height to a proper Screen Size
	Rock.Sprite = pygame.transform.scale(Rock.Sprite, (Rock.Width, Rock.Height)) # Scaling the Sprite to the new Width and Height
	Rock.Rect = Rock.build_rectangle()
	
	Rock2 = copy.copy(Rock)
	Rock2.X = WINDOWWIDTH / 4
	Rock2.Y = WINDOWHEIGHT / 4
	
	Rock3 = copy.copy(Rock)
	Rock3.X = WINDOWWIDTH / 2 + WINDOWWIDTH / 4
	Rock3.Y = 10
	
	Rock4 = copy.copy(Rock)
	Rock4.X = WINDOWWIDTH + WINDOWWIDTH + WINDOWWIDTH / 4
	
	Rock5 = copy.copy(Rock)
	Rock5.X = WINDOWWIDTH + WINDOWWIDTH / 2
	
	# Some Grass
	
	Grass = Object()
	Grass.X = WINDOWWIDTH / 2 + WINDOWWIDTH / 8 # Position on the Screen for the Object to appear
	Grass.Y = WINDOWHEIGHT / 4 # Position on the Screen for the Object to appear
	Grass.Sprite = IMAGE_LIBRARY['Object_Grass']
	Grass.Width = (Grass.Width * scale_X)  # Setting the Width and Height to a proper Screen Size
	Grass.Height = (Grass.Height * scale_Y) # Setting the Width and Height to a proper Screen Size
	Grass.Sprite = pygame.transform.scale(Grass.Sprite, (Grass.Width, Grass.Height)) # Scaling the Sprite to the new Width and Height
	Grass.Rect = Grass.build_rectangle()
	
	Grass2 = copy.copy(Grass)
	Grass2.X += WINDOWWIDTH / 4
	
	Grass3 = copy.copy(Grass2)
	Grass3.X += WINDOWWIDTH / 8
	
	Grass4 = copy.copy(Grass3)
	Grass4.X += WINDOWWIDTH / 2
	
	LIST_OF_OBJECTS.append(Rock) # Adding all the Objects to the global List
	LIST_OF_OBJECTS.append(Rock2)
	LIST_OF_OBJECTS.append(Rock3)
	LIST_OF_OBJECTS.append(Rock4)
	LIST_OF_OBJECTS.append(Rock5)
	LIST_OF_OBJECTS.append(Grass)
	LIST_OF_OBJECTS.append(Grass2)
	LIST_OF_OBJECTS.append(Grass3)
	LIST_OF_OBJECTS.append(Grass4)
	LIST_OF_OBJECTS.append(Monster)
	
	while True: # main game loop
		# BASICFONT = pygame.font.Font('Qlassik_TB.otf', 10)
		# do stuff
		
		# DISPLAYSURF.fill(bgColor)
		
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				return
				
			if event.type == KEYDOWN:
				if event.key == K_SPACE and not currentPlayer.currentState == 'Jumping' and not currentPlayer.Jump:
					currentPlayer.Y -= 5
					if currentPlayer.currentState == 'Running' and currentPlayer.RunBoost_Count	== 10:
						currentPlayer.RunBoost = True
						currentPlayer.RunBoost_Count = 0
					currentPlayer.Jump = True
					currentPlayer.currentState = 'Jumping'
			
				if event.key == K_p:
					Level1.Height += 40
						
		keys_pressed = pygame.key.get_pressed()
					
		if keys_pressed[K_LSHIFT] and not currentPlayer.Jump == True:
			if Player.currentState in ['Waiting', 'Walking']:
				currentPlayer.currentState = 'Running'
		else:
			if currentPlayer.currentState in ['Running'] and not (currentPlayer.moveRight or currentPlayer.moveLeft):
				currentPlayer.currentState = 'Waiting'
			elif currentPlayer.currentState in ['Running'] and (currentPlayer.moveRight or currentPlayer.moveLeft):
				currentPlayer.currentState = 'Walking'
			
		if keys_pressed[K_d] and pygame.key.get_pressed()[K_a]:
			if currentPlayer.currentState not in ['Jumping']:
				currentPlayer.currentState = 'Waiting'
				currentPlayer.moveLeft = True
				currentPlayer.moveRight = True
		else:
			if keys_pressed[K_a]:
				currentPlayer.moveLeft = True
				currentPlayer.moveRight = False
				if currentPlayer.currentState not in ['Running', 'Jumping']:
					currentPlayer.currentState = 'Walking'
			if keys_pressed[K_d]:
				currentPlayer.moveRight = True
				currentPlayer.moveLeft = False
				if currentPlayer.currentState not in ['Running', 'Jumping']:
					currentPlayer.currentState = 'Walking'
		
		if not ((keys_pressed[K_a] == True) or (keys_pressed[K_d] == True)):
			currentPlayer.moveLeft = False
			currentPlayer.moveRight = False
			currentPlayer.Wall_on_Left, currentPlayer.Wall_on_Right = False, False
			currentPlayer.RunBoost_Count = 0
		
		
		if currentPlayer.currentState == 'Running' and (currentPlayer.moveRight or currentPlayer.moveLeft) and not (currentPlayer.moveRight and currentPlayer.Wall_on_Right) and not (currentPlayer.moveLeft and currentPlayer.Wall_on_Left):
			if currentPlayer.RunBoost_Count	< 10:
				currentPlayer.RunBoost_Count += 1
		elif currentPlayer.currentState != 'Jumping':
				currentPlayer.RunBoost_Count = 0
					
		# print ("%i" % currentPlayer.RunBoost_Count)
		Gravity(currentPlayer, Level1, 'Player')
		for OBJECT in LIST_OF_OBJECTS:
			Gravity(OBJECT, Level1, 'Object')
		UpdatePositions(Level1)
		Animate()
		DISPLAYSURF.blit(Level1.BACKGROUND, (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
		drawPlayer(PLAYER_LIST)
		drawTerrain(Level1)
		drawObjects(LIST_OF_OBJECTS) # Drawing all the Objects
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		
def drawPlayer(ALL_PLAYERS):
	for PLAYER in ALL_PLAYERS:
		PLAYER.draw(DISPLAYSURF)
	
def UpdatePositions(Level):
	for Player in PLAYER_LIST:
		Player.Move(Level)
		
	for Object in LIST_OF_OBJECTS:
		Object.Move(Level)
		
def Gravity(OBJECT, TERRAIN, Type):
	if Type == 'Player':
		if gravity.makePlayerFall(OBJECT, TERRAIN):
			OBJECT.moveDown = True
			if OBJECT.Jump == False:
				OBJECT.currentState = 'Jumping'
				OBJECT.Jump = True
				OBJECT.JumpHeight = 120
		else:
			OBJECT.moveDown = False
	elif Type == 'Object':
		if gravity.makeObjectFall(OBJECT, TERRAIN):
			OBJECT.moveDown = True
		else:
			OBJECT.moveDown = False
	
def drawTerrain(TERRAIN):
	TERRAIN.Blit_To_Surface(DISPLAYSURF)
	
def drawObjects(ALL_OBJECTS):
	for Object in ALL_OBJECTS:
		Object.draw(DISPLAYSURF)
	
def Animate():
	for Player in PLAYER_LIST:
		Player.update_frame(pygame.time.get_ticks())

if __name__ == '__main__':
	main()

