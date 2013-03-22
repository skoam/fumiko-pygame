import sys, time, pygame, player, Terrain, random, Object, copy, Enemy
import collision_detection, gravity
from pygame.locals import *
# Basic Imports

def main():
	# Global Variables (They aren't so evil after all)
	global DISPLAYSURF, FPSCLOCK, FPS, PLAYER_LIST, LIST_OF_OBJECTS, LIST_OF_ENEMIES, IMAGE_LIBRARY, WINDOWWIDTH, WINDOWHEIGHT, scale_X, scale_Y
	
	# A Library for all the graphics
	IMAGE_LIBRARY =	{			'Fumiko': pygame.image.load("Fumiko.png"),
								'empty': pygame.image.load("charempty.png"),
								'Chipset_1': pygame.image.load("Chipset_1.png"),
								'BG_1': pygame.image.load("BG_2.jpg"),
								'Object_Rock': pygame.image.load("rock_smaller.png"),
								'Object_Rock_2': pygame.image.load("rock.png"),
								'Object_Grass': pygame.image.load("grass.png"),
								'Object_Grass_2': pygame.image.load("grass_2.png"),
								'Boss_A': pygame.image.load("mons6.png"),
								'Monsters': pygame.image.load("Monster_Charset.png"),
								'Monsters_Bigger': pygame.image.load("Monster_Charset_Bigger.png")
							}
	
	PLAYER_LIST = []
	LIST_OF_OBJECTS = []
	LIST_OF_ENEMIES = []
	
	FPS = 30
	WINDOWWIDTH = 800
	WINDOWHEIGHT = 600
	FULLSCREEN = False
	
	SPACE_KEY_TIMER_AFTER = pygame.time.get_ticks()

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
	IMAGE_LIBRARY['Object_Rock_2'] = IMAGE_LIBRARY['Object_Rock_2'].convert_alpha()
	IMAGE_LIBRARY['Object_Grass'] = IMAGE_LIBRARY['Object_Grass'].convert_alpha()
	IMAGE_LIBRARY['Object_Grass_2'] = IMAGE_LIBRARY['Object_Grass_2'].convert_alpha()
	IMAGE_LIBRARY['Fumiko'] = IMAGE_LIBRARY['Fumiko'].convert_alpha()
	IMAGE_LIBRARY['BG_1'] = IMAGE_LIBRARY['BG_1'].convert()
	IMAGE_LIBRARY['Monsters'] = IMAGE_LIBRARY['Monsters'].convert_alpha()
	IMAGE_LIBRARY['Monsters_Bigger'] = IMAGE_LIBRARY['Monsters_Bigger'].convert_alpha()
	
	# These two can be used to adjust values to the Screenheight and width.
	# For example it is used for the Terrain.List_of_Offsets to keep the velocity
	scale_X = int(WINDOWWIDTH / 320)
	scale_Y = int(WINDOWHEIGHT / 240)
	
	################### MAP_GENERATOR #############
	
	# Initialize class Terrain()
	Level1 = Terrain.Terrain()
	# Giving the Terrain Class the Display Resolution
	Level1.WINDOWWIDTH, Level1.WINDOWHEIGHT = WINDOWWIDTH, WINDOWHEIGHT
	# Scale the Size of the TILES to the resolution
	Level1.SIZE_ON_SCREEN = (WINDOWWIDTH / 10, int(WINDOWHEIGHT / 7.5))
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
		Level1.List_of_Offsets.append(random.randrange(0, 40, 5))
	Level1.List_of_Offsets.append(Level1.List_of_Offsets[len(Level1.List_of_Tops)-1])
	for i in range(len(Level1.List_of_Offsets)):
		Level1.List_of_Offsets[i] *= scale_Y # scaling
	
	# This function creates the actual subsprites from the chipset!
	Level1.Make_Tileset(IMAGE_LIBRARY)
	
	################### PLAYER ##################
	
	# Initializing the class
	Fumiko = player.Player()
	
	# Player Name
	Fumiko.Name = "Fumiko"
	
	# Giving the player class the display resolution
	Fumiko.WINDOWWIDTH = WINDOWWIDTH
	Fumiko.WINDOWHEIGHT = WINDOWHEIGHT
	
	# He also needs a pointer to the LIST_OF_OBJECTS and LIST_OF_ENEMIES
	Fumiko.LIST_OF_OBJECTS = LIST_OF_OBJECTS
	Fumiko.LIST_OF_ENEMIES = LIST_OF_ENEMIES
	
	# setting the default moveSpeed values depending on display resolution
	Fumiko.WALKSPEED = WINDOWWIDTH / 160
	Fumiko.RUNSPEED = WINDOWWIDTH / 80
	Fumiko.JUMPSPEED = WINDOWWIDTH / 100
	
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
	Fumiko.Width = Fumiko.Width * scale_X
	Fumiko.Height = Fumiko.Height * scale_Y
	for Frame in Fumiko.Frame_Dict:
		Fumiko.Frame_Dict[Frame] = pygame.transform.scale(Fumiko.get_frame(Frame), (Fumiko.Width, Fumiko.Height))
		
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
	
	################## ENEMIES #####################
	
	# add_objects('Enemy_Turtle')
	# add_objects('Enemy_Turtle')
	
	####################### OBJECTS ########################
	
	while True: # MAIN GAME LOOP
		
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
				
			if event.type == KEYDOWN:
				# Is SPACE key pressed? Make Player jump when possible
				# Also check for 'RunBoost' which makes the Player jump longer
				if event.key == K_SPACE and not currentPlayer.currentState == 'Jumping' and not currentPlayer.Jump:
					currentPlayer.Y -= 5
					if currentPlayer.currentState == 'Running' and currentPlayer.RunBoost_Count	== 10:
						currentPlayer.RunBoost = True
						currentPlayer.RunBoost_Count = 0
					currentPlayer.Jump = True
					currentPlayer.currentState = 'Jumping'
			
				if event.key == K_p:
					Level1.Height += 40
				if event.key == K_BACKSPACE:
					for OBJECT in LIST_OF_OBJECTS:
						OBJECT.Y = 0
					for PLAYER in PLAYER_LIST:
						PLAYER.Y = WINDOWHEIGHT / 8
					for ENEMY in LIST_OF_ENEMIES:
						ENEMY.Y = WINDOWHEIGHT / 8
					Level1.List_of_Offsets = []
					for i in range(1, len(Level1.List_of_Tops) + 1):
						Level1.List_of_Offsets.append(random.randrange(0, 40, 5))
					Level1.List_of_Offsets.append(Level1.List_of_Offsets[len(Level1.List_of_Tops)-1])
					for i in range(len(Level1.List_of_Offsets)):
						Level1.List_of_Offsets[i] *= scale_Y # scaling
				if event.key == K_r:
					add_objects('Stone')
				if event.key == K_g:
					add_objects('Grass')
				if event.key == K_e:
					add_objects('Enemy_Turtle')
				if event.key == K_h:
					add_objects('Enemy_Human_Mushroom')
					
			elif event.type == KEYUP:
				if (event.key == K_SPACE and currentPlayer.currentState == 'Jumping' and
					currentPlayer.Jump and currentPlayer.JumpHeight < 100):
					# Make Player fall when SPACE key is released
					SPACE_KEY_TIMER_BEFORE = SPACE_KEY_TIMER_AFTER
					if pygame.time.get_ticks() > SPACE_KEY_TIMER_BEFORE + 500:
						currentPlayer.JumpHeight = 100
					SPACE_KEY_TIMER_AFTER = pygame.time.get_ticks()
					
		# Getting the pressed keys and save them in a list []
		keys_pressed = pygame.key.get_pressed()
					
		# Is left shift key pressed? set Player to running mode when possible
		if keys_pressed[K_LSHIFT] and not currentPlayer.Jump == True:
			if currentPlayer.currentState in ['Waiting', 'Walking']:
				currentPlayer.currentState = 'Running'
		else:
			if currentPlayer.currentState in ['Running'] and not (currentPlayer.moveRight or currentPlayer.moveLeft):
				currentPlayer.currentState = 'Waiting'
			elif currentPlayer.currentState in ['Running'] and (currentPlayer.moveRight or currentPlayer.moveLeft):
				currentPlayer.currentState = 'Walking'
			
		# is a or d pressed? move the player when possible in the right direction.
		# don't move when both keys are pressed
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
		UpdatePositions(Level1)
		Gravity(currentPlayer, Level1, 'Player')
		for OBJECT in LIST_OF_OBJECTS:
			Gravity(OBJECT, Level1, 'Object')
		for ENEMY in LIST_OF_ENEMIES:
			# Let the enemies fall to the ground
			Gravity(ENEMY, Level1, 'Enemy')
			# Let the enemies calculate their next move
			ENEMY.Make_Move()
		
		Animate()
		DISPLAYSURF.blit(Level1.BACKGROUND, (0, 0, WINDOWWIDTH, WINDOWHEIGHT))
		drawObjects(LIST_OF_OBJECTS) # Drawing all the Objects
		drawEnemies(LIST_OF_ENEMIES) # Drawing all the Enemies
		drawPlayer(PLAYER_LIST) # Drawing the Players
		drawTerrain(Level1) # Drawing the Terrain
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
	
	for Enemy in LIST_OF_ENEMIES:
		Enemy.Move(Level)
	
	Level.adjust_offset(LIST_OF_OBJECTS)
		
