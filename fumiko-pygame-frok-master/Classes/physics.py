import pygame
from Classes.manage_game import game
from Classes.common import Position, debug

class Force:
    def __init__(self, x, y, damp=None, name=None):
       self.x = x
       self.y = y
       self.damp = damp if damp is not None else 0
       self.name = name if name is not None else ""

class Effect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def multiply(self, value):
        self.x *= value
        self.y *= value

class PhysicsController2D:
    def __init__(self, collider):
        self.gravity = -9.81
        self.forces = []
        self.reduce_factor = 1.1
        self.effect_factor = 0.02
        self.gravity_factor = 10
        self.minimum_force = 1
        self.grounded = False
        self.collider = collider

        self.groundingDensity = 8 
        self.groundingWidth = 30

        game.physics_controllers.append(self)

    def check_for_collision(self, point=None):
        for controller in game.physics_controllers:
            if point is None:
                if self is not controller and self.collider.colliderect(controller.collider):
                    return True
            else:
                if self is not controller and controller.collider.collidepoint(point):
                    return True
        return False

    def is_grounded(self):
        groundingPoints = []
        groundingStart = (self.collider.midbottom[0] - self.groundingWidth / 2, self.collider.midbottom[1])
        for i in range(0, self.groundingDensity):
            groundingPoints.append((groundingStart[0] + (self.groundingWidth / self.groundingDensity) * i, groundingStart[1])) 
        for point in groundingPoints:
            if self.check_for_collision(point):
                return True
        return False
  
    def update_forces(self):
        for i in range(len(self.forces)):
            if i >= len(self.forces):
                return
            force = self.forces[i]
            force.x = force.x / (force.damp + self.reduce_factor)
            force.y = force.y / (force.damp + self.reduce_factor)
            
            if abs(force.x) < self.minimum_force:
                force.x = 0
            if abs(force.y) < self.minimum_force:
                force.y = 0

            if force.x + force.y == 0:
                i -= 1
                self.forces.remove(force)

    def effect(self):
        self.update_forces()
        effect = Effect(0, 0)
        for force in self.forces:
            effect.x += force.x 
            effect.y += force.y
        if not self.is_grounded():
            effect.y -= self.gravity * self.gravity_factor
        effect.multiply(self.effect_factor)
        return effect 

    def add_force(self, x, y, damp):
        self.forces.append(Force(x, y, damp))
