import pygame
from common import Position, debug

class Force:
    def __init__(self, x, y, damp):
       self.x = x
       self.y = y
       self.damp = 0

class Effect:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def multiply(self, value):
        self.x *= value
        self.y *= value

class PhysicsController2D:
    def __init__(self):
        self.gravity = -9.81
        self.forces = []
        self.reduce_factor = 100
        self.effect_factor = 0.0125

    def update_forces(self):
        for i in range(len(self.forces)):
            if i >= len(self.forces):
                return
            force = self.forces[i]
            force.x -= force.damp + self.reduce_factor
            force.y -= force.damp + self.reduce_factor
            
            if force.x < 0:
                force.x = 0
            if force.y < 0:
                force.y = 0

            if force.x + force.y == 0:
                i -= 1
                self.forces.pop(i)

    def effect(self):
        self.update_forces()
        effect = Effect(0, 0)
        for force in self.forces:
            effect.x += force.x 
            effect.y += force.y
        effect.multiply(self.effect_factor)
        debug(effect)
        return effect 

    def add_force(self, x, y, damp):
        self.forces.append(Force(x, y, damp))
