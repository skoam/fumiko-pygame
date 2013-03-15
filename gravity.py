import GLOBAL_VARIABLES, pygame, collision_detection
from pygame.locals import *
from GLOBAL_VARIABLES import *
from collision_detection import *

def makePlayerFall(Object, Terrain):
	Object_on_Before, Object_on_Next, Object_on_Terrain = False, False, False
	
	for i in range(len(Terrain.List_of_Tops)):
		if Terrain.List_of_Tops[i] != '0':
			Object_on_Terrain = (collision_detection.Player_and_Terrain(Object, i, Terrain))
			
			#if Object_on_Terrain == True or (Object.Jump == True and Object.JumpHeight <= 120):
			
			Object_on_Before = (collision_detection.Player_and_Terrain(Object, i - 1, Terrain))
			if i < (len(Terrain.List_of_Tops) - 1):
				Object_on_Next = (collision_detection.Player_and_Terrain(Object, i + 1, Terrain))
			
			if Object_on_Next == 'Stop' and Object.Facing == 'Right':
				# print ("Stop Right")
				#if Object.Jump:
					#Object.X -= 5
				Object.X -= Object.moveSpeed
				Object.Wall_on_Right = True
				return False
				
			if Object_on_Before == 'Stop' and Object.Facing == 'Left':
				# print ("Stop Left")
				#if Object.Jump:
					#Object.X += 5
				Object.X += Object.moveSpeed
				Object.Wall_on_Left = True
				return False
			
			if Object.Facing == 'Right' and Object_on_Terrain == True and Object_on_Next == True:
				# print ("on next")
				if Object.JumpHeight == 0 or Object.JumpHeight >= 120:
					Object.Y = Terrain.Height - Terrain.List_of_Offsets[i + 1] - Object.HEIGHT_ON_SCREEN
				if Object.Jump == True and Object.JumpHeight >= 120:
					Object.currentState = 'Waiting'
					Object.Jump = False
					Object.JumpHeight = 0
					if Object.RunBoost_Count == 0:
						Object.RunBoost = False
				return False
			elif Object.Facing == 'Left' and Object_on_Terrain == True and Object_on_Before == True:
				# print ("on before")
				if Object.JumpHeight == 0 or Object.JumpHeight >= 120:
					Object.Y = Terrain.Height - Terrain.List_of_Offsets[i - 1] - Object.HEIGHT_ON_SCREEN
				if Object.Jump == True and Object.JumpHeight >= 120:
					Object.currentState = 'Waiting'
					Object.Jump = False
					Object.JumpHeight = 0
					if Object.RunBoost_Count == 0:
						Object.RunBoost = False
				return False
			elif Object_on_Terrain == True:
				# print ("on Terrain")
				# print ("%i, %i" % (Terrain.Position_Pointer, i))
				# Object.currentTileHeight = Terrain.Height - Terrain.List_of_Offsets[i]
				if Object.JumpHeight == 0 or Object.JumpHeight >= 120:
					Object.Y = Terrain.Height - Terrain.List_of_Offsets[i] - Object.HEIGHT_ON_SCREEN
				if Object.Jump == True and Object.JumpHeight >= 120:
					Object.currentState = 'Waiting'
					Object.Jump = False
					Object.JumpHeight = 0
					if Object.RunBoost_Count == 0:
						Object.RunBoost = False
				return False

	return True
	
def makeObjectFall(Object, Terrain):
	Object_on_Before, Object_on_Next, Object_on_Terrain = False, False, False
	
	for i in range(len(Terrain.List_of_Tops)):
		if Terrain.List_of_Tops[i] != '0':
			Object_on_Terrain = (collision_detection.Object_and_Terrain(Object, i, Terrain))
			
			if Object_on_Terrain:
				# Object.Y = Terrain.Height - Terrain.List_of_Offsets[i] - Object.HEIGHT_ON_SCREEN
				return False
		
	return True
