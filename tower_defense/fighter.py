from enemy import Enemy
from projectile import Projectile
import pygame as py
import math
from vector import Vector
class Fighter:
    """Squares placed by player to combat enemies."""
    position: Vector 
    color: tuple 
    speed: float = 5.0
    
    def __init__(self, position: Vector, color: tuple):
        self.position = position 
        self.color = color

    