def Gravity(OBJECT, TERRAIN, Type):
	if Type == 'Player':
		if gravity.makePlayerFall(OBJECT, TERRAIN, LIST_OF_OBJECTS, LIST_OF_ENEMIES):
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
	elif Type == 'Enemy':
		if gravity.makeEnemyFall(OBJECT, TERRAIN):
			OBJECT.moveDown = True
		else:
			OBJECT.moveDown = False
	
def drawTerrain(TERRAIN):
	TERRAIN.Blit_To_Surface(DISPLAYSURF)
	
def drawObjects(ALL_OBJECTS):
	for Object in ALL_OBJECTS:
		Object.draw(DISPLAYSURF)
		
def drawEnemies(ALL_ENEMIES):
	for Enemy in ALL_ENEMIES:
		Enemy.draw(DISPLAYSURF)
	
def Animate():
	for Player in PLAYER_LIST:
		Player.update_frame(pygame.time.get_ticks())
	for Enemy in LIST_OF_ENEMIES:
		Enemy.update_frame(pygame.time.get_ticks())
		
def add_objects(name):
	if name == 'Stone':
		# Creating an instance of the Object class
		Rock = Object.Object()
		# Position on the Screen for the Object to appear
		#Rock.X = random.randrange(0, WINDOWWIDTH, 1)
		Rock.X = PLAYER_LIST[0].X
		# Height on the Screen for the Object to appear
		Rock.Y = 0
		# Load a surface object from IMAGE_LIBRARY and link it to Object.Sprite
		Rock.Sprite = random.choice([IMAGE_LIBRARY['Object_Rock'], IMAGE_LIBRARY['Object_Rock'], IMAGE_LIBRARY['Object_Rock_2']])
		# Getting the real size
		Rock.Width = Rock.Sprite.get_width()
		Rock.Height = Rock.Sprite.get_height()
		# scaling the default weight to the display resolution
		Rock.Weight = 60 * (float(WINDOWHEIGHT / 600))
		# Setting the Width and Height to a proper Screen Size
		Rock.Width = int(Rock.Width * scale_X)
		# Setting the Width and Height to a proper Screen Size
		Rock.Height = int(Rock.Height * scale_Y) 
		# Scaling the Sprite to the new Width and Height
		Rock.Sprite = pygame.transform.scale(Rock.Sprite, (Rock.Width, Rock.Height))
		# Generate a starting Rect object
		Rock.Rect = Rock.build_rectangle()
		
		# Add this rocky stone to the List of Objects
		LIST_OF_OBJECTS.append(Rock)
	if name == 'Grass':
		# Creating an instance of the Object class
		Grass = Object.Object()
		# Position on the Screen for the Object to appear
		# Grass.X = random.randrange(0, WINDOWWIDTH, 1)
		Grass.X = PLAYER_LIST[0].X
		# Height on the Screen for the Object to appear
		Grass.Y = 0
		# Load a surface object from IMAGE_LIBRARY and link it to Object.Sprite
		Grass.Sprite = random.choice([	IMAGE_LIBRARY['Object_Grass'], IMAGE_LIBRARY['Object_Grass_2'], 
										IMAGE_LIBRARY['Object_Grass']])
		# Setting the Width and Height to a proper Screen Size
		Grass.Width = (Grass.Width * scale_X)  
		# Setting the Width and Height to a proper Screen Size
		Grass.Height = (Grass.Height * scale_Y) 
		# Scaling the Sprite to the new Width and Height
		Grass.Sprite = pygame.transform.scale(Grass.Sprite, (Grass.Width, Grass.Height))
		# Generate a starting Rect object
		Grass.Rect = Grass.build_rectangle()
		
		# Add this crazy grass to the List of Objects
		LIST_OF_OBJECTS.append(Grass)
	if name == 'Enemy_Turtle':
		# Creating an instance of the Enemy class
		Monster = Enemy.Enemy()
		# Giving the Enemy class the display resolution for calculation
		Monster.WINDOWWIDTH = WINDOWWIDTH
		Monster.WINDOWHEIGHT = WINDOWHEIGHT
		
		# Monster starting position
		# Monster.X = random.randrange(0, WINDOWWIDTH)
		Monster.X = PLAYER_LIST[0].X
		# Setting Width and Height of the original Charset (depends on the .png file!)
		Monster.Width = 24
		Monster.Height = 32
		# Loading the Charset
		Monster.Charset = IMAGE_LIBRARY['Monsters']
		
		# Cutting out the chars needed for the Monster and add them to the Frame_Dict {}
		Monster.Frame_Dict['Right_A'] = Monster.Charset.subsurface((Monster.build_frame(0, 32)))
		Monster.Frame_Dict['Right_N'] = Monster.Charset.subsurface((Monster.build_frame(24,32)))
		Monster.Frame_Dict['Right_B'] = Monster.Charset.subsurface((Monster.build_frame(48, 32)))
		Monster.Frame_Dict['Left_A'] = pygame.transform.flip(Monster.Frame_Dict['Right_A'], True, False)
		Monster.Frame_Dict['Left_N'] = pygame.transform.flip(Monster.Frame_Dict['Right_N'], True, False)
		Monster.Frame_Dict['Left_B'] = pygame.transform.flip(Monster.Frame_Dict['Right_B'], True, False)
		
		# Scaling the Width and Height for the screen resolution
		Monster.Width = Monster.Width * scale_X
		Monster.Height = Monster.Height * scale_Y
		
		# Scaling the starting surface depending on screen resolution
		for FRAME in Monster.Frame_Dict:
			Monster.Frame_Dict[FRAME] = pygame.transform.scale(Monster.get_frame(FRAME), (Monster.Width, Monster.Height))
		
		# Creating Animations for the enemy. Each Element is a frame in Enemy.Frame_Dict
		Monster.Animations['moveRight'] = ['Right_A', 'Right_N', 'Right_B', 'Right_N']
		Monster.Animations['moveLeft'] = ['Left_A', 'Left_N', 'Left_B', 'Left_N']
		
		# Creating Pointers to iterate through the list of Animations
		Monster.Animations['moveRight_pointer'] = 0
		Monster.Animations['moveLeft_pointer'] = 0
		
		# Setting the starting frame
		Monster.currentFrame = 'Right_N'
		Monster.Facing = 'Right'
		
		# Prebuild a rect object
		Monster.Rect = Monster.build_rectangle()
		
		# Scaling the weight depending on the screen resolution
		Monster.Weight = Monster.Weight * (float(WINDOWHEIGHT / 600)) # scaling the default weight to the display resolution
		
		# Setting the Starting State of the Monster
		Monster.set_state('Waiting')
		
		# Setting the AI type
		Monster.AI_type = 'walk_to_next_wall'
		
		# Add this horrible creature to the List of Enemies
		LIST_OF_ENEMIES.append(Monster)
	if name == 'Enemy_Human_Mushroom':
		Mushroom = Enemy.Enemy()
		# Giving the enemy class the WINDOWWIDTH and WINDOWHEIGHT for calculation
		Mushroom.WINDOWWIDTH = WINDOWWIDTH
		Mushroom.WINDOWHEIGHT = WINDOWHEIGHT
		
		# Setting the enemy to a random position
		#Mushroom.X = random.randrange(0, WINDOWWIDTH)
		Mushroom.X = PLAYER_LIST[0].X
		# Top of the screen for the enemy to fall down
		Mushroom.Y = 0
		
		# Giving the enemy a Charset
		Mushroom.Charset = IMAGE_LIBRARY['Monsters_Bigger']
		
		# Actual Frame Size
		Mushroom.Width = 64
		Mushroom.Height = 64
		
		# Cutting out frames from the Charset
		Mushroom.Frame_Dict['Right_N'] = Mushroom.Charset.subsurface(Mushroom.build_frame(64, 0))
		
		Mushroom.Width = Mushroom.Width * scale_X
		Mushroom.Height = Mushroom.Height * scale_Y
		
		for FRAME in Mushroom.Frame_Dict:
			Mushroom.Frame_Dict[FRAME] = pygame.transform.scale(Mushroom.Frame_Dict[FRAME], (Mushroom.Width, Mushroom.Height))
		
		# Starting frame for the Enemy
		Mushroom.currentFrame = 'Right_N'
		Mushroom.Facing = 'Right'
		Mushroom.set_state('Waiting')
		
		Mushroom.Rect = Mushroom.build_rectangle()
		
		# Scaling the Weight depending on the screen resolution
		Mushroom.Weight = Mushroom.Weight * (float(WINDOWHEIGHT / 600)) # scaling the default weight to the display resolution
		
		# Setting the AI type
		Mushroom.AI_type = 'none'
		
		LIST_OF_ENEMIES.append(Mushroom)
		

if __name__ == '__main__':
	main()
