import pygame as py
import math
from vector import Vector
from enemy import Enemy
class Projectile:
    """Moves on initialized vector, handled by fighter and gm classes."""
    position: Vector 
    color: tuple 
    speed: float = 5.0
    enemy: Enemy 
    unit_vector: Vector
    

    
    
    def __init__(self, position: Vector, color: tuple, speed: float, enemy: Enemy):
        self.position = position 
        self.color = color
        self.speed = speed
        self.enemy = enemy

        

    
    def move_projectile(self, new_position: Vector):
        vector: Vector = new_position - self.position
        unit_vector: Vector = vector.normalize()
        speed_vector: Vector = unit_vector * self.speed
        self.position = self.position + speed_vector
        return unit_vector
    
