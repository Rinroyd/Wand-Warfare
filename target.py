import pygame
from game_object import GameObject
from abc import ABC, abstractmethod




class Target(GameObject, ABC):
    def __init__(self, location, size, color):
        super().__init__(location, size)
        self.color = color
        
        
    
    @abstractmethod
    def draw(self, surface):
        pass
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def apply_effect(self, player, other=None):
        pass
