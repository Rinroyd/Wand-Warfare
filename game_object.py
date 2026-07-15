import pygame
from abc import ABC , abstractmethod
# لاس انتزاعی مادر برای تمام اشیا بازی از جمله بازیکنان و اهداف

class GameObject(ABC):
    def __init__(self, location, size):
        self.rect = pygame.Rect(*location, *size)
    
    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def update(self):
        pass