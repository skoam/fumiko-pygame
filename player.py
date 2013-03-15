import pygame, GLOBAL_VARIABLES
from pygame.locals import *
from GLOBAL_VARIABLES import *

# WINDOWWIDTH = 640
# WINDOWHEIGHT = 480

class Player():
	WALKSPEED = WINDOWWIDTH / 160
	RUNSPEED = WINDOWWIDTH / 80
	JUMPSPEED = WINDOWWIDTH / 100
	
	AnimationSpeed = 100
	time_since_last_update = 0
	
	Name = ""
	Health = 0
	Mana = 0
	X = 0
	Y = 0
	Height = 32
	Width = 24
	moveSpeed = 0
	Charset = pygame.Surface((0, 0))
	currentFrame = pygame.Surface((0, 0))
	
	Weight = 5 # For Gravity
	currentTileHeight = 0 # TILE the player stands on
	
	moveDown = False
	moveUp = False
	moveLeft = False
	moveRight = False
	
	Jump = False
	JumpHeight = 0

	Wall_on_Right = False
	Wall_on_Left = False
	
	RunBoost = False
	RunBoost_Count = 0
	
	#WIDTH_ON_SCREEN = WINDOWWIDTH / 17
	WIDTH_ON_SCREEN = Width * int(WINDOWWIDTH / 320)
	# HEIGHT_ON_SCREEN = WINDOWHEIGHT / 9
	HEIGHT_ON_SCREEN = Height * int(WINDOWHEIGHT / 240)
	
	Facing = 'Right'
	currentState = 	'Waiting'
	
	# Player dictionaries to save Player-related data (sprites, animation-lists etc.)
	Frame_Dict = {}
	Animations = 	{}
					
	def draw(self, surface):
		surface.blit(self.Frame_Dict[self.currentFrame], self.build_rectangle())
		return surface
						
	def set_state(self, state):
		# some sugar
		self.currentState = state
		
	def build_rectangle(self):
		# returns the actual rectangle of the player frame
		Rectangle = pygame.Rect(self.X, self.Y, self.WIDTH_ON_SCREEN, self.HEIGHT_ON_SCREEN)
		return Rectangle
		
	def build_rectangle_with_offset(self, OFFSETX, OFFSETY, BIGGERX, BIGGERY):
		# returns a modified rectangle of the player (for collision)
		Rectangle = pygame.Rect(self.X + OFFSETX, self.Y + OFFSETY, self.WIDTH_ON_SCREEN + BIGGERX, self.HEIGHT_ON_SCREEN + BIGGERY)
		return Rectangle
		
	def build_frame(self, x, y):
		# Returns a Rect to cut out a frame from a charset
		Rectangle = pygame.Rect(x, y, self.Width, self.Height)
		return Rectangle
		
	def get_frame(self, string):
		# Returns a surface Object of a named frame
		return self.Frame_Dict[string]
					
	def Move(self, Terrain):
		if self.Jump:
			if self.JumpHeight < 120:
				if self.Facing == 'Right':
					self.currentFrame = 'Jump_Before_R'
				elif self.Facing == 'Left':
					self.currentFrame = 'Jump_Before_L'
					
				if self.JumpHeight < 60:
					if self.RunBoost == True:
						self.Y -= 7 * (float(WINDOWWIDTH) / 800)
					self.Y -= 18 * (float(WINDOWHEIGHT) / 600)
					self.JumpHeight += 10
				elif self.JumpHeight < 90:
					self.Y -= 15 * (float(WINDOWHEIGHT) / 600)
					self.JumpHeight += 5
				elif self.JumpHeight < 120:
					self.Y -= 12 * (float(WINDOWHEIGHT) / 600)
					self.JumpHeight += 4
			else:
				if self.Facing == 'Right':
					self.currentFrame = 'Jump_After_R'
				elif self.Facing == 'Left':
					self.currentFrame = 'Jump_After_L'
				
		if self.moveDown:
			self.Y += self.Weight
			
		if self.Wall_on_Right == False:
			if self.moveRight and (self.X + self.WIDTH_ON_SCREEN < WINDOWWIDTH / 2):
				self.X += self.moveSpeed
				self.Wall_on_Left = False
				#self.Facing = 'Right'
			elif self.moveRight and (Terrain.Position_Pointer == (len(Terrain.List_of_Tops) * Terrain.SIZE_ON_SCREEN[0]) - WINDOWWIDTH):
				self.X += self.moveSpeed
				self.Wall_on_Left = False
				#self.Facing = 'Right'
			elif self.moveRight and (Terrain.Position_Pointer < (len(Terrain.List_of_Tops) * Terrain.SIZE_ON_SCREEN[0]) - WINDOWWIDTH):
				Terrain.Position_Pointer += self.moveSpeed
				for OBJECT in LIST_OF_OBJECTS:
					OBJECT.X -= self.moveSpeed
				self.Wall_on_Left = False
				#self.Facing = 'Right'
			
		if self.Wall_on_Left == False:
			if self.moveLeft and Terrain.Position_Pointer == 0:
				self.X -= self.moveSpeed
				self.Wall_on_Right = False
				#self.Facing = 'Left'
			elif (self.X + self.WIDTH_ON_SCREEN > WINDOWWIDTH / 2) and self.moveLeft and (Terrain.Position_Pointer == (len(Terrain.List_of_Tops) * Terrain.SIZE_ON_SCREEN[0]) - WINDOWWIDTH):
				self.X -= self.moveSpeed
				self.Wall_on_Right = False
				#self.Facing = 'Left'
			elif self.moveLeft:
				for OBJECT in LIST_OF_OBJECTS:
					OBJECT.X += self.moveSpeed
				Terrain.Position_Pointer -= self.moveSpeed
				self.Wall_on_Right = False
				#self.Facing = 'Left'
		
		Terrain.adjust_offset()
		
			
	def update_frame(self, t):
		if self.currentState == 'Jumping':
			self.moveSpeed = self.JUMPSPEED
			if self.RunBoost == True:
				self.moveSpeed += WINDOWWIDTH / 400
		elif self.currentState == 'Jumping' and self.JumpHeight == 120:
			self.moveSpeed = self.WALKSPEED
		elif self.currentState == 'Walking':
			self.moveSpeed = self.WALKSPEED
		elif self.currentState == 'Running':
			self.moveSpeed = self.RUNSPEED
		
		if not (self.currentState == 'Running' or self.currentState == 'Jumping'):
			""" Animation for normal Walking starts here """
			
			if not (self.moveRight and self.moveLeft):
				if self.moveRight:
					self.Facing = 'Right'
					if t - self.time_since_last_update > self.AnimationSpeed:
						pointer = self.Animations['moveRight_pointer']
						self.currentFrame = self.Animations['moveRight'][pointer]
						if self.Animations['moveRight_pointer'] < len(self.Animations['moveRight']) - 1:
							self.Animations['moveRight_pointer'] += 1
						else:
							self.Animations['moveRight_pointer'] = 0
						self.time_since_last_update = t
				if self.moveLeft:
					self.Facing = 'Left'
					if t - self.time_since_last_update > self.AnimationSpeed:
						pointer = self.Animations['moveLeft_pointer']
						self.currentFrame = self.Animations['moveLeft'][pointer]
						if self.Animations['moveLeft_pointer'] < len(self.Animations['moveRight']) - 1:
							self.Animations['moveLeft_pointer'] += 1
						else:
							self.Animations['moveLeft_pointer'] = 0
						self.time_since_last_update = t
			else:
					if self.Facing == 'Right':
						self.currentFrame = 'Right_N'
					elif self.Facing == 'Left':
						self.currentFrame = 'Left_N'
			""" Animation for normal Walking stops here """
			
		elif self.currentState == 'Running':
			""" Animation for Running starts here """
			
			if not (self.moveRight and self.moveLeft):
				if self.moveRight:
					self.Facing = 'Right'
					if t - self.time_since_last_update > self.AnimationSpeed:
						pointer = self.Animations['runRight_pointer']
						self.currentFrame = self.Animations['runRight'][pointer]
						if self.Animations['runRight_pointer'] < len(self.Animations['runRight']) - 1:
							self.Animations['runRight_pointer'] += 1
						else:
							self.Animations['runRight_pointer'] = 0
						self.time_since_last_update = t
				elif self.moveLeft:
					self.Facing = 'Left'
					if t - self.time_since_last_update > self.AnimationSpeed:
						pointer = self.Animations['runLeft_pointer']
						self.currentFrame = self.Animations['runLeft'][pointer]
						if self.Animations['runLeft_pointer'] < len(self.Animations['runLeft']) - 1:
							self.Animations['runLeft_pointer'] += 1
						else:
							self.Animations['runLeft_pointer'] = 0
						self.time_since_last_update = t
			else:
				if self.Facing == 'Right':
					self.currentFrame = 'Right_N'
					self.Animations['moveRight_pointer'] = 0
					self.Animations['moveLeft_pointer'] = 0
				elif self.Facing == 'Left':
					self.currentFrame = 'Left_N'
					self.Animations['moveRight_pointer'] = 0
					self.Animations['moveLeft_pointer'] = 0
			
			""" Animation for Running stops here """
		if self.currentState == 'Jumping':
			# Animation for Jump starts here 
			
			if not (self.moveRight and self.moveLeft):
				if self.moveRight:
					self.Facing = 'Right'
				if self.moveLeft:
					self.Facing = 'Left'
			else:
				self.Facing = 'Right'
		
		if not (self.moveRight or self.moveLeft or self.Jump):
			if self.Facing == 'Right':
				self.currentFrame = 'Right_N'
			elif self.Facing == 'Left':
				self.currentFrame = 'Left_N'
			self.Animations['moveRight_pointer'] = 0
			self.Animations['moveLeft_pointer'] = 0
