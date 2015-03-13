import pygame
from common import Position, debug

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
    def __init__(self):
        self.gravity = -9.81
        self.forces = []
        self.reduce_factor = 1.1
        self.effect_factor = 0.02
        self.gravity_factor = 10
        self.minimum_force = 0.00000000000000001

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
        effect.y -= self.gravity * self.gravity_factor
        effect.multiply(self.effect_factor)
        return effect 

    def add_force(self, x, y, damp):
        self.forces.append(Force(x, y, damp))
