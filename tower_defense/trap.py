import pygame as py
import math
from vector import Vector
from enemy import Enemy
class Trap:
    """Places Trap"""
    position: Vector 
    color: tuple 

    
    def __init__(self, position: Vector, color: tuple):
        self.position = position 
        self.color = color
        

        
